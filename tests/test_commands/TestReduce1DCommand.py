import unittest
import mock
from mock import MagicMock, PropertyMock, call

from framework.Reduce1DCommand import Reduce1DCommand
from framework.LoadWorkspacesCommand import LoadWorkspacesCommand
from models.WorkspaceModel import WorkspaceModel
from mantid.simpleapi import CreateSampleWorkspace, DeleteWorkspace
from mantid.api import AnalysisDataService

class TestReduce1DCommand(unittest.TestCase):
    def test_that_invalid_state_cannot_execute(self):
        # Arrange
        workspace_model = mock.create_autospec(WorkspaceModel)
        load_command = mock.create_autospec(LoadWorkspacesCommand)
        load_command.can_execute.return_value = False

        # Act
        command = Reduce1DCommand(workspace_model, load_command)
        # Assert
        self.assertFalse(command.can_execute())

    def test_that_divides_workspaces(self):
        # Arrange
        CreateSampleWorkspace(OutputWorkspace='scatter_workspace', WorkspaceType='Event')
        scatter_workspace = AnalysisDataService.retrieve('scatter_workspace')
        CreateSampleWorkspace(OutputWorkspace='scatter_empty_cell_workspace', WorkspaceType='Event')
        scatter_empty_cell_workspace = AnalysisDataService.retrieve('scatter_empty_cell_workspace')
        workspace_model = mock.create_autospec(WorkspaceModel)
        scatter_workspace_property = PropertyMock(return_value=scatter_workspace)
        scatter_empty_cell_workspace_property = PropertyMock(return_value=scatter_empty_cell_workspace)
        type(workspace_model).scattering_sample = scatter_workspace_property
        type(workspace_model).scattering_empty_cell = scatter_empty_cell_workspace_property

        load_command = mock.create_autospec(LoadWorkspacesCommand)
        load_command.can_execute.return_value = True

        # Act
        reduce_command = Reduce1DCommand(workspace_model, load_command)

        self.assertTrue(reduce_command.can_execute())
        reduce_command.execute()

        try:
            reduce_command.execute()
            has_raised = False
        except:
            has_raised = True
        self.assertFalse(has_raised)

        expected_output_workspace_name = 'scatter_workspace_reduced_1D'
        self.assertTrue(AnalysisDataService.doesExist(expected_output_workspace_name))

        # Clean up
        DeleteWorkspace(scatter_workspace)
        DeleteWorkspace(scatter_empty_cell_workspace)
        DeleteWorkspace(expected_output_workspace_name)
