import configparser
import json
import asyncio
from datetime import date, datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)


# some functions to parse json date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    user_input_channel = input('enter entity(telegram URL or entity id):')

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0

    while True:
        print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        
        ## All telegram data exporter ##
        # messages = history.messages
        # for message in messages:
        #     all_messages.append(message.to_dict())
        # offset_id = messages[len(messages) - 1].id
        # total_messages = len(all_messages)
        # if total_count_limit != 0 and total_messages >= total_count_limit:
        #     break
        ## All telegram sata exporter ##

        ## Tenx##
        
        messages = history.messages
        for message in messages:
            message_dict = {
                "id": message.id,
                "date": message.date,
                "message": message.message,
                "label":"Retail"
                }
            all_messages.append(message_dict)
        offset_id = messages[-1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break
        
        ## Tenx##
        ##new##
        # all_messages = []

        # messages = history.messages

        # # Extract channel ID from the first message
        # channel_id = messages[0].peer_id.channel_id

        # for message in messages:
        #     message_dict = {
        #         "id": message.id,
        #         "date": message.date.isoformat(),
        #         "message": message.message,
        #         "label": "Real State"
        #     }
        #     all_messages.append(message_dict)

        #     # Break loop if total_messages limit is reached
        #     total_messages = len(all_messages)
        #     if total_count_limit != 0 and total_messages >= total_count_limit:
        #         break

        # # Construct the final output
        # output = {
        #     "name": "Beton: Rentals 🇪🇹",  # Replace with the actual name if available
        #     "id": channel_id,
        #     "messages": all_messages
        # }

        # # Convert the output to JSON and write it to a file
        # with open('የኮንስትራክሽን_እቃዎች_አቅራቢ_construction_Materials_supplier.json', 'w', encoding='utf-8') as outfile:
        #     json.dump(output, outfile, ensure_ascii=False, indent=2)

        ##new##

    with open('Orkid_Design_&_Pillow.json', 'w', encoding='utf-8') as outfile:
        json.dump(all_messages, outfile, cls=DateTimeEncoder, ensure_ascii=False, indent=2)


with client:
    client.loop.run_until_complete(main(phone))
