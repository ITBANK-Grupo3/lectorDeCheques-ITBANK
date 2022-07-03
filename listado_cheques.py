import sys
import csv

def filtrarChequesPorDni(listado,dni):
  return(list(listado := filter(lambda lista:lista[-3] == dni, listado)))

def filtrarChequesPorTipo(listado, tipo):
  return(list(listado := filter(lambda lista:lista[-2] == tipo, listado)))

def filtrarChequesPorEstado(listado,estado):
  if estado == "sin entrada":
    return list(listado)    
  else:
    return(list(listado := filter(lambda lista:lista[-1] == estado, listado)))

def buscarRepetidos(i,lista,elemento):
  guardado=[]
  for j in range (len(lista)):
    cc=0
    if elemento in lista[j-1]: #Contador de elementos Repetidos
      cc+=1
    if cc>1 and (elemento not in guardado):
      guardado.append(lista[i-1])
  return guardado

def repiteCheque(listado):
  for i in range (len(listado)):
    cuenta=listado[i-1][3]
    cheques=buscarRepetidos(i,listado,cuenta) #Lista que guarda cheques con cuentas repetidas
    for k in range(len(cheques)):
      cheque=cheques[k-1][0]
      errorcheque=buscarRepetidos(i,cheques,cheque) #Lista que guarda cheques con Nro de cheque repetido de cuenta repetida
  if errorcheque != []:
    return errorcheque
  else:
    errorcheque=[]
    return errorcheque

def filtrarListadoDeCheques(archivo,dni,salida,tipo,estado,fecha="sin entrada"):
  rutaArchivo = open(archivo,"r")
  archivoCSV = list(csv.reader(rutaArchivo))
  chequesPorDni = filtrarChequesPorDni(archivoCSV,dni)
  chequesPorTipo = filtrarChequesPorTipo(chequesPorDni, tipo)
  chequesPorEstado = filtrarChequesPorEstado(chequesPorTipo,estado)
  errorChequeRepetido = repiteCheque(chequesPorEstado)

  if salida == "PANTALLA":
    print(archivoCSV[0])
    for linea in chequesPorEstado:
      print(linea)
    for lineas in errorChequeRepetido:
      print(lineas)

  else:
    archivoAImprimir = open("listado_de_cheques.csv","w")
    archivoAImprimirCSV = csv.writer(archivoAImprimir)
    archivoAImprimirCSV.writerow(archivoCSV[0])
    archivoAImprimirCSV.writerows(chequesPorEstado)
    archivoAImprimir.close()
  rutaArchivo.close()

        



estado = "sin entrada" if len(sys.argv) < 6 else sys.argv[5]

if len(sys.argv) < 5:
  print("Error! Debe colocar al menos 4 argumentos")
else:
  archivo,dni,salida,tipo = (sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
  filtrarListadoDeCheques(archivo,dni,salida,tipo,estado)