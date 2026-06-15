import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

LIMIT_MINUTES = 240  # 4 години

already_sent = False

# Встав свій Bearer токен сюди
ECHERHA_TOKEN = "YOUR_BEARER_TOKEN"


def send_message(text):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )


while True:
    try:

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ECHERHA_TOKEN}",
            "X-Client-Locale": "uk",
            "X-User-Agent": "UABorder/3.8.0 Web/1.1.0",
            "Origin": "https://echerha.gov.ua",
            "Referer": "https://echerha.gov.ua/",
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            "https://back.echerha.gov.ua/api/v4/workload/1",
            headers=headers,
            timeout=30
        )

        print("STATUS:", response.status_code)
        print("TEXT:", response.text[:500])

        response.raise_for_status()

        data = response.json()

        checkpoints = data["data"]

        chop = next(
            item for item in checkpoints
            if item["id"] == 17
        )

        wait_time = chop["wait_time"]
        vehicles = chop["vehicle_in_active_queues_counts"]

        print(
            f"Чоп-Захонь | wait_time={wait_time} хв | vehicles={vehicles}"
        )

        if wait_time >= LIMIT_MINUTES and not already_sent:

            hours = round(wait_time / 60, 1)

            send_message(
                f"🚛 Чоп–Захонь\n"
                f"Черга перевищила 4 години.\n"
                f"Поточне очікування: {hours} год.\n"
                f"Авто в черзі: {vehicles}"
            )

            already_sent = True

        if wait_time < LIMIT_MINUTES:
            already_sent = False

    except Exception as e:
        print("ERROR:", str(e))

    time.sleep(900)
