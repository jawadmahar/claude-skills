# Boomerang Lite for Gmail

A free, self-installed alternative to Boomerang for Gmail, built entirely on **Google Apps Script**. It runs inside your own Google account - no third-party servers, no subscription, no data leaving your mailbox.

## What it does

| Feature | How it works |
|---|---|
| **Snooze an email** | Apply a `Boomerang/Snooze/...` label (or tap a button in the add-on). The thread is archived, then returned to your inbox as **unread** when the time is up, tagged `Boomerang/Returned`. |
| **Remind me if no reply** | After sending, apply a `Boomerang/Awaiting-Reply/...` label. If nobody replies before the deadline, the thread comes back to your inbox tagged `Boomerang/No-Reply`. If a reply arrives in time, tracking clears silently. |
| **Wake on new mail** | If a snoozed thread receives a new message, the snooze cancels automatically. |
| **Cancel any time** | Remove the Boomerang label from a thread and tracking is dropped on the next check. |
| **Schedule send** | Not included - Gmail now has this built in (Send button > arrow > Schedule send). |

Built-in durations: snooze for 1, 2 or 3 days, 1 or 2 weeks, or 1 month; reply-watch for 2 or 3 days, 1 or 2 weeks. Edit `CONFIG` at the top of `Code.gs` to add your own - any label following the same pattern works.

Because it is label-driven, it works from **Gmail on desktop, Android and iOS** even without the add-on UI - just apply the label from the normal Gmail label menu.

## Part 1 - Core install (about 5 minutes, required)

1. Go to [script.google.com](https://script.google.com) while signed in to the Gmail account you want this on, and click **New project**.
2. Name the project **Boomerang Lite** (click "Untitled project" at the top).
3. Open **Project Settings** (gear icon) and tick **"Show 'appsscript.json' manifest file in editor"**.
4. Back in the **Editor**:
   - Open `appsscript.json`, delete its contents, and paste in the contents of [`appsscript.json`](appsscript.json) from this folder.
   - Open `Code.gs`, delete its contents, and paste in [`Code.gs`](Code.gs).
   - Click **+** next to Files, choose **Script**, name it `AddOn`, and paste in [`AddOn.gs`](AddOn.gs).
5. Save all files (Ctrl+S / Cmd+S).
6. In the toolbar, select the function **`setup`** and click **Run**.
7. Google will ask you to authorise. Because this is your own personal script, you will see an "unverified app" warning: click **Advanced > Go to Boomerang Lite (unsafe)** and approve. This is normal for self-made scripts - you are only granting access to yourself.
8. Check the execution log says setup completed. Done.

You now have the `Boomerang/...` labels in Gmail and a background check running every 15 minutes.

### Using it (label mode)

- **Snooze**: open any email, apply e.g. label `Boomerang/Snooze/3-Days`. Within 15 minutes it is archived; three days later it is back in your inbox, unread.
- **Follow-up reminder**: after sending an email, open it in your Sent folder (or the thread) and apply e.g. `Boomerang/Awaiting-Reply/1-Week`. If no reply arrives within a week, it returns tagged `Boomerang/No-Reply`.
- **Cancel**: remove the label from the thread.

## Part 2 - Optional add-on UI (nicer buttons in Gmail)

This adds a Boomerang Lite panel in the right-hand sidebar when you open a message, with one-click buttons instead of labels.

1. In the Apps Script editor, click **Deploy > Test deployments**.
2. Under "Application(s)", make sure **Gmail** is listed, then click **Install**.
3. Refresh Gmail. Open any email and click the alarm icon in the right sidebar.

The add-on appears on Gmail desktop and in the Gmail mobile apps. It is a "test deployment", which is exactly right for a personal install - only you can see it.

## Maintenance

- **Check what is tracked**: run `status()` in the editor and read the log.
- **Change durations or frequency**: edit `CONFIG` in `Code.gs`, save, then run `setup()` again.
- **Uninstall**: run `uninstall()` (removes the trigger and tracking data), then delete the `Boomerang/...` labels from Gmail settings if you no longer want them. To remove the add-on panel, go to Deploy > Test deployments > Uninstall.

## Limitations (by design, to keep it simple)

- Timing granularity is the trigger interval (default 15 minutes), not to the second.
- Reply detection compares sender addresses to your primary address. If you send from an alias ("send mail as"), a reply to the alias is still detected, but your *own* messages sent from an alias may be counted as a reply on watched threads. Most users never hit this.
- Snooze durations are day-based presets rather than a free-form date picker. Add more presets in `CONFIG` if needed (fractional days are fine, e.g. `0.5` for 12 hours... though the label name is up to you).
- Google quotas for free accounts are generous (90 minutes of trigger runtime per day); each check takes a few seconds, so you will not get near them.

## Privacy

Everything runs in your own Google account under your own Apps Script project. No data is sent anywhere. The broad Gmail scope is required because the script must archive threads and move them back to your inbox.
