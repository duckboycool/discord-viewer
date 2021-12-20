import sys
import os
import time
import json
import requests

avatars = set()

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

if not os.path.isdir(f"{sys.path[0]}/{channel}/avatars"):
	os.mkdir(f"{sys.path[0]}/{channel}/avatars")

# Fetch loop
for message in messages:
    # User has new avatar set
    if message['author']['id'] not in avatars:
        for retry in range(3, -1, -1):
            if message['author']['avatar']:
                r = requests.get(f"https://cdn.discordapp.com/avatars/{message['author']['id']}/{message['author']['avatar']}.webp?size=80")
            
            else:
                # Get correct defautl avatar if avatar is null
                r = requests.get(f"https://cdn.discordapp.com/embed/avatars/{int(message['author']['discriminator']) % 5}.png?size=80")

            # Retry on fail
            if not r.ok:
                if retry:
                    print(f"Failed to get {message['author']['id']} with code {r.status_code}, retrying {retry} time(s)...")
                    time.sleep(0.5)
                
                else:
                    print("Failed, continuing to next avatar")

            else:
                # Save avatar if successful
                with open(f"{sys.path[0]}/{channel}/avatars/{message['author']['id']}.webp", "wb") as file:
                    file.write(r.content)
                
                break
        
        # Add avatar to set (even if failed, so it doesn't retry more)
        avatars.add(message['author']['id'])

        # Sleep to prevent ratelimit
        time.sleep(0.5)
    
print(f"Finished with {len(avatars)} avatars")
