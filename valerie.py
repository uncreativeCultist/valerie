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
	pepito_loop.start()
	print(f'We have logged in as {client.user}')

# START: LOOPS 
# START: PEPITO LOOP 
@tasks.loop(seconds=15)
async def pepito_loop():
	channel = client.get_channel(1525694299881083021)
	global responseold

	response = requests.get("https://api.thecatdoor.com/rest/v1/last-status")
	responsejson = response.json()
	if 'responseold' not in globals():
			print("PEPITO: first run, just saving pepito info")
			#responseold = "empty" 
			responseold = responsejson['type'] # uncomment this and comment the line above to make him not send first pepito message
	else:
			if responsejson['type'] != responseold:
				#print(f"PEPITO: RESPONSEOLD={responseold}")
				#print(f"PEPITO: RESPONSE={responsejson}")
				responseold = responsejson['type']
				embed = discord.Embed()
				embed.set_image(url=responsejson['img'])
				if responsejson['type'] == 'in':
					pepitocurrently = 'returned home!\nHe came home about'
				else:
					pepitocurrently = 'gone for an adventure.\nHe was last seen about'
				await channel.send(f'Pepito has {pepitocurrently} <t:{responsejson['time']}:R> (<t:{responsejson['time']}:t>)', embed=embed)
			#else:
				#print(f"PEPITO: no reason to update he hasnt changed ({responsejson['type']})")
# END: PEPITO LOOP 
# END: LOOPS 

@client.event
async def on_message(message):
	if message.author == client.user:
		return

# START: PEPITO COMMAND 
	if message.content.startswith('!pepito'):
		response = requests.get("https://api.thecatdoor.com/rest/v1/last-status")
		response = response.json()
		if response['type'] == 'in':
			pepitocurrently = 'in his home'
		else:
			pepitocurrently = 'on an adventure'
		embed = discord.Embed(title=f'Pepito is currently {pepitocurrently}.', description=f'He was last seen about <t:{response['time']}:R> (<t:{response['time']}:t>)')
		embed.set_image(url=response['img'])
		await message.channel.send(embed=embed)
# END: PEPITO COMMAND 
# START: RORY COMMAND 
	elif message.content.startswith('!rory'):
		response = requests.get("https://rory.cat/purr")
		response = response.json()
		embed = discord.Embed(title=f"Rory ID: {response['id']}", url=f"https://rory.cat/id/{response['id']}")
		embed.set_image(url=response['url'])
		await message.channel.send(embed=embed)
# END: RORY COMMAND 

client.run(os.environ['BOT_TOKEN'])




