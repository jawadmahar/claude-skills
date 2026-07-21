/**
 * Boomerang Lite for Gmail
 * ------------------------
 * Self-hosted Boomerang-style email scheduling for your own Gmail account,
 * built on Google Apps Script. No third-party servers, no subscription.
 *
 * Features:
 *  - Snooze: apply a "Boomerang/Snooze/..." label to any thread and it is
 *    archived, then returned to your inbox (unread) when the time is up.
 *  - Awaiting reply: apply a "Boomerang/Awaiting-Reply/..." label to a thread
 *    you have sent. If nobody replies before the deadline, the thread comes
 *    back to your inbox tagged "Boomerang/No-Reply". If a reply arrives in
 *    time, the tracking is silently cleared.
 *  - Wake on new mail: if a snoozed thread receives a new message, the snooze
 *    is cancelled automatically (the thread is already back in your inbox).
 *
 * One-time setup: run setup() once from the Apps Script editor and authorise.
 * See README.md for full install instructions.
 */

var CONFIG = {
  // Label name -> days until the thread returns to the inbox.
  snoozeLabels: {
    'Boomerang/Snooze/1-Day': 1,
    'Boomerang/Snooze/2-Days': 2,
    'Boomerang/Snooze/3-Days': 3,
    'Boomerang/Snooze/1-Week': 7,
    'Boomerang/Snooze/2-Weeks': 14,
    'Boomerang/Snooze/1-Month': 30
  },
  // Label name -> days to wait for a reply before resurfacing the thread.
  replyLabels: {
    'Boomerang/Awaiting-Reply/2-Days': 2,
    'Boomerang/Awaiting-Reply/3-Days': 3,
    'Boomerang/Awaiting-Reply/1-Week': 7,
    'Boomerang/Awaiting-Reply/2-Weeks': 14
  },
  returnedLabel: 'Boomerang/Returned',
  noReplyLabel: 'Boomerang/No-Reply',
  // How often the background check runs, in minutes (1, 5, 10, 15 or 30).
  checkEveryMinutes: 15
};

var PROP_PREFIX = 'bmr_';
var MS_PER_DAY = 24 * 60 * 60 * 1000;

/**
 * Run this ONCE after pasting the code in. Creates all labels and installs
 * the recurring background trigger. Safe to run again at any time.
 */
function setup() {
  var labelNames = Object.keys(CONFIG.snoozeLabels)
    .concat(Object.keys(CONFIG.replyLabels))
    .concat([CONFIG.returnedLabel, CONFIG.noReplyLabel]);
  labelNames.forEach(getOrCreateLabel_);

  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'processBoomerangs') {
      ScriptApp.deleteTrigger(t);
    }
  });
  ScriptApp.newTrigger('processBoomerangs')
    .timeBased()
    .everyMinutes(CONFIG.checkEveryMinutes)
    .create();

  Logger.log('Boomerang Lite is set up. ' + labelNames.length +
    ' labels created and the background check runs every ' +
    CONFIG.checkEveryMinutes + ' minutes.');
}

/**
 * Removes the trigger and all tracking data. Labels are left in place so no
 * mail is lost; delete them from Gmail settings if you no longer want them.
 */
function uninstall() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'processBoomerangs') {
      ScriptApp.deleteTrigger(t);
    }
  });
  var props = PropertiesService.getUserProperties();
  props.getKeys().forEach(function (key) {
    if (key.indexOf(PROP_PREFIX) === 0) props.deleteProperty(key);
  });
  Logger.log('Boomerang Lite uninstalled. Labels were kept; remove them from Gmail settings if desired.');
}

/**
 * Main background job. Runs on the time trigger installed by setup().
 */
function processBoomerangs() {
  var props = PropertiesService.getUserProperties();
  trackNewlyLabelledThreads_(props);
  processTrackedThreads_(props);
}

/**
 * Logs everything currently being tracked. Run manually to inspect state.
 */
function status() {
  var props = PropertiesService.getUserProperties();
  var keys = props.getKeys().filter(function (k) { return k.indexOf(PROP_PREFIX) === 0; });
  if (keys.length === 0) {
    Logger.log('Nothing is currently tracked.');
    return;
  }
  keys.forEach(function (key) {
    var entry = JSON.parse(props.getProperty(key));
    var thread = GmailApp.getThreadById(key.slice(PROP_PREFIX.length));
    var subject = thread ? thread.getFirstMessageSubject() : '(thread not found)';
    Logger.log('[' + entry.type + '] "' + subject + '" due ' + new Date(entry.due));
  });
}

// ---------------------------------------------------------------------------
// Internals
// ---------------------------------------------------------------------------

function trackNewlyLabelledThreads_(props) {
  trackForLabelSet_(props, CONFIG.snoozeLabels, 'snooze');
  trackForLabelSet_(props, CONFIG.replyLabels, 'reply');
}

function trackForLabelSet_(props, labelSet, type) {
  Object.keys(labelSet).forEach(function (labelName) {
    var label = GmailApp.getUserLabelByName(labelName);
    if (!label) return;
    label.getThreads().forEach(function (thread) {
      var key = PROP_PREFIX + thread.getId();
      if (props.getProperty(key)) return; // already tracked
      var now = Date.now();
      props.setProperty(key, JSON.stringify({
        type: type,
        label: labelName,
        since: now,
        due: now + labelSet[labelName] * MS_PER_DAY
      }));
      thread.moveToArchive();
    });
  });
}

function processTrackedThreads_(props) {
  var me = getMyEmail_();
  var keys = props.getKeys().filter(function (k) { return k.indexOf(PROP_PREFIX) === 0; });

  keys.forEach(function (key) {
    var entry;
    try {
      entry = JSON.parse(props.getProperty(key));
    } catch (err) {
      props.deleteProperty(key);
      return;
    }

    var thread = GmailApp.getThreadById(key.slice(PROP_PREFIX.length));
    if (!thread) {
      props.deleteProperty(key);
      return;
    }

    // User removed the Boomerang label by hand: treat as cancelled.
    if (!threadHasLabel_(thread, entry.label)) {
      props.deleteProperty(key);
      return;
    }

    if (entry.type === 'reply' && hasReplySince_(thread, entry.since, me)) {
      // A reply arrived in time: clear tracking quietly.
      removeLabelByName_(thread, entry.label);
      props.deleteProperty(key);
      return;
    }

    if (entry.type === 'snooze' && thread.isInInbox()) {
      // New mail woke the thread up (or the user moved it back): cancel.
      removeLabelByName_(thread, entry.label);
      props.deleteProperty(key);
      return;
    }

    if (Date.now() >= entry.due) {
      returnThread_(thread, entry);
      props.deleteProperty(key);
    }
  });
}

function returnThread_(thread, entry) {
  thread.moveToInbox();
  thread.markUnread();
  removeLabelByName_(thread, entry.label);
  var tagName = entry.type === 'reply' ? CONFIG.noReplyLabel : CONFIG.returnedLabel;
  getOrCreateLabel_(tagName).addToThread(thread);
}

function hasReplySince_(thread, sinceMs, me) {
  return thread.getMessages().some(function (message) {
    return message.getDate().getTime() > sinceMs &&
      message.getFrom().toLowerCase().indexOf(me) === -1;
  });
}

function threadHasLabel_(thread, labelName) {
  return thread.getLabels().some(function (label) {
    return label.getName() === labelName;
  });
}

function removeLabelByName_(thread, labelName) {
  var label = GmailApp.getUserLabelByName(labelName);
  if (label) label.removeFromThread(thread);
}

function getOrCreateLabel_(name) {
  return GmailApp.getUserLabelByName(name) || GmailApp.createLabel(name);
}

function getMyEmail_() {
  return Session.getActiveUser().getEmail().toLowerCase();
}
