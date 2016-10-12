from presenters.presenter import Presenter


class ReductionPresenter(Presenter):
    def __init__(self):
        super(ReductionPresenter, self).__init__()
        self.view = None

    def view(self):
        return self.view

    def view(self, val):
        #