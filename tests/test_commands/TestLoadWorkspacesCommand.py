import unittest

from Commands.LoadWorkspacesCommand import LoadWorkspacesCommand
from model.WorkspaceModel import WorkspaceModel
from mantid.simpleapi import CreateSampleWorkspace, DeleteWorkspace


class TestLoadWorkspacesCommand(unittest.TestCase):
    def setUp(self):
        self.workspace_model = WorkspaceModel
        self.model = LoadWorkspacesCommand()

    def test_setting_valid_workspaces(self):
        sample_event_workspace = CreateSampleWorkspace(WorkspaceType="Event")
        self.model.scattering_sample = sample_event_workspace
        DeleteWorkspace(sample_event_workspace)
