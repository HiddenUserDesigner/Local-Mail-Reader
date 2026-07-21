import os
import base64
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ==========================================
# 1. CONFIGURACIÓN DEL SISTEMA (LM STUDIO)
# ==========================================
# Cambiamos la URL al puerto de comunicacion y la ruta oficial que maneja LM Studio
LM_STUDIO_URL ="http://localhost:1234/v1/chat/completions" #en este caso pudes poner la direccion de tu propio puerto
MODELO_IA = "llama3"  # Tu modelo de ia cargado en LM Studio/puede ser diferente

print("Conectando con el sistema local...")
# PREGUNTA DEL USUARIO
PREGUNTA = input("Que deseas preguntar?: ")

# READONLY (Sólamente leer correos)(indicacion de que acciones a realizar)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# ==========================================
# 2. AUTENTICACIÓN CON GOOGLE
# ==========================================
print(" Autenticando con Google...")
creds = None#Establecemos las credenciales como valor en None parasu val
if os.path.exists('tu archivo token.json'):#Es un archivo que se genera automáticamente la primera vez que ejecutas tu código Python. Contiene los tokens de acceso (access_token y refresh_token) que Google te otorga una vez que apruebas el inicio de sesión.
    
    creds = Credentials.from_authorized_user_file('tu archivo token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(r"ruta y nombre de tu archivo de credenciales de Api de google", scopes=SCOPES)#JSON que contiene la identificación oficial de tu aplicación ante la API de Google (Gmail API). Contiene datos como el client_id (ID de cliente) y el client_secret (secreto de cliente).
        
        creds = flow.run_local_server(port=0)
    with open('tu archivo token.json', 'w') as token:
        token.write(creds.to_json())

# ==========================================
# 3. DESCARGAR CORREOS 
# ==========================================
print("Conectando a Gmail para descargar correos recientes...")
contexto_correos = ""

try:
    # Construimos el servicio de Gmail
    servicio_gmail = build('gmail', 'v1', credentials=creds)
    
    # Solicitamos la lista de los últimos  mensajes de la bandeja de entrada (INBOX) (puedes solicitar un valor diferente de 15)
    resultado = servicio_gmail.users().messages().list(userId='me', maxResults=15, labelIds=['INBOX']).execute()
    mensajes = resultado.get('messages', [])

    if not mensajes:
        print("📭 No se encontraron correos en la bandeja de entrada.")
        exit()

    print(f"Leyendo {len(mensajes)} correos...")#len imprime los elelmentos que hay en la lista 
    
    # Iteramos sobre cada correo para extraer su contenido técnico
    for idx, msg in enumerate(mensajes):
        txt = servicio_gmail.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = txt['payload']
        headers = payload['headers']
        
        asunto = "Sin Asunto"
        remitente = "Desconocido"
        for header in headers:
            if header['name'] == 'Subject':
                asunto = header['value']
            if header['name'] == 'From':
                remitente = header['value']
        
        cuerpo = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain': 
                    data = part['body'].get('data')
                    if data:
                        cuerpo = base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            data = payload['body'].get('data')
            if data:
                cuerpo = base64.urlsafe_b64decode(data).decode('utf-8')
        
        cuerpo_resumido = cuerpo[:500] 
        contexto_correos += f"\n--- CORREO {idx+1} ---\nDe: {remitente}\nAsunto: {asunto}\nContenido: {cuerpo_resumido}\n"

except Exception as e:
    print(f"Error al leer correos de Gmail: {e}")
    exit()

# ==========================================
# 4. ENVIAR LOS CORREOS COMO CONTEXTO A LLAMA 3
# ==========================================
print(" Armando el paquete de datos para LM Studio...")

# Creamos el prompt estructurado combinando los correos y tu pregunta interactiva
PROMPT_FINAL = f"""Aquí tienes los correos electrónicos recientes del usuario:
{contexto_correos}

Instrucción o pregunta del usuario: {PREGUNTA}"""

# Armamos el formato de Mensajes (OpenAI Style) requerido por LM Studio
payload = {
    "model": MODELO_IA,
    "messages": [
        {
            "role": "system", 
            "content": "Eres un asistente personal inteligente. Basándote en la información de los correos provistos, responde de forma clara, concisa y profesional a lo que te pida el usuario."
        },
        {
            "role": "user", 
            "content": PROMPT_FINAL
        }
    ],
    "stream": False
}

print("Llama 3 está analizando tus correos en LM Studio (Procesamiento Local)...")
try:
    # Enviamos la petición a LM Studio
    respuesta_ia = requests.post(LM_STUDIO_URL, json=payload)
    datos_json = respuesta_ia.json()
    
    # Extraemos la respuesta según la estructura de LM Studio
    resultado_texto = datos_json["choices"][0]["message"]["content"]
    
    print("\n==================================================")
    print("🤖 RESPUESTA DE TU IA SOBRE TUS CORREOS:")
    print("==================================================")
    print(resultado_texto)
    print("==================================================")

except Exception as e:
    print(f"Error al conectar con LM Studio: {e}")
    print("💡 Recuerda verificar que el 'Local Server' de LM Studio esté encendido en el puerto 1234.")