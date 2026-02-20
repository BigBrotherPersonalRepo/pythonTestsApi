'''

'''
#import knihoven
import requests
import common

#nacteni testovacich dat ze souboru
measurements = common.load_data("PostMeasurementsData.json")
barrels = common.load_data("PostBarrelsData.json")
connects = common.load_data("config.json")

#nacteni testovacich dat ze souboru
urlBarrels = connects["urlBarrels"]
urlMeasurements = connects["urlMeasurements"]
header = connects["header"]

#vytvoreni barrelu
#=============================================================
#vytvoreni barrelu pomoci post requestu
barrelPostResponse = requests.post(urlBarrels, json=barrels["inputsValid"][0], headers=header, timeout=3)

#overeni, zda vytvoreni barrelu probehlo v poradku
common.is_format_valid(barrelPostResponse, 201)

#ulozeni barrelu do Jsonu a test validity ID
barrelJson = barrelPostResponse.json()
common.verify_id(barrelJson)

#vytvoreni measurementu
#============================================================
#vytvoreni promenne pro measurement
measurement = measurements["inputsValid"][0]

#nastaveni validniho id barrelu
measurement["barrelId"] = barrelJson["id"]

#provolani api s validnimi daty (vytvoreni measurementu)
measurementPostResponse = requests.post(urlMeasurements, json=measurement, headers=header, timeout=3) #***

#test zda vytvoreni measurementu probehlo v poradku
common.is_format_valid(measurementPostResponse, 201)

#ulozeni measurementu do Jsonu a test validity id
measurementJson = measurementPostResponse.json()
common.verify_id(measurementJson)

#test volani konkretniho measurementu pomoci validniho id
#============================================================
#sestaveni url pro get konkretniho measurementu
urlGetMeasurement = urlMeasurements + f"/{measurementJson["id"]}"

#volani GET pro konkretni measurement
measurementGetResponse = requests.get(urlGetMeasurement, timeout=3)

#overeni formatu odpovedi pro GET
common.is_format_valid(measurementGetResponse, 201)

#zde testujeme, zda id odpovida formatu uuid a zda jsou parametry odpovedi shodne s vlozenymi daty
responseJson = measurementGetResponse.json()
common.is_measurement_valid(responseJson, measurementJson)
#=============================================================

#delete pro zamezeni hromadeni dat
deleteBarrel = requests.delete(urlBarrels + f"/{barrelJson["id"]}")

#overeni zda delete zaznamu probehl spravne
common.verify_status(deleteBarrel, 204)

#test dotazu na konkretni measurement pomoci nevalidniho id
#=============================================================
#sestaveni url pro GET
urlInvalidId = urlGetMeasurement + "invalidAppendix"

#volani GET pro konkretni barrel
measurementInvalidGetResponse = requests.get(urlInvalidId, timeout=3)

#overeni odpovedi pro GET
common.verify_status_negative(measurementInvalidGetResponse, 200)