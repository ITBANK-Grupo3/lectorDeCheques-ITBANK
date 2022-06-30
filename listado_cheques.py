import sys
import csv

archivo,dni,salida,tipo = (sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])

if len(sys.argv) < 6:
  estado = "sin entrada"
else:
  estado = sys.argv[5]

def filtrarChequesPorDni(listado,dni):
  return(list(listado := filter(lambda lista:lista[-3] == dni, listado)))

def filtrarChequesPorTipo(listado, tipo):
  return(list(listado := filter(lambda lista:lista[-2] == tipo, listado)))

def filtrarChequesPorEstado(listado,estado):
  if estado == "sin entrada":
    return list(listado)    
  else:
    return(list(listado := filter(lambda lista:lista[-1] == estado, listado)))

def filtrarListadoDeCheques(archivo,dni,salida,tipo,estado="sin entrada",fecha="sin entrada"):
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


filtrarListadoDeCheques(archivo,dni,salida,tipo,estado)



