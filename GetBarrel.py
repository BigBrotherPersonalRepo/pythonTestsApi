'''
=======================================================================================
Testovaci skript pro endpoint GET/barrels/{barrelId}
https://to-barrel-monitor.azurewebsites.net/barrels/{barrelId}
=======================================================================================
Skript nacita vstupni url ze souboru "config.json, vstupni data ze souboru "PostBarrelsData.json"
a pouziva custom knihovnu "common.py"
=> soubory musi byt ve stejnem repozitari jako script.
Pokud test projde, program vypise posledni odpoved preveditelnou na json do souboru log.txt
Pokud test neprojde, prislusna assert funkce ukonci program, vypise chybovou hlasku a 
posledni odpoved preveditelna na json bude vypsana do souboru "log.txt" 
=======================================================================================
Ucel testu: Zjistit, zda endpoint GET/barrels/{barrelId} vraci data spravne a ve spravnem formatu
=======================================================================================
Scenar:
=======
1) Nacteni testovacich dat ze souboru
2) Vytvoreni barrelu pomoci post requestu
3) Analyza odpovedi (status odpovedi, format dat, preveditelnost dat na Json)
4) Ulozeni barrelu do jsonu a test validity id
5) Volani GET pro konkretni barrel
6) Analyza odpovedi (status odpovedi, format dat, preveditelnost dat na Json)
7) Volani delete pro zamezeni hromadeni dat
8) Overeni statusu odpovedi
9) Test dotazu na konkretni barrel pomoci nevalidniho id
10) Overeni odpovedi
=======================================================================================
Ocekavany vysledek: skript projde 
Realny vysledek: Skript spadne na interni serverovou chybu v kroku 4
=======================================================================================
Komentar: GET/barrels/{barrelId} a delete nefunguje spravne
'''
#import knihoven
import requests
import common

#nacteni testovacich dat ze souboru (krok 1)
barrels = common.load_data("PostBarrelsData.json")
connects = common.load_data("config.json")
url = connects["urlBarrels"]
header = connects["header"]

#vytvoreni barrelu
#=================================================================================================================
#vytvoreni barrelu pomoci post requestu (krok 2)
barrelPostResponse = requests.post(url, json=barrels["inputsValid"][0], headers=header, timeout=3)

#test, zda je status odpovedi validni (krok 3)
common.is_format_valid(barrelPostResponse, 201)

#ulozeni barrelu do Jsonu a test validity ID (krok 4)
barrelJson = barrelPostResponse.json()
common.verify_id(barrelJson)

#test dotazu na konkretni barrel pomoci validniho id
#=================================================================================================================
#volani GET pro konkretni barrel (krok 5)
urlGetBarrel = url + f"/{barrelJson["id"]}"
barrelGetResponse = requests.get(urlGetBarrel, timeout=3)

#overeni odpovedi pro GET (krok 6)
common.is_format_valid(barrelGetResponse, 200)

#prevedeni dat na json a test, zda id odpovida formatu uuid a zda jsou parametry odpovedi shodne s vlozenymi daty (krok 6)
responseJson = barrelGetResponse.json()
common.is_barrel_valid(responseJson, barrelJson)

#delete pro zamezeni hromadeni dat (krok 7)
delete = requests.delete(urlGetBarrel) #***

#overeni zda delete zaznamu probehl spravne (krok 8)
common.verify_status(delete, 204) #***

#test dotazu na konkretni barrel pomoci nevalidniho id
#======================================================
#volani GET pro konkretni barrel (krok 9)
urlInvalidId = urlGetBarrel + "invalidAppendix"
barrelInvalidGetResponse = requests.get(urlInvalidId, timeout=3)

#overeni odpovedi pro GET (krok 10)
common.verify_status_negative(barrelInvalidGetResponse, 200) #***