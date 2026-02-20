'''
=======================================================================================
Testovaci skript pro endpoint GET/barrels/
https://to-barrel-monitor.azurewebsites.net/barrels
=======================================================================================
Skript pouziva custom knihovnu "common.py" 
=> knihovna musi byt ve stejnem repozitari jako script.
Pokud test projde, program ulozi odpoved endpointu do souboru "log.txt"
Pokud test neprojde, prislusna assert funkce ukonci program, vypise chybovou hlasku a 
posledni odpoved volani endpointu ktera lze prevest na json vypise do souboru "log.txt" 
=======================================================================================
Ucel testu: Zjistit, zda endpoint GET/barrels/ vraci data spravne a ve spravnem formatu
=======================================================================================
Scenar:
=======
1) Nacteni url ze souboru
2) Provolani endpointu GET/barrels/ (dotaz na vraceni dat)
3) Analyza odpovedi (status odpovedi, format dat, preveditelnost dat na Json)
=======================================================================================
Ocekavany vysledek: skript projde 
Realny vysledek: skript projde
=======================================================================================
Komentar: Nebyla zaznamenana chyba, po skonceni program vypise data GET/barrels
          Data jsou seznam barrelu
'''
#import knihoven
import requests
import common
import datetime

#nacteni testovacich dat (krok 1)
connects = common.load_data("config.json")
url = connects["urlBarrels"]

#provolani api (krok 2)
start = datetime.datetime.now()
response = requests.get(url) #timeout=3)
end = datetime.datetime.now()
duration = end - start
print(duration)

#overeni zda je format dat validni (krok 3)
common.is_format_valid(response, 200)
