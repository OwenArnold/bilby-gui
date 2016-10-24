import unittest
import mock
from mock import MagicMock, PropertyMock, call

from Commands.LoadWorkspacesCommand import LoadWorkspacesCommand
from models.WorkspaceModel import WorkspaceModel
from models.WorkspaceNameModel import WorkspaceNameModel
from mantid.api import IEventWorkspace


class TestLoadWorkspacesCommand(unittest.TestCase):
    def test_loading_already_loaded_file_is_possible(self):
        # Arrange
        run_name = "BBY000123"
        expected_workspace_name = run_name + "_sans"
        file_name = "C:\\path11\\path2\\" + run_name + ".nxs"

        workspace_model = mock.create_autospec(WorkspaceModel)
        workspace_name_model = mock.create_autospec(WorkspaceNameModel)
        scattering_sample_file_name_property = PropertyMock(return_value=file_name)
        scattering_empty_cell_file_name_property = PropertyMock(return_value="")
        transmission_empty_cell_file_name_property = PropertyMock(return_value="")
        type(workspace_name_model).scattering_sample = scattering_sample_file_name_property
        type(workspace_name_model).scattering_empty_cell = scattering_empty_cell_file_name_property
        type(workspace_name_model).transmission_empty_cell = transmission_empty_cell_file_name_property

        workspace_mock = MagicMock()
        workspace_mock.name.return_value = expected_workspace_name
        scatter_sample_property = PropertyMock(return_value=workspace_mock)
        scattering_empty_cell_property = PropertyMock(return_value=None)
        transmission_empty_cell_property = PropertyMock(return_value=None)
        type(workspace_model).scattering_sample = scatter_sample_property
        type(workspace_model).scattering_empty_cell = scattering_empty_cell_property
        type(workspace_model).transmission_empty_cell = transmission_empty_cell_property
        # Act
        command = LoadWorkspacesCommand(workspace_model, workspace_name_model)

        self.assertTrue(command.can_execute())
        try:
            command.execute()
            has_raised = False
        except:
            has_raised = True

        # Assert
        self.assertFalse(has_raised)
        self.assertTrue(scattering_sample_file_name_property.call_count == 3)
        self.assertTrue(scattering_empty_cell_file_name_property.call_count == 1)
        self.assertTrue(transmission_empty_cell_file_name_property.call_count == 1)
        self.assertTrue(scatter_sample_property.call_count == 1)
        self.assertTrue(scattering_empty_cell_property.call_count == 0)
        self.assertTrue(transmission_empty_cell_property.call_count == 0)

        calls = [call()]
        self.assertTrue(transmission_empty_cell_file_name_property.has_calls(calls))

    def test_file_is_loaded_if_workspace_does_not_already_exist_in_model(self):
        # Arrange
        run_name = "BBY000123"
        file_name = "C:\\path11\\path2\\" + run_name + ".nxs"

        workspace_name_model = mock.create_autospec(WorkspaceNameModel)
        scattering_sample_file_name_property = PropertyMock(return_value=file_name)
        scattering_empty_cell_file_name_property = PropertyMock(return_value="")
        transmission_empty_cell_file_name_property = PropertyMock(return_value="")
        type(workspace_name_model).scattering_sample = scattering_sample_file_name_property
        type(workspace_name_model).scattering_empty_cell = scattering_empty_cell_file_name_property
        type(workspace_name_model).transmission_empty_cell = transmission_empty_cell_file_name_property

        workspace_model = mock.create_autospec(WorkspaceModel)
        scatter_sample_property = PropertyMock(return_value=None)
        scattering_empty_cell_property = PropertyMock(return_value=None)
        transmission_empty_cell_property = PropertyMock(return_value=None)
        type(workspace_model).scattering_sample = scatter_sample_property
        type(workspace_model).scattering_empty_cell = scattering_empty_cell_property
        type(workspace_model).transmission_empty_cell = transmission_empty_cell_property

        command = LoadWorkspacesCommand(workspace_model, workspace_name_model)
        mock_workspace = mock.create_autospec(IEventWorkspace)
        command._load_workspace = MagicMock(return_value=mock_workspace)

        self.assertTrue(command.can_execute())
        try:
            command.execute()
            has_raised = False
        except:
            has_raised = True

        # Assert
        self.assertFalse(has_raised)
        self.assertTrue(scattering_sample_file_name_property.call_count == 3)
        self.assertTrue(scattering_empty_cell_file_name_property.call_count == 1)
        self.assertTrue(transmission_empty_cell_file_name_property.call_count == 1)

        self.assertTrue(scatter_sample_property.call_count == 2)
        self.assertTrue(scattering_empty_cell_property.call_count == 0)
        self.assertTrue(transmission_empty_cell_property.call_count == 0)

        calls = [call(), call(mock_workspace)]
        self.assertTrue(transmission_empty_cell_file_name_property.has_calls(calls))

    def test_that_invalid_state_raises(self):
        # Arrange
        workspace_model = mock.create_autospec(WorkspaceModel)
        workspace_name_model = mock.create_autospec(WorkspaceNameModel)
        scattering_sample_file_name_property = PropertyMock(return_value="")
        type(workspace_name_model).scattering_sample = scattering_sample_file_name_property
        # Act
        command = LoadWorkspacesCommand(workspace_model, workspace_name_model)
        # Assert
        self.assertFalse(command.can_execute())
