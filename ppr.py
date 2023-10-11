
op=False
n=0
while op==False:
    n=n+1
    print(n)
    if n==4:
        op=True
print(n)



'''
#print(int('2')*2)
#print('2')
listaDirecciones = []
listaDirecciones.append(('00006','00005'))
listaDirecciones.append(('00005','00006'))
listaDirecciones.append(('00004','00006'))
listaDirecciones.append(('00004','00005'))
listaDirecciones.append(('00006','00004'))
print(listaDirecciones)
listaAsiginacion = []
listaAsiginacion.append(('00006',0))
listaAsiginacion.append(('00005',1))
listaAsiginacion.append(('00004',2))
print(listaAsiginacion)
listaNueva = []
# DIreccionando
for i,rutaoriginal in enumerate(listaDirecciones):
    ns1 = 0
    ns2 = 0
    for asignar in listaAsiginacion:
        if  rutaoriginal[0]==asignar[0]:
            ns1=asignar[1]
    for asignar in listaAsiginacion:
        if  rutaoriginal[1]==asignar[0]:
            ns2=asignar[1]
    listaNueva.append((ns1,ns2))
print(listaNueva)
###Redirecionando
listaDIRECCNueva = []
for i,ruta in enumerate(listaNueva):
    rd1 = '0'
    rd2 = '0'
    for reasignar in listaAsiginacion:
        if  ruta[0]==reasignar[1]:
            rd1=reasignar[0]
    for reasignar in listaAsiginacion:
        if  ruta[1]==reasignar[1]:
            rd2=reasignar[0]
    listaDIRECCNueva.append((rd1,rd2))
print(listaDIRECCNueva)
var1=1
var2=2
if var1==1 and var2==2:
    print("Datos Correctos")
'''