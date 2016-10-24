import unittest
import mock

from nose.tools import raises
from models.WorkspaceModel import WorkspaceModel
from mantid.api import IEventWorkspace


class TestWorkspaceModel(unittest.TestCase):
    def setUp(self):
        self.model = WorkspaceModel()

    def test_setting_valid_workspaces(self):
        sample_event_workspace = mock.create_autospec(IEventWorkspace)
        try:
            self.model.scattering_sample = sample_event_workspace
            has_raised = False
        except ValueError:
            has_raised = True
        self.assertFalse(has_raised)

    @raises(ValueError)
    def test_setting_invalid_scattering_sample(self):
        self.model.scattering_sample = None

    @raises(ValueError)
    def test_setting_invalid_scattering_empty_cell(self):
        self.model.scattering_empty_cell = None

    @raises(ValueError)
    def test_setting_invalid_transmission_empty_cell(self):
        self.model.transmission_empty_cell = None
