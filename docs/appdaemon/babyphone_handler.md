### BabyPhoneHandler and BabyPhoneLightHandler (AppDaemon)

**Purpose**: Provide audio alarm playback and optional visual alarm for a baby monitor signal based on an FFmpeg noise binary sensor.

- **Module**: `appdaemon/apps/babyphone.py`
- **Classes**: `BabyPhoneHandler`, `BabyPhoneLightHandler`

### BabyPhoneHandler

Plays/pauses a media player when `binary_sensor.ffmpeg_noise` toggles, with optional Sonos snapshot/restore.

Args:
- `media_player` (required): media_player entity to play the alarm
- `input_boolean` (required): input_boolean that enables responder behavior
- `sonos` (optional): set to a truthy value if the media player is a Sonos device

apps.yaml examples:

```yaml
BabyphoneChambre:
  module: babyphone
  class: BabyPhoneHandler
  media_player: media_player.chambre
  sonos: 1
  input_boolean: input_boolean.babyphone_chambre
  logfile: STDOUT
  errorfile: STDOUT

BabyphoneCuisine:
  module: babyphone
  class: BabyPhoneHandler
  media_player: media_player.cuisine
  sonos: 1
  input_boolean: input_boolean.babyphone_cuisine
  logfile: STDOUT
  errorfile: STDOUT

BabyphoneSalon:
  module: babyphone
  class: BabyPhoneHandler
  media_player: media_player.salon_google_home
  input_boolean: input_boolean.babyphone_salon
  logfile: STDOUT
  errorfile: STDOUT
```

Behavior:
- On `binary_sensor.ffmpeg_noise` → on: set volume (Sonos 0.6, others 0.8) and play a fixed MP3 URL `http://192.168.1.30:8000/babyphone.mp3`.
- On `binary_sensor.ffmpeg_noise` → off: pause playback. If Sonos, restore snapshot.
- When the configured `input_boolean` turns OFF: pause playback and restore if Sonos.

### BabyPhoneLightHandler

Flashes a light while noise is detected; turns light solid green when done.

Args:
- `alarm_light` (required): light entity to flash

apps.yaml example:

```yaml
BabyphoneLight:
  module: babyphone
  class: BabyPhoneLightHandler
  alarm_light: light.baby_alarm
```

Behavior:
- On `binary_sensor.ffmpeg_noise` from off→on: start flashing red every second.
- On `binary_sensor.ffmpeg_noise` off: stop flashing and set light to green.

### Notes

- The `lights` arg mentioned in comments is not used in the current implementation.
- Ensure the MP3 URL is reachable by your media players, or adapt the URL in the app code to your environment.