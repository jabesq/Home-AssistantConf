### HelloWorld (AppDaemon)

**Purpose**: Example app that logs a greeting when AppDaemon starts.

- **Module**: `appdaemon/apps/hello.py`
- **Class**: `HelloWorld`
- **Args**: none

### apps.yaml

```yaml
hello_world:
  module: hello
  class: HelloWorld
```

### Behavior

- On initialize, logs two lines confirming AppDaemon is ready.