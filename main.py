import time
import requests
import traceback

BOT_TOKEN = '7691092018:AAFNhWE2NDBDdtnwa6iZjv4I_stvV63EyRE'
USER_ID = 7239555470  # sin comillas

API_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
last_price = 15.13

def get_visible_price():
    payload = {
        "page": 1,
        "rows": 30,
        "asset": "USDT",
        "tradeType": "SELL",
        "fiat": "BOB",
        "transAmount": "8000",
        "payTypes": []  # Puedes agregar "BankTransfer" si quieres limitar
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            valid_prices = []
            for item in data["data"]:
                try:
                    adv = item["adv"]
                    advertiser = item["advertiser"]

                    min_amount = float(adv["minSingleTransAmount"])
                    max_amount = float(adv["maxSingleTransAmount"])
                    price = float(adv["price"])

                    # Filtrar por rango válido de monto
                    if not (min_amount <= 8000 <= max_amount):
                        continue

                    # Filtrar por usuarios verificados
                    if advertiser.get("userType") == "ordinary":
                        continue

                    # Opcional: reputación mínima
                    if advertiser.get("monthOrderCount", 0) < 100:
                        continue

                    valid_prices.append(price)

                except Exception:
                    continue

            if valid_prices:
                return min(valid_prices)
            else:
                print("No hay anuncios válidos según filtros.")
                return None
        else:
            print("Respuesta vacía.")
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
        price = get_visible_price()
        if price:
            print(f"Precio visible filtrado: Bs. {price}")
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
            print("No se pudo obtener precio visible.")
        time.sleep(150)