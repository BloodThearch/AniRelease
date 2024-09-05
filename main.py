import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from pymongo import MongoClient
import asyncio
import pickle

from src.logging import createLog
from src.getOngoing import getOngoing


# INIT ENV VARIABLES
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_URI = os.getenv('MONGO_URI')

# SETUP DB
dbClient = MongoClient(MONGO_URI)
db = dbClient['AniRelease']
collection = db['server_channels']

# SETUP BOT
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# FUNCTIONALITY
async def sendMsg(msg, usrMsg):
    if not usrMsg:
        e = 'empty msg, intents might not be enabled.'
        print(e)
        createLog(e)
        return
    
    if usrMsg.lower()[0:6] == "ar!set":
        try:
            # Get the channel ID
            channelID = int(usrMsg[6:].strip().split(" ")[0])
            channel = client.get_channel(channelID)

            # Get server id
            serverID = msg.guild.id

            # SET CHANNEL
            if channel is not None:
                # Store or update the serverID with the corresponding channelID
                collection.update_one(
                    {'serverID': serverID},
                    {'$set': {'channelID': channelID}},
                    upsert=True
                )
                await msg.channel.send(f"Channel set to {channelID}.")
            else:
                await msg.channel.send("Channel not found.")

        except Exception as e:
            print(e)
            createLog(e)

    if usrMsg.lower() == "ar!update":
        try:
            response = getOngoing()
            content = "Here is a list of recently aired anime:\n"+"\n".join([" - ".join(r) for r in response])
            await msg.channel.send(content)
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

# LOOPING FUNCTIONS

async def updateLoop():
    try:
        while(True):
            currentState = getOngoing()
            if not os.path.exists("oldState.pkl") or os.path.getsize("oldState.pkl") == 0:
                with open("oldState.pkl", 'wb') as file:
                    pickle.dump(currentState, file)
                records = collection.find()
                channelIDs = [record['channelID'] for record in records]
                channels = [client.get_channel(channelID) for channelID in channelIDs]

                content = "\n".join([" - ".join(r) for r in currentState])
                coroutines = [channel.send(content) for channel in channels]
                await asyncio.gather(*coroutines)
            with open("oldState.pkl", 'rb') as file:
                oldState = pickle.load(file)
            oldStateTemp = [record[0] for record in oldState]
            if len(oldState)>0:
                differenceList = [item for item in currentState if item[0] not in oldStateTemp]
                if len(differenceList)>0:
                    records = collection.find()
                    channelIDs = [record['channelID'] for record in records]
                    channels = [client.get_channel(channelID) for channelID in channelIDs]

                    content = "\n".join([" - ".join(r) for r in differenceList])
                    oldState = currentState
                    with open("oldState.pkl", 'wb') as file:
                        pickle.dump(currentState, file)
                    coroutines = [channel.send(content) for channel in channels]
                    await asyncio.gather(*coroutines)
            await asyncio.sleep(300)
    except Exception as e:
        createLog(e)
        print(e)
            

# APIs
@client.event
async def on_ready():
    print(f"{client.user} is now running.")
    client.loop.create_task(updateLoop())

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