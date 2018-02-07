import appdaemon.appapi as appapi

#
# App to handle babyphone
#
# Args:
#
#media_player: Media player to play the babyphone alarm
#lights: Lights to be turn on with the baby alarm
#sonos (optionnal): Set to 1 if the media player is a Sonos player
#
# Release Notes
#
# Version 1.0:
#   Initial Version

class BabyPhoneHandler(appapi.AppDaemon):
    """Event listener for babyphone events."""

    def initialize(self):
        self.register_constraint("media_player_selection")
        self.listen_state(
            self.babyphone_alarm_on, "binary_sensor.ffmpeg_noise", new="on"
            )
        self.listen_state(
            self.babyphone_alarm_off, "binary_sensor.ffmpeg_noise", new="off"
            )

    def babyphone_alarm_on(self, entity, attribute, old, new, kwargs):
        if self.get_state(self.args["input_boolean"]) == 'on':
            self.log("Babyphone alarm on")
            if "sonos" in self.args:
                self.call_service("media_player/sonos_snapshot",
                                   entity_id = self.args["media_player"])
                self.call_service("media_player/sonos_unjoin",
                                   entity_id = self.args["media_player"])
            self.call_service("media_player/volume_set",
                               entity_id = self.args["media_player"],
                               volume_level = 0.4)
            self.call_service("media_player/play_media",
                               entity_id = self.args["media_player"],
                               media_content_type = 'music',
                               media_content_id= 'http://127.0.0.1:8000/babyphone.mp3')
            self.call_service("light/turn_on", entity_id=self.args['lights'],
                               brightness=150)

    def babyphone_alarm_off(self, entity, attribute, old, new, kwargs):
        if self.get_state(self.args["input_boolean"]) == 'on':
            self.log("Babyphone alarm off")
            if "sonos" in self.args:
                self.call_service("media_player/sonos_restore",
                                   entity_id = self.args["media_player"])
            self.call_service("light/turn_off", entity_id=self.args['lights'])

    def media_player_selection(self, value):
        if self.get_state(self.args["input_boolean"]) == 'on':
            return True
        else:
            return False
