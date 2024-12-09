import requests

# URL da API
url = "https://www.habbo.com.br/api/public/users?name=Lajotado"

# Cabeçalho para simular uma solicitação de navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

try:
    # Enviando a solicitação GET
    response = requests.get(url, headers=headers)
    # Verificando o status
    if response.status_code == 200:
        print("Dados recebidos com sucesso!")
        print(response.json())
    else:
        print(f"Erro ao acessar a API. Status: {response.status_code}")
        print(response.text)
except requests.RequestException as e:
    print(f"Erro ao acessar a API: {e}")
