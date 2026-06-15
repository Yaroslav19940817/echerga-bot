import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

LIMIT_MINUTES = 240  # 4 години

already_sent = False


def send_message(text):
    response = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

    print("TELEGRAM STATUS:", response.status_code)


while True:
    try:
        response = requests.get(
    "https://back.echerha.gov.ua/api/v4/workload/1",
    headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://echerha.gov.ua/"
    },
    timeout=30
)

print("STATUS:", response.status_code)
print("TEXT:", response.text[:500])

response.raise_for_status()

        data = response.json()

        chop = next(
            x for x in data["data"]
            if x["id"] == 17
        )

        wait_time = chop["wait_time"]
        vehicles = chop["vehicle_in_active_queues_counts"]

        print("WAIT TIME:", wait_time)
        print("VEHICLES:", vehicles)

        if wait_time >= LIMIT_MINUTES and not already_sent:
            hours = round(wait_time / 60, 1)

            send_message(
                f"🚛 Чоп–Захонь\n"
                f"Черга перевищила 4 години.\n"
                f"Поточне очікування: {hours} год.\n"
                f"Авто в черзі: {vehicles}"
            )

            already_sent = True
            print("Notification sent")

        elif wait_time < LIMIT_MINUTES:
            already_sent = False

    except Exception as e:
        print("ERROR:", str(e))

    # перевірка кожні 15 хвилин
    time.sleep(900)
