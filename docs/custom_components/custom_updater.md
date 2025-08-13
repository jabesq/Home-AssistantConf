### custom_updater (Home Assistant custom component)

**Purpose**: Track and update custom Lovelace cards, custom components, and python_scripts from remote trackers.

- **Domain**: `custom_updater`
- **Version**: 3.1.8
- **Requirements**: `pyupdate==0.2.16`

### Configuration (configuration.yaml)

```yaml
automations: []  # example placeholder
# ...
custom_updater:
  track:
    - components
    - cards
    # - python_scripts
  hide_sensor: false
  show_installable: false
  card_urls:
    - https://raw.githubusercontent.com/kalkih/mini-media-player/master/tracker.json
  component_urls:
    - https://raw.githubusercontent.com/robmarkcole/Hue-sensors-HASS/master/custom_updater.json
  # python_script_urls:
  #   - https://example.com/python_scripts/tracker.json
```

- **track**: list of categories to track: `components`, `cards`, `python_scripts`.
- **hide_sensor**: if true, tracker sensors are hidden in UI.
- **show_installable**: include installable items (not just installed) in sensors.
- ***_urls**: optional additional tracker JSON URLs.

### Created sensors

- `sensor.custom_card_tracker`
- `sensor.custom_component_tracker`
- `sensor.custom_python_script_tracker`

Each sensor state is the number of updatable items. Attributes come from `pyupdate` plus `hidden: <bool>`.

### Services

- `custom_updater.check_all`
  - Triggers a cache refresh for configured trackers.
- `custom_updater.update_all`
  - Updates all updatable items for configured trackers, then refreshes sensors.
- `custom_updater.install`
  - Installs a single element by name.
  - Data: `element: <string>`

Examples:

```yaml
# Call from an automation or the Developer Tools → Services
service: custom_updater.check_all
```

```yaml
service: custom_updater.update_all
```

```yaml
service: custom_updater.install
data:
  element: mini-media-player  # an element name present in your tracker feed
```

### Notes

- Sensors update daily by default. Manual services can be called at any time.
- Ensure your tracker JSON feeds are reachable and correctly formatted for `pyupdate`.