from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import mysql.connector
import pyautogui
import datetime
import bs4
import requests
import json

connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="contraloria"
    )

cursor = connection.cursor()

cursor.execute("select * from ubdistrito where estado='1'")
municipalidades = cursor.fetchall()
cursor.execute("select * from palabras_clave where estado='1' limit 1")
palabra_clave = cursor.fetchall()

for pc in palabra_clave:
    id_p_clave = pc[0]
    p_clave = pc[1]

for m in municipalidades:

    cursor.execute("select * from paginas where id=1")
    gob_pe = cursor.fetchall()
    for g in gob_pe:
        estado_gob = g[3]
    if(estado_gob == 1):
        driver = webdriver.Chrome() 
        driver.get("https://www.gob.pe/busquedas?term=Municipalidad Distrital de "+m[1])
        time.sleep(3)      
        #------------ ingresa al primer link de busqueda <a>
        etiqueta = driver.find_elements(By.XPATH, '//a')
        etiqueta[5].click()
        #----------- recupera la url direccionado actual
        actual_url = driver.current_url
        driver.get(actual_url)
        #----------- busqueda la palabra clave
        Text = driver.find_elements(By.XPATH, '//input')
        Text[0].send_keys(p_clave) 
        #------------ button de busqueda
        Button = driver.find_elements(By.XPATH, '//button')
        Button[0].click()
        #----------- recupera la url direccionado actual
        actual_url = driver.current_url
        driver.get(actual_url)
        #------------ button de Normas y Documentos Legales
        Button = driver.find_elements(By.XPATH, '//button')
        Button[5].click()    
        #----------- analizar lo que se encuentra para definir si hay documento o no 
        #----------- recupera la url direccionado actual
        actual_url = driver.current_url
        resultado = requests.get(actual_url)
        total_count = 0
        try:
            sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
            scripts = sopa.find_all('script')
            # Encuentra el script que contiene el JSON
            for script in scripts:
                if 'window.initialData' in script.text:
                    script_text = script.string
                    break
            # Extrae la parte JSON del script
            start = script_text.find('{')
            end = script_text.rfind('}') + 1
            json_text = script_text[start:end]
            # Parsear el JSON extraído
            data = json.loads(json_text)
            # Acceder al valor de total_count
            total_count = data['data']['attributes']['total_count']
            #print(f"Total Count: {total_count}")
            if(total_count > 0):
                estado = 1
            else:
                estado = 0    
        except:
            estado = 1
        #--------------- hora actual
        hora_actual = datetime.datetime.now()
        hora_formateada = hora_actual.strftime("%Y%m%d%H%M%S%f")    
        #--------------- captura la pantalla
        time.sleep(3)
        screenshot = pyautogui.screenshot()
        nombre_archivo = "C:/xampp/htdocs/front-contraloria/file_img/" + str(m[0]) + m[1] + hora_formateada + ".png"
        nombre_guardar = "/file_img/" + str(m[0]) + m[1] + hora_formateada + ".png"
        screenshot.save(nombre_archivo)
        #--------------- url actual 
        actual_url = driver.current_url
        cursor = connection.cursor()
        cursor.execute("insert into info_distrito (id_distrito, captura, fuente, estado, id_palabra_clave, total_contenido) values ('"+ str(m[0]) + "', '"+ str(nombre_guardar) + "', '"+ str(actual_url) + "', '" + str(estado) + "', '" + str(id_p_clave) + "', '" + str(total_count) + "')")
        connection.commit()        
        time.sleep(2)        
        driver.quit()

    cursor.execute("select * from paginas where id=2")
    google = cursor.fetchall()
    for g in google:
        estado_google = g[3]
    if(estado_google == 1):
        driver = webdriver.Chrome() 
        actual_url = "https://www.google.com.pe/search?q=Municipalidad Distrital de "+m[1]
        driver.get(actual_url)
        time.sleep(3)  
        etiqueta = driver.find_element(By.ID, 'result-stats')
        result_stats_text = etiqueta.get_attribute('outerHTML')
        total_contenido = result_stats_text.split(' resultados')[0].split('Cerca de ')[-1]   
        total = total_contenido.replace(',', '')
        tot = int(total)
        if(tot > 0):
            estado = 1
        else:
            estado = 0
        #--------------- hora actual
        hora_actual = datetime.datetime.now()
        hora_formateada = hora_actual.strftime("%Y%m%d%H%M%S%f")    
        #--------------- captura la pantalla
        time.sleep(3)
        screenshot = pyautogui.screenshot()
        nombre_archivo = "C:/xampp/htdocs/front-contraloria/file_img/" + str(m[0]) + m[1] + hora_formateada + ".png"
        nombre_guardar = "/file_img/" + str(m[0]) + m[1] + hora_formateada + ".png"
        screenshot.save(nombre_archivo)
        #--------------- url actual 
        actual_url = driver.current_url
        cursor = connection.cursor()    
        cursor.execute("insert into info_distrito (id_distrito, captura, fuente, estado, id_palabra_clave, total_contenido) values ('"+ str(m[0]) + "', '"+ str(nombre_guardar) + "', '"+ str(actual_url) + "', '" + str(estado) + "', '" + str(id_p_clave) + "', '" + str(total_contenido) + "')")
        connection.commit()
        cursor.close()
        time.sleep(2)        
        driver.quit()
        
    cursor.close()
    

connection.close()