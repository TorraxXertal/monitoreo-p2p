from playwright.sync_api import sync_playwright
import requests
import time

BOT_TOKEN = '7691092018:AAFNhWE2NDBDdtnwa6iZjv4I_stvV63EyRE'
USER_ID = 7239555470  # sin comillas
URL = "https://p2p.binance.com/en/trade/sell/USDT?fiat=BOB"
last_price = 15.13

def send_telegram_message(message):
    try:
        api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": USER_ID, "text": message}
        response = requests.post(api_url, data=data)
        if response.status_code != 200:
            print(f"Error al enviar mensaje: {response.text}")
    except Exception as e:
        print("Excepción al enviar mensaje:", e)

def get_first_price(page):
    page.goto(URL)
    page.wait_for_selector("div.headline5.text-primaryText", timeout=15000)
    price_text = page.locator("div.headline5.text-primaryText").first.text_content().strip().replace(",", "")
    return float(price_text)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    try:
        while True:
            price = get_first_price(page)
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
            time.sleep(600)
    except KeyboardInterrupt:
        print("Detenido por el usuario")
    finally:
        browser.close()