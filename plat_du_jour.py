import datetime
import json
import time

from notify_run import Notify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def contain_or(sentence):
    list_word=sentence.split()
    if "Ou" in list_word:
        if len(list_word)==1:
            return 1
        else:
            return 2
    else:
        return 0

def get_current_menu():

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver.exe',options=options)
    driver.maximize_window()

    tous_menus = {}
    menu_current = []
    try:
        main_url = "https://www.crous-montpellier.fr/restaurant/cafet-space-2/"
        time.sleep(1)
        driver.get(main_url)

        date_du_jour = datetime.datetime.now()
        jour_semaine = date_du_jour.weekday()
        print("jul")
        time.sleep(1)
        menu = driver.find_element_by_xpath("//ul[@class='meal_foodies']")
        titre_plat = menu.find_elements_by_xpath("li")
        menu = (menu.text).split("\n")
        liste_menu = []
        for i in range(len(titre_plat)):
            liste_menu.append((titre_plat[i].text).split('\n')[0])
        for plat in menu:
            if plat in liste_menu:
                if len(menu_current)>0:
                    keys = list(tous_menus.keys())
                    tous_menus[keys[-1]] = menu_current
                    menu_current=[]
                tous_menus.update({plat:[]})
            else:
                if plat == "(plat végétarien)" or plat == "(plat unique)" or plat == "(plat unique végétarien )" or contain_or(plat)==2:
                    menu_current[-1] = menu_current[-1]+" "+plat
                else:
                    menu_current.append(plat)
        tous_menus[liste_menu[-1]]=menu_current
    except Exception as e:
        print(e)
        tous_menus = -1

    print(tous_menus)
    return tous_menus