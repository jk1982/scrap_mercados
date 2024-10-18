import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MultiMarket:
  def __init__(self, driver) -> None:
    self.driver = driver
    self.wait = WebDriverWait(driver, 20)

    database_path = os.getenv("database_path")
    self.client = chromadb.PersistentClient(path=database_path)
    
  def __scrap(self, url):
    self.driver.get(url)
    time.sleep(5)
    assert "promo" in self.driver.title.lower()

    self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'fechar_aviso')]"))).click()
    time.sleep(1)
    
    units = ["kg", "ml", "un"]

    current_page = 1
    while True:
      print(f"Processando a página {current_page}")
      products = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'box-produto')]")
      for prod in products:
        name = prod.find_element(By.XPATH, ".//div[@class='caption']//a//span").text
        price = f"{prod.find_element(By.XPATH, ".//span[@class='inteiro']").text}{prod.find_element(By.XPATH, ".//span[@class='decimal']").text}"
        #new_name = next((name.lower().replace(unit, "").strip() for unit in units if unit in name.lower()), name)
        unit = next((unit for unit in units if unit in name.lower()), None)
        print(f"Nome: {name} - Preço: {price} - Unidade: {unit}")
        break

      try:
        self.driver.find_element(By.LINK_TEXT, "Próxima").click()
      except:
        break
      current_page += 1
      time.sleep(3)

  def scrap(self):
    print("Processando mercado Multi Market Mindelense...")
    self.__scrap("https://lojavirtual.redemultimarket.com.br/mindelense/promocoes/")

    print("Processando mercado Multi Market Cachoeiras...")
    self.__scrap("https://lojavirtual.redemultimarket.com.br/multimarket-cachoeiras/promocoes/")