import sys
import json
import time
import PIL
import requests
from datetime import datetime
from colorama import init, Fore, Style
from urllib.parse import unquote
import cloudscraper
import os
import pyrogram
from pyrogram import Client
from fake_useragent import UserAgent
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
import random
from PIL import Image
from io import BytesIO
from fake_useragent import FakeUserAgentError
from pyrogram.errors import FloodWait

init(autoreset=True)

API_ID = 23477584  # api
API_HASH = '4ee989d60366feebdff6b26b7efec732'
REF = 'f5055600013'  # ref untuk menjalankan bot
SQUAD = -1001943111151  # id channel squad
SQUAD2 = "cmVmPTY5MjIxMjcwODk="  # ref squad
#=============================
TASKS_LIST = [
    "x:notcoin",
    "x:notpixel",
    "paint20pixels",
    "joinSquad",
    "channel:notpixel_channel",
    "channel:notcoin",
    "makePixelAvatar",
]

class Data:
    def __init__(self, token):
        self.init_data = token

class PixelTod:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.DEFAULT_COUNTDOWN = 1800  # waktu tunggu
        self.INTERVAL_DELAY = 1  # jeda antar akun
        self.account_delay = {}  # Store delays for each account
        self.invalid_sessions = set()  # Store invalid sessions
        self.user_agents_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/60.0.3112.113 Safari/537.36',
        ]

        try:
            user_agent = UserAgent().random
        except (FakeUserAgentError, IndexError):
            user_agent = random.choice(self.user_agents_list)

        self.base_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'id,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json',
            'Origin': 'https://app.notpx.app',
            'Referer': 'https://app.notpx.app/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': user_agent
        }
        self.ref = "f5055600013"
        self.peer = 'notpixel'
        self.name = "app"

    def api_call(self, url, data=None, headers=None, method='GET'):
        max_attempts = 3
        attempt = 0
        while attempt < max_attempts:
            try:
                if method == 'GET':
                    res = self.scraper.get(url, headers=headers)
                elif method == 'POST':
                    res = self.scraper.post(url, headers=headers, data=data)
                elif method == 'PUT':
                    res = self.scraper.put(url, headers=headers)
                else:
                    raise ValueError(f'Method not supported: {method}')
                
                if res.status_code == 401:
                    self.log(f'{Fore.LIGHTRED_EX}{res.text}')
                return res
            
            except FloodWait as e:
                wait_time = e.value
                print(f"FLOOD_WAIT error: waiting for {wait_time} seconds")
                self.account_delay[account] = wait_time
                time.sleep(wait_time)
                return None
            
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                self.log(f'{Fore.LIGHTRED_EX}Connection error! Retrying ({attempt + 1}/{max_attempts})')
                attempt += 1
                time.sleep(3)

        raise Exception('API call failed after maximum retries')

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_tg_web_data(self, account, ref: str, peer: str, name: str):
        auth_url = None
        client = Client(name=account, api_id=API_ID, api_hash=API_HASH, workdir="sessions/")
        client.connect()
        client.get_me()

        try:
            bot = client.resolve_peer(peer)
            app = InputBotAppShortName(bot_id=bot, short_name=f"{name}")
            web_view = client.invoke(RequestAppWebView(
                peer=bot,
                app=app,
                platform='android',
                write_allowed=True,
                start_param=ref
            ))
            auth_url = web_view.url

        except FloodWait as e:
            wait_time = e.value  # Get the wait time from the FloodWait exception
            print(f"FLOOD_WAIT error for account {account}. Waiting for {wait_time} seconds.")
            self.account_delay[account] = wait_time  # Store wait time for this account
            return None  # Skip processing for this account temporarily

        except Exception as err:
            print(f"Error while fetching Telegram web data for account {account}: {err}")
            self.invalid_sessions.add(account)  # Mark account as invalid if error occurs
        
        client.disconnect()

        if auth_url:
            try:
                return unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
            except IndexError:
                print(f"Error: Unexpected structure in auth_url for account {account}.")
                return None
        else:
            print(f"Error: auth_url is None for account {account}.")
            return None

    def main(self):
        action = int(input(f'{Fore.LIGHTBLUE_EX}Select action:\n{Fore.LIGHTWHITE_EX}1. Start farming\n{Fore.LIGHTWHITE_EX}2. Create new session\n>'))

        self.clear_console()

        if not os.path.exists('sessions'):
            os.mkdir('sessions')

        if action == 2:
            self.create_sessions()

        if action == 1:
            while True:
                self.clear_console()
                print(f"""{Fore.LIGHTYELLOW_EX}

 ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ 
██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗
██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║
██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║
╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝
 ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ 
    ██████╗  ██████╗ ██████╗ ██╗ █████╗            
    ██╔══██╗██╔═══██╗██╔══██╗██║██╔══██╗           
    ██████╔╝██║   ██║██████╔╝██║███████║           
    ██╔═══╝ ██║   ██║██╔══██╗██║██╔══██║           
    ██║     ╚██████╔╝██║  ██║██║██║  ██║           
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝           
                                                   

""")
                print(f'{Fore.LIGHTYELLOW_EX} support me 📌')
                print(f'{Fore.LIGHTGREEN_EX} 0x30611dA354E5732B5d849951bC69d5d41296ddf1')

                
                sessions = self.pars_sessions()
                accounts = self.check_valid_sessions(sessions)
                accounts += list(self.invalid_sessions)  # Re-check previously invalid sessions
                self.invalid_sessions.clear()  # Clear invalid sessions for re-validation
                
                self.account_delay.clear()  # Clear delay logs to reset
                
                if not accounts:
                    raise ValueError(f"{Fore.LIGHTRED_EX}No valid sessions found")

                for idx, account in enumerate(accounts):
                    if account in self.account_delay:
                        wait_time = self.account_delay[account]
                        print(f"Waiting for account {account} for {wait_time} seconds.")
                        time.sleep(wait_time)
                        self.account_delay.pop(account)
                        continue

                    print(f"Processing account {idx+1}: {account}")
                    data = self.get_tg_web_data(account, ref=self.ref, peer=self.peer, name=self.name)
                    if data is None:
                        continue
                    new_data = Data(data)
                    self.process_account(new_data)
                    print('-' * 50)
                    self.countdown(self.INTERVAL_DELAY)
                
                self.countdown(self.DEFAULT_COUNTDOWN)  # Wait before restarting all accounts

    def process_account(self, data):
        self.get_me(data)
        self.claim_hourly_reward(data)
        self.paint_pixel(data)
        self.task(data)
        self.buy_upgrades(data)

    def pars_sessions(self):
        sessions = []
        for file in os.listdir('sessions/'):
            if file.endswith(".session"):
                sessions.append(file.replace(".session", ""))

        self.log(f"{Fore.LIGHTYELLOW_EX}Ditemukan sesi: {Fore.LIGHTWHITE_EX}{len(sessions)}!")
        return sessions

    def create_sessions(self):
        while True:
            session_name = input(F'{Fore.LIGHTBLUE_EX}Masukkan nama sesi (untuk keluar tekan Enter)\n')
            if not session_name:
                return

            with pyrogram.Client(
                api_id=API_ID,
                api_hash=API_HASH,
                name=session_name,
                workdir="sessions/"
            ) as session:
                user_data = session.get_me()

            self.log(f'{Fore.LIGHTYELLOW_EX}Sesi ditambahkan +{user_data.phone_number} @{user_data.username}')

    def check_valid_sessions(self, sessions: list):
        self.log(f"{Fore.LIGHTYELLOW_EX}Memeriksa sesi yang valid!")
        valid_sessions = []
        for session in sessions:
            try:
                client = Client(name=session, api_id=API_ID, api_hash=API_HASH, workdir="sessions/")
                if client.connect():
                    client.get_me()
                    valid_sessions.append(session)
                else:
                    self.log(f"{session}.session tidak valid")
                client.disconnect()
            except:
                self.log(f"{Fore.LIGHTRED_EX}{session}.session tidak valid")

        self.log(f"{Fore.LIGHTYELLOW_EX}Sesi valid: {Fore.LIGHTWHITE_EX}{len(valid_sessions)}; {Fore.LIGHTYELLOW_EX}Sesi tidak valid: {Fore.LIGHTWHITE_EX}{len(sessions) - len(valid_sessions)}")
        return valid_sessions

    def countdown(self, t):
        while t:
            one, two = divmod(t, 3600)
            three, four = divmod(two, 60)
            print(f"{Fore.LIGHTWHITE_EX}Menunggu hingga {one:02}:{three:02}:{four:02} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def get_me(self, data: Data):
        url = "https://notpx.app/api/v1/users/me"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"initData {data.init_data}"
        res = self.api_call(url, headers=headers)
        if res.status_code == 200 or res.status_code == 201:
            response_data = res.json()
            
            self.log(f"{Fore.LIGHTYELLOW_EX}Akun: {Fore.LIGHTWHITE_EX}{response_data['firstName']}")
            self.log(f"{Fore.LIGHTYELLOW_EX}Pangkat: {Fore.LIGHTWHITE_EX}{response_data.get('league', 'Unknown')}")
            
            squad = response_data['squad']
            if squad['id'] is None:
                tg_web_data = self.get_tg_web_data(account=self.account_squad, ref=SQUAD2, peer="notgames_bot", name="squads")
                bearer_token = None
                custom_headers = {
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Referer": "https://webapp.notcoin.tg/",
                    "content-type": "application/json",
                    "Origin": "https://webapp.notcoin.tg",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "Priority": "u=4",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/129.0.0.0 Safari/537.36"
                }
                try:
                    login_url = "https://api.notcoin.tg/auth/login"
                    custom_headers["Host"] = "api.notcoin.tg"
                    custom_headers["bypass-tunnel-reminder"] = "x"
                    custom_headers['Content-Length'] = str(len(tg_web_data) + 18)
                    custom_headers['x-auth-token'] = "Bearer null"
                    r = {"webAppData": f"{tg_web_data}"}
                    login_req = self.api_call(login_url, headers=custom_headers, data=json.dumps(r), method='POST')

                    if login_req.status_code == 200 or login_req.status_code == 201:
                        login_data = login_req.json()
                        bearer_token = login_data.get("data", {}).get("accessToken", None)
                        time.sleep(3)
                        if not bearer_token:
                            raise Exception
                except Exception as error:
                    self.log(f"{Fore.LIGHTRED_EX}Kesalahan login squad: {error}")
                custom_headers["Content-Length"] = "26"
                custom_headers["x-auth-token"] = f"Bearer {bearer_token}"

                try:
                    join_url = "https://api.notcoin.tg/squads/absolateA/join"
                    b = {"chatId": SQUAD}
                    login_req = self.api_call(join_url, headers=custom_headers, data=json.dumps(b), method='POST')
                    if login_req.status_code == 200 or login_req.status_code == 201:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Bergabung dengan squad")
                except Exception as error:
                    self.log(f"{Fore.LIGHTRED_EX}Kesalahan bergabung dengan squad: {error}")
            time.sleep(3)

    def claim_hourly_reward(self, data: Data):
        if self.hourly_reward_stats(data):
            url = "https://notpx.app/api/v1/mining/claim"
            headers = self.base_headers.copy()
            headers["Authorization"] = f"initData {data.init_data}"
            res = self.api_call(url, headers=headers)
            if res.status_code == 200 or res.status_code == 201:
                self.log(f"{Fore.LIGHTYELLOW_EX}Mengambil hadiah")
            else:
                self.log(f"{Fore.LIGHTRED_EX}Kesalahan {res.text}")

    def hourly_reward_stats(self, data: Data) -> bool:
        url = "https://notpx.app/api/v1/mining/status"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"initData {data.init_data}"
        res = self.api_call(url, headers=headers)
        if res.status_code == 200 or res.status_code == 201:
            response_data = res.json()
            if response_data["fromStart"] > 3600:
                return True

    def compare_images(self):
        image1_path = '1.png'  # Path to the current image
        image2_path = 'orig4.png'  # Path to the original image

        areas = {
            (90, 153, 100, 163),  # Define areas of the image that should be compared
        }

        image1 = Image.open(image1_path)  # Open the first image
        image2 = Image.open(image2_path)  # Open the second image
        pixels1 = image1.load()  # Load pixel data for the first image
        pixels2 = image2.load()  # Load pixel data for the second image

        target_colors = [
            "#FFD635"  # List of target colors
        ]

        for area in areas:
            while True:
                (x, y) = self.get_random_coordinates(area)  # Get random coordinates in the area
                color1 = pixels1[x, y]  # Get the color of the pixel at these coordinates in the first image
                color2 = pixels2[x, y]  # Get the color of the pixel at these coordinates in the second image
                hex_color1 = self.rgb_to_hex(color1)  # Convert RGB color to hex for comparison
                hex_color2 = self.rgb_to_hex(color2)  # Convert RGB color to hex for comparison
                if hex_color1 != hex_color2 and hex_color2 in target_colors:
                    id = y * 1000
                    id += x + 1
                    col = hex_color2
                    return id, col  # Return the pixel ID and the color to be painted

    def get_random_coordinates(self, area):
        x_start, x_end, y_start, y_end = area
        x = random.randint(x_start, x_end)
        y = random.randint(y_start, y_end)
        return (x, y)

    def rgb_to_hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2]).upper()

    def paint_pixel(self, data: Data):
        url_img = "https://notpx.app/api/v2/image"
        url = "https://notpx.app/api/v1/mining/status"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"initData {data.init_data}"
        max_retries = 15
        for attempt in range(max_retries):
            try:
                res_img = self.api_call(url_img, headers=headers)
                image = Image.open(BytesIO(res_img.content))
                image.save("1.png")
                res_img.raise_for_status()
                break
            except (requests.exceptions.ChunkedEncodingError, requests.exceptions.HTTPError, PIL.UnidentifiedImageError):
                time.sleep(3)

        res = self.api_call(url, headers=headers)

        if res.status_code == 200 or res.status_code == 201:
            response_data = res.json()
            num = response_data['charges']
            self.log(f"{Fore.LIGHTYELLOW_EX}Saldo: {Fore.LIGHTWHITE_EX}{response_data['userBalance']}")

            url_st = "https://notpx.app/api/v1/image/template/my"
            url_s = "https://notpx.app/api/v1/image/template/subscribe/1467975528"
            res_st = self.api_call(url_st, headers=headers)

            if res_st.status_code == 200 or res_st.status_code == 201:
                response_st = res_st.json()
                if response_st["url"] != "https://static.notpx.app/templates/1467975528.png":
                    url_s = "https://notpx.app/api/v1/image/template/subscribe/1467975528"
                    self.api_call(url_s, headers=headers, method='PUT')
                    self.log(f"{Fore.LIGHTYELLOW_EX}Template dipasang")
                    time.sleep(0.5)
            elif res_st.status_code == 404:
                url_s = "https://notpx.app/api/v1/image/template/subscribe/1467975528"
                self.api_call(url_s, headers=headers, method='PUT')
                self.log(f"{Fore.LIGHTYELLOW_EX}Template dipasang")
                time.sleep(0.5)

            url_p = "https://notpx.app/api/v1/image/template/1467975528"
            res_i = self.api_call(url_p, headers=headers)

            if res_i.status_code == 200 or res.status_code == 201:
                for _ in range(num):
                    ids = self.compare_images()
                    pixel_id = ids[0]
                    color = ids[1]
                    datat = {
                        "pixelId": pixel_id,
                        "newColor": color
                    }
                    url = "https://notpx.app/api/v1/repaint/start"
                    headers = self.base_headers.copy()
                    headers["Authorization"] = f"initData {data.init_data}"
                    retry_count = 0
                    max_attempts = 3
                    while retry_count < max_attempts:
                        res = self.api_call(url, headers=headers, data=json.dumps(datat), method='POST')
                        time.sleep(0.5)

                        if res.status_code == 200 or res.status_code == 201:
                            response_data = res.json()
                            bal = response_data['balance']
                            self.log(f"{Fore.LIGHTYELLOW_EX}Menggambar, {Fore.LIGHTWHITE_EX} {Fore.LIGHTYELLOW_EX}Saldo: {Fore.LIGHTWHITE_EX}{bal}")
                            break
                        else:
                            self.log(f"{Fore.LIGHTRED_EX}Gagal menggambar. Percobaan {retry_count + 1} dari {max_attempts}.")
                            retry_count += 1
                            time.sleep(3)
                    if retry_count == max_attempts:
                        self.log(f"{Fore.LIGHTRED_EX}Gagal menggambar setelah {max_attempts} percobaan.")
                        break
            else:
                self.log(f"{Fore.LIGHTRED_EX}Kesalahan memasang template gambar")

    def buy_upgrades(self, data: Data):
        url = "https://notpx.app/api/v1/mining/status"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"initData {data.init_data}"
        res = self.api_call(url, headers=headers)

        if res.status_code == 200 or res.status_code == 201:
            response_data = res.json()
            user_balance = response_data['userBalance']
            levels_recharge = response_data['boosts']['reChargeSpeed'] + 1
            levels_paintreward = response_data['boosts']['paintReward'] + 1
            levels_energylimit = response_data['boosts']['energyLimit'] + 1

            time.sleep(3)
            if levels_paintreward - 1 < 7 and self.Reward[levels_paintreward]['Price'] <= user_balance:
                url1 = "https://notpx.app/api/v1/mining/boost/check/paintReward"
                headers1 = self.base_headers.copy()
                headers1["Authorization"] = f"initData {data.init_data}"
                res1 = self.api_call(url1, headers=headers1)
                if res1.status_code == 200 or res1.status_code == 201:
                    response_data1 = res1.json()
                    if response_data1["paintReward"]:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Membeli upgrade {Fore.LIGHTWHITE_EX}Paint Reward")

            time.sleep(3)
            if levels_recharge - 1 < 11 and self.Speed[levels_recharge]['Price'] <= user_balance:
                url2 = "https://notpx.app/api/v1/mining/boost/check/reChargeSpeed"
                headers2 = self.base_headers.copy()
                headers2["Authorization"] = f"initData {data.init_data}"
                res2 = self.api_call(url2, headers=headers2)
                if res2.status_code == 200 or res.status_code == 201:
                    response_data2 = res2.json()
                    if response_data2["reChargeSpeed"]:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Membeli upgrade {Fore.LIGHTWHITE_EX}Recharging Speed")

            time.sleep(3)
            if levels_energylimit - 1 < 6 and self.Limit[levels_energylimit]['Price'] <= user_balance:
                url3 = "https://notpx.app/api/v1/mining/boost/check/energyLimit"
                headers3 = self.base_headers.copy()
                headers3["Authorization"] = f"initData {data.init_data}"
                res3 = self.api_call(url3, headers=headers3)
                if res3.status_code == 200 or res1.status_code == 201:
                    response_data3 = res3.json()
                    if response_data3["energyLimit"]:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Membeli upgrade {Fore.LIGHTWHITE_EX}Energy Limit")

    def task(self, data: Data):
        url = "https://notpx.app/api/v1/mining/status"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"initData {data.init_data}"
        res = self.api_call(url, headers=headers)

        if res.status_code == 200 or res.status_code == 201:
            response_data = res.json()
            tasks = response_data["tasks"].keys()
            repaints = response_data['repaintsTotal']

            for task in TASKS_LIST:
                if task not in tasks:
                    if task == 'paint20pixels':
                        if repaints < 20:
                            continue
                    if "channel" in task:
                        entity, name = task.split(':')
                        taskk = f"{entity}?name={name}"
                        url2 = f'https://notpx.app/api/v1/mining/task/check/{taskk}'
                    else:
                        url2 = f'https://notpx.app/api/v1/mining/task/check/{task}'
                    time.sleep(3)

                    headers1 = self.base_headers.copy()
                    headers1["Authorization"] = f"initData {data.init_data}"
                    res1 = self.api_call(url2, headers=headers1)
                    if res1.status_code == 200 or res1.status_code == 201:
                        response_data1 = res1.json()
                        status = response_data1[task]
                        if status:
                            self.log(f"{Fore.LIGHTYELLOW_EX}Tugas selesai: {Fore.LIGHTWHITE_EX}{task}")

    def log(self, message):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{Fore.LIGHTBLACK_EX}[{now}]{Style.RESET_ALL} {message}")


if __name__ == "__main__":
    try:
        app = PixelTod()
        app.main()
    except KeyboardInterrupt:
        sys.exit()

