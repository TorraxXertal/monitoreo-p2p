import time
import requests
import traceback

BOT_TOKEN = '7691092018:AAFNhWE2NDBDdtnwa6iZjv4I_stvV63EyRE'
USER_ID = 7239555470  # sin comillas
API_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
last_price = 15.13

def get_first_price():
    payload = {
        "page": 1,
        "rows": 1,
        "payTypes": [],
        "asset": "USDT",
        "tradeType": "SELL",
        "fiat": "BOB"
    }

    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(API_URL, json=payload, headers=headers)
        data = response.json()
        price_str = data["data"][0]["adv"]["price"]
        return float(price_str)
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