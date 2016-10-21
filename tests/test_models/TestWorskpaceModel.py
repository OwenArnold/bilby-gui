from nose.tools import *
from models.WorkspaceModel import WorkspaceModel


def test_setting_valid_filenames():
    try:
        model = WorkspaceModel()
        model.scattering_sample = ""
        model.scattering_sample = __file__
        model.scattering_empty_cell = __file__
        model.transmission_empty_cell = __file__

        assert model.scattering_sample == __file__
        assert model.scattering_empty_cell == __file__
        assert model.transmission_empty_cell == __file__

    except ValueError:
        assert False


@raises(ValueError)
def test_setting_invalid_scattering_sample():
    model = WorkspaceModel()
    model.scattering_sample = None


@raises(ValueError)
def test_setting_invalid_scattering_empty_cell():
    model = WorkspaceModel()
    model.scattering_empty_cell = None


@raises(ValueError)
def test_setting_invalid_transmission_empty_cell():
    model = WorkspaceModel()
    model.transmission_empty_cell = None
