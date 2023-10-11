import serial
import time
import sys
import math
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from FrmKruskal import *
from AlgoritmoDeKruskal import *
from FrmNodosyPesosCodigo import ventana_NodosyPesos
from FrmDatosRecibidosCodigo import ventana_Datos_Recibidos

class ventana_Kruskal(QDialog):
    def __init__(self, numerodeNodos,nodoGWAsig,listaNodosyPesos,listaAsignacion,conexion,listaDireccionesyPesos,listaSubida):
        super().__init__()
        self.ventanaKR = Ui_kru()
        self.ventanaKR.setupUi(self)
        self.show()
        #Variables
        self.numerodeNodos = numerodeNodos
        self.nodoGWAsig = nodoGWAsig
        self.listaNodosyPesos = listaNodosyPesos
        self.listaAsignacion = listaAsignacion
        self.conexion = conexion
        self.listaDireccionesyPesos = listaDireccionesyPesos
        self.listaSubida = listaSubida
        self.listaNuevasRutasKruscal=[]
        self.listaBajada = []
        #Eventos
        #self.ventanaKR.btnCargarDatos.clicked.connect(self.imprimir)
        # self.ventanaKR.btnCargarDatos.clicked.connect(c)
        #self.ventanaKR.pushButton_PPP.clicked.connect(self.limpiarListaVisualeInterna)
        self.ventanaKR.btnEnviarRutas.clicked.connect(self.enviarNuevasRutas)
        self.ventanaKR.btnVerNodosyPesos.clicked.connect(self.verNodosyPesos)
        self.ventanaKR.btnVerTodosDatosRecibidos.clicked.connect(self.verTodosDatosRecibidos)
        # Fuciones
        self.ejecutarAlgoritmoKruskal()
        self.reasignacionyVisualiacion()

    def ejecutarAlgoritmoKruskal(self):
        numeroNodos =self.numerodeNodos
        print(self.listaNodosyPesos)
        AlgKr = GraphK(numeroNodos)
        for dat in self.listaNodosyPesos:
            print(dat)
            AlgKr.add_edge(dat[0], dat[1], dat[2])
        AlgKr.kruskal()
        print('resultados')
        print(AlgKr.resultados)
        for res in AlgKr.resultados:
            self.listaNuevasRutasKruscal.append(res)
        print('nuevas rutas 1')
        print(self.listaNuevasRutasKruscal)
        ################################# Modificacion de rutas para evitar lazos ###############################################
        nodosDstNuev = []
        nodoGW = self.nodoGWAsig
        print('For 1 : ')
        for i, ruta in enumerate(self.listaNuevasRutasKruscal):
            # for i, obj in enumerate(g.resultados):
            if ruta[0] == nodoGW:
                self.listaNuevasRutasKruscal[i] = (ruta[1], ruta[0], ruta[2], 'm')  # se deberia modificar el peso
                print('mg')
                print(self.listaNuevasRutasKruscal)
                # nodosDstNuev.append(ruta[0])
        print(self.listaNuevasRutasKruscal)
        print(nodosDstNuev)
        print('For 2 : ')
        for i, ruta in enumerate(self.listaNuevasRutasKruscal):
            # for i, obj in enumerate(g.resultados):
            if ruta[1] == nodoGW:
                self.listaNuevasRutasKruscal[i] = (ruta[0], ruta[1], ruta[2], 'v')
                print(self.listaNuevasRutasKruscal[i])
                nodosDstNuev.append(ruta[0])
        print(self.listaNuevasRutasKruscal)
        print(nodosDstNuev)
        print('For 3 : ')
        condicion=True
        while condicion==True:
            for i, ruta in enumerate(self.listaNuevasRutasKruscal):
                # for i, obj in enumerate(g.resultados):
                if ruta[3] != 'v':
                    print(self.listaNuevasRutasKruscal[i])
                    for dst in nodosDstNuev:
                        if ruta[1] == dst:
                            self.listaNuevasRutasKruscal[i] = (ruta[0], ruta[1], ruta[2], 'v')
                            nodosDstNuev.append(ruta[0])

            print(self.listaNuevasRutasKruscal)
            print(nodosDstNuev)
            print('For 4 : ')
            for i, ruta in enumerate(self.listaNuevasRutasKruscal):
                # for i, obj in enumerate(g.resultados):
                if ruta[3] != 'v':
                    print(self.listaNuevasRutasKruscal[i])
                    for rtc in self.listaNuevasRutasKruscal:
                        if ruta[0] == rtc[0] and rtc[3] == 'v':
                            self.listaNuevasRutasKruscal[i] = (ruta[1], ruta[0], ruta[2], 'v')
                            nodosDstNuev.append(ruta[1])
            continuar=0
            for i,ruta in enumerate(self.listaNuevasRutasKruscal):
                if ruta[3] !='v':
                    continuar=1
            if  continuar==0:
                condicion=False

        print('Nueva Rutas Organizadas:')
        print(self.listaNuevasRutasKruscal)
        print(nodosDstNuev)
        #ventanaKruskal= ventana_Kruskal(self.nodoGWDir, self.listaNuevasRutasKruscal, self.listaAsiginacion, self.conexion)
        #ventanaKruskal.exec_()

    def reasignacionyVisualiacion(self):
        # Reasignar rutas a los datos obtenidos por el algoritmo de kruskal
        for i, ruta in enumerate(self.listaNuevasRutasKruscal):
            rd1 = '0'
            rd2 = '0'
            for reasignar in self.listaAsignacion:
                if ruta[0] == reasignar[1]:
                    rd1 = reasignar[0]
            for reasignar in self.listaAsignacion:
                if ruta[1] == reasignar[1]:
                    rd2 = reasignar[0]
            self.listaBajada.append((rd1, rd2, str(i + 1)))
        print('Todas las listas')
        print(self.listaAsignacion)
        print(self.listaNuevasRutasKruscal)
        print(self.listaBajada)
        # Mostrar datos en la interfaz
        fila = 0
        for registro in self.listaBajada:  # se agregan los nuevos elementos a la lsita visual
            columna = 0
            self.ventanaKR.tbl_tableWidgetTX.insertRow(fila)
            for elemento in registro:
                celda = QTableWidgetItem(elemento)
                celda.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ventanaKR.tbl_tableWidgetTX.setItem(fila, columna, celda)
                columna += 1
            fila += 1

    def enviarNuevasRutas(self):

        self.conexion.open()
        self.conexion.close()
        nMax = 100
        retardo = 0.1
        div = math.trunc(nMax / len(self.listaBajada))
        print(div)
        self.ventanaKR.pgbrPogressBar.setMaximum(nMax)
        k = 0
        for i in range(len(self.listaBajada)):
            if i < len(self.listaBajada) - 1:
                for j in range(div):
                    time.sleep(retardo)
                    self.ventanaKR.pgbrPogressBar.setValue(k + 1)
                    #print(k+1)
                    k = k + 1
                print('Nueva Ruta: ' + self.listaBajada[i][0][2:6] + self.listaBajada[i][1][2:6] + self.listaBajada[i][2])
                NuevaRuta = self.listaBajada[i][0][2:6] + self.listaBajada[i][1][2:6] +'0'+self.listaBajada[i][2]
                self.conexionSerial(NuevaRuta)

            if i == len(self.listaBajada) - 1:
                for m in range(100 - k):
                    time.sleep(retardo)
                    self.ventanaKR.pgbrPogressBar.setValue(k + 1)
                    #print(k+1)
                    k = k + 1
                print('Nueva Ruta: ' + self.listaBajada[i][0][2:6] + self.listaBajada[i][1][2:6] + self.listaBajada[i][2])
                NuevaRuta = self.listaBajada[i][0][2:6] + self.listaBajada[i][1][2:6] + '0' + self.listaBajada[i][2]
                self.conexionSerial(NuevaRuta)

    def conexionSerial(self, nuevaRuta):
        self.conexion.open()
        self.conexion.flush()
        datosIniciales = nuevaRuta
        tramaHexString = datosIniciales
        print(tramaHexString)
        codificado = bytes.fromhex(tramaHexString)
        byteParada = b'\r'
        print('seriak')
        self.conexion.write(codificado + byteParada)
        print('MSG enviado: ' + tramaHexString)
        print('MSG HEX enviado: ')
        print(codificado + byteParada)
        RET2 = self.conexion.read_until(b'\xFF')
        print('Confirmacion: ')
        print(RET2)
        self.conexion.close()

    def verNodosyPesos(self):
        ventanaDireccionesNodosyPesos=ventana_NodosyPesos(self.listaDireccionesyPesos)
        ventanaDireccionesNodosyPesos.exec_()

    def verTodosDatosRecibidos(self):
        ventanaDatosRecibidos = ventana_Datos_Recibidos(self.listaSubida)
        ventanaDatosRecibidos.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    noNo = 5
    noGW = 0
    listaDePrueba = [(0, 1, 8), (0, 2, 5), (1, 2, 9), (1, 3, 11), (2, 3, 15), (2, 4, 10), (3, 4, 7)]
    listaAsiginacion = []
    listaAsiginacion.append(('0x0006', 0))
    listaAsiginacion.append(('0x0005', 1))
    listaAsiginacion.append(('0x0004', 2))
    listaAsiginacion.append(('0x0003', 3))
    listaAsiginacion.append(('0x0002', 4))
    conex = serial.Serial('COM5', 9600, 8, 'N', stopbits=1, timeout=None)
    conex.close()
    conex.open()
    conex.close()
    listaDiryPes = []
    listaDiryPes.append(('0006','1','0005'))
    listaDiryPes.append(('0006', '1', '0005'))
    listaDiryPes.append(('0006', '1', '0005'))
    listaSub = []
    listaSub.append(('0x0006', '2.4','0xff', '0x0005'))
    listaSub.append(('0x0006', '2.4', '0xff', '0x0005'))
    listaSub.append(('0x0006', '2.4', '0xff', '0x0005'))
    ventana = ventana_Kruskal(noNo,noGW, listaDePrueba, listaAsiginacion, conex,listaDiryPes,listaSub)
    ventana.show()
    sys.exit(app.exec_())

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    noNo = 5
    noGW = 0
    listaDePrueba = [(0, 1, 8), (0, 2, 5), (1, 2, 9), (1, 3, 11), (2, 3, 15), (2, 4, 10), (3, 4, 7)]
    listaAsiginacion = []
    listaAsiginacion.append(('0006', 0))
    listaAsiginacion.append(('0005', 1))
    listaAsiginacion.append(('0004', 2))
    listaAsiginacion.append(('0003', 3))
    listaAsiginacion.append(('0002', 4))
    conex = serial.Serial()

    ventana = ventana_Kruskal(noNo,noGW, listaDePrueba, listaAsiginacion, conex)
    ventana.show()
    sys.exit(app.exec_())
'''

# for i in range(100):
# time.sleep(0.01)
# self.ventanaKR.pgbrPogressBar.setValue(i + 1)

'''
self.limpiarListaVisual()  # Hay que limpiar todos los datos de la lsita visual para que no se acumulen
fila = 0
for registro in self.listaSubida:  # se agregan los nuevos elementos a la lsita visual
    columna = 0
    self.primeraventana.tbl_tableWidgetRX.insertRow(fila)
    for elemento in registro:
        celda = QTableWidgetItem(elemento)
        celda.setTextAlignment(QtCore.Qt.AlignCenter)
        self.primeraventana.tbl_tableWidgetRX.setItem(fila, columna, celda)
        columna += 1
    fila += 1
self.primeraventana.btnProceso.setEnabled(True)
'''