import unittest
import mock

from nose.tools import raises
from models.WorkspaceModel import WorkspaceModel


class TestWorkspaceModel(unittest.TestCase):

    def setUp(self):
        self.model = WorkspaceModel()

    def test_setting_valid_filenames(self):
        test_path = "@path"

        self.assertEqual("", self.model.scattering_sample)
        self.assertEqual("", self.model.scattering_empty_cell)
        self.assertEqual("", self.model.transmission_empty_cell)
        self.assertEqual(False, self.model.debug_mode)

        self.model.scattering_sample = test_path
        self.model.scattering_empty_cell = test_path
        self.model.transmission_empty_cell = test_path
        self.model.debug_mode = True

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

    @raises(ValueError)
    def test_setting_invalid_debug_mode(self):
        self.model.debug_mode = None

    def test_valid_listener(self):
        test_path = "@path"
        listener = mock.create_autospec(WorkspaceModel.IListener)

        # test add_listener
        self.model.add_listener(listener)
        # first pass
        self.model.scattering_sample = test_path
        self.model.scattering_empty_cell = test_path
        self.model.transmission_empty_cell = test_path
        self.model.debug_mode = True
        # second pass
        self.model.scattering_sample = test_path
        self.model.scattering_empty_cell = test_path
        self.model.transmission_empty_cell = test_path
        self.model.debug_mode = True

        listener.on_scattering_sample_changed.assert_called_once_with(self.model, test_path)
        listener.on_scattering_empty_cell_changed.assert_called_once_with(self.model, test_path)
        listener.on_transmission_empty_cell_changed.assert_called_once_with(self.model, test_path)
        listener.on_debug_mode_changed.assert_called_once_with(self.model, True)

        # test remove_listener
        listener.reset_mock()
        self.model.remove_listener(listener)
        self.model.scattering_sample = ""
        self.model.scattering_empty_cell = ""
        self.model.transmission_empty_cell = ""
        self.model.debug_mode = False

        listener.on_scattering_sample_changed.assert_not_called()
        listener.on_scattering_empty_cell_changed.assert_not_called()
        listener.on_transmission_empty_cell_changed.assert_not_called()
        listener.on_debug_mode_changed.assert_not_called()

    @raises(ValueError)
    def test_invalid_listener(self):
        self.model.add_listener(None)
