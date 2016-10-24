import os
from framework.ICommand import ICommand
from framework.LoadWorkspacesCommand import LoadWorkspacesCommand
from models.WorkspaceModel import WorkspaceModel
from mantid.simpleapi import Divide


# ----------------------------------------------------------------------------------------------------------------------
# Free functions
# ----------------------------------------------------------------------------------------------------------------------
def get_output_workspace_name(input_workspace):
    """
    We take the name of the input workspace and append _reduced_1D

    :param input_workspace: the scattering sample workspace
    :return: the name of the output workspace
    """
    input_workspace_name = input_workspace.name()
    return input_workspace_name + "_reduced_1D"

class Reduce1DCommand(ICommand):
    def __init__(self, workspace_model, load_command):
        super(Reduce1DCommand, self).__init__()
        if not isinstance(workspace_model, WorkspaceModel):
            raise ValueError("LoadWorkspacesCommand: Expected a workspace model of type WorkspaceModel but "
                             "instead got type {0}".format(type(workspace_model)))
        if not isinstance(load_command, LoadWorkspacesCommand):
            raise ValueError("LoadWorkspacesCommand: Expected a workspace name model of type WorkspaceNameModel but "
                             "instead got type {0}".format(type(workspace_model)))
        self._workspace_model = workspace_model
        self._load_command = load_command

    def can_execute(self):
        is_valid = True

        # There has to be valid data
        if not self._load_command.can_execute():
            is_valid = False

        # Add further requirements regarding the configuration here

        return is_valid

    def execute(self):
        # Check that can execute the file
        if not self.can_execute():
            raise RuntimeError("Reduce1DCommand: The command cannot execute. The command does not appear to be"
                               " in a valid state.")

        # Load the data
        self._load_command.execute()

        # Perform a 1D reduction
        self._reduce_1D()

    def _reduce_1D(self):
        # Get the workspaces from the workspace model
        scattering_sample = self._workspace_model.scattering_sample
        scattering_empty_cell = self._workspace_model.scattering_empty_cell
        transmission_empty_cell = self._workspace_model.transmission_empty_cell

        # Here we need to access other models for the configuration
        self._load_configuration()

        # Divide Workspace
        self._divide(scattering_sample=scattering_sample,
                           scattering_empty_cell=scattering_empty_cell,
                           transmission_empty_cell=transmission_empty_cell)

    def _divide(self, scattering_sample, scattering_empty_cell, transmission_empty_cell):
        """
        Perform the 1D reduction.

        :param scattering_sample: the scatter sample workspace
        :param scattering_empty_cell: the scattering empty cell workspace
        :param transmission_empty_cell: the transmission empty cell workspace
        """
        _ = transmission_empty_cell

        # Get the name of the output workspace
        output_workspace_name = get_output_workspace_name(scattering_sample)

        # As a dummy operation add the scattering sample and the scattering empty cell together
        Divide(LHSWorkspace=scattering_sample,
               RHSWorkspace=scattering_empty_cell,
               OutputWorkspace=output_workspace_name)

    def _load_configuration(self):
        pass
