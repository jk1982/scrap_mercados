import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Mundial:
  def __init__(self, driver) -> None:
    self.driver = driver
    self.wait = WebDriverWait(driver, 20)

  def scrap(self):
    print("Processando mercado Mundial...")
    self.driver.get("https://www.supermercadosmundial.com.br/ofertas")
    time.sleep(3)
    assert "ofertas" in self.driver.title.lower()

    reject_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-cookiefirst-action="reject"]')))
    reject_button.click()
    time.sleep(2)

    while True:
      elem = EC.element_to_be_clickable((By.ID, "bnt-carregar"))
      self.wait.until(elem).click()
      time.sleep(1)

      button_style = self.driver.find_element(By.ID, "bnt-carregar").get_attribute("style")
      if "display: none;" in button_style:
        break
    
    products = self.driver.find_elements(By.XPATH, "//div[@class='container']//div[contains(@class, 'product')]")

    for prod in products:
      name = prod.find_element(By.XPATH, ".//span[@class='name-product']").text
      price = prod.find_elements(By.XPATH, ".//span[@id='porStylePrice']//div[@id='stylePrice']//span")[0].text
      unit = prod.find_elements(By.XPATH, ".//span[@id='porStylePrice']//div[@id='stylePrice']//span")[1].text
      print(f"Nome: {name} - Preço: {price} - Unidade: {unit}")
      break