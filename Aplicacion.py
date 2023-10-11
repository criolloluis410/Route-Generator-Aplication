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
        # Eventos click
        self.primeraventana.btnConectar.clicked.connect(self.ejecutarConexion)
        self.primeraventana.btnEnvioInicial.clicked.connect(self.enviarPrimeraTrama)
        self.primeraventana.btnContinuar.clicked.connect(self.continuarSinEnviarPrimeraTrama)
        self.primeraventana.btnRecibirDatos.clicked.connect(self.escucharDatos)
        self.primeraventana.btnRxDatosGw.clicked.connect(self.escucharDatosGateway)
        self.primeraventana.btnRxDatosNodos.clicked.connect(self.escucharDatosNodos)
        #self.primeraventana.btnRecibirDatos.clicked.connect(self.mostrarDatosRecibidos)
        self.primeraventana.btnEliminarDatos.clicked.connect(self.limpiarListaVisualeInterna)
        self.primeraventana.btnRegresarEnvioInicial.clicked.connect(self.retornoEnvioInicial)
        self.primeraventana.btnRegresarRecepcion.clicked.connect(self.retornoRecepcion)
        self.primeraventana.btnProceso.clicked.connect(self.procesarAristasyPesos)
        self.primeraventana.btnDijkstra.clicked.connect(self.ejecutarAlgoritmoDijkstra)
        self.primeraventana.btnKruskal.clicked.connect(self.ejecutarAlgoritmoKruskal)
        self.show()
        # Variables y listas Globales
        self.listaSubida = [] # Lista general, contiene los listaSubida de subida
        self.listaSubidaCompeta = [] # Lista general, contiene los listaSubida de subida
        self.listaAsiginacion = []# Lista que almacena el ID de los nodos y su respectiva asignacion
        self.listaNodosyPesos = []
        self.listaBajada = []  # Lista general, contiene los listaSubida de subida
        self.listaDireccionesyPesos = []
        self.puertoSerial = '' #Puerto serial, almacena el puerto COM
        self.conexion = serial.Serial() #Conexion serial, almacena la conexion serial
        self.numerodeNodos=0
        self.numeroAristas = 0
        #Funciones Iniciales
        self.desaparecerTodosComponentes()

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

##########################################################################################################
    def ejecutarConexion(self):# Configuracion de conexion serial
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

    def continuarSinEnviarPrimeraTrama(self):
        self.desaparecerTodosComponentes()
        self.reaparecerComponentesRx()

    def escucharDatos(self):
        self.primeraventana.groupBoxRecepcionConf.hide()
        self.primeraventana.groupBoxRecepcionSelec.show()

    def escucharDatosGateway(self):
        self.conexion.open()  # Inicio de la conexion serial
        self.conexion.flush()  # Limpieza del Buffer de RX
        consulta=b'c'
        self.conexion.write(consulta)
        recepcionSerial = self.conexion.read_until(b'\xFE')  # Recepcion de datos seriales hasta el caracter FE
        dirNodo = recepcionSerial[:2].hex()  # Separacion de la direccion del nodo que envia la informacion (.hex si el valor exadecimal no es compatible con un digito ACII)
        nivelBat = recepcionSerial[2:6].decode()  # Separacion del Nivel de Bateria del nodo (.decode si el valor exadecimal es compatible con un digito ACII)
        nivelNSyID = recepcionSerial[6:len(recepcionSerial) - 1]  # Separacion de los niveles de señal y el identificador, del nodo al que pertenece, almacenados en el nodo
        numerodeDatosNS = int((len(nivelNSyID)) / 2)  # total de caracteres, correspondientes a NS y ID, almacenados en la variable dividido para dos
        listaNSyID = []
        for i in range(numerodeDatosNS):  # Almacenamieto de todos los NS y ID en una unica lista
            listaNSyID.append(nivelNSyID[2 * i: 2 * i + 2].hex())
        numerodeDatosNS = int((len(listaNSyID)) / 2)  # total de NS y ID, en hexadecimal, almacenados en la variable dividido para dos
        for j in range(
                numerodeDatosNS):  # Almacenamiento de todos los datos del Nodo ID Fuente, Nivel de bateria, Nivel o niveles Señal y su correspondiente ID Origen
            if j == 0:
                self.listaSubida.append(('0x' + dirNodo, nivelBat + ' V', '0x' + listaNSyID[2 * j], '0x' + listaNSyID[2 * j + 1]))
                self.listaAsiginacion.append(('0x' + dirNodo, self.numerodeNodos))  # Carga de asignaciones
                self.nodoGWAsig=self.numerodeNodos
                self.nodoGWDir='0x' + dirNodo
                self.numerodeNodos = self.numerodeNodos + 1
            else:
                self.listaSubida.append(('---', '---', '0x' + listaNSyID[2 * j], '0x' + listaNSyID[2 * j + 1]))
            self.listaSubidaCompeta.append(('0x' + dirNodo, nivelBat + ' V', '0x' + listaNSyID[2 * j], '0x' + listaNSyID[2 * j + 1]))
            self.numeroAristas=self.numeroAristas+1
        self.conexion.close()
        self.mostrarDatosRecibidos()# muestra en la lista visual todos los datos
        self.primeraventana.groupBoxRecepcionSelec.hide()
        self.primeraventana.groupBoxRecepcionConf.show()

    def escucharDatosNodos(self):
        self.conexion.open()# Inicio de la conexion serial
        self.conexion.flush()# Limpieza del Buffer de RX
        recepcionSerial = self.conexion.read_until(b'\xFE')# Recepcion de datos seriales hasta el caracter FE
        dirNodo = recepcionSerial[:2].hex()    # Separacion de la direccion del nodo que envia la informacion (.hex si el valor exadecimal no es compatible con un digito ACII)
        nivelBat = recepcionSerial[2:6].decode()   # Separacion del Nivel de Bateria del nodo (.decode si el valor exadecimal es compatible con un digito ACII)
        #print(recepcionSerial)
        #print(('0x' + dirNodo, '0x' +nivelBat))
        nivelNSyID = recepcionSerial[6:len(recepcionSerial) - 1]# Separacion de los niveles de señal y el identificador, del nodo al que pertenece, almacenados en el nodo
        numerodeDatosNS = int((len(nivelNSyID)) / 2)# total de caracteres, correspondientes a NS y ID, almacenados en la variable dividido para dos
        #print(nivelNSyID)
        #print(numerodeDatosNS)
        listaNSyID=[]
        for i in range(numerodeDatosNS):#Almacenamieto de todos los NS y ID en una unica lista
            #print(nivelNSyID[ 2*i : 2*i+2 ])
            #print(nivelNSyID[2 * i: 2 * i + 2].hex())
            listaNSyID.append(nivelNSyID[2 * i: 2 * i + 2].hex())
        numerodeDatosNS = int((len(listaNSyID)) / 2)# total de NS y ID, en hexadecimal, almacenados en la variable dividido para dos
        #print(numerodeDatosNS)
        for j in range(numerodeDatosNS): # Almacenamiento de todos los datos del Nodo ID Fuente, Nivel de bateria, Nivel o niveles Señal y su correspondiente ID Origen
            #print(listaNSyID[2 * j], listaNSyID[2 * j + 1])
            #print((dirNodo, nivelBat, listaNSyID[2 * j], listaNSyID[2 * j + 1]))
            if j==0:
                self.listaSubida.append(('0x'+dirNodo, nivelBat+' V', '0x'+listaNSyID[2 * j], '0x'+listaNSyID[2 * j + 1]))
                self.listaAsiginacion.append(('0x'+dirNodo, self.numerodeNodos))#Carga de asignaciones
                self.numerodeNodos = self.numerodeNodos + 1
            else:
                self.listaSubida.append(('---', '---', '0x'+listaNSyID[2 * j], '0x'+listaNSyID[2 * j + 1]))
            self.listaSubidaCompeta.append(('0x' + dirNodo, nivelBat + ' V', '0x' + listaNSyID[2 * j], '0x' + listaNSyID[2 * j + 1]))
            self.numeroAristas = self.numeroAristas + 1
        self.conexion.close()
        self.mostrarDatosRecibidos()
        self.primeraventana.groupBoxRecepcionSelec.hide()
        self.primeraventana.groupBoxRecepcionConf.show()

    def mostrarDatosRecibidos(self):# Mostrar datos en la interfaz visual
        self.limpiarListaVisual() # Hay que limpiar todos los datos de la lsita visual para que no se acumulen
        fila=0
        for registro in self.listaSubida:# se agregan los nuevos elementos a la lsita visual
            columna=0
            self.primeraventana.tbl_tableWidgetRX.insertRow(fila)
            for elemento in registro:
                celda=QTableWidgetItem(elemento)
                celda.setTextAlignment(QtCore.Qt.AlignCenter)
                self.primeraventana.tbl_tableWidgetRX.setItem(fila,columna,celda)
                columna+=1
            fila+=1

    def retornoEnvioInicial(self):
        self.limpiarListaVisualeInterna()
        self.desaparecerTodosComponentes()
        self.reaparecerComponentesPrimerEnvio()

    def procesarAristasyPesos(self):
        aprob = True #Busqueda de incongruencias antes del procesamiento de rutas
        if  self.numerodeNodos<=1:#Evita errores si solo existe la informacion de un solo nodo
            aprob = False
            print('numero n: ',self.numerodeNodos)
        for buscVacio in self.listaSubidaCompeta:#Busqyeda de nodos con informacion incompleta
            if  buscVacio[2]=='0x0000' or buscVacio[3]=='0x0000':
                aprob=False
                print('listaSubida: ')
                print(self.listaSubidaCompeta)
        nrep=0#Busqueda de nodos repetidos
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
            #self.listaAsiginacion.append(('0x0006',6))
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
            #self.numerodeNodos=0
            #self.listaAsiginacion.clear()
            #self.listaSubida.clear()

    def retornoRecepcion(self):
        self.desaparecerTodosComponentes()
        self.reaparecerComponentesRx()

    def ejecutarAlgoritmoDijkstra(self):
        ventanaDijkstra= ventana_Dijkstra(self.numerodeNodos,self.nodoGWAsig,self.listaNodosyPesos,self.listaAsiginacion,self.conexion,self.listaDireccionesyPesos,self.listaSubida)
        ventanaDijkstra.exec_()

    def ejecutarAlgoritmoKruskal(self):
        ventanaKruskal= ventana_Kruskal(self.numerodeNodos,self.nodoGWAsig,self.listaNodosyPesos,self.listaAsiginacion,self.conexion,self.listaDireccionesyPesos,self.listaSubida)
        ventanaKruskal.exec_()


    def limpiarListaVisualeInterna(self):  # Limpia la lista visual e interna para recibir nuevos datos
        for registro in self.listaSubida:
            self.primeraventana.tbl_tableWidgetRX.removeRow(0)
        self.listaSubida.clear()
        self.listaAsiginacion.clear()
        self.listaSubidaCompeta.clear()
        self.numerodeNodos = 0
        self.numeroAristas = 0

    def limpiarListaVisual(self):  # Limpia solo lista visual
        for registro in self.listaSubida:
            self.primeraventana.tbl_tableWidgetRX.removeRow(0)
        ##################################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana= mostrar()
    ventana.show()
    sys.exit(app.exec_())


'''     conexion.open()
        conexion.flush()
        deciInt = self.obtexto()
        deciStr = str(deciInt)
        MSG = 'ho' + "\r"
        conexion.write(MSG.encode())
        print('Se envió el MSG: ' + MSG)
        print('Se envió el MSG2 HEX: ')
        RET2 = conexion.read(3)
        print("LLEGADA:")
        print(RET2)
        conexion.close()'''

'''#RET1 = RET[:2].decode()# si el valor exadecimal es compatible con un digito ACII
RET1 = RET[:2].hex() # si el valor exadecimal no es compatible con un digito ACII
RET2 = RET[2:4].hex()
RET3 = RET[4:6].hex()
RET4 = RET[6:8].hex()
print(('0x' + RET1, RET2, RET3, RET4))
self.listaSubida.append(('0x'+RET1, '0x'+RET2, '0x'+RET3, '0x'+RET4))
RET = conexion.readline()
print("LLEGADA 1 bytes:")
print(RET)
#RET1 = RET[:2].decode()# si el valor exadecimal es compatible con un digito ACII
RET1 = RET[:2].hex() # si el valor exadecimal no es compatible con un digito ACII
RET2 = RET[2:4].hex()
RET3 = RET[4:6].hex()
RET4 = RET[6:8].hex()
print(('0x' + RET1, RET2, RET3, RET4))
self.listaSubida.append(('0x'+RET1, '0x'+RET2, '0x'+RET3, '0x'+RET4))
RET = conexion.readline()
print("LLEGADA 1 bytes:")
print(RET)
#RET1 = RET[:2].decode()# si el valor exadecimal es compatible con un digito ACII
RET1 = RET[:2].hex() # si el valor exadecimal no es compatible con un digito ACII
RET2 = RET[2:4].hex()
RET3 = RET[4:6].hex()
RET4 = RET[6:8].hex()
print(('0x' + RET1, RET2, RET3, RET4))
self.listaSubida.append(('0x'+RET1, '0x'+RET2, '0x'+RET3, '0x'+RET4))
####################################################################
        if  aprob==True:
            self.desaparecerTodosComponentes()
            self.reaparecerComponentesAlgoritmo()
            print(self.listaSubida)
            fila = 0
            for datosFila in self.listaSubidaCompeta:
                print(datosFila[0][2:6], datosFila[1][0:4], datosFila[2][2:6] + datosFila[3][2:6])
                IS_S = datosFila[0][2:6];NB = datosFila[1][0:4];NS = datosFila[2][2:6];ID_NS = datosFila[3][2:6]
                IS_S = int(IS_S, 16);NB = round(float(NB), 2);NS = int(NS, 16);ID_NS = int(ID_NS, 16)
                nodoDestino = IS_S;peso = NB + NS;nodoOrigen = ID_NS
                self.listaNodosyPesos.append((nodoOrigen - 4, nodoDestino - 4, peso))
                print(nodoOrigen, nodoDestino, peso)
            print(self.listaNodosyPesos)
'''

'''    def ejecutarAlgoritmoKruskal(self):
        numeroNodos =self.numerodeNodos
        print(self.listaNodosyPesos)
        AlgKr = GraphK(numeroNodos)
        for dat in self.listaNodosyPesos:
            print(dat)
            AlgKr.add_edge(dat[0], dat[1], dat[2])
        AlgKr.kruskal()
        print('resultados')
        print(AlgKr.resultados)
        self.listaNuevasRutas=[]
        for res in AlgKr.resultados:
            self.listaNuevasRutas.append(res)
        print('nuevas rutas 1')
        print(self.listaNuevasRutas)
        ################################# Modificacion de rutas para evitar lazos ###############################################
        nodosDstNuev = []
        nodoGW = self.nodoGWAsig
        print('For 1 : ')
        for i, ruta in enumerate(self.listaNuevasRutas):
            # for i, obj in enumerate(g.resultados):
            if ruta[0] == nodoGW:
                self.listaNuevasRutas[i] = (ruta[1], ruta[0], ruta[2], 'm')  # se deberia modificar el peso
                print('mg')
                print(self.listaNuevasRutas)
                # nodosDstNuev.append(ruta[0])
        print(self.listaNuevasRutas)
        print(nodosDstNuev)
        print('For 2 : ')
        for i, ruta in enumerate(self.listaNuevasRutas):
            # for i, obj in enumerate(g.resultados):
            if ruta[1] == nodoGW:
                self.listaNuevasRutas[i] = (ruta[0], ruta[1], ruta[2], 'v')
                print(self.listaNuevasRutas[i])
                nodosDstNuev.append(ruta[0])
        print(self.listaNuevasRutas)
        print(nodosDstNuev)
        print('For 3 : ')
        condicion=True
        while condicion==True:
            for i, ruta in enumerate(self.listaNuevasRutas):
                # for i, obj in enumerate(g.resultados):
                if ruta[3] != 'v':
                    print(self.listaNuevasRutas[i])
                    for dst in nodosDstNuev:
                        if ruta[1] == dst:
                            self.listaNuevasRutas[i] = (ruta[0], ruta[1], ruta[2], 'v')
                            nodosDstNuev.append(ruta[0])

            print(self.listaNuevasRutas)
            print(nodosDstNuev)
            print('For 4 : ')
            for i, ruta in enumerate(self.listaNuevasRutas):
                # for i, obj in enumerate(g.resultados):
                if ruta[3] != 'v':
                    print(self.listaNuevasRutas[i])
                    for rtc in self.listaNuevasRutas:
                        if ruta[0] == rtc[0] and rtc[3] == 'v':
                            self.listaNuevasRutas[i] = (ruta[1], ruta[0], ruta[2], 'v')
                            nodosDstNuev.append(ruta[1])
            continuar=0
            for i,ruta in enumerate(self.listaNuevasRutas):
                if ruta[3] !='v':
                    continuar=1
            if  continuar==0:
                condicion=False

        print('Nueva Rutas Organizadas:')
        print(self.listaNuevasRutas)
        print(nodosDstNuev)
        ventanaKruskal= ventana_Kruskal(self.nodoGWDir,self.listaNuevasRutas,self.listaAsiginacion,self.conexion)
        ventanaKruskal.exec_()'''
