from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from dotenv import load_dotenv
from pathlib import Path
import os
import json

load_dotenv(Path("./userbot/src/configs/.env"))

userbot: Client = Client(
    name=os.environ.get("APP_NAME"),
    api_hash=os.environ.get("API_HASH"),
    api_id=os.environ.get("API_ID")
)

@userbot.on_message(filters.command("alive", prefixes="."))
async def alive(client: Client, message: Message):
    await client.send_message(chat_id=message.chat.id, text=f"Siii !! estoy vivo, no tienes de que preocuparte @{message.from_user.username}")

@userbot.on_message(filters.command("help", prefixes="."))
async def help(client: Client, message: Message):
    commands = {
        "alive": "Ver si el userbot se encuentra funcionando",
        "help": "Recibir este mensaje",
        "search": """Utiliza este comando seguido de un hashtag para buscar todos los textos que lo contengan, seguido del ID/username del usuario al que se le enviara el JSON, ejemplos:\n\n**Para enviarselo a un usuario en especifico: .search #LaHabana 123456789**\n**Para recibirlo el mismo usuario que lo pidio: .search #LaHabana me**""",
    }
    await client.send_message(chat_id=message.chat.id, text=f"Los comandos disponibles son: \nalive - {commands['alive']}\nhelp - {commands['help']}\n.search - {commands['search']}")

@userbot.on_message(filters.command("search", prefixes="."))
async def scrape_menucuba(client: Client, message: Message):
    
    if len(message.text.split(" ")) == 1 or len(message.text.split(" ")) >= 4:
        await client.send_message(chat_id=message.chat.id, text="No ha introducido ningun hashtag o ha introducido mas de 1, el minimo a introducir es 1, introduzca uno")        
    else:
        await client.send_message(chat_id=message.chat.id, text=f"Ok, buscare todos los mensajes que pueda acerca de {message.text.split(" ")[1]}, esto puede tomar un momento, por la limitacion de la API de Telegram, pero seran solo unos segundos")
        
        links: list = []
        async for messages in client.get_chat_history(chat_id=os.environ.get("CHANNEL_USERNAME")):

            if messages.caption:
                if message.text.split(" ")[1] in messages.caption:
                    links.append(f"https://t.me/{os.environ.get("CHANNEL_USERNAME")}/{messages.id}")
                
        schema = {
            "data" : []
        }
                
        if links != []:
            print("All links obtained, now creating and sending JSON")        
            
            with open("data.json", "w") as file:
                file.write(json.dumps({"links": links}, indent=4))
                
            
            await client.send_document(chat_id=message.text.split(" ")[2] if not "me" else message.chat.id, document="data.json", caption=message.id)
            print("JSON already sent")
            os.remove("./data.json")
        
        await client.send_message(chat_id=message.chat.id, text="No se han encontrado links acerca de este hashtag")
        
if __name__ == "__main__":
    print("starting userbot")
    userbot.start()
    print("userbot started")
    userbot.loop.run_forever()