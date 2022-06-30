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

def filtrarListadoDeCheques(archivo,dni,salida,tipo,estado,fecha="sin entrada"):
  rutaArchivo = open(archivo,"r")
  archivoCSV = list(csv.reader(rutaArchivo))
  chequesPorDni = filtrarChequesPorDni(archivoCSV,dni)
  chequesPorTipo = filtrarChequesPorTipo(chequesPorDni, tipo)
  chequesPorEstado = filtrarChequesPorEstado(chequesPorTipo,estado)
  if salida == "PANTALLA":
    print(archivoCSV[0])
    for linea in chequesPorEstado:
      print(linea)
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