import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, Embed, Color
from discord.ext import tasks
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
            print(usrMsg)
            # Get the channel ID
            # Get server id
            serverID = msg.guild.id
            channelID = msg.channel.id

            # SET CHANNEL
            # Store or update the serverID with the corresponding channelID
            collection.update_one(
                {'serverID': serverID},
                {'$set': {'channelID': channelID}},
                upsert=True
            )
            await msg.channel.send(f"Channel set to {channelID}.")

        except Exception as e:
            print(e)
            createLog(e)
    
    if usrMsg.lower()[0:8] == "ar!clear":
        try:
            # Get the server ID
            print(usrMsg)
            serverID = msg.guild.id

            # Clear channels of that server
            result = collection.delete_many({"serverID": serverID})
            await msg.channel.send("All registered channels of this server has been cleared from registration.")

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
            # response = getOngoing()
            with open("src/help.txt",'r') as f:
                content = f.read()
            await msg.channel.send(content)
        except Exception as e:
            print(e)
            createLog(e)

# LOOPING FUNCTIONS

@tasks.loop(minutes=15)
async def updateLoop():
    try:
        currentState = getOngoing()
        currentSet = set(tuple(item) for item in currentState)
        records = collection.find()
        channelIDs = [record['channelID'] for record in records]
        channels = [client.get_channel(channelID) for channelID in channelIDs]
        if not os.path.exists("oldState.pkl") or os.path.getsize("oldState.pkl") == 0:
            with open("oldState.pkl", 'wb') as file:
                pickle.dump(currentState, file)
            for title, episode, image_url in currentState:
                embed = Embed(
                    title=title.replace("- ", "").strip(),
                    description=f"Current episode: **{episode}**",
                    color=Color.blue()
                )
                embed.set_image(url=image_url)
                embed.set_footer(text="Initial update from MyAnimeList")
                # embed.set_thumbnail(url=image_url)

                coroutines = [channel.send(embed=embed) for channel in channels if channel]
                await asyncio.gather(*coroutines)
        else:
            with open("oldState.pkl", 'rb') as file:
                oldState = pickle.load(file)
            oldSet = set(tuple(item) for item in oldState)
            differenceSet = currentSet - oldSet
            if differenceSet:
                differenceList = [list(item) for item in differenceSet]                
                with open("oldState.pkl", 'wb') as file:
                    pickle.dump(currentState, file)
        
                
                for title, episode, image_url in differenceList:
                    embed = Embed(
                        title=title.replace("- ", "").strip(),
                        description=f"New episode released: **{episode}**",
                        color=Color.purple()  # You can change the color
                    )
                    embed.set_image(url=image_url)
                    embed.set_footer(text="Auto-update from MyAnimeList")
                    # embed.set_thumbnail(url=image_url)

                    coroutines = [channel.send(embed=embed) for channel in channels if channel]
                    await asyncio.gather(*coroutines)

    except Exception as e:
        createLog(e)
        print(e)            

# APIs
@client.event
async def on_ready():
    print(f"{client.user} is now running.")
    if not updateLoop.is_running():
        updateLoop.start()

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