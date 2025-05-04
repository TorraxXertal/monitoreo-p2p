import time
import requests
import traceback

BOT_TOKEN = '7691092018:AAFNhWE2NDBDdtnwa6iZjv4I_stvV63EyRE'
USER_ID = 7239555470  # sin comillas
API_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
last_price = 15.13

def get_lowest_price():
    payload = {
        "page": 1,
        "rows": 20,
        "asset": "USDT",
        "tradeType": "SELL",
        "fiat": "BOB",
        "transAmount": "8000",  # Filtra anuncios que aceptan desde 8000 BOB
        "payTypes": []  # Ejemplo: ["BankTransfer"] si lo necesitas
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            prices = []
            for item in data["data"]:
                try:
                    price = float(item["adv"]["price"])
                    prices.append(price)
                except:
                    continue

            if prices:
                lowest_price = min(prices)
                return lowest_price
            else:
                print("No se pudo extraer ningún precio.")
                return None
        else:
            print("Respuesta vacía o formato inesperado:", data)
            return None
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
        price = get_lowest_price()
        if price:
            print(f"Precio más bajo: Bs. {price}")
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
        time.sleep(150)