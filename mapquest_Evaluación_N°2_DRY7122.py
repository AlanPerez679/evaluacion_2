import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
clave = "sVRfEISRTSZw5q4N9iCFiQw9dfZppubO"

def traducir_texto(texto, idioma_destino):
    traduccion = ""
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={idioma_destino}&dt=t&q={urllib.parse.quote(texto)}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        traduccion = data[0][0][0]
    return traduccion

while True:
    origen = input("Ubicación de partida: ")
    if origen == "salir" or origen == "s":
        break
    destino = input("Destino: ")
    if destino == "salir" or destino == "s":
        break

    url = main_api + urllib.parse.urlencode({"key": clave, "from": origen, "to": destino})
    print("URL: " + url)

    json_data = requests.get(url).json()
    json_estado = json_data["info"]["statuscode"]

    if json_estado == 0:
        print("Estado de la API: " + str(json_estado) + " = Llamada de ruta exitosa.\n")
        print("=============================================")
        print("Direcciones desde " + origen + " hasta " + destino)
        print("Duración del viaje: " + json_data["route"]["formattedTime"])
        print("Kilometros:      " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
        print("=============================================")

        for each in json_data["route"]["legs"][0]["maneuvers"]:
            maniobra = each["narrative"]
            maniobra_traducida = traducir_texto(maniobra, "es")
            distancia_km = "{:.2f}".format(each["distance"] * 1.61)
            print(maniobra_traducida + " (" + str(distancia_km) + " km)")

        print("=============================================\n")