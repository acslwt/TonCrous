from instagrapi import Client
import plat_du_jour
import config

def get_id_resto(link):
    switch = {
        'https://www.instagram.com/p/Co0ITjEjz5WPpLVJTDFl2Pek18Zurngj1bhcmU0/': 0,
        'https://www.instagram.com/p/Co0IOOPjOCYSFULUWfV-BytpQ0EWVXoj22Qipk0/': 1,
        'https://www.instagram.com/p/Co0ILEsDao1_KHrCfZNsn7iCnACAvoMxRoGpgg0/': 2,
        'https://www.instagram.com/p/Co0B1HCjVBCJCpsqvH5aka5CJqnNivXx8DE93I0/': 3,
        'https://www.instagram.com/p/Co0BxFaDiDt1fNisuc9pehBwflY8yhFnz3R4-80/': 4,
        'https://www.instagram.com/p/Co0BlKYDhg1Uoy0K7WsOsCH3hN-587C9LKkQvo0/': 5

    }
    return switch.get(link,-1) 

def get_link_resto(id_resto):
    link_resto = {
        0:'https://www.crous-montpellier.fr/restaurant/brasserie-triolet-2/',
        1:'https://www.crous-montpellier.fr/restaurant/brasserie-odontologie-2/',
        2:'https://www.crous-montpellier.fr/restaurant/brasserie-veyrassi/',
        3:'https://www.crous-montpellier.fr/restaurant/resto-u-vert-bois-2/',
        4:'https://www.crous-montpellier.fr/restaurant/resto-u-richter-2/',
        5:'https://www.crous-montpellier.fr/restaurant/brasserie-boutonnet-2/'
    }
    return link_resto.get(id_resto,-1) 
def send_message(cl,texte,id):
    return cl.direct_send(texte,[id],[])

def user_list_for_resto(cl,link):
    current_resto = cl.media_id(cl.media_pk_from_url(link))
    list_comments = cl.media_comments(current_resto)
    
    return [ (list_comments[i].dict())['user']['username'] for i in range(len(list_comments))]

cl = Client()
cl.login(config.username,config.password)

list_resto = [
        'https://www.instagram.com/p/Co0ITjEjz5WPpLVJTDFl2Pek18Zurngj1bhcmU0/',
        'https://www.instagram.com/p/Co0IOOPjOCYSFULUWfV-BytpQ0EWVXoj22Qipk0/',
        'https://www.instagram.com/p/Co0ILEsDao1_KHrCfZNsn7iCnACAvoMxRoGpgg0/',
        'https://www.instagram.com/p/Co0B1HCjVBCJCpsqvH5aka5CJqnNivXx8DE93I0/',
        'https://www.instagram.com/p/Co0BxFaDiDt1fNisuc9pehBwflY8yhFnz3R4-80/',
        'https://www.instagram.com/p/Co0BlKYDhg1Uoy0K7WsOsCH3hN-587C9LKkQvo0/'
        ]

# print(get_link_resto(0))

cl.direct_send("jul",[cl.user_info_by_username("asma.mem_")])

print("DEBUT ENVOI MESSAGE")
print("___________________")
for resto in list_resto:
    current_id_resto = get_id_resto(resto)
    user_list_comment = user_list_for_resto(cl,get_id_resto(resto))
    cl.direct_send("jul",user_list_comment)
print("___________________")
print('    FIN ENVOI')

menu = plat_du_jour.get_current_menu()

if(menu==-1):
    send_message(cl,"Le menu n'est pas disponible pour le moment, je te renvoi un message plus tard si il est de nouveau disponible.",user_id)
else:
    message = "Hey, voila le menu du jour \n"
    cle_menu = list(menu.keys())
    for i in range(len(cle_menu)):
        if(menu[cle_menu[i]]==['menu non communiqué'] or menu[cle_menu[i]]==[]):
            menu.pop(cle_menu[i])
    for cle,plats in menu.items():
        if(cle!=cle_menu[0]):
            message+='\n'
        message+=cle+" :"+'\n'
        for plat in plats:
            if(plat=="Ou"):
                message+=plat+'\n'
            else:
                message+="- "+plat+'\n'
    message=message[0:len(message)-1]+"\nRégale toi !"
    send_message(cl,message,user_id)