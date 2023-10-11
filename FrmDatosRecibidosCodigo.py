import sys
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from FrmDatosRecibidos import *

class ventana_Datos_Recibidos (QDialog):
    def __init__(self,listaSubida):
        super().__init__()
        self.ventanaDatosRecibidos = Ui_FrmDatosRecibidos()
        self.ventanaDatosRecibidos.setupUi(self)
        self.show()
        #Atributos
        self.listaSubida=listaSubida
        #Eventos
        self.ventanaDatosRecibidos.btnCerrar.clicked.connect(self.cerrarVentana)
        #Funciones Iniciales
        self.mostrarLista()

    def mostrarLista(self):
        #self.limpiarListaVisual() # Hay que limpiar todos los datos de la lsita visual para que no se acumulen
        fila=0
        for registro in self.listaSubida:# se agregan los nuevos elementos a la lsita visual
            columna=0
            self.ventanaDatosRecibidos.tbl_tableWidget_DatosRecibidos.insertRow(fila)
            for elemento in registro:
                celda=QTableWidgetItem(elemento)
                celda.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ventanaDatosRecibidos.tbl_tableWidget_DatosRecibidos.setItem(fila,columna,celda)
                columna+=1
            fila+=1

    def cerrarVentana(self):
        self.close()

if __name__ == '__main__':
    app =QApplication(sys.argv)
    dtAd='lista'
    ventana = ventana_Datos_Recibidos(dtAd)
    ventana.show()
    sys.exit(app.exec_())