import appdaemon.plugins.hass.hassapi as hass


class HarmonySceneHandler(hass.Hass):
    """State listener for Harmony states."""

    def initialize(self):
        self.listen_state(self.activate_scene_input, "remote.harmony_hub",
                                  attribute="current_activity",
                                  new=self.args["scene"])
        self.listen_state(self.deactivate_scene_input, "remote.harmony_hub",
                                  attribute="current_activity",
                                  old=self.args["scene"])
        self.listen_state(self.activate_scene, self.args["input_boolean"],
                            new='on')

    def activate_scene_input(self, entity, attribute, old, new, kwargs):
        #self.log_notify("State change: {} to {}".format(entity, new))
        self.log("Scène: {} démarré depuis Harmony".format(self.args["scene"]))
        if self.get_state(self.args["input_boolean"]) == 'off':
            self.turn_on(self.args["input_boolean"])

    def deactivate_scene_input(self, entity, attribute, old, new, kwargs):
        #self.log_notify("State change: {} to {}".format(entity, new))
        self.log("Scène: {} arrêtée depuis Harmony".format(self.args["scene"]))
        if self.get_state(self.args["input_boolean"]) == 'on':
            self.turn_off(self.args["input_boolean"])

    def activate_scene(self, entity, attribute, old, new, kwargs):
        self.log("Démarrer {}".format(self.args["scene"]))
        if self.entities.remote.harmony_hub.attributes.current_activity != self.args["scene"]:
            self.turn_on("remote.harmony_hub", activity=self.args["scene"])
