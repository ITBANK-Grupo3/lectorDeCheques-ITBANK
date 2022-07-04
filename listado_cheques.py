from itertools import count
import sys
import csv
from datetime import datetime

def validarRepeticionesCheques(listado):
  nrosDeCheques = [cheque[0] for cheque in listado]
  chequesRepetidos = [nrosDeCheques.count(nroCheque) for nroCheque in nrosDeCheques]
  repetidos = False 
  for cantidad in chequesRepetidos:
    if cantidad>1:
      repetidos = True
    else:
      pass
  return repetidos

def filtrarChequesPorDni(listado,dni):
  return(list(listado := filter(lambda lista:lista[-3] == dni, listado)))

def filtrarChequesPorTipo(listado, tipo):
  return(list(listado := filter(lambda lista:lista[-2] == tipo, listado)))

def filtrarChequesPorEstado(listado,estado):
  if estado == "sin entrada":
    return list(listado)    
  else:
    return(list(listado := filter(lambda lista:lista[-1] == estado, listado)))

def filtarChequesPorDias(listado,fechas):
  if fechas == "sin entrada":
    return list(listado)
  else:
    return(list(listado:=filter(lambda lista:fechas[0]<=int(lista[-5])<=fechas[1],listado)))

def fechaToTimestamp(fechas):
  fechas =fechas.split(":")
  fechas[0] = int((datetime.strptime(fechas[0], '%d-%m-%Y') ).timestamp())
  fechas[1] = int((datetime.strptime(fechas[1], '%d-%m-%Y') ).timestamp())
  return fechas

def timestampToFecha(fecha):
  return (datetime.fromtimestamp(int(fecha))).strftime("%d/%m/%Y")

def buscarRepetidos(i,lista,elemento):
  guardado=[]
  for j in range (len(lista)):
    cc=0
    if elemento in lista[j-1]: #Contador de elementos Repetidos
      cc+=1
    if cc>1 and (elemento not in guardado):
      guardado.append(lista[i-1])
  return guardado

def filtrarListadoDeCheques(archivo,dni,salida,tipo,estado,fechas):
  rutaArchivo = open(archivo,"r")
  archivoCSV = list(csv.reader(rutaArchivo))
  chequesPorDni = filtrarChequesPorDni(archivoCSV,dni)
  repetido = validarRepeticionesCheques(chequesPorDni)
  if not repetido:
    chequesPorTipo = filtrarChequesPorTipo(chequesPorDni, tipo)
    chequesPorEstado = filtrarChequesPorEstado(chequesPorTipo,estado)
    chequesPorFechas = filtarChequesPorDias(chequesPorEstado, fechas)
    if salida.upper() == "PANTALLA":
      if chequesPorFechas == []:
        print("No se encotraron resultados")
      else:  
        NroCheque,CodigoBanco,CodigoSucursal,NumeroCuentaOrigen,NumeroCuentaDestino,Valor,FechaOrigen,FechaPago,Dni,Tipo,Estado = archivoCSV[0]
        print ("{:<12} {:<13} {:<16} {:<22} {:<22} {:<16} {:<16} {:<16} {:<16} {:<16} {:<16}".format(NroCheque,CodigoBanco,CodigoSucursal,NumeroCuentaOrigen,NumeroCuentaDestino,Valor,FechaOrigen,FechaPago,Dni,Tipo,Estado))
        for linea in chequesPorFechas:
          linea[-4], linea[-5] = timestampToFecha(linea[-4]),timestampToFecha(linea[-5])
          NroCheque,CodigoBanco,CodigoSucursal,NumeroCuentaOrigen,NumeroCuentaDestino,Valor,FechaOrigen,FechaPago,Dni,Tipo,Estado = linea
          print ("{:<12} {:<13} {:<16} {:<22} {:<22} {:<16} {:<16} {:<16} {:<16} {:<16} {:<16}".format(NroCheque,CodigoBanco,CodigoSucursal,NumeroCuentaOrigen,NumeroCuentaDestino,Valor,FechaOrigen,FechaPago,Dni,Tipo,Estado))
    elif salida.upper() == "CSV":
      archivoAImprimir = open(dni+'-'+ str(datetime.now().timestamp()) +".csv","w", newline="")
      archivoAImprimirCSV = csv.writer(archivoAImprimir)     
      info = [archivoCSV[0][-5], archivoCSV[0][-4], archivoCSV[0][-6], archivoCSV[0][-8]]
      archivoAImprimirCSV.writerow(info)
      for linea in chequesPorFechas:
        info = [linea[-5], linea[-4], linea[-6],linea[-8]]
        archivoAImprimirCSV.writerow(info)
      archivoAImprimir.close()
    else:
        print("No se reconoce esa salida, vuelva intentar nuevamente con PANTALLA o CSV")
  else:
    print("ERROR: Se repite número de cheque de la cuenta seleccionada.")
  rutaArchivo.close()

estado,fechas = "sin entrada" , "sin entrada" 

if len(sys.argv) < 5:
  print("Error! Debe colocar al menos 4 argumentos")
elif len(sys.argv) == 6:
  if sys.argv[5].upper() == "APROBADO" or sys.argv[5].upper() == "RECHAZADO" or sys.argv[5].upper()=="PENDIENTE":
      archivo,dni,salida,tipo,estado = (sys.argv[1],sys.argv[2],sys.argv[3].upper(),sys.argv[4].upper(),sys.argv[5].upper())
  else:
      archivo,dni,salida,tipo,fechas = (sys.argv[1],sys.argv[2],sys.argv[3].upper(),sys.argv[4].upper(),sys.argv[5])
      fechas=fechaToTimestamp(fechas)
elif len(sys.argv) == 7:
  archivo,dni,salida,tipo,estado,fechas = (sys.argv[1],sys.argv[2],sys.argv[3].upper(),sys.argv[4].upper(),sys.argv[5].upper(),sys.argv[6])
  fechas=fechaToTimestamp(fechas)
else:
  archivo,dni,salida,tipo = (sys.argv[1],sys.argv[2],sys.argv[3].upper(),sys.argv[4].upper())

filtrarListadoDeCheques(archivo,dni,salida,tipo,estado,fechas)
