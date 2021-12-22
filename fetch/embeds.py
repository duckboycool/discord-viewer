import sys
import os
import time
import json
import requests

embeds = {''}

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

if not os.path.isdir(f"{sys.path[0]}/{channel}/embeds"):
	os.mkdir(f"{sys.path[0]}/{channel}/embeds")

i = 0
n = 0
# Fetch loop
for message in messages:
    for embed in message["embeds"]:
        typ = embed["type"]

        url = ''

        if typ == "gifv":
            url = embed["video"]["url"]

        elif typ == "image":
            url = embed["url"]
        
        elif "thumbnail" in embed:
            url = embed["thumbnail"]["url"]
        
        elif "image" in embed:
            url = embed["image"]["url"]

        if url not in embeds:
            for retry in range(3, -1, -1):
                r = requests.get(url)

                # Retry on fail
                if not r.ok:
                    if retry:
                        print(f"Failed to get {url} with code {r.status_code}, retrying {retry} time(s)...")
                        time.sleep(1)
                    
                    else:
                        print("Failed, continuing to next file")

                else:
                    # Save embed if successful
                    with open(f"{sys.path[0]}/{channel}/embeds/{requests.utils.quote(url, safe='')}", "wb") as file:
                        file.write(r.content)
                    
                    embeds.add(url)
                    n += 1
                    break

        # Sleep to prevent ratelimit
        time.sleep(0.5)

    i += 1
    if not (i % 100):
        print(f"Searched {i} messages, and grabbed {n} embeds")

print(f"Finished {i} messages with {n} embeds")
