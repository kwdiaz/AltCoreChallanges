import requests

# Define la clave de la API y las URLs de los endpoints
api_key = "3841757512a14e20b637eabb62eb62f6"
measurement_url = "https://makers-challenge.altscore.ai/v1/s1/e2/resources/stars"
solution_url = "https://makers-challenge.altscore.ai/v1/s1/e2/solution"

# Configura los headers con la clave de la API
headers = {
    "API-KEY": api_key
}

# Inicializa la lista de datos de estrellas
all_stars = []
current_page = 1

# Navega por la nebulosa y obtiene los datos de las estrellas
while True:
    params = {
        "page": current_page,       # Página de resultados
        "sort-by": "id",            # Campo por el cual ordenar
        "sort-direction": "asc"     # Dirección de la ordenación
    }
    
    response = requests.get(measurement_url, headers=headers, params=params)
    
    # Verifica si la respuesta fue exitosa
    if response.status_code == 200:
        stars_data = response.json()
        if not stars_data:  # Si no hay más datos, termina el bucle
            break
        all_stars.extend(stars_data)  # Agrega los datos de estrellas a la lista
        current_page += 1  # Pasa a la siguiente página
    else:
        print(f"Error al obtener datos de la página {current_page}: {response.text}")
        break

# Calcula la resonancia promedio
total_resonance = sum(star['resonance'] for star in all_stars)
average_resonance = total_resonance / len(all_stars) if all_stars else 0
average_resonance_integer = round(average_resonance)  # Redondea la resonancia promedio

print("Resonancia promedio calculada:", average_resonance_integer)

# Envía la solución a la API
solution_payload = {
    "average_resonance": average_resonance_integer  # Asegúrate de enviar un entero
}

solution_response = requests.post(solution_url, headers=headers, json=solution_payload)

# Verifica si la solución fue enviada exitosamente
if solution_response.status_code == 200:
    result = solution_response.json()
    print("Solución enviada exitosamente:", result)
else:
    print("Error al enviar la solución:", solution_response.text)
