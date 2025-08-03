import requests

api_key = "3841757512a14e20b637eabb62eb62f6"
measurement_url = "https://makers-challenge.altscore.ai/v1/s1/e1/resources/measurement"
solution_url = "https://makers-challenge.altscore.ai/v1/s1/e1/solution"

headers = {
    "API-KEY": api_key
}

try:
    response = requests.get(measurement_url, headers=headers)
    response.raise_for_status()
except requests.RequestException as e:
    print("Error al realizar la solicitud de medición:", e)
    exit()

if response.status_code == 200:
    data = response.json()
    distance = data.get('distance')
    time = data.get('time')

    print("Valor de distance recibido:", distance)
    print("Valor de time recibido:", time)

    if isinstance(distance, str) and "failed to measure" in distance:
        print("Error al medir la distancia:", distance)
    elif isinstance(time, str) and "failed to measure" in time:
        print("Error al medir el tiempo:", time)
    else:
        try:
            distance = float(distance) if distance is not None else 0
            time = float(time) if time is not None else 0

            if time > 0:
                velocidad_orbital = distance / time
                velocidad_orbital_redondeada = round(velocidad_orbital)
                solution = {
                    "velocity": velocidad_orbital_redondeada
                }

                try:
                    solution_response = requests.post(solution_url, json=solution, headers=headers)
                    solution_response.raise_for_status()
                except requests.RequestException as e:
                    print("Error al enviar la solución:", e)
                    exit()

                if solution_response.status_code == 200:
                    print("Solución enviada exitosamente:", solution_response.json())
                else:
                    print("Error al enviar la solución:", solution_response.status_code, solution_response.text)
            else:
                print("El tiempo debe ser mayor que cero.")
        except ValueError:
            print("Error: no se pudo convertir distance o time a un número válido.")
else:
    print("Error en la solicitud de medición:", response.status_code, response.text)
