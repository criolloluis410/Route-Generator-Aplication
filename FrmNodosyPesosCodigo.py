import sys
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from FrmNodosyPesos import *

class ventana_NodosyPesos(QDialog):
    def __init__(self,listaDireccionesyPesos):
        super().__init__()
        self.ventanaNodoyPesos = Ui_FrmNodosyPesos()
        self.ventanaNodoyPesos.setupUi(self)
        self.show()
        #Atributos
        self.listaDireccionesyPesos=listaDireccionesyPesos
        #Eventos
        self.ventanaNodoyPesos.btnCerrar.clicked.connect(self.cerrarVentana)
        #Funciones Iniciales
        self.mostrarLista()

    def mostrarLista(self):
        print(self.listaDireccionesyPesos)
        #self.limpiarListaVisual() # Hay que limpiar todos los datos de la lsita visual para que no se acumulen
        fila=0
        for registro in self.listaDireccionesyPesos:# se agregan los nuevos elementos a la lsita visual
            columna=0
            self.ventanaNodoyPesos.tbl_tableWidgetNodosyPesos.insertRow(fila)
            for elemento in registro:
                celda=QTableWidgetItem(elemento)
                celda.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ventanaNodoyPesos.tbl_tableWidgetNodosyPesos.setItem(fila,columna,celda)
                columna+=1
            fila+=1

    def cerrarVentana(self):
        self.close()

if __name__ == '__main__':
    app =QApplication(sys.argv)
    dtAd='lista'
    print('main')
    ventana = ventana_NodosyPesos(dtAd)
    ventana.show()
    print('main')
    sys.exit(app.exec_())