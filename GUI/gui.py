from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QTabWidget, QVBoxLayout, QPushButton, QToolBar, QStatusBar, QFileDialog
from PySide6.QtGui import QIcon, QAction
import sys
from os.path import exists, join

from GUI.customDialogs import DenoiseDialog, StaticArrayDialog,StaticArrayGradDialog, StaticArrayMCMCGradVDialog, StaticIndividualDialog, NewProjectDialog
from customLayout import FileExplorerLayout

import yaml, os

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
    ### ATTRIBUTES ###

        self.base_path = ""
        self.ANT_path = ""
        self.PXP_path = ""
        self.SSP_path = ""
        self.OBS_path = ""
        self.prj_path = ""

    ### TOOLBAR ###

        toolbar = QToolBar("My main toolbar")

        self.new_project_action = QAction("New")
        self.new_project_action.setStatusTip("Create a new project file")
        self.new_project_action.triggered.connect(self.create_new_project)

        self.load_proj_action = QAction("Load")
        self.load_proj_action.setStatusTip("Load existing folder")
        self.load_proj_action.triggered.connect(self.load_proj)

        self.save_project_action = QAction("Save")
        self.save_project_action.setStatusTip("Save current project")
        self.save_project_action.triggered.connect(self.save_project)

        toolbar.addAction(self.new_project_action)
        toolbar.addAction(self.load_proj_action)
        toolbar.addAction(self.save_project_action)

        self.addToolBar(toolbar)
        self.setStatusBar(QStatusBar(self))

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

        self.static_array_grad_Button = QPushButton("Static array grad")
        self.static_array_grad_Button.clicked.connect(self.run_static_array_grad_dlg)
        self.calc_tab_layout.addWidget(self.static_array_grad_Button)

        self.static_array_mcmcgradv_Button = QPushButton("Static array mcmcgradv")
        self.static_array_mcmcgradv_Button.clicked.connect(self.run_static_array_mcmcgradv_dlg)
        self.calc_tab_layout.addWidget(self.static_array_mcmcgradv_Button)

        self.static_individual_Button = QPushButton("Static individual")
        self.static_individual_Button.clicked.connect(self.run_static_individual_dlg)
        self.calc_tab_layout.addWidget(self.static_individual_Button)

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

    def create_new_project(self):
        dlg = NewProjectDialog()
        dlg.setWindowTitle("Select new project folder")
        dlg.exec()
        if dlg.proj_file_path != "" :
            self.load_proj(None, proj_file_path=dlg.proj_file_path)
        print("NEW")

    def load_proj(self, _, proj_file_path=""):
        if proj_file_path == "" :
            dlg = QFileDialog()
            dlg.setWindowTitle("Select project file")
            proj_file_path = dlg.getOpenFileName(filter="project(*.prj)")[0]
        
        if not exists(proj_file_path) :
            print("wrong project file")
            return
        with open(proj_file_path) as f:
            dict_prj = yaml.full_load(f)

            self.base_path = dict_prj["base_path"]
            if self.base_path != "" :
                os.chdir(self.base_path)
                self.ANT_file_explorer.default_path = self.base_path
                self.PXP_file_explorer.default_path = self.base_path
                self.SSP_file_explorer.default_path = self.base_path
                self.OBS_file_explorer.default_path = self.base_path

            self.ANT_path = dict_prj["ANT_path"]
            self.ANT_file_explorer.line_edit.setText(self.ANT_path)

            self.PXP_path = dict_prj["PXP_path"]
            self.PXP_file_explorer.line_edit.setText(self.PXP_path)

            self.SSP_path = dict_prj["SSP_path"]
            self.SSP_file_explorer.line_edit.setText(self.SSP_path)

            self.OBS_path = dict_prj["OBS_path"]
            self.OBS_file_explorer.line_edit.setText(self.OBS_path)


            self.proj_file_path = proj_file_path

        print("LOAD")

    def save_project(self):
        if self.proj_file_path == "" :
            print("warning : no project selected")
        with open(self.proj_file_path, "w") as proj_file_path :
            proj_file_path.write('---\n')
            proj_file_path.write('base_path : "'+os.path.dirname(self.proj_file_path)+'"\n')
            proj_file_path.write('proj_name : "'+os.path.splitext(os.path.basename(self.proj_file_path))[0]+'"\n')
            proj_file_path.write('ANT_path : "'+self.ANT_file_explorer.line_edit.text()+'"\n')
            proj_file_path.write('PXP_path : "'+self.PXP_file_explorer.line_edit.text()+'"\n')
            proj_file_path.write('SSP_path : "'+self.SSP_file_explorer.line_edit.text()+'"\n')
            proj_file_path.write('OBS_path : "'+self.OBS_file_explorer.line_edit.text()+'"\n')
        print("SAVE")

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


    def run_static_array_grad_dlg(self):

        l_path = self.get_path_list()
        if not is_path_list_valid(l_path):
            print("Paths not valid")
            return
        static_array_grad_dlg = StaticArrayGradDialog(l_path, jl)
        static_array_grad_dlg.exec()
        print("END END END")


    def run_static_array_mcmcgradv_dlg(self):

        l_path = self.get_path_list()
        if not is_path_list_valid(l_path):
            print("Paths not valid")
            return
        static_array_mcmcgradv_dlg = StaticArrayMCMCGradVDialog(l_path, jl)
        static_array_mcmcgradv_dlg.exec()
        print("END END END")


    def run_static_individual_dlg(self):

        l_path = self.get_path_list()
        if not is_path_list_valid(l_path):
            print("Paths not valid")
            return
        static_array_individual_dlg = StaticIndividualDialog(l_path, jl)
        static_array_individual_dlg.exec()
        print("END END END")



if __name__ == '__main__':
    # jl.println("Hello from Julia!")

    # z, v, nz_st, numz = jl.SeaGap.read_prof("../data/ss_prof.inp",3.0)
    # print(z)
    # Create the Qt Application
    app = QApplication()

    # Create and show the form
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec())