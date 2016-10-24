import os
from framework.ICommand import ICommand
from models.WorkspaceModel import WorkspaceModel
from models.WorkspaceNameModel import WorkspaceNameModel
from mantid.simpleapi import Load
from mantid.api import AnalysisDataService


# ----------------------------------------------------------------------------------------------------------------------
# Free functions
# ----------------------------------------------------------------------------------------------------------------------
class InputDataType(object):
    class Scattering(object):
        pass

    class ScatteringCellEmpty(object):
        pass

    class TransmissionCellEmpty(object):
        pass


def get_extension(data_type):
    if data_type is InputDataType.Scattering:
        return "_sans"
    elif data_type is InputDataType.ScatteringCellEmpty:
        return "_cell"
    elif data_type is InputDataType.TransmissionCellEmpty:
        return "_cell_trans"
    else:
        raise ValueError("Trying to select an unknown data type for loading. The data type was {0}.".format(data_type))


def create_output_workspace_name(file_path, data_type):
    """
    Extracts the workspace name from the file name and appends
    the data type. This can be
    1. sans for scattering sample
    2. cell for empty cell
    3. trans_cell for transmission of the empty cell

    :param file_path: the full path of the file to load
    :param data_type: describes the usage of the workspace
    """
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    extension = get_extension(data_type)
    return base_name + extension


# ----------------------------------------------------------------------------------------------------------------------
# LoadWorkspaceCommand
# ----------------------------------------------------------------------------------------------------------------------
class LoadWorkspacesCommand(ICommand):
    def __init__(self, workspace_model, workspace_name_model):
        super(LoadWorkspacesCommand, self).__init__()
        if not isinstance(workspace_model, WorkspaceModel):
            raise ValueError("LoadWorkspacesCommand: Expected a workspace model of type WorkspaceModel but "
                             "instead got type {0}".format(type(workspace_model)))
        if not isinstance(workspace_name_model, WorkspaceNameModel):
            raise ValueError("LoadWorkspacesCommand: Expected a workspace name model of type WorkspaceNameModel but "
                             "instead got type {0}".format(type(workspace_model)))
        self._workspace_model = workspace_model
        self._workspace_name_model = workspace_name_model

    def can_execute(self):
        is_valid = True

        # We need to ensure that the sample scatter input exists
        scattering_sample_name = self._workspace_name_model.scattering_sample
        if scattering_sample_name == "":
            is_valid = False

        return is_valid

    def execute(self):
        # Check that can execute the file
        if not self.can_execute():
            raise RuntimeError("LoadWorkspacesCommand: The command cannot execute. The model does not appear to be"
                               " in a valid state.")
        # ------------------------------
        # Load the sample scatter entry
        # ------------------------------
        scattering_sample_file_path = self._workspace_name_model.scattering_sample
        self._set_workspace_on_model(scattering_sample_file_path, InputDataType.Scattering)

        # ------------------------------------
        # Load the scattering empty cell entry
        # ------------------------------------
        scattering_empty_cell_file_path = self._workspace_name_model.scattering_empty_cell
        self._set_workspace_on_model(scattering_empty_cell_file_path, InputDataType.ScatteringCellEmpty)

        # --------------------------------------
        # Load the transmission empty cell entry
        # --------------------------------------
        transmission_empty_cell_file_path = self._workspace_name_model.transmission_empty_cell
        self._set_workspace_on_model(transmission_empty_cell_file_path, InputDataType.TransmissionCellEmpty)

    def _set_workspace_on_model(self, file_name, data_type):
        """
        Loads a workspace from a specified file.

        The steps are:
        1. Create expected workspace name from file name and data type (e.g. scatter sample)
        2. Check if the workspace already exists in the WorkspaceModel if it does, then dont't reload it
        3. If the workspace has not been loaded yet, then load it and add it to the WorkspaceModel
        :param file_name:
        :param data_type:
        :return:
        """
        if not file_name:
            return

        # 1. Create workspace name
        workspace_name = create_output_workspace_name(file_name, data_type)
        # 2. Check if workspace already exists on WorkspaceModel
        workspace = self._get_workspace_model_entry(data_type)
        exists_already_on_workspace_model = self._check_if_workspace_exists_already_on_workspace_model(workspace_name,
                                                                                                       workspace)
        # 3. Load the workspace into the model if required
        if not exists_already_on_workspace_model:
            self._add_workspace_to_workspace_model(file_name, workspace_name, data_type)

    def _get_workspace_model_entry(self, data_type):
        if data_type is InputDataType.Scattering:
            workspace = self._workspace_model.scattering_sample
        elif data_type is InputDataType.ScatteringCellEmpty:
            workspace = self._workspace_model.scattering_empty_cell
        elif data_type is InputDataType.TransmissionCellEmpty:
            workspace = self._workspace_model.transmission_empty_cell
        else:
            raise ValueError("LoadWorkspacesCommand: The data type is not supported")
        return workspace

    def _set_workspace_model_entry(self, workspace, data_type):
        if data_type is InputDataType.Scattering:
            self._workspace_model.scattering_sample = workspace
        elif data_type is InputDataType.ScatteringCellEmpty:
            self._workspace_model.scattering_empty_cell = workspace
        elif data_type is InputDataType.TransmissionCellEmpty:
            self._workspace_model.transmission_empty_cell = workspace
        else:
            raise ValueError("LoadWorkspacesCommand: The data type is not supported")
        return workspace

    @staticmethod
    def _check_if_workspace_exists_already_on_workspace_model(workspace_name, workspace):
        workspace_already_exists = True
        if not workspace or workspace_name != workspace.name():
            workspace_already_exists = False
        return workspace_already_exists

    def _add_workspace_to_workspace_model(self, file_name, workspace_name, data_type):
        workspace = self._load_workspace(file_name, workspace_name)
        self._set_workspace_model_entry(workspace, data_type)

    @staticmethod
    def _load_workspace(file_name, workspace_name):
        Load(Filename=file_name, OutputWorkspace=workspace_name)
        return AnalysisDataService.retrieve[workspace_name]
