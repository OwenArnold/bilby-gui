import unittest
import mock

from nose.tools import raises
from models.WorkspaceNameModel import WorkspaceNameModel


class TestWorkspaceNameModel(unittest.TestCase):

    def setUp(self):
        self.model = WorkspaceNameModel()

    @mock.patch('models.WorkspaceModel.os.path')
    def test_setting_valid_filenames(self, mock_path):
        test_path = "@path"
        mock_path.isfile.return_value = True

        self.model.scattering_sample = ""
        mock_path.isfile.assert_not_called()

        mock_path.reset_mock()
        self.model.scattering_sample = test_path
        mock_path.isfile.assert_called_once_with(test_path)

        mock_path.reset_mock()
        self.model.scattering_empty_cell = test_path
        mock_path.isfile.assert_called_once_with(test_path)

        mock_path.reset_mock()
        self.model.transmission_empty_cell = test_path
        mock_path.isfile.assert_called_once_with(test_path)

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

    @mock.patch('models.WorkspaceModel.os.path')
    def test_valid_listener(self, mock_path):
        test_path = "@path"
        mock_path.isfile.return_value = True
        listener = mock.create_autospec(WorkspaceNameModel.IListener)

        self.model.add_listener(listener)
        self.model.scattering_sample = test_path
        self.model.scattering_empty_cell = test_path
        self.model.transmission_empty_cell = test_path

        self.model.remove_listener(listener)
        self.model.scattering_sample = ""
        self.model.scattering_empty_cell = ""
        self.model.transmission_empty_cell = ""

        listener.scattering_sample_changed.assert_called_once_with(self.model, test_path)
        listener.scattering_empty_cell_changed.assert_called_once_with(self.model, test_path)
        listener.transmission_empty_cell_changed.assert_called_once_with(self.model, test_path)

    @raises(ValueError)
    def test_invalid_listener(self):
        self.model.add_listener(None)
