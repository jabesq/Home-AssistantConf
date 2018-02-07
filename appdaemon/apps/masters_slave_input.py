import appdaemon.appapi as appapi

#
# App to merge
#
# Args:
#
#master_inputs_boolean: list of input master
#slave_input
#not_on (optionnal) disallow the masters to turn_on the slave (disable by
#                    default). ie: needed for remote
#
# Release Notes
#
# Version 1.0:
#   Initial Version

class BooleanORHandler(appapi.AppDaemon):

    def initialize(self):

        #self.register_constraint("slave_is_on")
        if 'not_on' not in self.args:
            for input_boolean in self.args["master_inputs_boolean"]:
                self.listen_state(self.boolean_or, input_boolean, new='on')
            self.listen_state(self.reset_masters, self.args["slave_input"],
                              new='off')

        for input_boolean in self.args["master_inputs_boolean"]:
            self.listen_state(self.boolean_and, input_boolean, new='off',
                              slave_is_on=1)

    def boolean_or(self, entity, attribute, old, new, kwargs):
        if self.get_state(self.args["slave_input"]) == 'off':
            self.log("{} is ON".format(entity))
            self.log("boolean_or: Turn {} ON".format(self.args["slave_input"]))
            self.turn_on(self.args["slave_input"])

    def boolean_and(self, entity, attribute, old, new, kwargs):
        if self.get_state(self.args["slave_input"]) == 'on':
            toBeTurnOff = True
            for input_boolean in self.args["master_inputs_boolean"]:
                if self.get_state(input_boolean) == 'on':
                    self.log("boolean_and: {} is ON".format(input_boolean))
                    toBeTurnOff = False
                    break
                else:
                    self.log("boolean_and: {} is OFF".format(input_boolean))

            if toBeTurnOff:
                self.log("boolean_and: {} to be turn off".format(self.args["slave_input"]))
                self.turn_off(self.args["slave_input"])

    def reset_masters(self, entity, attribute, old, new, kwargs):
        self.log("reset_masters: {} is OFF".format(entity))
        for input_boolean in self.args["master_inputs_boolean"]:
            self.log("reset_masters: Turn {} OFF".format(input_boolean))
            self.turn_off(input_boolean)

    def slave_is_on(self, value):
        if self.get_state(self.args["slave_input"]) == 'on':
            return True
        else:
            return False
