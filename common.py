'''
soubor pro sdilene funkce
'''
#import knihoven
import json
import uuid

#funkce pro overeni, zda je hodnota ve formatu uuid
#vraci bool
def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except (ValueError, TypeError, AttributeError):
        return False

#funkce pro nacteni connect dat
#prijima argument: nazev souboru typu string
#vraci data ve formatu json 
def load_data(file: str):
    f = open(file, encoding="utf8")
    data = json.load(f)
    f.close()
    return data

#funkce pro overeni satusu odpovedi s operatorem ==
#prijima argumenty: response = odpoved volani ve formatu json, satus_code = ocekavany status odpovedi typu int
#vystupem funkce je zapis json dat do logu v pripade ze data lze na json prevest
def verify_status(response: json, status_code: int):
    #test, zda je status odpovedi validni + pokus o zapis odpovedi do logu
    try:
        jsonStr = json.dumps(response.json(), indent=4)
        with open("log.txt", "a") as f:
            f.write(jsonStr)
        assert response.status_code == status_code, f"unexpected response => StatusCode: <{response.status_code}> || Message: {response.reason}"
    except:
        assert response.status_code == status_code, f"unexpected response => StatusCode: <{response.status_code}> || Message: {response.reason}"

#funkce pro overeni validity id
#prijima argument: object = objekt ve formatu json
#nema vystup
def verify_id(object: json):
    assert is_valid_uuid(object["id"]) is True, "id is in incorrect format"

#funkce pro overeni satusu odpovedi s operatorem !=
#prijima argumenty: response = odpoved volani ve formatu json, satus_code = ocekavany status odpovedi typu int
#vystupem funkce je zapis json dat do logu v pripade ze data lze na json prevest
def verify_status_negative(response: json, status_code: int):
    #test, zda je status odpovedi validni + pokus o zapis odpovedi do logu
    try:
        jsonStr = json.dumps(response.json(), indent=4)
        with open("log.txt", "a") as f:
            f.write(jsonStr)
        assert response.status_code != status_code, f"unexpected response => StatusCode: <{response.status_code}> || Message: {response.reason}"
    except:
        assert response.status_code != status_code, f"unexpected response => StatusCode: <{response.status_code}> || Message: {response.reason}"

#funkce pro overeni zda je format dat validni
#prijima argumenty: response = odpoved volani, satus_code = ocekavany status odpovedi
#nema vystup
def is_format_valid(response: json, status_code: int):
    #test, zda je status odpovedi validni + pokus o zapis odpovedi do logu
    try:
        jsonStr = json.dumps(response.json(), indent=4)
        with open("log.txt", "a") as f:
            f.write(jsonStr)
        assert response.status_code == status_code, f"unexpected response => StatusCode: <{response.status_code}> || Message: {response.reason}"
    except:
        assert response.status_code == status_code, f"unexpected response => StatusCode: <{response.status_code}> || Message: {response.reason}"

    #test, zda je odpoved v pozadovanem formatu
    assert response.headers["content-type"] == "application/json; charset=utf-8", "data has incorrect format"

    #test, zda je odpoved preveditelna na json
    assert response.json() is not None, "response is not convertable to Json"

#funkce pro overeni validity id a atributu barrelu
#prijima argumenty: response = odpoved volani, barrel = testovaci data barrelu ve formatu json
#nema vystup
def is_barrel_valid(response: json, barrel: json):
    #overeni validity id
    assert is_valid_uuid(response["id"]) is True, "id is in incorrect format"

    #overeni validity atributu podle testovacich dat
    assert response["qr"] == barrel["qr"], "qr has unexpected value"
    assert response["rfid"] == barrel["rfid"], "rfid has unexpected value"
    assert response["nfc"] == barrel["nfc"], "nfc has unexpected value"

#funkce pro overeni validity id a atributu measurementu
#prijima argumenty: response = odpoved volani, measurement = testovaci data measurementu ve formatu json
#nema vystup
def is_measurement_valid(response: json, measurement: json):
    #overeni validity id
    assert is_valid_uuid(response["id"]) is True, "id is in incorrect format"

    #overeni validity atributu podle testovacich dat
    assert response["barrelId"] == measurement["barrelId"], "barrelId has unexpected value"
    assert response["dirtLevel"] == measurement["dirtLevel"], "dirtLevel has unexpected value"
    assert response["weight"] == measurement["weight"], "weight has unexpected value"

    