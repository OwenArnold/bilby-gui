import unittest
import mock

from nose.tools import raises
from models.WorkspaceModel import WorkspaceModel
from mantid.simpleapi import CreateSampleWorkspace, DeleteWorkspace


class TestWorkspaceModel(unittest.TestCase):
    def setUp(self):
        self.model = WorkspaceModel()

    def test_setting_valid_workspaces(self):
        sample_event_workspace = CreateSampleWorkspace(WorkspaceType="Event")
        self.model.scattering_sample = sample_event_workspace
        DeleteWorkspace(sample_event_workspace)

    @raises(ValueError)
    def test_setting_invalid_scattering_sample(self):
        self.model.scattering_sample = None

    @raises(ValueError)
    def test_setting_invalid_scattering_empty_cell(self):
        self.model.scattering_empty_cell = None

    @raises(ValueError)
    def test_setting_invalid_transmission_empty_cell(self):
        self.model.transmission_empty_cell = None
