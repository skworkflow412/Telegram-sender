import csv
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact
from database import log_message
from config import API_ID, API_HASH, SESSION_NAME, MESSAGE_TEMPLATE

def send_bulk_messages(csv_file):
    client = TelegramClient(f"sessions/{SESSION_NAME}", API_ID, API_HASH)
    client.start()

    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipient = row.get('username') or row.get('phone')

            if not recipient:
                print("❌ No recipient found in row:", row)
                continue

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

            except Exception as e:
                log_message(recipient, f"Failed: {str(e)}")
                print(f"❌ Failed to send to {recipient}: {str(e)}")

    client.disconnect()
