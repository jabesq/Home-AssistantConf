### HarmonySceneHandler (AppDaemon)

**Purpose**: Keep an `input_boolean` in sync with a specific Harmony Hub activity and allow turning on the activity by toggling the boolean.

- **Module**: `appdaemon/apps/harmony.py`
- **Class**: `HarmonySceneHandler`

### Args

- `scene` (required): exact Harmony activity name (as shown in HA state attributes)
- `input_boolean` (required): the input_boolean entity to mirror/control the scene

### apps.yaml

```yaml
HarmonyAppleTV:
  module: harmony
  class: HarmonySceneHandler
  scene: Regarder Apple TV
  input_boolean: input_boolean.appletv
  logfile: STDOUT
  errorfile: STDOUT
```

Additional examples exist in `appdaemon/apps/apps.yaml` for PS4, Switch, Music, Chromecast.

### Behavior

- When `remote.harmony_hub` `current_activity` becomes `scene`, turns ON `input_boolean`.
- When `current_activity` leaves `scene`, turns OFF `input_boolean`.
- When `input_boolean` is turned ON, starts the Harmony activity if not already active.

### Notes

- Ensure your Harmony Hub is integrated as `remote.harmony_hub` in Home Assistant.
- Activity names must match exactly.