/**
 * Boomerang Lite - optional Gmail add-on UI
 * -----------------------------------------
 * Gives you one-click snooze and "remind me if no reply" buttons in a
 * sidebar when reading a message, on Gmail desktop and the mobile apps.
 *
 * The add-on is optional: everything also works by applying the
 * Boomerang labels by hand. See README.md ("Part 2") for how to install
 * this UI via Deploy -> Test deployments.
 */

function buildMessageCard(e) {
  var snoozeSection = CardService.newCardSection()
    .setHeader('Snooze (return to inbox later)');
  Object.keys(CONFIG.snoozeLabels).forEach(function (labelName) {
    snoozeSection.addWidget(actionButton_(shortName_(labelName), labelName, 'snooze'));
  });

  var replySection = CardService.newCardSection()
    .setHeader('Remind me if no reply within');
  Object.keys(CONFIG.replyLabels).forEach(function (labelName) {
    replySection.addWidget(actionButton_(shortName_(labelName), labelName, 'reply'));
  });

  return CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader()
      .setTitle('Boomerang Lite')
      .setSubtitle('Archive now, come back when it matters'))
    .addSection(snoozeSection)
    .addSection(replySection)
    .build();
}

function buildHomepageCard() {
  var props = PropertiesService.getUserProperties();
  var tracked = props.getKeys().filter(function (k) {
    return k.indexOf(PROP_PREFIX) === 0;
  }).length;

  var section = CardService.newCardSection()
    .addWidget(CardService.newTextParagraph()
      .setText('Currently tracking <b>' + tracked + '</b> thread(s).'))
    .addWidget(CardService.newTextButton()
      .setText('Run check now')
      .setOnClickAction(CardService.newAction().setFunctionName('runCheckFromAddOn')));

  return CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle('Boomerang Lite'))
    .addSection(section)
    .build();
}

function handleBoomerangAction(e) {
  var labelName = e.parameters.label;
  var type = e.parameters.type;
  var days = (type === 'snooze' ? CONFIG.snoozeLabels : CONFIG.replyLabels)[labelName];

  GmailApp.setCurrentMessageAccessToken(e.gmail.accessToken);
  var thread = GmailApp.getMessageById(e.gmail.messageId).getThread();

  getOrCreateLabel_(labelName).addToThread(thread);
  var now = Date.now();
  PropertiesService.getUserProperties().setProperty(
    PROP_PREFIX + thread.getId(),
    JSON.stringify({ type: type, label: labelName, since: now, due: now + days * MS_PER_DAY })
  );
  thread.moveToArchive();

  var verb = type === 'reply' ? 'Watching for a reply until ' : 'Snoozed until ';
  return CardService.newActionResponseBuilder()
    .setNotification(CardService.newNotification()
      .setText(verb + formatDue_(now + days * MS_PER_DAY)))
    .build();
}

function runCheckFromAddOn() {
  processBoomerangs();
  return CardService.newActionResponseBuilder()
    .setNotification(CardService.newNotification().setText('Boomerang check complete.'))
    .setNavigation(CardService.newNavigation().updateCard(buildHomepageCard()))
    .build();
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function actionButton_(text, labelName, type) {
  return CardService.newTextButton()
    .setText(text)
    .setOnClickAction(CardService.newAction()
      .setFunctionName('handleBoomerangAction')
      .setParameters({ label: labelName, type: type }));
}

function shortName_(labelName) {
  return labelName.split('/').pop().replace(/-/g, ' ');
}

function formatDue_(dueMs) {
  return Utilities.formatDate(new Date(dueMs), Session.getScriptTimeZone(), 'EEE d MMM, HH:mm');
}
