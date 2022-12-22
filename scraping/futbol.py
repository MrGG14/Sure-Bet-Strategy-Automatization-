# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 17:47:15 2022

@author: Nico
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
import pandas as pd

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

driver = webdriver.Chrome(dname+'\chromedriver.exe')

url = 'https://www.casasdeapuestas.com/cuotas/futbol/'
driver.get(url)

try:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "age-yes")))
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div/div[6]/div[3]/div/div/button[1]').click()
except:
    pass


df = pd.DataFrame({'local': [], 'visitante': [], 'cuota_local': [], 'cuota_empate': [], 'cuota_visitante': [], 'euros_min': []})
partidos = driver.find_elements(By.CLASS_NAME,"pC")


for partido in partidos:
    equipos = partido.find_elements(By.CLASS_NAME, 'pNb')[0].text.split('\n')[:2]
    local = equipos[0]
    visitante = equipos[1] 

    cuotas = partido.find_elements(By.CLASS_NAME, 'odd')
    cuota_local = cuotas[0].text
    cuota_empate = cuotas[1].text
    cuota_visitante = cuotas[2].text
  
    euros_min = (1/float(cuota_local)) + (1/float(cuota_empate)) + (1/float(cuota_visitante))
    new_row = {'local': local, 'visitante': visitante, 'cuota_local': cuota_local, 'cuota_empate': cuota_empate, 'cuota_visitante': cuota_visitante, 'euros_min': euros_min}
    df = df.append(new_row,ignore_index=True)
        
print(df[df['euros_min']<1])

