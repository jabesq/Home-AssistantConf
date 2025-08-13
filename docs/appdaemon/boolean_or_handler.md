### BooleanORHandler (AppDaemon)

**Purpose**: Merge multiple `input_boolean` entities into a single slave entity using logical OR semantics, with optional synchronization back from the slave.

- **Module**: `appdaemon/apps/masters_slave_input.py`
- **Class**: `BooleanORHandler`

### Args

- `master_inputs_boolean` (required): list of input_boolean entity IDs (masters)
- `slave_input` (required): target entity to control (e.g., an `input_boolean` or a `remote.*` entity)
- `not_on` (optional): if set, disallows the OR path that turns the slave ON; OFF behavior still mirrors masters

### apps.yaml

```yaml
HarmonyInputSelects:
  module: masters_slave_input
  class: BooleanORHandler
  master_inputs_boolean:
    - input_boolean.appletv
    - input_boolean.ps4
    - input_boolean.switch
    - input_boolean.music
    - input_boolean.chromecast
  slave_input: remote.harmony_hub
  not_on: 1
```

Another example for merging babyphone booleans into a single `input_boolean.babyphone` exists in `appdaemon/apps/apps.yaml`.

### Behavior

- When any master turns ON, turns ON the `slave_input` (unless `not_on` is set).
- When all masters are OFF, turns OFF the `slave_input`.
- When the slave turns OFF, resets all masters to OFF.

### Constraints

Custom constraints available for targeted callbacks:

- `slave_is(value: 'on'|'off')`: triggers only when the slave matches `value`.
- `masters_are(value: 'on'|'off')`: triggers only when any master matches `value`.