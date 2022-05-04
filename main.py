import os
import requests
from bs4 import BeautifulSoup
import telebot
import WazeRouteCalculator
import logging



#Waze Connect

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

# Adresy 

from_address = 'Chalupkova, Čadca, Slovakia'
to_address = 'Vysokoškolákov 41, Žilina, Slovakia'
caza_cesta = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address)
zaca_cesta = WazeRouteCalculator.WazeRouteCalculator(to_address, from_address)

# Vytvorenie BOTA

my_secret = os.environ['API_KEY']
bot = telebot.TeleBot(my_secret)

# Úvodná správa

@bot.message_handler(commands=['start'])
def start(message):
  cid = message.chat.id
  subor="home"+str(cid)+".txt"
  text_file = open(subor, "w")
  text_file.close()
  bot.send_message(message.chat.id, "Ahoj, ja som Lukášov prvý BOT, ktorý chce pomôcť mapovať kolóny na trase Čadca - Žilina(alebo vlastnej zadanej)! Časom budem toho vedieť omnoho viac. Zatiaľ viem len príkazy /caza , /zaca , /AdresaDomov , /MojaAdresa . Po zmenení adresy pomocou príkazu /AdresaDomov je možné adresu overiť pomocou príkazu /MojaAdresa a taktiež CAZA počíta s novou adresou ")

# Premena funkcie na text



# Správa na trase CAZA

@bot.message_handler(commands=['caza'])
def caza(message):
  cid = message.chat.id
  subor="home"+str(cid)+".txt"
  text_file = open(subor, "r")
  home = text_file.read() 
  text_file.close()
  from_address = home
  to_address = 'Vysokoškolákov 41, Žilina, Slovakia'
  caza_cesta = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address)
  caza_minuty=caza_cesta.calc_route_info()
  caza_minuty_fl=float(caza_minuty[0])
  caza_minuty_i=round(caza_minuty_fl,1)
  caza_minuty_stri=str(caza_minuty_i)
  caza_text="Aktuálny čas na trase: "+caza_minuty_stri+" minút!"
  bot.send_message(message.chat.id,caza_text)


  # Správa na trase ZACA

@bot.message_handler(commands=['zaca'])
def zaca(message):
  cid = message.chat.id
  subor="home"+str(cid)+".txt"
  text_file = open(subor, "r")
  home = text_file.read() 
  text_file.close()
  from_address = home
  to_address = 'Vysokoškolákov 41, Žilina, Slovakia'
  zaca_cesta = WazeRouteCalculator.WazeRouteCalculator(to_address, from_address)
  zaca_minuty=zaca_cesta.calc_route_info()
  zaca_minuty_fl=float(zaca_minuty[0])
  zaca_minuty_i=round(zaca_minuty_fl,1)
  zaca_minuty_stri=str(zaca_minuty_i)
  zaca_text="Aktuálny čas na trase: "+zaca_minuty_stri+" minút!"
  bot.send_message(message.chat.id,zaca_text)
  
  # Zadanie novej adresy domov

@bot.message_handler(commands=['AdresaDomov'])
def handle_text(message):
    cid = message.chat.id
    ulicadomovtext = bot.send_message(cid, 'Zadajte ulicu aj s popisným číslom:')
    bot.register_next_step_handler(ulicadomovtext , zadaj_ulicu)

def zadaj_ulicu(message):
    ulica_domov= message.text
    print(ulica_domov)
  
    cid = message.chat.id
    subor="home"+str(cid)+".txt"
    text_file = open(subor, "w")
    text_file.write(ulica_domov+", ")
    text_file.close()
  
    mestodomovtext = bot.send_message(cid, 'Zadajte mesto:')
    bot.register_next_step_handler(mestodomovtext , zadaj_mesto)

def zadaj_mesto(message):
    cid = message.chat.id
    subor="home"+str(cid)+".txt"
    text_file = open(subor, "a")
  
    mesto_domov= message.text
    print(mesto_domov)
  
    
    text_file.write(mesto_domov+", ")
    text_file.close()
  
    krajinadomovtext = bot.send_message(cid, 'Zadajte krajinu po anglicky:')
    bot.register_next_step_handler(krajinadomovtext , zadaj_krajinu)

def zadaj_krajinu(message):
    krajina_domov= message.text
    print(krajina_domov)
  
    cid = message.chat.id
    subor="home"+str(cid)+".txt"
    text_file = open(subor, "a")
  
    text_file.write(krajina_domov)
    text_file.close()

  # Vypísanie adresy domov
  
@bot.message_handler(commands=['MojaAdresa'])
def mojaadresa(message):
  cid = message.chat.id
  subor="home"+str(cid)+".txt"
  text_file = open(subor, "r")
  home = text_file.read() 
  text_file.close()
  bot.send_message(message.chat.id,home)


  
# BOT počúva, čaká na príkazy

bot.infinity_polling()




#-------------------------------------------------------------------------
# dorobiť načitanie cieľovej adresy do work.txt
#-------------------------------------------------------------------------
# ak nie sú súbory prázdne, tak fungujú príkazy, ak sú plné vyrátať adresy
#-------------------------------------------------------------------------
# hosting na RPI
#-------------------------------------------------------------------------
# súbory Home a Work prerobiť na riadky 
#-------------------------------------------------------------------------
# HOME + CHATID nový súbor pre každého užívateľa
#----------------------------------------------------------------
