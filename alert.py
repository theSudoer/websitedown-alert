import requests
import time
from datetime import datetime
#run - pip install requests
#can run this a cron job in linux or Task Scheduler in Windows to check uptime every 5 minutes or so.
# 
#to add cron job do    crontab -e and add to the bottong of file 
# */10 * * * * /usr/bin/python3 /path/to/your/folder/uptime_checker.py >> /path/to/your/folder/uptime_log.txt 2>&1
# set for 10 min change the 10 to change this , use reccomended option 
#
#  # --- CONFIGURATION ---
WEBSITES = [
    "https://change.me",
    "https://changeme.com"
]

# Replace with a Discord/Slack webhook URL to get pinged on your phone/desktop.
# Leave blank ("") if you only want to use local log files.
WEBHOOK_URL = "" 

def send_notification(message):
    """Sends a push notification via Webhook and prints to terminal/log."""
    print(message) # Always print so it goes to the cron log file
    
    if WEBHOOK_URL:
        try:
            # This payload format works for Discord. 
            # Adjust slightly if using Slack or Telegram.
            requests.post(WEBHOOK_URL, json={"content": message})
        except Exception as e:
            print(f"Failed to send webhook notification: {e}")

def check_websites():
    # Cloudflare blocks the default python-requests User-Agent. 
    # We spoof a standard Google Chrome User-Agent here.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for url in WEBSITES:
        try:
            # timeout=15 ensures the script doesn't hang forever if the server is unresponsive
            response = requests.get(url, headers=headers, timeout=15)

            # Cloudflare Origin errors (Host down, timeout, etc.) are 520-527.
            # Standard server errors are 500+. 
            if response.status_code >= 500:
                send_notification(f"🚨 **ALERT**: {url} is DOWN! (Cloudflare/Server Error: {response.status_code})")
            
            # 400+ are client errors (like 403 Forbidden or 404 Not Found)
            elif response.status_code >= 400:
                send_notification(f"⚠️ **WARNING**: {url} returned an error. (Status: {response.status_code})")
            
            else:
                # 200 OK range - Site is up and functioning.
                print(f"✅ {url} is UP. (Status: {response.status_code})")

        except requests.exceptions.Timeout:
            send_notification(f"🚨 **ALERT**: {url} TIMED OUT after 15 seconds.")
        except requests.exceptions.ConnectionError:
            send_notification(f"🚨 **ALERT**: {url} failed to connect completely (DNS or network failure).")
        except requests.exceptions.RequestException as e:
            send_notification(f"🚨 **ALERT**: {url} encountered an error: {e}")

if __name__ == "__main__":
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n--- Running uptime check at {now} ---")
    check_websites()
