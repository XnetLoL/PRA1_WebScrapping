# Librerías
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# Opciones de navegación
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

# Get path of the parent directory
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Inicializamos el navegador
driver.set_window_position(0, 0)
driver.maximize_window()
time.sleep(1)

# Abrimos la página
driver.get('https://www.fotocasa.es/es/')


# Cerramos el pop-up
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '//*[@id="App"]/div[2]/div/div/div/footer/div/button[2]')))\
    .click()

# Buscamos la zona
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '//*[@id="App"]/div[1]/main/section/div[2]/div/div/div/div/div[2]/div[2]/form/div/div/div/div/div/input')))\
    .send_keys('Barcelona')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '//*[@id="App"]/div[1]/main/section/div[2]/div/div/div/div/div[2]/div[2]/form/button')))\
    .click()
    
# TODO: Cambiar filtro de búsqueda por las últimas viviendas publicadas

time.sleep(2)

# Navegamos hacia el pie de página para que se carguen todas las viviendas
max = height = driver.execute_script("return document.body.scrollHeight")
y = 400
while y < max:
        driver.execute_script("window.scrollTo(0, "+str(y)+")")
        y += 400  
        time.sleep(0.05)

# Obtenemos los enlaces de las viviendas
links = driver.find_elements(By.CSS_SELECTOR, "article>a")
hrefs = [link.get_attribute('href') for link in links]

# Abrimos cada vivienda y extraemos los datos
driver.execute_script("window.open('{}');".format(hrefs[0]))
driver.switch_to.window(driver.window_handles[1])

#time.sleep(5)
driver.quit()