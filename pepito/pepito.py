import requests
import json
from datetime import datetime
import discord
from discord.ext import tasks
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
global responseold
@client.event
async def on_ready():
	task_loop.start() # important to start the loop
	print(f'We have logged in as {client.user}')

@tasks.loop(seconds=15)
async def task_loop():
	channel = client.get_channel(1525694299881083021)
	global responseold

	response = requests.get("https://api.thecatdoor.com/rest/v1/last-status")
	responsejson = response.json()
	if 'responseold' not in globals():
			print("first run, just saving pepito info")
			responseold = "empty"
	else:
			if responsejson['type'] != responseold:
				print(f"RESPONSEOLD={responseold}")
				print(f"RESPONSE={responsejson}")
				responseold = responsejson['type']
				embed = discord.Embed()
				embed.set_image(url=responsejson['img'])
				if responsejson['type'] == 'in':
					pepitocurrently = 'returned home!\nHe came home about'
				else:
					pepitocurrently = 'gone for an adventure.\nHe was last seen about'
				await channel.send(f'Pepito has {pepitocurrently} <t:{responsejson['time']}:R> (<t:{responsejson['time']}:t>)', embed=embed)
			else:
				print(f"no reason to update he hasnt changed ({responsejson['type']})")
@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('!pepito'):
		response = requests.get("https://api.thecatdoor.com/rest/v1/last-status")
		response = response.json()
		embed = discord.Embed()
		embed.set_image(url=response['img'])
		if response['type'] == 'in':
			pepitocurrently = 'in his home'
		else:
			pepitocurrently = 'out on an adventure'
		await message.channel.send(f'Pepito is currently {pepitocurrently}.\nHe was last seen about <t:{response['time']}:R> (<t:{response['time']}:t>)', embed=embed)

client.run(os.environ['BOT_TOKEN'])




