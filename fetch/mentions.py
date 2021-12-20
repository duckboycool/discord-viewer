import sys
import time
import json
import re
import requests

mentions = {}

# Read token from file "token.txt"
with open(sys.path[0] + "/token.txt") as file:
	TOKEN = "Bot " + file.read()

# Get channel name from last argument
if len(sys.argv) > 1:
    channel = sys.argv[-1]

else:
	print("Please input a fetched channel name as last argument.")
	sys.exit(1)

try:
    with open(f"{sys.path[0]}/{channel}/messages.json") as file:
        messages = json.load(file)

except FileNotFoundError:
	print("Could not find channel with input name. Make sure that its messages have already been fetched.")
	sys.exit(1)

finder = re.compile("<([#@])!?(\d+)>")

i = 0
n = 0
# Fetch loop
for message in messages:
    for typ, mention in finder.findall(message["content"]):
        if mention in mentions: continue

        for retry in range(3, -1, -1):
            if typ == "@":
                r = requests.get(f"https://discord.com/api/v9/users/{mention}", headers={"authorization": TOKEN})
            elif typ == "#":
                r = requests.get(f"https://discord.com/api/v9/channels/{mention}", headers={"authorization": TOKEN})

            # Retry on fail
            if not r.ok:
                if retry:
                    print(f"Failed to get {typ}{mention} with code {r.status_code}, retrying {retry} time(s)...")
                    time.sleep(3)
                
                else:
                    print("Failed, continuing to next mention")
            
            else:
                mentions[mention] = {"type": typ, "name": r.json()["username" if typ == "@" else "name"]}
                n += 1
                break
        
        time.sleep(0.5)
    
    i += 1
    if not (i % 100):
        print(f"Searched {i} messages, and grabbed {n} unique mentions")

print(f"Finished {i} messages with {n} unique mentions")

# Make output file
with open(f"{sys.path[0]}/{channel}/mentions.json", "w") as file:
    json.dump(mentions, file)
