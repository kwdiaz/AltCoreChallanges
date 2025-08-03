import requests
import base64
from urllib.parse import quote

# Paso 1: Obtener personajes de la API de Star Wars
def obtener_personajes():
    url = "https://swapi.dev/api/people/"
    personajes = []
    
    while url:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            personajes.extend(data.get('results', []))
            url = data.get('next')  # Obtiene la siguiente página de resultados
        else:
            print(f"Error al obtener personajes: Código de estado {response.status_code} - Contenido: {response.text}")
            break
            
    return personajes

# Paso 2: Obtener planetas de la API de Star Wars
def obtener_planetas():
    url = "https://swapi.dev/api/planets/"
    planetas = []
    
    while url:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            planetas.extend(data.get('results', []))
            url = data.get('next')  # Obtiene la siguiente página de resultados
        else:
            print(f"Error al obtener planetas: Código de estado {response.status_code} - Contenido: {response.text}")
            break
            
    return planetas

# Paso 3: Consultar el rolodex del oráculo para obtener la alineación de los personajes
def consultar_oracle_rolodex(nombre_personaje):
    # Codificar el nombre del personaje
    nombre_codificado = quote(nombre_personaje)
    url = f"https://makers-challenge.altscore.ai/v1/s1/e3/resources/oracle-rolodex?name={nombre_codificado}"
    headers = {
        "API-KEY": "3841757512a14e20b637eabb62eb62f6",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # Decodificar la alineación de la fuerza
        alineacion_decodificada = base64.b64decode(data['oracle_notes']).decode('utf-8')
        # print(f"Alineación de {nombre_personaje}: {alineacion_decodificada}")  # Imprimir alineación
        return alineacion_decodificada
    else:
        print(f"Error al consultar el rolodex del oráculo: Código de estado {response.status_code} - Contenido: {response.text}")
        return None

# Paso 4: Calcular el IBF para un planeta específico
def calcular_ibf(personajes, alineaciones):
    num_luminoso = sum(1 for p in personajes if 'Light Side' in alineaciones.get(p['name'], ''))
    num_oscuro = sum(1 for p in personajes if 'Dark Side' in alineaciones.get(p['name'], ''))
    total_personajes = len(personajes)

    # print(f"Número de personajes del Lado Luminoso: {num_luminoso}")
    # print(f"Número de personajes del Lado Oscuro: {num_oscuro}")
    # print(f"Total de personajes en el planeta: {total_personajes}")

    if total_personajes == 0:
        return None  # Evitar división por cero

    ibf = (num_luminoso - num_oscuro) / total_personajes
    return ibf

# Paso 5: Enviar la solución
def enviar_solucion(planeta):
    api_key = "3841757512a14e20b637eabb62eb62f6"  # Reemplaza con tu API Key real
    headers = {
        "API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    # Cambiar el campo 'oracle_notes' a 'planet'
    data = {
        "planet": planeta  # Asegúrate de que este sea el campo correcto requerido por la API
    }
    
    response = requests.post("https://makers-challenge.altscore.ai/v1/s1/e3/solution", headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"Respuesta enviada con éxito: {response.json()}")
    else:
        print(f"Error al enviar solución: Código de estado {response.status_code} - Contenido: {response.text}")

# Integración de todo
def main():
    # Obtener personajes y planetas
    personajes = obtener_personajes()
    planetas = obtener_planetas()

    # Crear un diccionario para las alineaciones de los personajes
    alineaciones = {}
    
    # Consultar alineaciones para todos los personajes obtenidos
    for personaje in personajes:
        nombre_personaje = personaje['name']
        alineacion = consultar_oracle_rolodex(nombre_personaje)
        if alineacion:
            alineaciones[nombre_personaje] = alineacion

    # Iterar sobre los planetas y calcular IBF
    for planeta in planetas:
        nombre_planeta = planeta['name']
        # Filtrar personajes que pertenecen a este planeta
        personajes_en_planeta = [p for p in personajes if 'homeworld' in p and p['homeworld'] == planeta['url']]
        
        # Calcular IBF
        ibf_resultado = calcular_ibf(personajes_en_planeta, alineaciones)

        if ibf_resultado is not None:
            print(f"Índice de Balance de la Fuerza (IBF) para {nombre_planeta}: {ibf_resultado:.2f}")
            
            # Verificar si hay equilibrio
            if ibf_resultado == 0:
                print(f"El IBF para {nombre_planeta} es 0, se enviará la solución.")
                enviar_solucion(nombre_planeta)  # Enviar la solución
                break  # Salimos del bucle después de enviar la solución
        else:
            print(f"No se puede calcular el IBF para {nombre_planeta} (división por cero).")

# Ejecutar el programa
if __name__ == "__main__":
    main()
