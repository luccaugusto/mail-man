import os
import signal
import datetime
import subprocess
import time
from api import Api
from ui_display import ASCIIArt, Colors  # Import the new UI system


class TrackBot:

    def __init__(self):
        self.api = Api()
        self.cookies = []
        self.headers = {
            "Host": "rastreamento.correios.com.br",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://rastreamento.correios.com.br/app/index.php",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        }
        self.get_session_cookies()

    def get_package_status(self, code_list: list[str]) -> list[dict]:
        print(ASCIIArt.captcha_solving())
        while True:
            image_cookies, image = self.get_secure_image()
            self.update_mail_cookie(image_cookies)
            captcha_answer = self.solve_captcha()
            package_status = self.package_status(captcha_answer, code_list)
            if not "erro" in package_status:
                break
            print(f"    {Colors.RED}❌ Captcha error, trying again...{Colors.END}")

        self.save_captcha(captcha_answer)
        return package_status

    def solve_captcha(self) -> str:
        try:
            process = subprocess.Popen(
                "feh captcha.png &",
                shell=True,
                stdout=subprocess.PIPE,
                preexec_fn=os.setsid,
            )
        except FileNotFoundError:
            process = subprocess.Popen(
                "xdg-open captcha.png &",
                shell=True,
                stdout=subprocess.PIPE,
                preexec_fn=os.setsid,
            )

        print(f"    {Colors.YELLOW}❓ Please enter the captcha solution:{Colors.END}")
        captcha_answer = input(f"    {Colors.CYAN}📝 Answer => {Colors.END}").strip()
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        return captcha_answer

    def save_captcha(self, captcha_answer: str) -> None:
        os.rename("captcha.png", os.path.join("solved_captchas/", f"{captcha_answer}.png"))

    def track_single(self, code: str) -> dict:
        return self.get_package_status([code])

    def track(self, packages: list) -> list[dict]:
        code_list = [p.code for p in packages if p.delivered == "False"]
        return self.get_package_status(code_list)

    def get_session_cookies(self) -> None:
        max_retries = 6
        for attempt in range(max_retries):
            try:
                print(f"    {Colors.BLUE}🔄 Getting session cookies (attempt {attempt + 1}/{max_retries}){Colors.END}")
                response = self.api.get(self.api.cookie_url, self.headers, self.cookies)

                # Check if response has the expected cookie header
                if "set-cookie" not in response.headers:
                    raise Exception("No set-cookie header in response")

                self.cookies = self.api.format_cookies(response.headers["set-cookie"])
                print(f"    {Colors.GREEN}✅ Successfully obtained session cookies{Colors.END}")
                return  # Success - exit the retry loop

            except Exception as e:
                print(f"    {Colors.YELLOW}⚠️  Attempt {attempt + 1} failed: {str(e)}{Colors.END}")

                # If this was the last attempt, re-raise the exception
                if attempt == max_retries - 1:
                    print(f"    {Colors.RED}❌ Max retries exceeded. Unable to get session cookies.{Colors.END}")
                    raise e

                # Calculate exponential backoff wait time (2^attempt seconds)
                wait_time = 2**attempt
                print(f"    {Colors.CYAN}⏳ Waiting {wait_time} seconds before retry...{Colors.END}")
                time.sleep(wait_time)

    def get_secure_image(self) -> tuple[str, bytes]:
        max_retries = 6
        for attempt in range(max_retries):
            try:
                print(f"    {Colors.BLUE}🔄 Getting secure image (attempt {attempt + 1}/{max_retries}){Colors.END}")
                response = self.api.get(self.api.secure_image_url, self.headers, self.cookies)

                # Save the captcha image to file
                with open("captcha.png", "wb") as file:
                    file.write(response.content)

                print(f"    {Colors.GREEN}✅ Successfully obtained secure image{Colors.END}")
                return [response.headers["set-cookie"], response.content]

            except Exception as e:
                print(f"    {Colors.YELLOW}⚠️  Attempt {attempt + 1} failed: {str(e)}{Colors.END}")

                # If this was the last attempt, re-raise the exception
                if attempt == max_retries - 1:
                    print(f"    {Colors.RED}❌ Max retries exceeded. Unable to get secure image.{Colors.END}")
                    raise e

                # Calculate exponential backoff wait time (2^attempt seconds)
                wait_time = 2**attempt
                print(f"    {Colors.CYAN}⏳ Waiting {wait_time} seconds before retry...{Colors.END}")
                time.sleep(wait_time)

    def package_status(self, captcha_answer: str, package_code: list[str]) -> list[dict]:
        codes = "".join(package_code)
        base_url = self.api.rastro_multi_url
        url = f"{base_url}&objeto={codes}&captcha={captcha_answer}"
        response = self.api.get(url, self.headers, self.cookies)
        return response.json()

    def update_mail_cookie(self, cookies: str) -> None:
        mail_cookie_name = ""
        mail_cookie_value = ""
        for name, value in self.api.format_cookies(cookies).items():
            if name[0:2] == "TS":
                mail_cookie_name = name
                mail_cookie_value = value
                break
        self.cookies[mail_cookie_name] = mail_cookie_value

    def fetch_a_bunch_of_captchas(self, size_of_bunch: int):
        print(f"    {Colors.BLUE}🔄 Fetching {size_of_bunch} captchas from server...{Colors.END}")
        for i in range(size_of_bunch):
            image_cookies, _ = self.get_secure_image()
            self.update_mail_cookie(image_cookies)
            filename = f"{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}-{i}.png"
            os.rename("captcha.png", os.path.join("downloaded_captchas/", filename))
            print(f"    {i}/{size_of_bunch} {Colors.CYAN} Captcha saved as {filename}{Colors.END}")
        print(f"    {Colors.GREEN}✅ Successfully fetched {size_of_bunch} captchas{Colors.END}")
