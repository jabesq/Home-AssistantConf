import appdaemon.plugins.hass.hassapi as hass

#
# App to handle babyphone
#
# Args:
#
#media_player: Media player to play the babyphone alarm
#lights: Lights to be turn on with the baby alarm
#sonos (optionnal): Set to 1 if the media player is a Sonos player
#constrain_input_boolean: input_boolean.room
#
# Release Notes
#
# Version 1.0:
#   Initial Version

class BabyPhoneHandler(hass.Hass):
    """Event listener for babyphone events."""

    def initialize(self):
        self.register_constraint("media_player_selection")
        self.listen_state(
            self.babyphone_alarm_on, "binary_sensor.ffmpeg_noise", new="on",
            media_player_selection=1
            )
        self.listen_state(
            self.babyphone_alarm_off, "binary_sensor.ffmpeg_noise", new="off",
            media_player_selection=1
            )
        self.listen_state(
            self.stop_babyphone, self.args["input_boolean"], new="off"
            )

    def babyphone_alarm_on(self, entity, attribute, old, new, kwargs):
        self.log("Babyphone alarm on")
        if "sonos" in self.args:
            self.call_service("media_player/sonos_snapshot",
                               entity_id = self.args["media_player"])
            self.call_service("media_player/sonos_unjoin",
                               entity_id = self.args["media_player"])
            self.call_service("media_player/volume_set",
                               entity_id = self.args["media_player"],
                               volume_level = 0.6)
        else:
            self.call_service("media_player/volume_set",
                              entity_id = self.args["media_player"],
                              volume_level = 0.8)
        self.call_service("media_player/play_media",
                           entity_id = self.args["media_player"],
                           media_content_type = 'music',
                           media_content_id= 'http://192.168.1.30:8000/babyphone.mp3')

    def babyphone_alarm_off(self, entity, attribute, old, new, kwargs):
        self.log("Babyphone alarm off")
        self.call_service("media_player/media_pause",
                          entity_id = self.args["media_player"])
        if "sonos" in self.args:
            self.call_service("media_player/sonos_restore",
                               entity_id = self.args["media_player"])

    def stop_babyphone(self, entity, attribute, old, new, kwargs):
        self.log("Babyphone stopped")
        self.call_service("media_player/media_pause",
                          entity_id = self.args["media_player"])
        if "sonos" in self.args:
            self.call_service("media_player/sonos_restore",
                               entity_id = self.args["media_player"])

    def media_player_selection(self, value):
        if self.get_state(self.args["input_boolean"]) == 'on':
            return True
        else:
            return False

class BabyPhoneLightHandler(hass.Hass):
    def initialize(self):
        self.listen_state(
            self.start_alarm, "binary_sensor.ffmpeg_noise", new="on", old="off"
            )
        self.listen_state(
            self.stop_alarm, "binary_sensor.ffmpeg_noise", old="on"
            )

    def start_alarm(self, entity, attribute, old, new, kwargs):
        self.alarm_light_on = True
        self.turn_on(self.args["alarm_light"], color_name="red")
        self.light_alarm(kwargs)

    def light_alarm(self, kwargs):
        self.toggle(self.args["alarm_light"])
        if self.alarm_light_on:
            self.run_in(self.light_alarm, 1)
        else:
            self.turn_on(self.args["alarm_light"], color_name="green")

    def stop_alarm(self, entity, attribute, old, new, kwargs):
        self.alarm_light_on = False
