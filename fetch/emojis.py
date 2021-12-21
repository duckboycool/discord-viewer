import sys
import os
import json
import re
import time
import requests

emojis = {None}

# Get channel id from last argument
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

if not os.path.isdir(f"{sys.path[0]}/{channel}/emojis"):
	os.mkdir(f"{sys.path[0]}/{channel}/emojis")

finder = re.compile("<(a?):[^\s:]+:(\d+)>")

reactions = []

i = 0
n = 0
# Emoji fetch loop
for message in messages:
    # Get emoji in reactions
    if "reactions" in message: reactions = [(e["emoji"]["animated"] if "animated" in e["emoji"] else False, e["emoji"]["id"]) for e in message["reactions"]]

    for animated, eid in finder.findall(message["content"]) + reactions:
        if eid in emojis: continue

        for retry in range(3, -1, -1):
            if animated:
                r = requests.get(f"https://cdn.discordapp.com/emojis/{eid}.gif")
            else:
                r = requests.get(f"https://cdn.discordapp.com/emojis/{eid}.png")

            # Retry on fail
            if not r.ok:
                if retry:
                    print(f"Failed to get {eid} with code {r.status_code}, retrying {retry} time(s)...")
                    time.sleep(3)
                
                else:
                    print("Failed, continuing to next emoji")
            
            else:
                # Save attachment if successful
                with open(f"{sys.path[0]}/{channel}/emojis/{eid}.webp", "wb") as file:
                    file.write(r.content)

                emojis.add(eid)
                n += 1
                break
        
        time.sleep(0.5)
    
    i += 1
    if not (i % 100):
        print(f"Searched {i} messages, and grabbed {n} unique emoji")

print(f"Finished {i} messages with {n} unique emoji")
