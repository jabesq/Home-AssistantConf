### sensor.hue (Custom Hue sensors platform)

**Purpose**: Exposes Philips Hue motion, remote, tap, and geofence sensors as Home Assistant sensors by polling the Hue Bridge API.

- **Module**: `custom_components/sensor/hue.py`
- **Version**: 0.7
- **Dependencies**: Hue Bridge reachable over HTTP; Bridge API token; Python packages provided by Home Assistant (requests, voluptuous)

### Configuration (configuration.yaml)

```yaml
sensor:
  - platform: hue
    ip_address: 192.168.1.2   # Hue Bridge IP
    token: YOUR_HUE_API_KEY   # Hue API username/token
```

- Obtain a Hue API token by following the official Hue API getting started guide (press the bridge link button, then create a username). See the "Getting Started" section of the Hue API documentation.

### How it works

- Polls `http://<ip_address>/api/<token>/sensors` and parses response into logical sensors.
- Creates one HA sensor per logical Hue device keyed by model and unique ID.
- Update throttle: 0.1s. Avoid adding heavy automations that assume per-event streaming.

### Entities and attributes

Different Hue devices expose different attributes:

- SML (Hue Motion Sensor)
  - State: 'on' or 'off' (presence)
  - Attributes: `light_level`, `lx`, `dark`, `daylight`, `battery`, `on`, `reachable`, `last_updated`, `temperature`

- RWL (Hue Dimmer Remote)
  - State: button event string composed of button number and action: `1_click`, `1_hold`, `1_click_up`, `1_hold_up`, `2_*`, `3_*`, `4_*`
  - Attributes: `battery`, `on`, `reachable`, `last_updated`

- ZGP (Hue Tap)
  - State: one of `1_click`, `2_click`, `3_click`, `4_click`
  - Attributes: `last_updated`

- Geofence (Hue Mobile App presence)
  - State: 'on' or 'off'
  - Attributes: `model: Geofence`, `name`

### Example automations

Trigger on a motion sensor turning on:

```yaml
automation:
  - alias: Turn on hallway light on motion
    trigger:
      - platform: state
        entity_id: sensor.sml_hall_motion  # replace with your entity
        to: 'on'
    action:
      - service: light.turn_on
        target:
          entity_id: light.hall
```

Trigger on a specific dimmer button click:

```yaml
automation:
  - alias: Dimmer top button click
    trigger:
      - platform: state
        entity_id: sensor.rwl_living_remote
    condition:
      - condition: template
        value_template: "{{ trigger.to_state.state == '1_click' }}"
    action:
      - service: script.toggle_tv
```

### Developer reference

Public functions in `sensor/hue.py` used internally by the platform:

- `parse_hue_api_response(response: dict) -> dict`
- `parse_sml(response: dict) -> dict`
- `parse_zgp(response: dict) -> dict`
- `parse_rwl(response: dict) -> dict`
- `parse_geofence(response: dict) -> dict`
- `setup_platform(hass, config, add_devices, discovery_info=None)`
- `HueSensorData(parse_hue_api_response, config)` with `update()` and `_build_url(config)`
- `HueSensor(Entity)` with HA-standard properties and `update()`

These are exposed as part of the platform implementation; end users configure via YAML as shown above.