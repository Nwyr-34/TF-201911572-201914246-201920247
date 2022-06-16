# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BAfRabgAwmKHj_ZtnPaki5Oeyfv_Ikh9
"""

import psycopg2
conexion = psycopg2.connect(
    host="bwmc2spjnkl3asahsdwf-postgresql.services.clever-cloud.com", 
    database="bwmc2spjnkl3asahsdwf", 
    user="ui9vqx1cbdowhfoap3dq", 
    password="9wNAizIxMMQtBryr1tOZ")
cur = conexion.cursor()
#cur.execute("SELECT * FROM \"hh_2po_4pgr\" WHERE id=1")

horas=[0.5833333,1,6.8,12.6,18.4,24.2,30,26,22,18,14,10,9.25,8.5,7.75,7,12.75,18.5,24.25,30,25.16666667,20.333333,15.5,10.6666667]

def getTiempoTraficoXHora(hora, origen, destino):
  query="SELECT * FROM \"hh_2po_4pgr\" WHERE source="+str(origen)+" and target="+str(destino)
  cur.execute(query)
  trafico=cur.fetchall()[0][12]*horas[hora]
  return trafico

def convertDecimalToHourMinute(time):
  hours = int(time)
  minutes = int((time*60) % 60)
  seconds = int((time*3600) % 60)
  pocoTiempo= 0 #si el tiempo es menos de 1 segundo 
  if (hours==0) and (minutes==0) and (seconds ==0):
    pocoTiempo=(time*3600) % 60
 
  timeFormat=[hours,minutes,seconds,pocoTiempo]
  return timeFormat

def getDistancia(origen, destino):
  query="SELECT * FROM \"hh_2po_4pgr\" WHERE source="+str(origen)+" and target="+str(destino)
  cur.execute(query)
  kms=cur.fetchall()[0][11]
  return kms

def existeRuta(origen, destino):
   query="SELECT * FROM \"hh_2po_4pgr\" WHERE source="+str(origen)+" and target="+str(destino)
   cur.execute(query)
   result=cur.fetchall()
  
   if result == []:
     query="SELECT * FROM \"hh_2po_4pgr\" WHERE source="+str(destino)+" and target="+str(origen)
     cur.execute(query)
     result2=cur.fetchall()
     if result2 == []:
       return False
     else:
       if result2[0][13]== 1000000:
        return False
       else:
          return "Reverse"
   else: 
     return True


# de 6 a 51668

arregloPath=[6]

def ArrayPath(origen, destino):
  query="select target from \"hh_2po_4pgr\" where source="+str(origen)
  cur.execute(query)
  destinos=cur.fetchall()
  if len(destinos) ==1:
    menorId=destinos[0][0]
    arregloPath.append(menorId)
    print(menorId)
  

  if len(destinos)>1:
    i=1
    menorId=destinos[0][0]
    while i< len(destinos):
      if int(getTiempoTraficoXHora(1,origen,destinos[i][0])) < int(getTiempoTraficoXHora(1,origen,menorId)):
        menorId=destinos[i][0]
      i=i+1
    arregloPath.append(menorId)
    print(menorId)
  #print(menorId)

  if arregloPath[len(arregloPath)-1]!=destino and len(destinos)>0:
    ArrayPath(menorId,destino)
  else:
    return print(arregloPath)


print(ArrayPath(6,7))
#print(cur.fetchall())

conexion.close()