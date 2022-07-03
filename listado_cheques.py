import sys
import csv
from datetime import datetime
    
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

def filtrarListadoDeCheques(archivo,dni,salida,tipo,estado,fechas):
  rutaArchivo = open(archivo,"r")
  archivoCSV = list(csv.reader(rutaArchivo))
  chequesPorDni = filtrarChequesPorDni(archivoCSV,dni)
  chequesPorTipo = filtrarChequesPorTipo(chequesPorDni, tipo)
  chequesPorEstado = filtrarChequesPorEstado(chequesPorTipo,estado)
  chequesPorFechas = filtarChequesPorDias(chequesPorEstado, fechas)
  if salida == "PANTALLA":
    if chequesPorFechas == []:
      print("No se encotraron resultados")
    else:  
      print(archivoCSV[0])
      for linea in chequesPorFechas:
        linea[-4], linea[-5] = timestampToFecha(linea[-4]),timestampToFecha(linea[-5])
        print(linea)

  else:
    archivoAImprimir = open(dni +".csv","w", newline="")
    archivoAImprimirCSV = csv.writer(archivoAImprimir)
    archivoAImprimirCSV.writerow(archivoCSV[0])
    archivoAImprimirCSV.writerows(chequesPorFechas)
    archivoAImprimir.close()
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