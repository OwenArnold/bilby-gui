from presenters.presenter import Presenter


class ReductionPresenter(Presenter):
    def __init__(self):
        super(ReductionPresenter, self).__init__()
        self._view = None

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, val):
        pass
