'''s= 'abc'.encode('utf-8')
print(s)
print(s.hex())
'''


str="ab\r"+"6263"
by = bytes.fromhex(str)
print("bytes 1")
print(by)
#print(by.decode())
en = str.encode()
print("bytes 2")
print(en)
print("bytes union b y e")
print(by + en)
s=0
tramaBinaroString = "ff020111000102220002"
tramaBinaroString2 = bytes.fromhex(tramaBinaroString)
sparador = b'\r'
print(sparador)
tramaBinaroString2 = tramaBinaroString2 + sparador
tramaBinaroString3=tramaBinaroString2[2:len(tramaBinaroString2)-1]
print(tramaBinaroString2)
print(tramaBinaroString3)
longi=int((len(tramaBinaroString3))/2)
print(longi)
lista2=[]
for i in range(longi):
    print(tramaBinaroString3[2*i:2*i+2])
    lista2.append(tramaBinaroString3[2*i:2*i+2].hex())
for var in lista2:
    print(var)
longi2=int((len(lista2))/2)
print(longi2)
for j in range(longi2):
    print(lista2[2*j],lista2[2*j+1])

for var in tramaBinaroString2:
   # print(hex(var))
    if var==b'\x00':
        print('ok')
#print(en.decode())

#by.hex().encode()
#print(by.hex().encode())

#print("hola\r".encode())


hx = '00029a'
hx = int(hx, 16)
print(hx)
decimal=666
hexadecimal = hex(decimal)
ne=hexadecimal.replace('x','00')
print(hexadecimal)
print(ne)
print(ne[len(ne)-4:len(ne)])
nf='2.2'
ni=2
nf=float(nf)
hdd='0000'
hdd=int(hdd,16)
print(float(nf)+ni)


'''
binario1 = '00000110'
print('Binario: ' + binario1)
decimal = int(binario1, 2)
print('Decimal: ')
print(decimal)
#print(int(s, 16))
hexadecimal = hex(decimal)
print(hexadecimal)

s = '0xab03'
codificado = s.encode()
print(codificado)

TramaBinaroString = "0x000200010a"
codificado = TramaBinaroString.encode()
print(codificado)'''