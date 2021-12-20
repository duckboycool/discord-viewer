import sys
import os
import time
import json
import requests

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

if not os.path.isdir(f"{sys.path[0]}/{channel}/attachments"):
	os.mkdir(f"{sys.path[0]}/{channel}/attachments")

i = 0
n = 0
# Fetch loop
for message in messages:
    for att in message["attachments"]:
        for retry in range(3, -1, -1):
            r = requests.get(att["url"])

            # Retry on fail
            if not r.ok:
                if retry:
                    print(f"Failed to get {att['url']} with code {r.status_code}, retrying {retry} time(s)...")
                    time.sleep(0.5)
                
                else:
                    print("Failed, continuing to next file")

            else:
                # Save attachment if successful
                with open(f"{sys.path[0]}/{channel}/attachments/{requests.utils.quote(att['url'], safe='')}", "wb") as file:
                    file.write(r.content)
                
                n += 1
                break

        # Sleep to prevent ratelimit
        time.sleep(0.5)
    
    i += 1
    if not (i % 100):
        print(f"Searched {i} messages, and grabbed {n} attachments")

print(f"Finished {i} messages with {n} attachments")
