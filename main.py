import time
import traceback
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = '7691092018:AAFNhWE2NDBDdtnwa6iZjv4I_stvV63EyRE'
USER_ID = 7239555470  # sin comillas
URL = "https://p2p.binance.com/en/trade/sell/USDT?fiat=BOB"
last_price = 15.13

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_first_price():
    try:
        response = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        price_element = soup.select_one("div.headline5.text-primaryText")
        if not price_element:
            print("No se encontró el precio.")
            return None
        price = float(price_element.text.strip().replace(",", ""))
        return price
    except Exception:
        traceback.print_exc()
        return None

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": USER_ID, "text": message}
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"Error al enviar mensaje: {response.text}")
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    while True:
        price = get_first_price()
        if price:
            print(f"Precio actual: Bs. {price}")
            diff = price - last_price
            if diff >= 0.03:
                last_price = price
                mensaje = f"SUBIÓ Bs. {diff:.2f} - Nuevo precio: Bs. {price:.2f}"
                send_telegram_message(mensaje)
            elif diff <= -0.02:
                last_price = price
                mensaje = f"BAJÓ Bs. {abs(diff):.2f} - Nuevo precio: Bs. {price:.2f}"
                send_telegram_message(mensaje)
        else:
            print("No se pudo obtener el precio.")
        time.sleep(600)