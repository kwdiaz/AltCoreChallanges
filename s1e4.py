import requests

# Definir la API Key
api_key = "3841757512a14e20b637eabb62eb62f6"  # Reemplaza con tu API Key real

# Usuario
username = "Elrond"

# Lista de posibles contraseñas para probar
possible_passwords = [
       "Starlight",
  
]

# URL de la API
url = "https://makers-challenge.altscore.ai/v1/s1/e4/solution"

# Configurar los encabezados
headers = {
    "API-KEY": api_key,
    "Content-Type": "application/json"
}

# Probar cada contraseña posible
for password in possible_passwords:
    data = {
        "username": username,
        "password": password
    }
    
    # Enviar la respuesta
    response = requests.post(url, headers=headers, json=data)
    
    # Verificar la respuesta
    if response.status_code == 200:
        print(f"Probando: {password} - Respuesta:", response.json())
    else:
        print(f"Error al enviar respuesta con {password}:", response.status_code, response.text)
