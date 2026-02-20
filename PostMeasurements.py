'''
====================================================================================================================================
Skript nacita vstupni url ze souboru "config.json, vstupni data ze souboru "PostBarrelsData.json"
a pouziva custom knihovnu "common.py"
=> soubory musi byt ve stejnem repozitari jako script.
Pokud test projde, program vypise posledni odpoved preveditelnou na json do souboru log.txt+
Pokud test neprojde, prislusna assert funkce ukonci program, vypise chybovou hlasku a 
posledni odpoved preveditelna na json bude vypsana do souboru "log.txt" 
====================================================================================================================================
Ucel testu: Zjistit, zda endpoint POST/measurements/ uklada data spravne a ve spravnem formatu
====================================================================================================================================
Scenar:
=======
1) Nacteni testovacich dat ze souboru
2) Vytvoreni barrelu pomoci post requestu
3) Overeni, zda vytvoreni barrelu probehlo v poradku
4) Ulozeni barrelu do Jsonu a test validity ID
5) Cyklus prochazejici sadu validnich dat
    5.a - Nastaveni validniho id barrelu
    5.b - Vytvoreni measurementu s validnimi daty
    5.c - Analyza odpovedi (status odpovedi, format dat, preveditelnost dat na Json)
    5.d - Prevedeni dat na Json a overeni spravnosti dat (validita id, validita dat measurementu)
6) Cyklus prochazejici sadu nevalidnich dat
    6.a - Pokus o vytvoreni measurementu s nevalidnimi daty
    6.b - Overeni statusu odpovedi
7) Delete drive vytvoreneho barrelu kvuli zamezeni hromadeni dat
8) Overeni zda delete probehl spravne
====================================================================================================================================
Ocekavany vysledek: skript projde
Realny vysledek: skript spadne v kroku 5.b na chybu 400. (bad request)
====================================================================================================================================
Komentar:
            1) Volani POST vypisuje chybovou hlasku "Barrel field is required." Je to velmi zvlastni, protoze 
               navazani measurement zaznamu na barrel je v samotnem measurement. Zkousel jsem zmenit vstupni data tak, aby 
               obsahovala i zaznam barrelu, zkousel jsem misto parametru json={objekt xy} parametr data={objekt xy}, 
               zkousel jsem vlozit barrel do parametru params={objekt xy} a mnoho dalsich moznych zpusobu vlozeni barrelu 
               spolecne se zaznamem measurement, nicmene mi neco asi uchazi, nebo je to chytak. Endpoint evidentne chce 
               nejakym zpusobem vlozit barrel spolecne se zaznamem measurement, nicmene se mi nepodarilo zjistit jak a proc. 
               V normalnim pripade bych se poradil s vyvojarem, ktery to vyvijel, ale protoze je to pohovor, neni ta moznost.
====================================================================================================================================
'''
#import knihoven
import requests
import common

#nacteni testovacich dat ze souboru (krok 1)
measurements = common.load_data("PostMeasurementsData.json")
barrels = common.load_data("PostBarrelsData.json")
connects = common.load_data("config.json")
urlBarrels = connects["urlBarrels"]
urlMeasurements = connects["urlMeasurements"]
header = connects["header"]

#vytvoreni barrelu pomoci post requestu (krok 2)
barrelResponse = requests.post(urlBarrels, json=barrels["inputsValid"][0], headers=header, timeout=3)

#overeni, zda vytvoreni barrelu probehlo v poradku (krok 3)
common.is_format_valid(barrelResponse, 201)

#ulozeni barrelu do Jsonu a test validity ID (krok 4)
barrelJson = barrelResponse.json()
common.verify_id(barrelJson)

#cyklus prochazejici sadu validnich dat (krok 5)
#===============================================
for measurement in measurements["inputsValid"]:

    #nastaveni validniho id barrelu (krok 5.a)
    measurement["barrelId"] = barrelJson["id"]

    #provolani api s validnimi daty (vytvoreni measurementu) (krok 5.b)
    measurementResponse = requests.post(urlMeasurements, json=measurement, headers=header, timeout=3) #***

    #test zda vytvoreni measurementu probehlo v poradku (krok 5.c)
    common.is_format_valid(measurementResponse, 201)

    #zde testujeme, zda id odpovida formatu uuid a zda jsou parametry odpovedi shodne s vlozenymi daty (krok 5.d)
    measurementJson = measurementResponse.json()
    common.is_measurement_valid(measurementJson, measurement)

#cyklus prochazejici sadu nevalidnich dat (krok 6)
#========================================
for measurement in measurements["inputsInvalid"]:

    #provolani api s nevalidnimi daty (krok 6.a)
    responseInvalid = requests.post(urlMeasurements, json=measurement, headers=header, timeout=3)

    #overeni, zda api odmitla nevalidni data (krok 6.b)
    common.verify_status_negative(responseInvalid, 201)

#delete pro zamezeni hromadeni dat (krok 7)
#======================================================
deleteBarrel = requests.delete(urlBarrels + f"/{barrelJson["id"]}")

#overeni zda delete zaznamu probehl spravne (krok 8)
common.verify_status(deleteBarrel, 204)