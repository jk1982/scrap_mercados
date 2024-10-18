import os
from fake_headers import Headers
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dotenv import load_dotenv

load_dotenv()

from multimarket import MultiMarket
from mundial import Mundial
from guanabara import Guanabara

download_dir = os.getenv("download_path")
log_path = "logs/log.txt"

browser_options = FirefoxOptions()
ua = Headers().generate()      #fake user agent
browser_options.add_argument('--headless')
browser_options.add_argument('--ignore-certificate-errors')
browser_options.add_argument('--disable-extensions')
browser_options.add_argument('--incognito')
browser_options.add_argument('--disable-gpu')
browser_options.add_argument('--log-level=3')
browser_options.add_argument(f'user-agent={ua}')
browser_options.add_argument('--disable-notifications')
browser_options.add_argument('--disable-popup-blocking')
browser_options.page_load_strategy = 'none'

firefox_profile = webdriver.FirefoxProfile()
# Definir diretório de download padrão
firefox_profile.set_preference("browser.download.folderList", 2)  # Usar diretório definido
firefox_profile.set_preference("browser.download.dir", os.path.abspath(download_dir))

# Configurar para não exibir a janela de download
firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
firefox_profile.set_preference("pdfjs.disabled", True)  # Desabilitar o visualizador de PDF embutido no Firefox
# firefox_profile.set_preference('permissions.default.stylesheet', 2)
# firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
firefox_profile.set_preference("http.response.timeout", 10)
firefox_profile.set_preference("dom.max_script_run_time", 10)

browser_options.profile = firefox_profile
driver = webdriver.Firefox(options=browser_options)
webdriver.FirefoxService(log_output=log_path, service_args=['--log', 'debug'])

database_path = os.getenv("database_path")
if not os.path.exists(database_path):
  from pathlib import Path
  filename = Path(database_path)
  filename.touch(exist_ok=True)

if __name__ == '__main__':
  try:
    #MultiMarket(driver=driver).scrap()
    #Mundial(driver=driver).scrap()
    Guanabara(driver=driver).scrap()
  finally:
     driver.quit()