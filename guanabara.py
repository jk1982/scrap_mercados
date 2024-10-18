import os
import re
import time
import requests
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
import glob
from pdf2image import convert_from_path, pdfinfo_from_path
#from PIL import Image
import matplotlib.pyplot as plt
from transformers import pipeline

class Guanabara:
  def __init__(self, driver) -> None:
    self.driver = driver
    self.wait = WebDriverWait(driver, 20)
    self.pipe = pipeline("image-to-text", model="microsoft/trocr-base-handwritten")

  def scrap(self):
    print("Processando mercado Guanabara...")
    self.driver.get("https://www.supermercadosguanabara.com.br/encarte")
    time.sleep(3)
    assert "encarte" in self.driver.title.lower()
    
    self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Baixar encarte')]"))).click()
    time.sleep(3)
    self.__convert_pdf_to_img()
    list_of_files = glob.glob('./temp/*.jpg')

    for image_path in list_of_files:
      text = self.pipe(image_path)[0]["generated_text"]
      print(text)
      pass

  def __convert_pdf_to_img(self):
    path = os.getenv("download_path")
    list_of_files = glob.glob(f'{path}/*guanabara*.pdf')
    
    latest_file = max(list_of_files, key=os.path.getmtime)
    pdf_file = os.path.abspath(latest_file)
    info = pdfinfo_from_path(pdf_file, userpw=None, poppler_path=None)
    maxPages = info["Pages"]
    for page in range(1, maxPages+1, 10):
      convert_from_path(pdf_file, dpi=200, first_page=page, last_page = min(page+10-1, maxPages), output_folder=os.path.abspath("./temp"), grayscale=True, fmt="jpg")