import requests
commands = {
    "Geraetetyp": "FF00",
    "Geraetenummer": "0600",
    "SW-Version": "0100",
    "Inbetriebnahmedatum": "0E00",
    "Betriebsstundenzaehler": "2500",
    "Kundendienst-Serviceadresse": "5800",
    "Wunschwasserhaerte": "5100",
    "Salzvorrat": "5600",
    "Salzreichweite": "5700",
    "Salzreichweite": "5700",
    "Gesamtwassermenge": "2800",
    "Weichwassermenge": "2900",
    "Tagesstatistik": "FB00",
    "Wochenstatistik": "FC00",
    "Monatsstatistik": "FD00",
    "Jahresstatistik": "FE00",
}
api_url = "http://user:pass@192.168.1.11/api/rest/"

for index, item in enumerate(commands):
    print(item)
    url = api_url + commands[item]
    response = requests.get(url)
    res =  response.json()
    print("Scanning "+ item)
    print(res["data"])
    if item == "Salzvorrat":
        mass = res["data"][2:4]+res["data"][0:2]
        print(mass)
        mass_int = int(mass, 16)
        print("Restmenge:",str(mass_int/1000)+" kg")
        days = res["data"][6:8]+res["data"][4:6]
        print(days)
        days_int = int(days, 16)
        print("Resttage:",str(days_int))
    else:
        print(res)
