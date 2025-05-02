# main.py
import requests

API_URL = "http://127.0.0.1:8000/api"
API_KEY = "b7b0db6ba73eed6aa29588a62b8f1fb07268b6ff"  # reemplaza con tu token real

HEADERS = {
    "Authorization": f"Token {API_KEY}"
}

def menu():
    while True:
        print("\n1. Ver información del hotel")
        print("2. Ver habitaciones disponibles")
        print("3. Crear una reserva")
        print("4. Ver lista de pasajeros")
        print("5. Hacer checkout")
        print("6. Consultar reserva por nombre y autobús")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            r = requests.get(f"{API_URL}/hotel/", headers=HEADERS)
            try:
                data = r.json()
                print(data)
            except Exception:
                print("❌ Error: el servidor no respondió con JSON.")
                print("Código de estado:", r.status_code)
                print("Respuesta cruda:", r.text)

        elif opcion == "2":
            r = requests.get(f"{API_URL}/room/enable/", headers=HEADERS)
            try:
                data = r.json()
                print(data)
            except Exception:
                print("❌ Error: el servidor no respondió con JSON.")
                print("Código de estado:", r.status_code)
                print("Respuesta cruda:", r.text)

        elif opcion == "3":
            name = input("Nombre del pasajero: ")
            room = input("ID de la habitación: ")
            bus = input("ID del autobús: ")
            check_in = input("Fecha inicio (YYYY-MM-DD): ")
            check_out = input("Fecha fin (YYYY-MM-DD): ")

            data = {
                "name": name,
                "room_id": room,
                "bus_id": bus,
                "check_in": check_in,
                "check_out": check_out,
            }

            r = requests.post(f"{API_URL}/create-reservation/", headers=HEADERS, json=data)
            try:
                data = r.json()
                print(data)
            except Exception:
                print("❌ Error: el servidor no respondió con JSON.")
                print("Código de estado:", r.status_code)
                print("Respuesta cruda:", r.text)

        elif opcion == "4":
            r = requests.get(f"{API_URL}/list-clients-info/", headers=HEADERS)
            try:
                data = r.json()
                print(data)
            except Exception:
                print("❌ Error: el servidor no respondió con JSON.")
                print("Código de estado:", r.status_code)
                print("Respuesta cruda:", r.text)

        elif opcion == "5":
            reservation_id = input("ID de la reserva a hacer checkout: ")
            r = requests.post(f"{API_URL}/checkout/", headers=HEADERS, json={"reservation_id": reservation_id})
            try:
                data = r.json()
                print(data)
            except Exception:
                print("❌ Error: el servidor no respondió con JSON.")
                print("Código de estado:", r.status_code)
                print("Respuesta cruda:", r.text)

        elif opcion == "6":
            name = input("Nombre del pasajero: ")
            bus = input("ID del autobús: ")
            r = requests.post(f"{API_URL}/reservation-client-bus/", headers=HEADERS, json={
                "name": name,
                "bus_id": bus
            })
            try:
                data = r.json()
                print(data)
            except Exception:
                print("❌ Error: el servidor no respondió con JSON.")
                print("Código de estado:", r.status_code)
                print("Respuesta cruda:", r.text)


        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
