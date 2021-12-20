import sys
import os
import time
import json
import requests

messages = []

# Number of messages to fetch (None gets all)
NUM = None

# Read token from file "token.txt"
with open(sys.path[0] + "/token.txt") as file:
	TOKEN = "Bot " + file.read()

# Get channel id from last argument
if len(sys.argv) > 1:
	try:
		channel = int(sys.argv[-1])

	except ValueError:
		print("Input channel ID is not an integer.")
		sys.exit(1)

else:
	print("Please input a channel ID as last argument.")
	sys.exit(1)

try:
	NAME = requests.get(f"https://discord.com/api/v9/channels/{channel}", headers={"authorization": TOKEN}).json()["name"]

except KeyError:
	print("Could not find channel with input ID.")
	sys.exit(1)

# Fetch loop
while not(NUM) or len(messages) < NUM:
	# ID to start fetching from
	next_id = messages[0]['id'] if messages else 0

	# Request for 100 messages
	r = requests.get(f"https://discord.com/api/v9/channels/{channel}/messages?after={next_id}&limit=100", headers={"authorization": TOKEN})

	if not r.ok:
		print(f"Failed with code {r.status_code}, retrying...")
		time.sleep(3)

	else:
		# Append messages if successful
		data = r.json()
		
		if data:
			messages = r.json() + messages
			print(f"{len(messages)} messages fetched")
		
		else:
			print(f"Did not find any messages past {len(messages)}, exiting...")
			break

	# Sleep to prevent ratelimit
	time.sleep(1)

# Make output file
if not os.path.isdir(f"{sys.path[0]}/{NAME}"):
	os.mkdir(f"{sys.path[0]}/{NAME}")

with open(f"{sys.path[0]}/{NAME}/messages.json", "w") as file:
    json.dump(messages[::-1], file)
