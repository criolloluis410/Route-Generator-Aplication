import serial
import time
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from FrmAplicacion import *
#from AlgoritmoDeKruskal import *
#from AlgoritmoDeDijkstra import *
from FrmKruskalCodigo import ventana_Kruskal
from FrmDijkstraCodigo import ventana_Dijkstra
from FrmAdvertenciaCodigo import ventana_Advertencia

class mostrar(QDialog):
    def __init__(self):
        super().__init__()
        self.primeraventana = Ui_FrmAplicacion2()
        self.primeraventana.setupUi(self)
        #----------------------Click event control of each button------------------------#
        self.primeraventana.btnConectar.clicked.connect(self.ejecutarConexion)
        self.primeraventana.btnEnvioInicial.clicked.connect(self.enviarPrimeraTrama)
        self.primeraventana.btnContinuar.clicked.connect(self.continuarSinEnviarPrimeraTrama)
        self.primeraventana.btnRecibirDatos.clicked.connect(self.escucharDatos)
        self.primeraventana.btnRxDatosGw.clicked.connect(self.escucharDatosGateway)
        self.primeraventana.btnRxDatosNodos.clicked.connect(self.escucharDatosNodos)
        self.primeraventana.btnEliminarDatos.clicked.connect(self.limpiarListaVisualeInterna)
        self.primeraventana.btnRegresarEnvioInicial.clicked.connect(self.retornoEnvioInicial)
        self.primeraventana.btnRegresarRecepcion.clicked.connect(self.retornoRecepcion)
        self.primeraventana.btnProceso.clicked.connect(self.procesarAristasyPesos)
        self.primeraventana.btnDijkstra.clicked.connect(self.ejecutarAlgoritmoDijkstra)
        self.primeraventana.btnKruskal.clicked.connect(self.ejecutarAlgoritmoKruskal)
        self.show()
        #----------------------variables and lists------------------------#
        self.listaSubida = [] # Uplink list
        self.listaSubidaCompeta = [] # Uplink list Complete
        self.listaAsiginacion = [] # List that stores the ID of the nodes and an assignment
        self.listaNodosyPesos = [] # List of nodes and weights
        self.listaBajada = []  # Downlink list
        self.listaDireccionesyPesos = []# List of Addrs and weights
        self.puertoSerial = '' # Serial port, stores COM port
        self.conexion = serial.Serial() #Serial connection, stores the serial connection
        self.numerodeNodos=0 # Number of  nodes
        self.numeroAristas = 0 # Number of Edges
        self.desaparecerTodosComponentes()

    # ----------------------Functions for handling graphical interface controls------------------------#
    def desaparecerTodosComponentes(self):
        self.primeraventana.tbl_tableWidgetRX.hide()
        self.primeraventana.groupBoxEnvioInicial.hide()
        self.primeraventana.groupBoxRecepcionConf.hide()
        self.primeraventana.groupBoxRecepcionSelec.hide()
        self.primeraventana.groupBoxSeleccionAlgoritmo.hide()
        self.primeraventana.btnRegresarEnvioInicial.hide()
        self.primeraventana.btnProceso.hide()
        self.primeraventana.btnRegresarRecepcion.hide()

    def reaparecerComponentesPrimerEnvio(self):
        self.primeraventana.groupBoxConexion.setEnabled(False)
        self.primeraventana.groupBoxEnvioInicial.show()
        self.primeraventana.btnRegresarEnvioInicial.hide()
        self.primeraventana.btnProceso.hide()
        self.primeraventana.btnRegresarRecepcion.hide()

    def reaparecerComponentesRx(self):
        self.primeraventana.tbl_tableWidgetRX.show()
        self.primeraventana.groupBoxRecepcionConf.show()
        self.primeraventana.btnProceso.show()
        self.primeraventana.btnRegresarEnvioInicial.show()
        self.primeraventana.btnRegresarRecepcion.hide()

    def reaparecerComponentesEjecutarAlgoritmos(self):
        self.primeraventana.groupBoxSeleccionAlgoritmo.show()
        self.primeraventana.btnProceso.hide()
        self.primeraventana.btnRegresarEnvioInicial.hide()
        self.primeraventana.btnRegresarRecepcion.show()

    def continuarSinEnviarPrimeraTrama(self):
        self.desaparecerTodosComponentes()
        self.reaparecerComponentesRx()

    def escucharDatos(self):
        self.primeraventana.groupBoxRecepcionConf.hide()
        self.primeraventana.groupBoxRecepcionSelec.show()

    # ----------------------Function to connect to the serial interface of the node. -----------------------#
    def ejecutarConexion(self):
        try:
            SeleccionDePuerto=self.primeraventana.comboxPuertos.itemText(self.primeraventana.comboxPuertos.currentIndex())
            self.puertoSerial=SeleccionDePuerto[0:3]+SeleccionDePuerto[4]
            self.conexion= serial.Serial(self.puertoSerial, 9600, 8, 'N', stopbits=1, timeout=None)
            time.sleep(1)
            self.conexion.close()
            print('Successful Connection')
            self.reaparecerComponentesPrimerEnvio()
        except:
            mensaje='¡ CONNECTION FAILED !'
            mensaje = 'CONNECTION FAILED  !'
            print(mensaje)
            ventanaAdvertencia=ventana_Advertencia(mensaje)
            ventanaAdvertencia.exec_()

    # ---------------------- Function to send the first test frame (Broadcast)----------------------#
    def enviarPrimeraTrama(self):
        self.conexion.open()
        self.conexion.flush()
        datosIniciales=self.primeraventana.txtDatoBajada_1.text()+self.primeraventana.txtDatoBajada_2.text()+self.primeraventana.txtDatoBajada_3.text()
        tramaHexString=datosIniciales
        codificado=bytes.fromhex(tramaHexString)
        byteParada=b'\r'
        self.conexion.write(codificado+byteParada)
        RET2 = self.conexion.read_until(b'\xFF')
        self.conexion.close()
        self.desaparecerTodosComponentes()
        self.reaparecerComponentesRx()

    # --------------------- Gets all data stored in the controller node ----------------------#
    def escucharDatosGateway(self):
        self.conexion.open()
        self.conexion.flush()
        consulta=b'c'
        self.conexion.write(consulta)
        recepcionSerial = self.conexion.read_until(b'\xFE')
        dirNodo = recepcionSerial[:2].hex()
        nivelBat = recepcionSerial[2:6].decode()
        nivelNSyID = recepcionSerial[6:len(recepcionSerial) - 1]
        numerodeDatosNS = int((len(nivelNSyID)) / 2)
        listaNSyID = []
        for i in range(numerodeDatosNS):
            listaNSyID.append(nivelNSyID[2 * i: 2 * i + 2].hex())
        numerodeDatosNS = int((len(listaNSyID)) / 2)
        for j in range(numerodeDatosNS):
            if j == 0:
                self.listaSubida.append(('0x' + dirNodo, nivelBat + ' V', '0x' + listaNSyID[2 * j], '0x' + listaNSyID[2 * j + 1]))
                self.listaAsiginacion.append(('0x' + dirNodo, self.numerodeNodos))
                self.nodoGWAsig=self.numerodeNodos
                self.nodoGWDir='0x' + dirNodo
                self.numerodeNodos = self.numerodeNodos + 1
            else:
                self.listaSubida.append(('---', '---', '0x' + listaNSyID[2 * j], '0x' + listaNSyID[2 * j + 1]))
            self.listaSubidaCompeta.append(('0x' + dirNodo, nivelBat + ' V', '0x' + listaNSyID[2 * j], '0x' + listaNSyID[2 * j + 1]))
            self.numeroAristas=self.numeroAristas+1
        self.conexion.close()
        self.mostrarDatosRecibidos()
        self.primeraventana.groupBoxRecepcionSelec.hide()
        self.primeraventana.groupBoxRecepcionConf.show()

    # ---------------------- Gets all the data stored in a normal node which ----------------------#
    # ---------------------- sends its data to the controller. ------------------------------------#
    def escucharDatosNodos(self):
        self.conexion.open()
        self.conexion.flush()
        recepcionSerial = self.conexion.read_until(b'\xFE')
        dirNodo = recepcionSerial[:2].hex()
        nivelBat = recepcionSerial[2:6].decode()
        nivelNSyID = recepcionSerial[6:len(recepcionSerial) - 1]
        numerodeDatosNS = int((len(nivelNSyID)) / 2)
        listaNSyID=[]
        for i in range(numerodeDatosNS):
            listaNSyID.append(nivelNSyID[2 * i: 2 * i + 2].hex())
        numerodeDatosNS = int((len(listaNSyID)) / 2)
        for j in range(numerodeDatosNS):
            if j==0:
                self.listaSubida.append(('0x'+dirNodo, nivelBat+' V', '0x'+listaNSyID[2 * j], '0x'+listaNSyID[2 * j + 1]))
                self.listaAsiginacion.append(('0x'+dirNodo, self.numerodeNodos))
                self.numerodeNodos = self.numerodeNodos + 1
            else:
                self.listaSubida.append(('---', '---', '0x'+listaNSyID[2 * j], '0x'+listaNSyID[2 * j + 1]))
            self.listaSubidaCompeta.append(('0x' + dirNodo, nivelBat + ' V', '0x' + listaNSyID[2 * j], '0x' + listaNSyID[2 * j + 1]))
            self.numeroAristas = self.numeroAristas + 1
        self.conexion.close()
        self.mostrarDatosRecibidos()
        self.primeraventana.groupBoxRecepcionSelec.hide()
        self.primeraventana.groupBoxRecepcionConf.show()

    # ----------------------Show neighbor tables in the graphical interface  ------------------------------------#
    def mostrarDatosRecibidos(self):
        self.limpiarListaVisual()
        fila=0
        for registro in self.listaSubida:
            columna=0
            self.primeraventana.tbl_tableWidgetRX.insertRow(fila)
            for elemento in registro:
                celda=QTableWidgetItem(elemento)
                celda.setTextAlignment(QtCore.Qt.AlignCenter)
                self.primeraventana.tbl_tableWidgetRX.setItem(fila,columna,celda)
                columna+=1
            fila+=1

    # ----------------------Functions for handling graphical interface controls------------------------#
    def retornoEnvioInicial(self):
        self.limpiarListaVisualeInterna()
        self.desaparecerTodosComponentes()
        self.reaparecerComponentesPrimerEnvio()

    # ----------------------This function performs processing to convert the neighbor --------------------------------------#
    # ---------------------tables into edges and weights to be used by the algorithms.  ------------------------------------#
    def procesarAristasyPesos(self):
        aprob = True
        if  self.numerodeNodos<=1:
            aprob = False
            print('numero n: ',self.numerodeNodos)
        for buscVacio in self.listaSubidaCompeta:
            if  buscVacio[2]=='0x0000' or buscVacio[3]=='0x0000':
                aprob=False
                print('listaSubida: ')
                print(self.listaSubidaCompeta)
        nrep=0
        for buscRep in self.listaSubidaCompeta:
            for nodo in self.listaSubida:
                if buscRep[0]==nodo[0]:
                    nrep=nrep+1
                    if nrep==2:
                        aprob = False
                        print('listaSubida: ')
                        print(self.listaSubidaCompeta)
                        print(self.listaSubida)
            nrep = 0
        if  aprob==True:
            print('Poceso de pesos')
            print(self.listaAsiginacion)
            print(self.listaSubidaCompeta)
            fila = 0
            for i,datosDRPOrg in enumerate(self.listaSubidaCompeta):
                print(datosDRPOrg[0][2:6], datosDRPOrg[1][0:4], datosDRPOrg[2][2:6], datosDRPOrg[3][2:6])
                asg1 = 0
                asg2 = 0
                for asignacion in self.listaAsiginacion:
                    if datosDRPOrg[0] == asignacion[0]:
                        asg1 = asignacion[1]
                for asignacion in self.listaAsiginacion:
                    if datosDRPOrg[3] == asignacion[0]:
                        asg2 = asignacion[1]
                ID_S = asg1; ID_NS = asg2
                NB = datosDRPOrg[1][0:4]; NS = datosDRPOrg[2][2:6]
                NB = round(float(NB), 2); NS = int(NS, 16)
                nodoDestino = ID_S; nodoOrigen = ID_NS; peso =round(float(100-(NB + NS)),2)
                self.listaNodosyPesos.append((nodoOrigen, nodoDestino, peso))
                self.listaDireccionesyPesos.append((datosDRPOrg[0],str(peso),datosDRPOrg[3]))
                print(nodoOrigen, nodoDestino, peso)
            print('lista Nodos Asignados Peso')
            print(self.listaNodosyPesos)
            print('lista Direeciones y pesos')
            print(self.listaDireccionesyPesos)
            self.desaparecerTodosComponentes()
            self.reaparecerComponentesEjecutarAlgoritmos()
            self.primeraventana.lblDatoGateway.setText(self.nodoGWDir)
            self.primeraventana.lblDatoNodos.setText(str(self.numerodeNodos))
            self.primeraventana.lblDatoArista.setText(str(self.numeroAristas))
        else:
            mensaje="Datos Recibidos Incorrectos !"
            print(mensaje)
            ventanaAdvertencia=ventana_Advertencia(mensaje)
            ventanaAdvertencia.exec_()
            self.limpiarListaVisualeInterna()

    # ----------------------Functions for handling graphical interface controls------------------------#
    def retornoRecepcion(self):
        self.desaparecerTodosComponentes()
        self.reaparecerComponentesRx()

    # ----------------------Functions for handling graphical interface controls------------------------#
    def limpiarListaVisualeInterna(self):
        for registro in self.listaSubida:
            self.primeraventana.tbl_tableWidgetRX.removeRow(0)
        self.listaSubida.clear()
        self.listaAsiginacion.clear()
        self.listaSubidaCompeta.clear()
        self.numerodeNodos = 0
        self.numeroAristas = 0

    # ----------------------Execution of the window corresponding to Dijkstra's algorithm.------------------------#
    def ejecutarAlgoritmoDijkstra(self):
        ventanaDijkstra= ventana_Dijkstra(self.numerodeNodos,self.nodoGWAsig,self.listaNodosyPesos,self.listaAsiginacion,self.conexion,self.listaDireccionesyPesos,self.listaSubida)
        ventanaDijkstra.exec_()
    # ----------------------Execution of the window corresponding to Kruskal's algorithm.------------------------#
    def ejecutarAlgoritmoKruskal(self):
        ventanaKruskal= ventana_Kruskal(self.numerodeNodos,self.nodoGWAsig,self.listaNodosyPesos,self.listaAsiginacion,self.conexion,self.listaDireccionesyPesos,self.listaSubida)
        ventanaKruskal.exec_()

    # ----------------------Functions for handling graphical interface controls------------------------#
    def limpiarListaVisual(self):
        for registro in self.listaSubida:
            self.primeraventana.tbl_tableWidgetRX.removeRow(0)

# --------------------- Main function.------------------------#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana= mostrar()
    ventana.show()
    sys.exit(app.exec_())