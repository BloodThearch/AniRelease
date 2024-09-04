import os
from dotenv import load_dotenv
from discord import Intents, Client, Message

from src.logging import createLog
from src.getOngoing import getOngoing

# INIT ENV VARIABLES
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# SETUP BOT
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# MSG FUNCTIONALITY
async def sendMsg(msg, usrMsg):
    if not usrMsg:
        e = 'empty msg, intents might not be enabled.'
        print(e)
        createLog(e)
        return
    
    if usrMsg.lower()[0:6] == "ar!set":
        try:
            response = getOngoing()
            channelID = int(usrMsg[6:].strip().split(" ")[0])
            channel = client.get_channel(channelID)

            content = "Here is a list of recently aired anime:\n"+"\n".join([" - ".join(r) for r in response])
            await channel.send(content)
        except Exception as e:
            print(e)
            createLog(e)

    if usrMsg.lower() == "ar!update":
        try:
            response = getOngoing()
            content = "Here is a list of recently aired anime:\n"+"\n".join([" - ".join(r) for r in response])
            await msg.channel.send(content)
            # channel = client.get_channel(535131978039689216)
            # await channel.send(content)
        except Exception as e:
            print(e)
            createLog(e)
    
    if usrMsg.lower() == "ar!help":
        try:
            response = getOngoing()
            with open("src/help.txt",'r') as f:
                content = f.read()
            await msg.channel.send(content)
        except Exception as e:
            print(e)
            createLog(e)

# APIs
@client.event
async def on_ready():
    print(f"{client.user} is now running.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)
    await sendMsg(message,user_message)


# MAIN ENTRY POINT
def main():
    client.run(token=DISCORD_TOKEN)

if __name__ == "__main__":
    main()