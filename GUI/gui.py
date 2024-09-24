from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog
from PySide6.QtGui import QIcon, QDoubleValidator
import sys
from PySide6.QtCore import QLocale
from os.path import exists

from juliacall import Main as jl

jl.seval("using SeaGap")

def is_path_list_valid(path_list):
    for path in path_list :
        if not exists(path):
            return False
    return True

class DoubleSelector(QVBoxLayout):
    def __init__(self, min, max, label, dec=16, *args, **kwargs):
        super(DoubleSelector, self).__init__(*args, **kwargs)

        self.min = min
        self.max = max

        self.line_edit = QLineEdit("")
        self.line_edit.setPlaceholderText("*required")
        validator = QDoubleValidator(self.min, self.max, dec)
        locale = QLocale(QLocale.English, QLocale.UnitedStates)
        validator.setLocale(locale)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.line_edit.setValidator(validator)

        self.line_edit.textChanged.connect(self.check_lat)

        self.addWidget(QLabel(label + " :"))
        self.addWidget(self.line_edit)

    def check_lat(self):
        try :
            if float(self.line_edit.text()) > self.max :
                self.line_edit.setText(str(self.max))
            elif float(self.line_edit.text()) < self.min :
                self.line_edit.setText(str(self.min))
        except :
            return

class FileExplorerLayout(QVBoxLayout):
    def __init__(self, label, *args, **kwargs):
        super(FileExplorerLayout, self).__init__(*args, **kwargs)
        self.label = label

        self.file_path = ""

        self.addWidget(QLabel(self.label+" :"))

        selector = QHBoxLayout()
        self.button = QPushButton("Select file")
        self.button.clicked.connect(self.open_file_dialog)
        selector.addWidget(self.button)

        self.line_edit = QLineEdit(self.file_path)
        self.line_edit.setDisabled(True)
        self.line_edit.setPlaceholderText("*required")
        selector.addWidget(self.line_edit)

        self.addLayout(selector)

    def open_file_dialog(self):
        dlg = QFileDialog()
        dlg.setWindowTitle("Select " + self.label + " File")
        self.line_edit.setText(dlg.getOpenFileName()[0])

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

        self.preproc_maintab = QTabWidget()


        # DENOISE
        self.denoise_tab = QWidget()
        self.denoise_tab_layout = QVBoxLayout()

        self.denoise_lat_selector = DoubleSelector(-89.99, 89.99, "Latitude")
        self.denoise_tab_layout.addLayout(self.denoise_lat_selector)
        self.denoise_TR_DEPTH_selector = DoubleSelector(0, 99999.0, "Surface transducer depth")
        self.denoise_tab_layout.addLayout(self.denoise_TR_DEPTH_selector)
        self.run_denoise_button = QPushButton("Run denoise")
        self.run_denoise_button.clicked.connect(self.run_denoise)
        self.denoise_tab_layout.addWidget(self.run_denoise_button)


        self.denoise_tab.setLayout(self.denoise_tab_layout)

        # Aplying tabs
        self.preproc_maintab.addTab(self.denoise_tab, "Denoise")


        self.preproc_tab_layout.addWidget(self.preproc_maintab)
        self.preproc_tab.setLayout(self.preproc_tab_layout)

    ### CALC TAB ###

        self.calc_tab = QWidget()
        self.calc_tab_layout = QVBoxLayout()

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



    def run_denoise(self):

        l_path = self.get_path_list()
        if not is_path_list_valid(l_path):
            print("Paths not valid")
            return
        if self.denoise_lat_selector.line_edit.text() == "" or self.denoise_TR_DEPTH_selector.line_edit.text() == "" :
            print("lacking denoise parameters")
            return
        path_ANT, path_PXP, path_SSP, path_OBS = l_path
        lat = float(self.denoise_lat_selector.line_edit.text())
        TR_DEPTH = float(self.denoise_TR_DEPTH_selector.line_edit.text())
        print(path_ANT)
        print(path_PXP)
        print(path_SSP)
        print(path_OBS)
        print(lat)
        print(TR_DEPTH)
        jl.SeaGap.denoise(lat,TR_DEPTH, fn1=path_ANT , fn2=path_PXP , fn3=path_SSP , fn4=path_OBS)
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