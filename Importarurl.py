#Consumir datos de API
#Enmascarar datos
#Guardar en Bases de datos

import requests
import re
import mysql.connector
import getpass

#Enmascaramietno de datos Sensibles para cada dato sensible
def mask_ccn(cc_string, digits_to_keep=4, mask_char='*'): #contener el total de los caracteres en la cadena.
   cc_string_total = sum(map(str.isdigit, cc_string))  #mapear o recorrer la cadena para verificar si cada carácter es un dígito. 
   digits_to_mask = cc_string_total - digits_to_keep #diferencia
   masked_cc_string = re.sub('\d', mask_char, cc_string, digits_to_mask)#reemplaza por *
   return masked_cc_string

def mask_ccv(cc_string, digits_to_keep=0, mask_char='*'): 
   cc_string_total = sum(map(str.isdigit, cc_string))  
   digits_to_mask = cc_string_total - digits_to_keep 
   masked_cc_string = re.sub('\d', mask_char, cc_string, digits_to_mask)
   return masked_cc_string

def mask_nc(cc_string, digits_to_keep=3, mask_char='*'):
   cc_string_total = sum(map(str.isdigit, cc_string))   
   digits_to_mask = cc_string_total - digits_to_keep 
   masked_cc_string = re.sub('\d', mask_char, cc_string, digits_to_mask)
   return masked_cc_string

# Conexión a base de datos
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    #passwd= "Gu3rr0",
    passwd = getpass.getpass("Introduce el password: "),
    database="db_meli"
)
#GET BORRRA LA TABLA DATA_USER

urldelete = 'https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios'
datadelete = requests.get(urldelete)

if datadelete.status_code == 200:
    data = datadelete.json()
    for b in data:
        curborra = connection.cursor()
        eliminar="""delete from data_user"""
        curborra.execute(eliminar)
        connection.commit()
        curborra.close()

#GET A LA BASE DE DATOS
url = 'https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios'
data = requests.get(url)

if data.status_code == 200:
   data = data.json()
   for e in data:
      cursor = connection.cursor()
      val = (e.get('fec_alta'), e.get('user_name'),e.get('codigo_zip'), mask_ccn(e.get('credit_card_num')), mask_ccv(e.get('credit_card_ccv')), mask_nc(e.get('cuenta_numero')), e.get('direccion'), e.get('geo_latitud'), e.get('geo_longitud'), e.get('color_favorito'), e.get('foto_dni'), e.get('ip'), e.get('auto'), e.get('auto_modelo'), e.get('auto_tipo'), e.get('auto_color'), e.get('cantidad_compras_realizadas'), e.get('avatar'), e.get('fec_birthday'), e.get('id'))
      sql='''INSERT INTO data_user (fec_altadb,user_namedb,codigo_zipdb,credit_card_numdb,credit_card_ccvdb,cuenta_numerodb,direcciondb,geo_latituddb,geo_longituddb,color_favoritodb,foto_dnidb,ipdb,autodb,auto_modelodb,auto_tipodb,auto_colordb,cantidad_compras_realizadasdb,avatardb,fec_birthdaydb,iddb) values (%s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
      
      cursor.execute(sql,val)
      connection.commit()
      print ("Fecha de alta: ",e['fec_alta'])
      print ("Nombre de usuario: ",e['user_name'])
      print ("Código ZIP: ",e['codigo_zip'])
      #print ("Número tarjeta de crédito en claro: ", e['credit_card_num'])
      print ("Número tarjeta de crédito: ",mask_ccn(e['credit_card_num']))
      #print ("Número de CCV en claro: ", e['credit_card_ccv'])
      print ("Número de CCV: ",mask_ccv(e['credit_card_ccv']))
      #print ("Número de cuenta en claro: ", e['cuenta_numero'])
      print ("Número de cuenta: ",mask_nc(e['cuenta_numero']))
      print ("Dirección: ",e['direccion'])
      print ("Geo latitud: ",e['geo_latitud'])
      print ("Geo longitud: ",e['geo_longitud'])
      print ("Color favorito: ",e['color_favorito'])
      print ("Foto DNI: ",e['foto_dni'])
      print ("IP: ",e['ip'])
      print ("Automóvil: ",e['auto'])
      print ("Modelo auto: ",e['auto_modelo'])
      print ("Tipo de auto: ",e['auto_tipo'])
      print ("Color del auto: ",e['auto_color'])
      print ("Cantidad transacciones: ",e['cantidad_compras_realizadas'])
      print ("Avatar: ",e['avatar'])
      print ("Fecha de cumpleanos: ",e['fec_birthday'])
      print ("Id: ",e['id'])
      print (" ---- ")
      