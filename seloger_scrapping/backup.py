# ============
# SeLoger.com Annuaires API:
# ============
# Packages:
# ===========

from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# ===========
# WebService:
# ===========

def main():
    driver = Firefox()
    Annuaire = []

    #    Entreprise = []
    #    nb_projets = []
    #    Addresse = []
    #    Numero = []
    #    Lien = []
    #    Region = []

    def scrape_page(url):
        # Listes de variables vide

        # headers = ['Entreprise ', 'Addresse ', 'Numero ', 'Lien']

        driver.get(url)
        elements = driver.find_elements_by_class_name("agenciesSearchListItem")
        global nb_elems
        global nb_entreprise
        global nb_entreprise
        global Entreprise
        global nb_projets
        global Addresse
        global Numero
        global Lien

        Entreprise = driver.find_elements_by_xpath("//div[@class='agencieItemInfos']/h2/a")
        nb_projets = driver.find_elements_by_xpath("//div[@class='agencieItemInfos']/p")
        Addresse = driver.find_elements_by_xpath("//div[@class='agencieItemInfos']/address")
        Numero = driver.find_elements_by_xpath("//div[@class='agencieItemButtons']/div[2]")
        Lien = driver.find_elements_by_xpath("//div[@class='agencieItemInfos']/h2/a")

        nb_elems = len(elements)
        nb_entreprise = len(Entreprise)

        for i in range(0, nb_entreprise - 1):
            temporary_data = {'Entreprise': Entreprise[i].text,
                              'Projets': nb_projets[i].text,
                              'Addresse': Addresse[i].text,
                              'Numero': Numero[i].get_attribute("data-agence-phone"),
                              'Lien': Lien[i].get_attribute("href"),
                              }
            Annuaire.append(temporary_data)
            print('scrap fait')

        df_data = pd.DataFrame(Annuaire)
        df_data.to_csv('annuaire_3.csv')

        print("=========================")

    def find_captchaorpopup():
        try:
            popup = driver.find_element_by_class_name("page_Annuaire didomi-popup-open")
            if popup.is_displayed():
                print('popup trouvé')
                bypass = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.ID, "didomi-notice-agree-button"))
                )
                time.sleep(6)
                bypass.click()
            else:
                time.sleep(4)
                pass
        except NoSuchElementException:
            print("Pas de popup")
            pass
        try:
            frame = driver.find_element_by_xpath('//iframe[contains(@src, "captcha")]')
            if frame.is_displayed():
                driver.switch_to.frame(frame)
                # captcha = driver.find_element_by_class_name("captcha__human")
                print('captcha trouvé')
                time.sleep(35)
                driver.switch_to.default_content()
        except NoSuchElementException:
            print('Pas de captcha')
            pass

    # token = 'https://www.selogerneuf.com/annuaire/promoteur-immobilier/'
    time.sleep(4)
    page = 0

    for i in range(0, 65):
        page = page + 1
        print(page)
        token = 'https://www.selogerneuf.com/annuaire/promoteur-immobilier/'
        token = token + str(page)
        driver.get(token)
        # find_CaptchaOrPopup()
        try:
            find_captchaorpopup()
            time.sleep(20)
            print("Scrap de : " + token)
            scrape_page(token)
            # print(page)
            time.sleep(15)
        except Exception as e:
            print(e)

        time.sleep(4)


main()
