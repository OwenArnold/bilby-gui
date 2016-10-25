import unittest
import os
from mock import PropertyMock, create_autospec

from framework.SaveCommand import SaveCommand
from models.SaveModel import SaveModel
from mantid.simpleapi import CreateSampleWorkspace, DeleteWorkspace


class TestSaveCommand(unittest.TestCase):
    def test_that_invalid_state_raises(self):
        # Arrange
        save_model = create_autospec(SaveModel)
        file_name_property = PropertyMock(return_value="")
        workspace_name_property = PropertyMock(return_value="test")
        type(save_model).file_name = file_name_property
        type(save_model).workspace_name = workspace_name_property

        # Act
        command = SaveCommand(save_model)
        # Assert
        self.assertFalse(command.can_execute())

    def test_that_can_save_valid_state(self):
        # Arrange
        workspace_name = "sample_workspace"
        CreateSampleWorkspace(OutputWorkspace=workspace_name)
        test_file_name = "test_file.nxs"
        test_path = os.path.dirname(__file__)
        test_file = os.path.join(test_path, test_file_name)

        save_model = create_autospec(SaveModel)
        file_name_property = PropertyMock(return_value=test_file)
        workspace_name_property = PropertyMock(return_value=workspace_name)
        type(save_model).file_name = file_name_property
        type(save_model).workspace_name = workspace_name_property

        # Act
        command = SaveCommand(save_model)
        # Assert
        self.assertTrue(command.can_execute())

        try:
            command.execute()
            has_raised = False
        except:
            has_raised = True
        self.assertFalse(has_raised)

        # Clean up
        DeleteWorkspace(workspace_name)
        if os.path.exists(test_file):
            os.remove(test_file)
