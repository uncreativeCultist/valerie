import asyncio
import requests_async
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

	try:
		response = await requests_async.get("https://api.thecatdoor.com/rest/v1/last-status", timeout=5)
		responsejson = response.json()
		return response
	except:
	        print(f"Can't locate Pepito... I think the API is down. :(")
	        return None

	if 'responseold' not in globals():
			print("PEPITO: first run, just saving pepito info")
			#responseold = "empty" 
			responseold = responsejson['type'] # uncomment this and comment the line above to make him not send first pepito message
	else:
			if responsejson['type'] != responseold:
				#print(f"PEPITO: RESPONSEOLD={responseold}")
				#print(f"PEPITO: RESPONSE={responsejson}")
				responseold = responsejson['type']
				embed = discord.Embed(title=f'Pepito has {pepitocurrently}', description=f'{pepitocurrently2} <t:{responsejson['time']}:R> (<t:{responsejson['time']}:t>)')
				embed.set_image(url=responsejson['img'])
				if responsejson['type'] == 'in':
					pepitocurrently = 'returned home!'
					pepitocurrently2 = 'He came home about'
				else:
					pepitocurrently = 'gone for an adventure.'
					pepitocurrently2 = 'He was last seen about'
				await channel.send(embed=embed)
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
		try:
			response = await requests_async.get("https://api.thecatdoor.com/rest/v1/last-status", timeout=5)
			responsejson = response.json()
		except:
		        print(f"Can't locate Pepito... I think the API is down. :(")
		        await message.channel.send("Can't locate Pepito... I think the API is down. :(")
		        return None
		if responsejson['type'] == 'in':
			pepitocurrently = 'in his home'
			pepitocurrently2 = 'He came home about'
		else:
			pepitocurrently = 'on an adventure'
			pepitocurrently2 = 'He was last seen about'
		embed = discord.Embed(title=f'Pepito is currently {pepitocurrently}.', description=f'{pepitocurrently2} <t:{responsejson['time']}:R> (<t:{responsejson['time']}:t>)')
		embed.set_image(url=responsejson['img'])
		await message.channel.send(embed=embed)
# END: PEPITO COMMAND 
# START: RORY COMMAND 
	elif message.content.startswith('!rory'):
		response = await requests_async.get("https://rory.cat/purr", timeout=5)
		responsejson = response.json()
		embed = discord.Embed(title=f"Rory ID: {responsejson['id']}", url=f"https://rory.cat/id/{responsejson['id']}")
		embed.set_image(url=responsejson['url'])
		await message.channel.send(embed=embed)
# END: RORY COMMAND 

client.run(os.environ['BOT_TOKEN'])




