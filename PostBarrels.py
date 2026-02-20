'''
==================================================================================================
Testovaci skript pro endpoint POST/barrels/
https://to-barrel-monitor.azurewebsites.net/barrels
==================================================================================================
Skript nacita vstupni url ze souboru "config.json, vstupni data ze souboru "PostBarrelsData.json"
a pouziva custom knihovnu "common.py"
=> soubory musi byt ve stejnem repozitari jako script.
Pokud test projde, program vypise posledni odpoved preveditelnou na json do souboru log.txt
Pokud test neprojde, prislusna assert funkce ukonci program a vypise chybovou hlasku. Posledni
odpoved preveditelna na json bude vypsana do souboru "log.txt"
==================================================================================================
Ucel testu: Zjistit, zda endpoint POST/barrels/ uklada data spravne a ve spravnem formatu
==================================================================================================
Scenar:
=======
1) Nacteni url a vstupnich dat ze souboru
2) Provedeni cyklu kde kazda iterace provede test pro jeden validni datovy objekt
    2.a - Provolani endpointu POST/barrels/
    2.b - Analyza odpovedi (status odpovedi, format dat, preveditelnost dat na Json)
    2.c - Prevedeni dat na Json a overeni spravnosti dat (validita id, validita dat barrelu)
    2.d - Delete vytvoreneho barrelu
    2.e - Overeni, zda delete probehl spravne (status odpovedi)
3) Provedeni cyklu, kde kazda iterace provede test pro jeden nevalidni datovy objekt
    3.a - Provolani endpointu POST/barrels/
    3.b - Pokud byl nevalidni barrel vytvoren, program ho smaze a overi status smazani 
          (zamezeni hromadeni dat)
    3.c - Overeni, zda nevalidni vytvoreni neproslo
==================================================================================================
Ocekavany vysledek: skript projde
Realny vysledek: 
                    1) Skript skonci v kroku 2.e u overeni, zda delete funkce vraci spravny 
                       status code, tj. 200. Namisto toho prijde 500 (internal server error)
                    2) V pripade zakomentovani delete postovani validnich dat projde, ale
                       nastane chyba pri postovani nevalidnich dat v kroku 3.c. 
                       Jedna z datovych struktur projde.
==================================================================================================
Komentar:
            1) Chyba serveru, delete nefunguje jak ma 
            2) Kdyz script postne barrel ktery ma vsechny atributy spravne a jeden navic, 
               projde to a barrel se ulozi, nicmene bez atributu navic. Podle me je to chyba,
               protoze vstupni data zkratka nejsou validni. Teoreticky je ale mozne ze je to
               nejaky feature, i kdyz podle me velmi malo pravdepodobne. Zalezi na nazoru 
               spravce systemu.

'''
#import knihoven
import requests
import common

#nacteni testovacich dat ze souboru (krok 1)
barrels = common.load_data("PostBarrelsData.json")
connects = common.load_data("config.json")
url = connects["urlBarrels"]
header = connects["header"]

#cyklus prochazejici sadu validnich dat (krok 2)
#====================================================================================================================================
for barrel in barrels["inputsValid"]:

    #provolani api s validnimi daty (vytvoreni barrelu) - (krok 2.a)
    response = requests.post(url, json=barrel, headers=header, timeout=3)

    #test, zda je status odpovedi validni (krok 2.b)
    common.is_format_valid(response, 201)

    #prevedeni dat na json a test, zda id odpovida formatu uuid a zda jsou parametry odpovedi shodne s vlozenymi daty (krok 2.c)
    responseJson = response.json()
    common.is_barrel_valid(responseJson, barrel)

    #delete pro zamezeni hromadeni dat (krok 2.d)
    delete = requests.delete(url + f"/{responseJson["id"]}") #***

    #overeni zda delete zaznamu probehl spravne (krok 2.e)
    common.verify_status(delete, 204) #***

#cyklus prochazejici sadu nevalidnich dat (krok 3)
#====================================================================================================================================
for barrel in barrels["inputsInvalid"]:

    #provolani api s nevalidnimi daty (krok 3.a)
    responseInvalid = requests.post(url, json=barrel, headers=header, timeout=3) #***

    #pokud k vytvoreni zaznamu s nevalidnimi hodnotami dojde, zde se zaznam pred spadnutim testu smaze aby se nehromadila data (krok 3.b)
    if (responseInvalid.status_code == 201):
        deleteInvalid = requests.delete(url + f"{responseInvalid.json()["id"]}") #***
        common.verify_status(deleteInvalid, 204)

    #overeni, zda api odmitla nevalidni data (krok 3.c)
    common.verify_status_negative(responseInvalid, 201) #***