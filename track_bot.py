import os
import signal
import subprocess
from api import Api

class TrackBot:

    def __init__(self):
        self.api = Api()
        self.cookies = []
        self.headers = {
            'Host': 'rastreamento.correios.com.br',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer':	'https://rastreamento.correios.com.br/app/index.php',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        self.get_session_cookies()

    def get_package_status(self, code_list: list[str]) -> list[dict]:
        print('=========== Solve captcha ===========')
        while True:
            image_cookies, image = self.secure_image()
            self.update_mail_cookie(image_cookies)
            captcha_answer = self.solve_captcha()
            package_status = self.package_status(captcha_answer, code_list)
            if not 'erro' in package_status:
                break
            print("Captcha error, try again")

        self.save_captcha(captcha_answer)
        return package_status

    def solve_captcha(self) -> str:
        try:
            process = subprocess.Popen('feh captcha.png &', shell=True,
                                       stdout=subprocess.PIPE, preexec_fn=os.setsid)
        except FileNotFoundError:
            process = subprocess.Popen('xdg-open captcha.png &', shell=True,
                                       stdout=subprocess.PIPE, preexec_fn=os.setsid)

        captcha_answer = input('Answer => ').strip()
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        return captcha_answer

    def save_captcha(self, captcha_answer: str) -> None:
        os.rename('captcha.png', os.path.join('solved_captchas/', f'{captcha_answer}.png'))

    def track_single(self, code: str) -> dict:
        return self.get_package_status([code])

    def track(self, packages: list) -> list[dict]:
        code_list = [p.code for p in packages]
        return self.get_package_status(code_list)

    def get_session_cookies(self) -> None:
        response = self.api.get(self.api.cookie_url, self.headers, self.cookies)

        self.cookies = self.api.format_cookies(response.headers['set-cookie'])

    def secure_image(self) -> [str, bytes]:
        response = self.api.get(self.api.secure_image_url, self.headers, self.cookies)

        with open('captcha.png', 'wb') as file:
            file.write(response.content)

        return [response.headers['set-cookie'], response.content]

    def package_status(self, captcha_answer: str, package_code: list[str]) -> list[dict]:
        codes = ''.join(package_code)
        base_url = self.api.rastro_multi_url
        url = f"{base_url}&objeto={codes}&captcha={captcha_answer}"
        response = self.api.get(url, self.headers, self.cookies)
        return response.json()

    def update_mail_cookie(self, cookies: str) -> None:
        mail_cookie_name = ''
        mail_cookie_value = ''
        for name, value in self.api.format_cookies(cookies).items():
            if name[0:2] == 'TS':
                mail_cookie_name = name
                mail_cookie_value = value
                break
        self.cookies[mail_cookie_name] = mail_cookie_value
