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
        linea[-4] = (datetime.fromtimestamp(int(linea[-4]))).strftime("%d/%m/%Y")
        linea[-5] = (datetime.fromtimestamp(int(linea[-5]))).strftime("%d/%m/%Y")
        print(linea)

  else:

    archivoAImprimir = open(dni +".csv","w", newline="")
    archivoAImprimirCSV = csv.writer(archivoAImprimir)
    archivoAImprimirCSV.writerow(archivoCSV[0])
    archivoAImprimirCSV.writerows(chequesPorFechas)
    archivoAImprimir.close()
  rutaArchivo.close()

estado = "sin entrada" 
fechas = "sin entrada"

if len(sys.argv) < 5:
  print("Error! Debe colocar al menos 4 argumentos")
elif len(sys.argv) == 6:
  archivo,dni,salida,tipo,estado = (sys.argv[1],sys.argv[2],sys.argv[3].upper(),sys.argv[4].upper(),sys.argv[5].upper())
elif len(sys.argv) == 7:
  archivo,dni,salida,tipo,estado,fechas = (sys.argv[1],sys.argv[2],sys.argv[3].upper(),sys.argv[4].upper(),sys.argv[5].upper(),sys.argv[6])
  fechas=fechas.split(":")
  fechas[0] = int((datetime.strptime(fechas[0], '%d-%m-%Y') ).timestamp())
  fechas[1] = int((datetime.strptime(fechas[1], '%d-%m-%Y') ).timestamp())
else:
  archivo,dni,salida,tipo = (sys.argv[1],sys.argv[2],sys.argv[3].upper(),sys.argv[4].upper())

filtrarListadoDeCheques(archivo,dni,salida,tipo,estado,fechas)  