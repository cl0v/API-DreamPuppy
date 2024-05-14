# from google_auth_oauthlib import service_account
from google.oauth2 import service_account
import google.auth.transport.requests

# Caminho para o arquivo JSON da chave da conta de serviço
KEY_PATH = "service-account.json"

# Define o escopo da API do Google Merchant
SCOPES = ['https://www.googleapis.com/auth/content']

last_token: str = None


def refresh_token() -> str:
    """
    Gera um novo token de autenticação
    """
    # Carrega as credenciais e solicita um token de acesso
    credentials = service_account.Credentials.from_service_account_file(
        KEY_PATH, scopes=SCOPES)

    # Solicita um token de acesso
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    
    
    return credentials.token

def get_token() -> str:
    """
    Retorna o token mais recente e válido para ser usado sem a necessidade do refresh
    """
    if(last_token is None):
        last_token = refresh_token()
        
    return last_token