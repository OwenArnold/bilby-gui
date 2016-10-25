import unittest
import mock

from nose.tools import raises
from models.SaveModel import SaveModel


class TestSaveModel(unittest.TestCase):
    def setUp(self):
        self.model = SaveModel()

    def test_setting_valid_file_name_and_workpace_names(self):
        try:
            self.model.file_name = "C:/path1/path2/test.nxs"
            self.model.workspace_name = "my_workspace"
            has_raised = False
        except ValueError:
            has_raised = True
        self.assertFalse(has_raised)

    @raises(ValueError)
    def test_setting_invalid_workspace_name(self):
        self.model.workspace_name = ["test"]

    @raises(ValueError)
    def test_setting_invalid_file_name(self):
        self.model.file_name = ["test"]

    def test_valid_listener(self):
        test_path = "C:/path1/test.nxs"
        test_name = "name"
        listener = mock.create_autospec(SaveModel.IListener)

        # test add_listener
        self.model.add_listener(listener)
        # first pass
        self.model.file_name = test_path
        self.model.workspace_name = test_name
        # second pass
        self.model.file_name = test_path
        self.model.workspace_name = test_name

        listener.on_file_name_changed.assert_called_once_with(self.model, test_path)
        listener.on_workspace_name_changed.assert_called_once_with(self.model, test_name)

        # test remove_listener
        listener.reset_mock()
        self.model.remove_listener(listener)
        self.model.file_name = ""
        self.model.workspace_name = ""

        listener.on_file_name_changed.assert_not_called()
        listener.on_workspace_name_changed.assert_not_called()

    @raises(ValueError)
    def test_invalid_listener(self):
        self.model.add_listener(None)