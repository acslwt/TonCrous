import datetime
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def text_to_list(text):
    return text.split('\n')

def ingredients_aliment(url):
    driver.get(url)

    liste_ingredients = text_to_list((driver.find_element_by_xpath("//div[@class ='wysiwyg editor']")).text)

    nom_produit = driver.find_element_by_xpath("//h1[@class ='product-name']")
    
    return {nom_produit.text:liste_ingredients}
    

driver = webdriver.Chrome('C:/Users/ayoub/Desktop/chromedriver.exe')
driver.maximize_window()

main_url = "https://infos-nutrition.crous-montpellier.fr"
link_plats_chaud = "https://infos-nutrition.crous-montpellier.fr/restaurant/1/type/2"

driver.get(link_plats_chaud)

liste_plats_chauds_driver = driver.find_elements_by_xpath("//a[@class='photo-wrapper card-link block-link']")

liste_plats_chauds = []
for plat_chaud in liste_plats_chauds_driver:
    liste_plats_chauds.append(plat_chaud.get_attribute('href'))

liste_plats_chauds_ingredients = {}
for plat_chaud in liste_plats_chauds:
    liste_plats_chauds_ingredients.update(ingredients_aliment(plat_chaud))

json_liste_plats_chauds_ingredients = json.dumps(liste_plats_chauds_ingredients, indent=4)
 
# Creer fichier json avec toutes les valeurs nutritionnelles de tous les plats chauds.
with open("liste_plats_chauds_ingredients.json", "w") as outfile:
    outfile.write(json_liste_plats_chauds_ingredients)