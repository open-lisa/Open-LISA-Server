from open_lisa.domain.command.command import Command, CommandType
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.command_return import CommandReturn

C_LIBS_PATH = 'data/clibs/'


class CLibCommand(Command):
    def __init__(self, name, lib_function, lib_file_name, parameters=CommandParameters(), command_return=CommandReturn(), description=''):
        """Creates a new SCPI command

        Args:
            name (string): the string syntax that identifies the command
            lib_function (string): Lib function to be called in the lib file
            lib_file_name (string): Lib file name (C libs should be stored in C_LIBS_PATH)
            parameters (CommandParameters): an instance of command parameters
        """
        super().__init__(name=name, command=lib_function,
                         parameters=parameters, type=CommandType.CLIB, description=description)

        self.lib_function = lib_function
        self.lib_file_name = lib_file_name
        self.command_return = command_return

    @staticmethod
    def from_dict(command_dict, pyvisa_resource):
        return CLibCommand(
            name=command_dict["name"],
            lib_function=pyvisa_resource,
            lib_file_name=command_dict["lib_file_name"],
            parameters=CommandParameters.from_dict(command_dict["params"]),
            description=command_dict["description"]
        )

    def to_dict(self, instrument_id):
        return {
            "instrument_id": instrument_id,
            "name": self.name,
            "command": self.lib_function,
            "type": str(self.type),
            "lib_file_name": self.lib_file_name,
            "description": self.description,
            "params": self.parameters.to_dict(),
            "return": self.command_return.to_dict()
        }

    def execute(self, params_values=[]):
        # TODO: implement execution
        # similar to __process_c_lib_call in Instrument
        # remember to handle bytes CommandReturn type with a tmp file
        pass
