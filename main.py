import discord
import os # the os module is used to access environment variables (in this case, the bot token)
from dotenv import load_dotenv # the dotenv module is used to load environment variables from a .env file
import requests # the requests module is used to make HTTP requests to the API
import json # the json module is used to parse JSON responses into Python dictionaries
import random # the random module is used to choose a random item from a list

load_dotenv() # load the environment variables from the .env file

intents = discord.Intents.default() # create the default intents object; intents are like permissions for the bot
intents.message_content = True # set the message_content intent to True so we can access message content

client = discord.Client(intents=intents) # we create a new discord client, this is the connection to discord; we pass in the intents object so the bot can access message content

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"] # a list of sad words

def get_encouragements(message):
    return [
        f"Cheer up, {message.author.mention}!",
        f"Hang in there, {message.author.mention}!",
        f"You are a great person, {message.author.mention}!"
    ]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random") # make a get request to the API
    json_data = json.loads(response.text) # convert the response to a Python dictionary
    quote = json_data[0]['q'] + " -" + json_data[0]['a'] # get the quote and the author from the dictionary
    return(quote) # return the quote

@client.event # we use this decorator to register an event
async def on_ready(): # the on_ready event is called when the bot has finished logging in and setting things up
    print("Logged in as {0.user}".format(client)) # we print the bot's username once it is logged in
    
@client.event # another event
async def on_message(message): # called when a message is sent to a channel the bot has access to
    if message.author == client.user: # ignore messages from the bot itself
        return # return from the function so we don't do anything
    
    if message.content.startswith("$Hello"): # if the message starts with "Hello"
        await message.channel.send("Hello!") # send a message in the same channel with "Hello!"
    
    if message.content.startswith("$Inspire"):
        quote = get_quote()
        await message.channel.send(quote)
        
    if any(word in message.content for word in sad_words): # if any of the words in the sad_words list are in the message
        await message.channel.send(random.choice(get_encouragements(message))) # send a random encouraging message from the starter_encouragements list
        
client.run(os.getenv("TOKEN")) # run the bot with the token from the environment variables
