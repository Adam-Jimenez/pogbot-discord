import os
import random
import json
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

questions = json.loads(open("./questions.json").read())
cur_question = None
state = 0

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global state
    global questions
    global cur_question

    if message.content == '!trivia' and state == 0:
        state = 1
        cur_question = random.choice(questions)
        await message.channel.send(cur_question["question"])

    if state == 1:
        if message.content.strip().lower() == cur_question["answer"].strip().lower():
            state = 0
            await message.channel.send(f"{cur_question['answer']} is correct. Congratulations to {message.author}!")
            await message.channel.send(cur_question["explanation"])

client.run(TOKEN)
