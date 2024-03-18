import requests

class Api:
    def __init__(self):
        self.cookie_url = 'https://rastreamento.correios.com.br/app/index.php'
        self.secure_image_url = 'https://rastreamento.correios.com.br/core/securimage/securimage_show.php'
        self.result_url = 'https://rastreamento.correios.com.br/app/resultado.php?mqs=S'
        self.rastro_multi_url = 'https://rastreamento.correios.com.br/app/rastroMulti.php?'

    def get(self, url, headers, cookies):
        response = requests.get(url, headers=headers, cookies=cookies)

        if not response.ok:
            raise 'Failed to call correios api'

        return response

    def format_cookies(self, cookies: str) -> dict:
        formatted_cookies = {}
        for cookie in cookies.split(','):
            cookie_data = cookie.split('=')
            formatted_cookies[cookie_data[0]] = '='.join(cookie_data[1:])

        return formatted_cookies
