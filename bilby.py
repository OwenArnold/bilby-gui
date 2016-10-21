
from build_all_ui_files import build_all_ui_files, script_folder

try:
    build_all_ui_files(script_folder, verbose=False)
except:
    print ('ui files not built')

from views.MainView import MainView

main_view = MainView()
main_view.show()
