# Librerías
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time, random
import pandas as pd

# Opciones de navegación
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('--profile-directory=Default')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# Get path of the parent directory
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Inicializamos el navegador
driver.set_window_position(0, 0)
driver.maximize_window()
time.sleep(1)

def search_region(region):
    # Abrimos la página
    driver.get('https://www.fotocasa.es/es/')

    # Cerramos el pop-up
    try:
        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            '//*[@id="App"]/div[2]/div/div/div/footer/div/button[2]')))\
            .click()
    except:
        pass

    # Buscamos la zona
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="App"]/div[1]/main/section/div[2]/div/div/div/div/div[2]/div[2]/form/div/div/div/div/div/input')))\
        .send_keys(region)

    # Seleccionamos la zona
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="App"]/div[1]/main/section/div[2]/div/div/div/div/div[2]/div[2]/form/button')))\
        .click()    
    
    # Cerramos el pop-up de alerta
    try:
        WebDriverWait(driver, 3)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            'button.sui-AtomButton.sui-AtomButton--primary.sui-AtomButton--flat.sui-AtomButton--center.sui-AtomButton--fullWidth')))\
            .click()
    except:
        pass

    # Seleccionamos las opciones de filtro
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                            '//*[@id="App"]/div[1]/div[2]/main/div/div[2]/div/div[2]/div/div/input')))\
        .click()
        
    # Filtramos por fecha de publicación
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                            '//*[@id="App"]/div[1]/div[2]/main/div/div[2]/div/div[2]/div/ul/li[2]')))\
        .click()    
    
    # Cerramos el pop-up de alerta
    try:
        WebDriverWait(driver, 3)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            'button.sui-AtomButton.sui-AtomButton--primary.sui-AtomButton--flat.sui-AtomButton--center.sui-AtomButton--fullWidth')))\
            .click()
    except:
        pass

def get_data(region, items):   
    # Inicializamos las listas
    rows = items
    df_data = {
        'Región': [region] * rows,
        'Precio': [None] * rows,
        'Habitaciones': [None] * rows,
        'Baños': [None] * rows,
        'Superfície': [None] * rows,
        'Dirección': [None] * rows,
    }
    i = 0
    page = 1
    while items > 0:
        time.sleep(random.uniform(1, 3))
        # Navegamos hacia el pie de página para que se carguen todas las viviendas
        max = driver.execute_script("return document.body.scrollHeight")
        y = 400
        while y < max:
                driver.execute_script("window.scrollTo(0, "+str(y)+")")
                y += 400  
                time.sleep(random.uniform(0.04, 0.6))

        # Obtenemos los enlaces de las viviendas
        links = driver.find_elements(By.CSS_SELECTOR, "article>a")
        hrefs = [link.get_attribute('href') for link in links]

        # Obtenemos los datos de las viviendas 
        for href in hrefs:
            # Si hemos llegado al límite de items, salimos del bucle
            if items == 0:
                break

            # Abrimos cada vivienda y extraemos los datos
            driver.execute_script("window.open('{}');".format(href))
            driver.switch_to.window(driver.window_handles[1])

            # Esperar un tiempo aleatorio para no ser detectado como bot
            time.sleep(random.randint(1, 2))

            # Navegamos hacia el pie de página para que se carguen todos los datos
            max = 2000
            y = 400
            while y < max:
                driver.execute_script("window.scrollTo(0, "+str(y)+")")
                y += 400  
                time.sleep(random.uniform(0.04, 0.5))

            # Extraemos los datos principales
            try:
                df_data['Precio'][i] = driver.find_element(By.CSS_SELECTOR, 'span.re-DetailHeader-price').text
            except:
                pass
            try:
                df_data['Habitaciones'][i] = driver.find_element(By.XPATH, '//*[@id="App"]/div[1]/main/div[3]/div[1]/div/section[1]/div/div[1]/div[3]/ul/li[1]/span[2]').text
            except:
                pass
            try:
                df_data['Baños'][i] = driver.find_element(By.XPATH, '//*[@id="App"]/div[1]/main/div[3]/div[1]/div/section[1]/div/div[1]/div[3]/ul/li[2]/span[2]').text
            except:
                pass
            try:
                df_data['Superfície'][i] = driver.find_element(By.XPATH, '//*[@id="App"]/div[1]/main/div[3]/div[1]/div/section[1]/div/div[1]/div[3]/ul/li[3]/span[2]').text
            except:
                pass
            try:
                df_data['Dirección'][i] = driver.find_element(By.XPATH, '//*[@id="App"]/div[1]/main/div[3]/div[1]/div/section[3]/div/div/div[1]/h2').text.replace(',', ' -')
            except:
                pass
            
            labels = driver.find_elements(By.CSS_SELECTOR, 'p.re-DetailFeaturesList-featureLabel')
            values = driver.find_elements(By.CSS_SELECTOR, 'p.re-DetailFeaturesList-featureValue')

            # Extraemos los datos secundarios
            for label in labels:
                if label.text not in df_data.keys():
                    df_data[label.text] = [None] * rows
                df_data[label.text][i] = values[labels.index(label)].text
            
            # Cerramos la pestaña
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Actualizamos el contador
            items -= 1
            i += 1
                 
        # Navegamos a la siguiente página
        if items > 0:
            page += 1
            
            try:
                # Navegamos a la siguiente página
                url = driver.current_url
                next_path = url[:url.find('/l')] + '/l/' + str(page)
                driver.get(next_path)
            except:
                break

    return df_data

def scrap(regions, items):
    # Creamos los dataframes
    df = pd.DataFrame()
    try:
        for region in regions:
            search_region(region)
            df_data = get_data(region, items)
            df = df.append(pd.DataFrame(df_data), ignore_index=True)
    except:
        pass
    return df

if __name__ == '__main__':
    # Regiones a buscar
    regions = ['Madrid', 'Barcelona', 'Valencia', 'Málaga', 'Sevilla', 'Zaragoza', 'Bilbao', 'Mallorca', 'Tenerife', 'Gran Canaria']
    # Profundidad de la búsqueda
    items = 50

    # Realizamos la búsqueda
    df = scrap(regions, items)

    # Guardamos los datos en un csv
    df.to_csv('data.csv', index=False)
    
    # Cerramos el navegador
    driver.quit()