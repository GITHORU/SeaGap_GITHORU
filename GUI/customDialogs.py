from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialogButtonBox
from customLayout import DoubleSelector, IntSelector, FolderExplorerLayout
from PySide6.QtGui import QIcon, QPixmap
import shutil, os
from PySide6.QtCore import Qt
import juliacall

from os.path import exists

class DenoiseDialog(QDialog):
    
    def __init__(self, l_path, jl):
        super().__init__()

        self.setWindowTitle("Denoise")
        my_icon = QIcon("./img/logo.png")
        self.setWindowIcon(my_icon)

        self.first_denoise = True

        self.l_path = l_path
        self.jl = jl

        self.layout = QHBoxLayout()

        self.input_layout = QVBoxLayout()

        self.lat_selector = DoubleSelector(-89.99, 89.99, "Latitude", True)
        self.input_layout.addLayout(self.lat_selector)

        self.TR_DEPTH_selector = DoubleSelector(0, 99999.0, "Surface transducer depth", True)
        self.input_layout.addLayout(self.TR_DEPTH_selector)

        self.n_selector = IntSelector(3, 99999, "Window size for the running filter", False, backText="Must be odd (def : 15)")
        self.input_layout.addLayout(self.n_selector)

        self.k_selector = IntSelector(0, 99999, "Which Transpounder", False, backText="(def : 0 = all)")
        self.input_layout.addLayout(self.k_selector)

        self.sigma_selector = DoubleSelector(0.1, 99999.0, "Number of Sigmas", False, backText="(def : 4.0)")
        self.input_layout.addLayout(self.sigma_selector)

        self.run_denoise_button = QPushButton("Run denoise")
        self.run_denoise_button.clicked.connect(self.run_denoise)
        self.input_layout.addWidget(self.run_denoise_button)

        self.graph_img = QLabel()
        self.layout.addLayout(self.input_layout)
        self.layout.addWidget(self.graph_img)

        QBtn = (
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setDisabled(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.input_layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def run_denoise(self):
        self.graph_img.clear()
        self.graph_img.repaint()
        if self.lat_selector.line_edit.text() == "" or self.TR_DEPTH_selector.line_edit.text() == "" :
            print("lacking denoise parameters")
            return

        path_ANT, path_PXP, path_SSP, self.path_OBS_ori = self.l_path
        if self.first_denoise :
            shutil.copyfile(self.path_OBS_ori, "gui_tmp/tmp_denoise_obs.inp")
            self.first_denoise = False

        path_OBS = "gui_tmp/tmp_denoise_obs.inp"
        lat = float(self.lat_selector.line_edit.text())
        TR_DEPTH = float(self.TR_DEPTH_selector.line_edit.text())
        if self.n_selector.line_edit.text() != "":
            n = int(self.n_selector.line_edit.text())
        else :
            n = 15
        if self.k_selector.line_edit.text() != "":
            k = int(self.k_selector.line_edit.text())
        else :
            k = 0
        if self.sigma_selector.line_edit.text() != "":
            sigma = float(self.sigma_selector.line_edit.text())
        else :
            sigma = 4.0
        self.jl.SeaGap.denoise(lat,TR_DEPTH, fn1=path_ANT , fn2=path_PXP , fn3=path_SSP , fn4=path_OBS, fno1="gui_tmp/tmp_denoise.out", fno2="gui_tmp/tmp_denoise.png", save=False, show=False, prompt=False, n=n, sigma=sigma, k=k)
        pixmap = QPixmap('gui_tmp/tmp_denoise.png')
        self.graph_img.setPixmap(pixmap.scaled(pixmap.width()//2, pixmap.height()//2, Qt.AspectRatioMode.KeepAspectRatio ))
        self.graph_img.repaint()

        self.buttonBox.setDisabled(False)

    def accept(self):
        print("ACCEPTED !")
        try :
            shutil.copyfile("gui_tmp/tmp_denoise_obs.inp", self.path_OBS_ori)
            os.remove("gui_tmp/tmp_denoise_obs.inp")
            os.remove("gui_tmp/tmp_denoise.out")
            os.remove("gui_tmp/tmp_denoise.png")
        except :
            pass
        super().accept()

    def reject(self):
        print("REJECTED !")
        try :
            os.remove("gui_tmp/tmp_denoise_obs.inp")
            os.remove("gui_tmp/tmp_denoise.out")
            os.remove("gui_tmp/tmp_denoise.png")
        except :
            pass
        super().reject()


class StaticArrayDialog(QDialog):

    def __init__(self, l_path, jl):
        super().__init__()

        self.setWindowTitle("Static array")
        my_icon = QIcon("./img/logo.png")
        self.setWindowIcon(my_icon)

        self.l_path = l_path
        self.jl = jl

        self.layout = QHBoxLayout()

        self.input_layout = QVBoxLayout()

        self.lat_selector = DoubleSelector(-89.99, 89.99, "Latitude", True)
        self.input_layout.addLayout(self.lat_selector)

        self.TR_DEPTH_selector = DoubleSelector(0.0, 99999.0, "Surface transducer depth", True)
        self.input_layout.addLayout(self.TR_DEPTH_selector)

        self.NPB_selector = IntSelector(3, 99999, "Number of temporal B-spline bases", False, backText="(def : 100)")
        self.input_layout.addLayout(self.NPB_selector)

        self.eps_selector = DoubleSelector(0.0, 99999.0, "Convergence threshold", False, backText="(def : 1.e-4)")
        self.input_layout.addLayout(self.eps_selector)

        self.ITMAX_selector = IntSelector(1, 99999, "Max. number of iterations", False, backText="(def : 50)")
        self.input_layout.addLayout(self.ITMAX_selector)

        self.delta_pos_selector = DoubleSelector(0, 99999.0, "Infinitesimal distance value for Jacobian matrix", False, backText="(def : 1.e-4)")
        self.input_layout.addLayout(self.delta_pos_selector)

        self.folder_selector = FolderExplorerLayout("Static array folder")
        self.input_layout.addLayout(self.folder_selector)

        self.run_static_array_button = QPushButton("Run static array")
        self.run_static_array_button.clicked.connect(self.run_static_array)
        self.input_layout.addWidget(self.run_static_array_button)

        self.graph_img = QLabel()
        self.layout.addLayout(self.input_layout)
        self.layout.addWidget(self.graph_img)

        QBtn = (
                QDialogButtonBox.Ok
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setDisabled(True)
        self.buttonBox.accepted.connect(self.accept)

        self.input_layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def run_static_array(self):
        if self.lat_selector.line_edit.text() == "" or self.TR_DEPTH_selector.line_edit.text() == "" or self.folder_selector.line_edit.text() == "":
            print("lacking static array parameters")
            return

        if not exists(self.folder_selector.line_edit.text()):
            print("wrong path entered")
            return

        path_ANT, path_PXP, path_SSP, path_OBS = self.l_path
        lat = float(self.lat_selector.line_edit.text())
        folder_path = self.folder_selector.line_edit.text()
        TR_DEPTH = float(self.TR_DEPTH_selector.line_edit.text())
        if self.NPB_selector.line_edit.text() != "":
            NPB = int(self.NPB_selector.line_edit.text())
        else:
            NPB = 100
        if self.eps_selector.line_edit.text() != "":
            eps = float(self.eps_selector.line_edit.text())
        else:
            eps = 0.0001
        if self.ITMAX_selector.line_edit.text() != "":
            ITMAX = int(self.ITMAX_selector.line_edit.text())
        else:
            ITMAX = 50
        if self.delta_pos_selector.line_edit.text() != "":
            delta_pos = float(self.delta_pos_selector.line_edit.text())
        else:
            delta_pos = 0.0001
        log_path = os.path.join(folder_path, "static_array_log.out")
        solve_path = os.path.join(folder_path, "static_array_solve.out")
        position_path = os.path.join(folder_path, "static_array_position.out")
        residual_path = os.path.join(folder_path, "static_array_residual.out")
        bspline_path = os.path.join(folder_path, "static_array_bspline.out")
        AICBIC_path = os.path.join(folder_path, "static_array_AICBIC.out")
        self.jl.SeaGap.static_array(lat, juliacall.convert(self.jl.Vector[self.jl.Float64], [TR_DEPTH]), NPB, fn1=path_ANT, fn2=path_PXP, fn3=path_SSP, fn4=path_OBS, eps=eps, ITMAX=ITMAX, delta_pos=delta_pos, fno0=log_path, fno1=solve_path, fno2=position_path, fno3=residual_path, fno4=bspline_path, fno5=AICBIC_path)

        self.buttonBox.setDisabled(False)
        
        
class StaticArrayGradDialog(QDialog):

    def __init__(self, l_path, jl):
        super().__init__()

        self.setWindowTitle("Static array grad")
        my_icon = QIcon("./img/logo.png")
        self.setWindowIcon(my_icon)

        self.l_path = l_path
        self.jl = jl

        self.layout = QHBoxLayout()

        self.input_layout = QVBoxLayout()

        self.lat_selector = DoubleSelector(-89.99, 89.99, "Latitude", True)
        self.input_layout.addLayout(self.lat_selector)

        self.TR_DEPTH_selector = DoubleSelector(0.0, 99999.0, "Surface transducer depth", True)
        self.input_layout.addLayout(self.TR_DEPTH_selector)

        self.NPB_selector = IntSelector(3, 99999, "Number of temporal B-spline bases", False, backText="(def : 100)")
        self.input_layout.addLayout(self.NPB_selector)

        self.ITMAX_selector = IntSelector(1, 99999, "Max. number of iterations", False, backText="(def : 50)")
        self.input_layout.addLayout(self.ITMAX_selector)

        self.delta_pos_selector = DoubleSelector(0, 99999.0, "Infinitesimal distance value for Jacobian matrix", False, backText="(def : 1.e-4)")
        self.input_layout.addLayout(self.delta_pos_selector)

        self.folder_selector = FolderExplorerLayout("Static array grad folder")
        self.input_layout.addLayout(self.folder_selector)

        self.run_static_array_grad_button = QPushButton("Run static array grad")
        self.run_static_array_grad_button.clicked.connect(self.run_static_array_grad)
        self.input_layout.addWidget(self.run_static_array_grad_button)

        self.graph_img = QLabel()
        self.layout.addLayout(self.input_layout)
        self.layout.addWidget(self.graph_img)

        QBtn = (
                QDialogButtonBox.Ok
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setDisabled(True)
        self.buttonBox.accepted.connect(self.accept)

        self.input_layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def run_static_array_grad(self):
        if self.lat_selector.line_edit.text() == "" or self.TR_DEPTH_selector.line_edit.text() == "" or self.folder_selector.line_edit.text() == "":
            print("lacking static array parameters")
            return

        if not exists(self.folder_selector.line_edit.text()):
            print("wrong path entered")
            return

        path_ANT, path_PXP, path_SSP, path_OBS = self.l_path
        lat = float(self.lat_selector.line_edit.text())
        folder_path = self.folder_selector.line_edit.text()
        TR_DEPTH = float(self.TR_DEPTH_selector.line_edit.text())
        if self.NPB_selector.line_edit.text() != "":
            NPB = int(self.NPB_selector.line_edit.text())
        else:
            NPB = 100
        if self.ITMAX_selector.line_edit.text() != "":
            ITMAX = int(self.ITMAX_selector.line_edit.text())
        else:
            ITMAX = 50
        if self.delta_pos_selector.line_edit.text() != "":
            delta_pos = float(self.delta_pos_selector.line_edit.text())
        else:
            delta_pos = 0.0001
        log_path = os.path.join(folder_path, "static_array_grad_log.out")
        solve_path = os.path.join(folder_path, "static_array_grad_solve.out")
        position_path = os.path.join(folder_path, "static_array_grad_position.out")
        residual_path = os.path.join(folder_path, "static_array_grad_residual.out")
        bspline_path = os.path.join(folder_path, "static_array_grad_bspline.out")
        self.jl.SeaGap.static_array_grad(lat, juliacall.convert(self.jl.Vector[self.jl.Float64], [TR_DEPTH]), NPB, fn1=path_ANT, fn2=path_PXP, fn3=path_SSP, fn4=path_OBS, ITMAX=ITMAX, delta_pos=delta_pos, fno0=log_path, fno1=solve_path, fno2=position_path, fno3=residual_path, fno4=bspline_path)

        self.buttonBox.setDisabled(False)
        

class StaticIndividualDialog(QDialog):

    def __init__(self, l_path, jl):
        super().__init__()

        self.setWindowTitle("Static array individual")
        my_icon = QIcon("./img/logo.png")
        self.setWindowIcon(my_icon)

        self.l_path = l_path
        self.jl = jl

        self.layout = QHBoxLayout()

        self.input_layout = QVBoxLayout()

        self.lat_selector = DoubleSelector(-89.99, 89.99, "Latitude", True)
        self.input_layout.addLayout(self.lat_selector)

        self.TR_DEPTH_selector = DoubleSelector(0.0, 99999.0, "Surface transducer depth", True)
        self.input_layout.addLayout(self.TR_DEPTH_selector)

        self.NPB_selector = IntSelector(3, 99999, "Number of temporal B-spline bases", False, backText="(def : 100)")
        self.input_layout.addLayout(self.NPB_selector)

        self.eps_selector = DoubleSelector(0.0, 99999.0, "Convergence threshold", False, backText="(def : 1.e-4)")
        self.input_layout.addLayout(self.eps_selector)

        self.ITMAX_selector = IntSelector(1, 99999, "Max. number of iterations", False, backText="(def : 50)")
        self.input_layout.addLayout(self.ITMAX_selector)

        self.delta_pos_selector = DoubleSelector(0, 99999.0, "Infinitesimal distance value for Jacobian matrix", False, backText="(def : 1.e-4)")
        self.input_layout.addLayout(self.delta_pos_selector)

        self.folder_selector = FolderExplorerLayout("Static array individual folder")
        self.input_layout.addLayout(self.folder_selector)

        self.run_static_array_button = QPushButton("Run static array individual")
        self.run_static_array_button.clicked.connect(self.run_static_individual)
        self.input_layout.addWidget(self.run_static_array_button)

        self.graph_img = QLabel()
        self.layout.addLayout(self.input_layout)
        self.layout.addWidget(self.graph_img)

        QBtn = (
                QDialogButtonBox.Ok
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setDisabled(True)
        self.buttonBox.accepted.connect(self.accept)

        self.input_layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def run_static_individual(self):
        if self.lat_selector.line_edit.text() == "" or self.TR_DEPTH_selector.line_edit.text() == "" or self.folder_selector.line_edit.text() == "":
            print("lacking static array individual parameters")
            return

        if not exists(self.folder_selector.line_edit.text()):
            print("wrong path entered")
            return

        path_ANT, path_PXP, path_SSP, path_OBS = self.l_path
        lat = float(self.lat_selector.line_edit.text())
        folder_path = self.folder_selector.line_edit.text()
        TR_DEPTH = float(self.TR_DEPTH_selector.line_edit.text())
        if self.NPB_selector.line_edit.text() != "":
            NPB = int(self.NPB_selector.line_edit.text())
        else:
            NPB = 100
        if self.eps_selector.line_edit.text() != "":
            eps = float(self.eps_selector.line_edit.text())
        else:
            eps = 0.0001
        if self.ITMAX_selector.line_edit.text() != "":
            ITMAX = int(self.ITMAX_selector.line_edit.text())
        else:
            ITMAX = 50
        if self.delta_pos_selector.line_edit.text() != "":
            delta_pos = float(self.delta_pos_selector.line_edit.text())
        else:
            delta_pos = 0.0001
        log_path = os.path.join(folder_path, "static_array_individual_log.out")
        solve_path = os.path.join(folder_path, "static_array_individual_solve.out")
        position_path = os.path.join(folder_path, "static_array_individual_position.out")
        residual_path = os.path.join(folder_path, "static_array_individual_residual.out")
        bspline_path = os.path.join(folder_path, "static_array_individual_bspline.out")
        self.jl.SeaGap.static_individual(lat, juliacall.convert(self.jl.Vector[self.jl.Float64], [TR_DEPTH]), NPB, fn1=path_ANT, fn2=path_PXP, fn3=path_SSP, fn4=path_OBS, eps=eps, ITMAX=ITMAX, delta_pos=delta_pos, fno0=log_path, fno1=solve_path, fno2=position_path, fno3=residual_path, fno4=bspline_path)

        self.buttonBox.setDisabled(False)