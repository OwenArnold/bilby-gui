import unittest
import mock

from nose.tools import raises
from models.WorkspaceNameModel import WorkspaceNameModel


class TestWorkspaceNameModel(unittest.TestCase):
    def setUp(self):
        self.model = WorkspaceNameModel()

    def test_setting_valid_filenames(self):
        test_path = "@path"

        self.model.scattering_sample = test_path
        self.model.scattering_empty_cell = test_path
        self.model.transmission_empty_cell = test_path

        self.assertEqual(test_path, self.model.scattering_sample)
        self.assertEqual(test_path, self.model.scattering_empty_cell)
        self.assertEqual(test_path, self.model.transmission_empty_cell)

    @raises(ValueError)
    def test_setting_invalid_scattering_sample(self):
        self.model.scattering_sample = None

    @raises(ValueError)
    def test_setting_invalid_scattering_empty_cell(self):
        self.model.scattering_empty_cell = None

    @raises(ValueError)
    def test_setting_invalid_transmission_empty_cell(self):
        self.model.transmission_empty_cell = None

    def test_valid_listener(self):
        test_path = "@path"
        listener = mock.create_autospec(WorkspaceNameModel.IListener)

        # test add_listener
        self.model.add_listener(listener)
        # first pass
        self.model.scattering_sample = test_path
        self.model.scattering_empty_cell = test_path
        self.model.transmission_empty_cell = test_path
        # second pass
        self.model.scattering_sample = test_path
        self.model.scattering_empty_cell = test_path
        self.model.transmission_empty_cell = test_path

        listener.on_scattering_sample_changed.assert_called_once_with(self.model, test_path)
        listener.on_scattering_empty_cell_changed.assert_called_once_with(self.model, test_path)
        listener.on_transmission_empty_cell_changed.assert_called_once_with(self.model, test_path)

        # test remove_listener
        listener.reset_mock()
        self.model.remove_listener(listener)
        self.model.scattering_sample = ""
        self.model.scattering_empty_cell = ""
        self.model.transmission_empty_cell = ""

        listener.on_scattering_sample_changed.assert_not_called()
        listener.on_scattering_empty_cell_changed.assert_not_called()
        listener.on_transmission_empty_cell_changed.assert_not_called()

    @raises(ValueError)
    def test_invalid_listener(self):
        self.model.add_listener(None)
