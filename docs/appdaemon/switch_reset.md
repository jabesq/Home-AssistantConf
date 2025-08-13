### SwitchReset (AppDaemon)

**Purpose**: Persist and restore states of `input_boolean`, `input_select`, `input_number`, and `device_tracker` across Home Assistant/AppDaemon restarts.

- **Module**: `appdaemon/apps/switch_reset.py`
- **Class**: `SwitchReset`

### Args

- `delay` (required): seconds to wait after startup before restoring states
- `file` (required): path to a shelve DB file for persisted states
- `dependencies` (optional): include `globals` to resolve notifier name
- `notify` (optional): if set, send notifications via `globals.notify`
- `verbose_log` (optional): if set, also log messages

### apps.yaml

```yaml
SwitchReset:
  module: switch_reset
  class: SwitchReset
  delay: 10
  dependencies: globals
  file: /home/homeassistant/appdaemon_log/switches.db
  # notify: 1
  # verbose_log: 1
```

### Behavior

- Subscribes to `ha_started` and `appd_started` and schedules a restore after `delay` seconds.
- Listens for state changes on the entity types above and persists the latest state to the shelve DB.
- On restore, iterates over current entities and sets the last known value where different.

### Notes

- Ensure the directory for the shelve DB is writable by the AppDaemon process.
- `globals.notify` is defined in `appdaemon/apps/globals.py` and can be adapted to your notifier of choice.