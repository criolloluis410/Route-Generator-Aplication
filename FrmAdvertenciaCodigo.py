import sys
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from FrmAdvertencia import *

class ventana_Advertencia(QDialog):
    def __init__(self,msgAdv):
        super().__init__()
        self.ventanaAdv = Ui_FrmAdvertencia()
        self.ventanaAdv.setupUi(self)
        self.mensajeAdvertencia=msgAdv
        self.ventanaAdv.btnAceptar.clicked.connect(self.cerrarAdvertencia)
        self.mostrarAdvertencia()

    def mostrarAdvertencia(self):
        self.ventanaAdv.lblAdvertencia.setText(self.mensajeAdvertencia)

    def cerrarAdvertencia(self):
        self.close()

if __name__ == '__main__':
    app =QApplication(sys.argv)
    dtAd='DATO'
    ventana = ventana_Advertencia(dtAd)
    ventana.show()
    sys.exit(app.exec_())