'''
Testovaci skript pro endpoint GET/measurements/
https://to-barrel-monitor.azurewebsites.net/measurements
=======================================================================================
Skript pouziva custom knihovnu "common.py" 
=> knihovna musi byt ve stejnem repozitari jako script.
Pokud test projde, program ulozi odpoved endpointu do souboru "log.txt"
Pokud test neprojde, prislusna assert funkce ukonci program, vypise chybovou hlasku a 
posledni odpoved volani endpointu ktera lze prevest na json vypise do souboru "log.txt" 
=======================================================================================
Ucel testu: Zjistit, zda endpoint GET/measurements/ vraci data spravne a ve 
spravnem formatu
=======================================================================================
Scenar:
=======
1) Nacteni url ze souboru
2) Provolani endpointu GET/measurements/ (dotaz na vraceni dat)
3) Analyza odpovedi (status odpovedi, format dat, preveditelnost dat na Json)
=======================================================================================
Ocekavany vysledek: skript projde 
Realny vysledek: skript projde
=======================================================================================
Komentar: Nebyla zaznamenana chyba, po skonceni program vypise data GET/measurements.
          Data jsou prazdny seznam mereni.
'''
#import knihoven
import requests
import common

#nacteni testovacich dat (krok 1)
connects = common.load_data("config.json")
url = connects["urlMeasurements"]

#provolani api (krok 2)
response = requests.get(url, timeout=3)

#overeni zda je format dat validni (krok 3)
common.is_format_valid(response, 200)