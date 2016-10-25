import os
from framework.ICommand import ICommand
from models.SaveModel import SaveModel
from mantid.simpleapi import SaveNexus
from mantid.api import AnalysisDataService


# ----------------------------------------------------------------------------------------------------------------------
# LoadWorkspaceCommand
# ----------------------------------------------------------------------------------------------------------------------
class SaveCommand(ICommand):
    def __init__(self, save_model):
        super(SaveCommand, self).__init__()
        if not isinstance(save_model, SaveModel):
            raise ValueError("SaveCommand: Expected a save model of type SaveModel but "
                             "instead got type {0}".format(type(save_model)))
        self._save_model = save_model

    def can_execute(self):
        is_valid = True

        # We need to ensure that the file name is not none and that the workspace exists.
        file_name = self._save_model.file_name
        workspace_name = self._save_model.workspace_name
        if file_name == "" or not AnalysisDataService.doesExist(workspace_name):
            is_valid = False
        return is_valid

    def execute(self):
        # Check that can execute the file
        if not self.can_execute():
            raise RuntimeError("SaveCommand: The command cannot execute. The model does not appear to be"
                               " in a valid state.")
        file_name = self._save_model.file_name
        workspace_name = self._save_model.workspace_name

        workspace = AnalysisDataService.retrieve(workspace_name)
        SaveNexus(InputWorkspace=workspace, Filename=file_name)


