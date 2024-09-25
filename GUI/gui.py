from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QTabWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
import sys
from os.path import exists

from GUI.customDialogs import DenoiseDialog, StaticArrayDialog
from customLayout import DoubleSelector, FileExplorerLayout

from juliacall import Main as jl

jl.seval("using SeaGap")

def is_path_list_valid(path_list):
    for path in path_list :
        if not exists(path):
            return False
    return True


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.maintab = QTabWidget()

    ### FILE TAB ###

        self.file_tab = QWidget()
        self.file_tab_layout = QVBoxLayout()

        self.ANT_file_explorer = FileExplorerLayout("ANT")
        self.file_tab_layout.addLayout(self.ANT_file_explorer)

        self.PXP_file_explorer = FileExplorerLayout("PXP")
        self.file_tab_layout.addLayout(self.PXP_file_explorer)

        self.SSP_file_explorer = FileExplorerLayout("SSP")
        self.file_tab_layout.addLayout(self.SSP_file_explorer)

        self.OBS_file_explorer = FileExplorerLayout("OBS")
        self.file_tab_layout.addLayout(self.OBS_file_explorer)



        self.file_tab.setLayout(self.file_tab_layout)

    ### PREPROC TAB ###

        self.preproc_tab = QWidget()
        self.preproc_tab_layout = QVBoxLayout()

        self.denoise_Button = QPushButton("Denoise")
        self.denoise_Button.clicked.connect(self.run_denoise_dlg)
        self.preproc_tab_layout.addWidget(self.denoise_Button)

        self.preproc_tab.setLayout(self.preproc_tab_layout)

    ### CALC TAB ###

        self.calc_tab = QWidget()
        self.calc_tab_layout = QVBoxLayout()

        self.static_array_Button = QPushButton("Static array")
        self.static_array_Button.clicked.connect(self.run_static_array_dlg)
        self.calc_tab_layout.addWidget(self.static_array_Button)

        self.calc_tab.setLayout(self.calc_tab_layout)

    ### PLOTTING TAB ###

        self.plotting_tab = QWidget()
        self.plotting_tab_layout = QVBoxLayout()


        self.plotting_tab.setLayout(self.plotting_tab_layout)

    ### ASSIGNING TABS

        self.maintab.addTab(self.file_tab, "Files")
        self.maintab.addTab(self.preproc_tab, "Pre-processing")
        self.maintab.addTab(self.calc_tab, "Calculs")
        self.maintab.addTab(self.plotting_tab, "Plotting")

    ### FINAL DETAILS ###

        # Définition du titre de la fenêtre
        self.setWindowTitle("SeaGap - GUI")

        my_icon = QIcon("./img/logo.png")

        self.setWindowIcon(my_icon)

        # self.ANT_file_explorer.button.clicked.connect(self.get_path_list)
        # self.PXP_file_explorer.button.clicked.connect(self.get_path_list)
        # self.SSP_file_explorer.button.clicked.connect(self.get_path_list)
        # self.OBS_file_explorer.button.clicked.connect(self.get_path_list)

        self.setCentralWidget(self.maintab)

    def get_path_list(self):
        return [self.ANT_file_explorer.line_edit.text(), self.PXP_file_explorer.line_edit.text(), self.SSP_file_explorer.line_edit.text(), self.OBS_file_explorer.line_edit.text()]



    def run_denoise_dlg(self):

        l_path = self.get_path_list()
        if not is_path_list_valid(l_path):
            print("Paths not valid")
            return
        denoise_dlg = DenoiseDialog(l_path, jl)
        denoise_dlg.exec()
        print("END END END")


    def run_static_array_dlg(self):

        l_path = self.get_path_list()
        if not is_path_list_valid(l_path):
            print("Paths not valid")
            return
        static_array_dlg = StaticArrayDialog(l_path, jl)
        static_array_dlg.exec()
        print("END END END")



if __name__ == '__main__':
    # jl.println("Hello from Julia!")

    # z, v, nz_st, numz = jl.SeaGap.read_prof("../example_hugo/ss_prof.inp",3.0)
    # print(z)
    # Create the Qt Application
    app = QApplication()

    # Create and show the form
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec())