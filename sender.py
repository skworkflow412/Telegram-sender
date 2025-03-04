import csv
import os
import time
import requests
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError, RPCError
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact
from database import log_message
from config import API_ID, API_HASH, SESSION_NAME, MESSAGE_TEMPLATE, UPLOAD_FOLDER, GITHUB_CSV_URL

def download_csv_from_github():
    """Download CSV file from GitHub (if URL is provided)."""
    if not GITHUB_CSV_URL:
        print("❌ No GitHub CSV URL provided. Skipping download.")
        return None

    response = requests.get(GITHUB_CSV_URL)
    if response.status_code == 200:
        csv_filename = os.path.join(UPLOAD_FOLDER, "contacts.csv")
        with open(csv_filename, "wb") as file:
            file.write(response.content)
        print(f"✅ CSV downloaded: {csv_filename}")
        return "contacts.csv"
    else:
        print(f"❌ Failed to download CSV. HTTP Status: {response.status_code}")
        return None

def send_bulk_messages(csv_file=None):
    """Send messages from CSV with retry & error handling."""
    client = TelegramClient(f"sessions/{SESSION_NAME}", API_ID, API_HASH)
    client.start()

    csv_file = csv_file or download_csv_from_github()
    if not csv_file:
        print("❌ No CSV file available. Aborting.")
        return

    file_path = os.path.join(UPLOAD_FOLDER, csv_file)
    with open(file_path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipient = row.get('username') or row.get('phone')

            if not recipient:
                print("❌ No recipient found in row:", row)
                continue

            for attempt in range(3):  # Retry up to 3 times
                try:
                    if recipient.startswith("+"):
                        contact = InputPhoneContact(client_id=0, phone=recipient, first_name=row.get('name', 'User'))
                        result = client(ImportContactsRequest([contact]))
                        recipient = result.users[0].id

                    message = MESSAGE_TEMPLATE.format(
                        name=row.get('name', 'User'),
                        username=row.get('username', recipient),
                        phone=row.get('phone', recipient)
                    )

                    client.send_message(recipient, message)
                    log_message(recipient, "Sent")
                    print(f"✅ Sent to {recipient}")
                    break

                except FloodWaitError as e:
                    print(f"⚠️ FloodWaitError: Sleeping for {e.seconds} seconds")
                    time.sleep(e.seconds)

                except RPCError as e:
                    log_message(recipient, f"Failed: {str(e)}")
                    print(f"❌ RPCError for {recipient}: {str(e)}")
                    break

    client.disconnect()
