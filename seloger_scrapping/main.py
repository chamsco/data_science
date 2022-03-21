# ============
# SeLoger.com Annuaires API:
# ============
# Packages:
# ===========

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd


# ===========
# WebService:
# ===========

def main():
    driver = Firefox()
    Annuaire = []
    token = 'https://www.selogerneuf.com/annuaire/promoteur-immobilier/'
    time.sleep(4)
    wait = WebDriverWait(driver, 10)

    # page = 0
    driver.get(token)

    #    Entreprise = []
    #    nb_projets = []
    #    Addresse = []
    #    Numero = []
    #    Lien = []
    #    Region = []

    def scrape_page(url, fichier):
        # Listes de variables vide

        global nb_elems
        global nb_entreprise
        global nb_entreprise
        global Entreprise
        global nb_projets
        global Addresse
        global Numero
        global Lien

        # headers = ['Entreprise ', 'Addresse ', 'Numero ', 'Lien']
        elements = driver.find_elements_by_class_name("agenciesSearchListItem")
        print(len(elements))
        print(str(elements))
        print("============================================")
        count = 1
        for x in driver.find_elements_by_class_name("agenciesSearchListItem"):
            print(count)
            # print(x.text)
            print("================================================")
            try:
                Entreprise = x.find_element_by_css_selector('.agencieItemTitle.titleSmall.titleBold').text
                print(Entreprise)
            except NoSuchElementException as ex:
                print(ex)
                Entreprise = 'None'
                pass
            try:
                nb_projets = x.find_element_by_css_selector('.agencieItemCount.summarySmall').text
                print(nb_projets)
            except NoSuchElementException as exc:
                print(exc)
                nb_projets = 'None'
                pass
            try:
                Addresse = x.find_element_by_css_selector('.agencieItemAddress.summaryMedium.summaryBold').text
                print(Addresse)
            except NoSuchElementException as exce:
                Addresse = 'none'
                print(exce)
                pass
            try:
                Numero = x.find_element_by_xpath("//div[@class='agencieItemButtons']/div[2]").get_attribute(
                    "data-agence-phone")
                print(Numero)
            except NoSuchElementException as excep:
                Numero = 'None'
                print(excep)
                pass
            try:
                Lien = x.find_element_by_xpath("//div[@class='agencieItemInfos']/h2/a").get_attribute("href")
                print(Lien)
            except NoSuchElementException as excep:
                Lien = 'None'
                Lien = 'None'
                print(excep)
                pass
            print("================================================")
            count += 1
            Annuaire.append(
                dict(Entreprise=Entreprise, Projets=nb_projets, Addresse=Addresse, Numero=Numero, Lien=Lien)
            )
            print(Annuaire)
            #  print(str(x + 1) + ': scrap fait')

        df_data = pd.DataFrame(Annuaire)
        df_data.to_csv(fichier)

        print("=========================")

    def find_captchaorpopup():
        try:
            popup = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div/div[2]/button[2]/span")
            if popup.is_displayed():
                print('popup trouvé')
                bypass = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[2]/button[2]/span")),
                )
                time.sleep(3)
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
                time.sleep(10)
                driver.switch_to.default_content()
        except NoSuchElementException:
            print('Pas de captcha')
            pass

    def scroll_to_element():
        try:
            element = driver.find_element_by_xpath('/html/body/div[4]/div/div/ul[2]/li[8]/a')
            print('suivant trouvé')
            coordinates = element.location_once_scrolled_into_view  # returns dict of X, Y coordinates
            driver.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))
        except TimeoutException:
            print('error scrolling down web element')
            scroll_to_element()

    for i in range(0, 65):
        time.sleep(5)
        find_captchaorpopup()
        while True:
            # next_page_btn_real = driver.find_element_by_xpath('/html/body/div[4]/div/div/ul[2]/li[9]/a')
            next_page_btn = driver.find_elements_by_xpath('//*[@id="wrapper"]/div/div/ul[2]/li[8]/a')
            if len(next_page_btn) < 1:
                print("No more pages left")
                break
            else:
                print('=========================')
                time.sleep(15)
                print("Scrap de : " + driver.current_url)
                time.sleep(5)
                scrape_page(driver.current_url, './csv/annuaire_test.csv')
                # scroll_to_element()
                print("suivant trouvé")
                suiv = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//li[@class='pagingItem pagingNext']/a "))
                )
                suiv.click()
                time.sleep(5)


main()
