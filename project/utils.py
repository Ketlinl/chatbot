import requests


def zip_code_request(zip_code):
    """
    A partir co CEP pegar os outros dados de endereço.
    """

    result = None
    if zip_code:
        try:
            response = requests.get(f"https://viacep.com.br/ws/{zip_code}/json/")
            response = response.json()
        except:
            return None

        if response:
            return {
                "zip_code": response.get('cep'),
                "state": response.get('uf'),
                "city": response.get('localidade'),
                "neighborhood": response.get('bairro'),
                "address": response.get('logradouro'),
                "complement": response.get('complemento')
            }
