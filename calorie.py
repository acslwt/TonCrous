import datetime
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def text_to_int(text):
    return float((text.split())[0])

def text_to_list(text):
    return text.split('\n')

def contient_alcool(liste_ingredients):
    for ingredient in liste_ingredients:
        ingredient = ingredient.split()
        for word in ingredient:
            if "vin"==word.lower():
                return True

def info_aliment(url,dessert):
    driver.get(url)

    type_valeur = ["Acides gras satures",
                    "Sucres simples",
                    "Kj",
                    "Kcal",
                    "Lipides",
                    "Glucides",
                    "Fibres",
                    "Proteines",
                    "Sel"]

    valeur_nutritionnelle = {}

    nom_produit = driver.find_element_by_xpath("//h1[@class ='product-name']")

    calories_mauvaise = driver.find_elements_by_xpath("//span[@class ='portion-gram text']")
    calories_bonne = driver.find_elements_by_xpath("//strong[@class ='portion-gram']")
    calories = calories_mauvaise+calories_bonne

    liste_ingredients = text_to_list((driver.find_element_by_xpath("//div[@class ='wysiwyg editor']")).text)

    # Mettre les valeurs nutrionnelles de l'aliment dans le dictionnaire
    for i in range(len(type_valeur)):
            valeur_nutritionnelle.update({type_valeur[i]:text_to_int(calories[i].text)})

    #Obtenir les allergenes
    liste_allergenes = []
    liste_allergenes_driver = driver.find_elements_by_xpath("//li[@class ='allergen']")
    for i in range(len(liste_allergenes_driver)):
        liste_allergenes.append(liste_allergenes_driver[i].text)

    if dessert==False:
        #L'aliment est-il végétarien ?
        est_vegetarien = False
        try:
            img_vegetarien = driver.find_elements_by_xpath("//img[@alt='Produit végétarien']")
            img_vegetarien = img_vegetarien[0].find_element_by_xpath('..')
            img_vegetarien = img_vegetarien.find_element_by_xpath('..')
            img_vegetarien = img_vegetarien.find_element_by_xpath('..')

            if img_vegetarien.get_attribute('class')=="cover":
                est_vegetarien = True
        except:
            None

        #L'aliment est-il halal ?
        est_halal = True
        if est_vegetarien==False and ("Poisson" not in liste_allergenes) and ("Mollusque" not in liste_allergenes) and ("Crustacé" not in liste_allergenes) or contient_alcool(liste_ingredients):
            est_halal = False
        
        return {nom_produit.text:{"valeur nutritionnelle":valeur_nutritionnelle,"ingredients":liste_ingredients,'allergenes':liste_allergenes,"vegetarien":est_vegetarien,"halal":est_halal}}
    
    #Retourne un dictionnaire avec clé le nom du plat est en valeur un dictionnaire contenant les ingredients et les valeurs nutrionnelles
    return {nom_produit.text:{"valeur nutritionnelle":valeur_nutritionnelle,"ingredients":liste_ingredients,'allergenes':liste_allergenes}}
    
driver = webdriver.Chrome('C:/Users/ayoub/Desktop/chromedriver.exe')
driver.maximize_window()

main_url = "https://infos-nutrition.crous-montpellier.fr"

link_plats_chaud = "https://infos-nutrition.crous-montpellier.fr/restaurant/1/type/2"
link_pizza_pates = "https://infos-nutrition.crous-montpellier.fr/restaurant/1/type/16"
link_entree = "https://infos-nutrition.crous-montpellier.fr/restaurant/1/type/10"
link_dessert = "https://infos-nutrition.crous-montpellier.fr/restaurant/1/type/4"
link_garniture = "https://infos-nutrition.crous-montpellier.fr/restaurant/1/type/17"

#JSON pour les plats chauds
driver.get(link_plats_chaud)

liste_plats_chauds_driver = driver.find_elements_by_xpath("//a[@class='photo-wrapper card-link block-link']")

liste_plats_chauds = []
for plat_chaud in liste_plats_chauds_driver:
    liste_plats_chauds.append(plat_chaud.get_attribute('href'))

liste_plats_chauds_valeurs_nutritionnelles = {}
for plat_chaud in liste_plats_chauds:
    liste_plats_chauds_valeurs_nutritionnelles.update(info_aliment(plat_chaud,False))

json_liste_plats_chauds_valeurs_nutritionnelles = json.dumps(liste_plats_chauds_valeurs_nutritionnelles, indent=4)
 
# Creer fichier json avec toutes les valeurs nutritionnelles de tous les plats chauds.
with open("liste_plats_chauds_valeurs_nutritionnelles.json", "w") as outfile:
    outfile.write(json_liste_plats_chauds_valeurs_nutritionnelles)

#JSON pour les pizzas et pates
driver.get(link_pizza_pates)

liste_pizza_pates_driver = driver.find_elements_by_xpath("//a[@class='photo-wrapper card-link block-link']")

liste_pizza_pates = []
for plat_chaud in liste_pizza_pates_driver:
    liste_pizza_pates.append(plat_chaud.get_attribute('href'))

liste_pizza_pates_valeurs_nutritionnelles = {}
for plat_chaud in liste_pizza_pates:
    liste_pizza_pates_valeurs_nutritionnelles.update(info_aliment(plat_chaud,False))

json_liste_pizza_pates_valeurs_nutritionnelles = json.dumps(liste_pizza_pates_valeurs_nutritionnelles, indent=4)
 
# Creer fichier json avec toutes les valeurs nutritionnelles de toutes les pizzas et pates.
with open("liste_pizza_pates_valeurs_nutritionnelles.json", "w") as outfile:
    outfile.write(json_liste_pizza_pates_valeurs_nutritionnelles)

#JSON pour les entrees
driver.get(link_entree)

liste_entree_driver = driver.find_elements_by_xpath("//a[@class='photo-wrapper card-link block-link']")

liste_entree = []
for plat_chaud in liste_entree_driver:
    liste_entree.append(plat_chaud.get_attribute('href'))

liste_entree_valeurs_nutritionnelles = {}
for plat_chaud in liste_entree:
    liste_entree_valeurs_nutritionnelles.update(info_aliment(plat_chaud,False))

json_liste_entree_valeurs_nutritionnelles = json.dumps(liste_entree_valeurs_nutritionnelles, indent=4)
 
# Creer fichier json avec toutes les valeurs nutritionnelles de toutes les entres.
with open("liste_entree_valeurs_nutritionnelles.json", "w") as outfile:
    outfile.write(json_liste_entree_valeurs_nutritionnelles)

#JSON pour les desserts
driver.get(link_dessert)

liste_dessert_driver = driver.find_elements_by_xpath("//a[@class='photo-wrapper card-link block-link']")

liste_dessert = []
for plat_chaud in liste_dessert_driver:
    liste_dessert.append(plat_chaud.get_attribute('href'))

liste_dessert_valeurs_nutritionnelles = {}
for plat_chaud in liste_dessert:
    liste_dessert_valeurs_nutritionnelles.update(info_aliment(plat_chaud,True))

json_liste_dessert_valeurs_nutritionnelles = json.dumps(liste_dessert_valeurs_nutritionnelles, indent=4)
 
# Creer fichier json avec toutes les valeurs nutritionnelles de toutes les entres.
with open("liste_dessert_valeurs_nutritionnelles.json", "w") as outfile:
    outfile.write(json_liste_dessert_valeurs_nutritionnelles)

#JSON pour les garnitures
driver.get(link_garniture)

liste_garniture_driver = driver.find_elements_by_xpath("//a[@class='photo-wrapper card-link block-link']")

liste_garniture = []
for plat_chaud in liste_garniture_driver:
    liste_garniture.append(plat_chaud.get_attribute('href'))

liste_garniture_valeurs_nutritionnelles = {}
for plat_chaud in liste_garniture:
    liste_garniture_valeurs_nutritionnelles.update(info_aliment(plat_chaud,False))

json_liste_garniture_valeurs_nutritionnelles = json.dumps(liste_garniture_valeurs_nutritionnelles, indent=4)
 
# Creer fichier json avec toutes les valeurs nutritionnelles de toutes les entres.
with open("liste_garniture_valeurs_nutritionnelles.json", "w") as outfile:
    outfile.write(json_liste_garniture_valeurs_nutritionnelles)
