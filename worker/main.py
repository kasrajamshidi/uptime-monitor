import os
import time
import requests


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:8000"
)


CHECK_INTERVAL = 30


def get_monitors():
    try:
        response = requests.get(
            f"{BACKEND_URL}/monitors",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print(f"❌ Failed to get monitors: {error}")
        return []


def check_url(url):
    try:
        start = time.time()

        response = requests.get(
            url,
            timeout=5
        )

        response_time = round(
            (time.time() - start) * 1000
        )

        return {
            "status": "up",
            "status_code": response.status_code,
            "response_time": response_time,
        }

    except requests.RequestException as error:
        return {
            "status": "down",
            "status_code": None,
            "response_time": None,
            "error": str(error),
        }


def save_check_result(monitor_id, result):
    try:
        response = requests.post(
            f"{BACKEND_URL}/monitors/{monitor_id}/check",
            json=result,
            timeout=5
        )

        response.raise_for_status()

        return True

    except requests.RequestException as error:
        print(
            f"❌ Failed to save result "
            f"for monitor {monitor_id}: {error}"
        )

        return False


def main():
    print("🚀 Uptime Worker started")

    while True:
        monitors = get_monitors()

        print(f"\n📋 Found {len(monitors)} monitor(s)")

        for monitor in monitors:

            print(
                f"\n🔍 Checking "
                f"{monitor['name']} ({monitor['url']})..."
            )

            result = check_url(monitor["url"])

            print(
                f"Status: {result['status']} | "
                f"Code: {result['status_code']} | "
                f"Response: {result['response_time']}ms"
            )

            saved = save_check_result(
                monitor["id"],
                result
            )

            if saved:
                print("💾 Result saved successfully")

        print(
            f"\n⏳ Next check in "
            f"{CHECK_INTERVAL} seconds..."
        )

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
