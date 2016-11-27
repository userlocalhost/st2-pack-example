import os

from st2actions.runners.pythonrunner import Action


class OutputContext(Action):
    def run(self, context):
        output_path = self.config.get('log', None)

        if output_path:
            try:
                with open(output_path, 'a') as file:
                    file.write(context + '\n')
            except IOError as err:
                return (False, "IOError is occurred (%s)" % (err))

            return (True, "This processing is succeeded.")
        else:
            return (False, "The output filepath is invalid.")
