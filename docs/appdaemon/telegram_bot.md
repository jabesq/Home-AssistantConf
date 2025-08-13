### TelegramBotEventListener (AppDaemon)

**Purpose**: Demonstrate handling of Telegram bot text and callback events from Home Assistant and responding with messages and inline keyboards.

- **Module**: `appdaemon/apps/TelegramBot.py`
- **Class**: `TelegramBotEventListener`
- **Args**: none

### Prerequisites

- Home Assistant Telegram Bot integration configured and working.

### apps.yaml

```yaml
TelegramBot:
  module: TelegramBot
  class: TelegramBotEventListener
```

### Behavior

- Listens for `telegram_text` events:
  - Echoes back the received text with a simple inline keyboard.
- Listens for `telegram_callback` events:
  - `/edit_msg`: answers callback, then edits the originating message with details.
  - `/remove button`: answers callback, then edits the reply markup to remove a row.
  - `/do_nothing`: answers callback with a short acknowledgement.

### Example interaction

- Send any text to your bot → the app replies "You said: <text>" with inline buttons.
- Tap "Edit message" → the bot updates the previous message.
- Tap "Remove this button" → the inline keyboard is edited.