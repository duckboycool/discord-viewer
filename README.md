# discord-viewer

Message viewer for discord optimized for offline/downloaded use and wide feature support.

This viewer is not a client, and you cannot interact in any direct way with servers using it. It also requires fetching messages before use.

## Features
* Includes utility scripts to fetch messages and data.
* Basic UI similar to the discord client's dark mode.
* Support for video, image, and audio attachments.
* Support for direct image/gif embeds.
* Semi-support for discord markdown, including user/channel mention highlighting and spoiler tags.
* Support for custom emoji.
* Support for user logos and message timestamps.
* Support for reactions and message replies.
* Basic exact phrase search function.
* Remote asset fallback if not downloaded.

## Requirements
[Node.JS](https://nodejs.org/en/) and [Electron](https://www.electronjs.org/)

[Python](https://python.org/) 3.6 or newer for fetch scripts.

This is not a hard requirement, but the page does not dynamically adjust for resolution, and will likely display poorly if not on a monitor set to 1080p.

## Use
### Fetch
To get messages, use `fetch/messages.py` (or `fetch/all.py` to additionally get all assets). The script takes a command line argument of the ID of the channel you want to fetch. It will also require a bot token at `fetch/token.txt`. You can get bot tokens at the [Discord Developer Portal](https://discord.com/developers/applications).

Once you have messages, you can run the individual other fetches to choose what data to get.

### View
Currently, you need to manually set the channel name you want to view in the `channel` variable in `renderer.js`. Then, change your directory into `discord-viewer` and run `npm start`.

The viewer itself is pretty intuitive and similar to the discord client in supported features. 

In terms of possible to miss features, you can click on replied messages to jump to the original. There is also a search bar at the right side of the screen, which you use by typing into and then pressing the search button. The box to the right is the starting message index, and will automatically update on a search if it did not reach the end, meaning that presssing search again will show more results.

## Notes
Messages loaded in when near the bottom of the page or jumping to newer messages, and are not unloaded. Jumping also requires loading messages in order, meaning that when jumping to a searched messgae later down in the history, it may take a while to load in. Additionally, markdown for multiline code is currently broken and quotes are not supported. 

---

This is the first major webdev-oriented project I've worked on, and there were certainly some difficulties about it. Overall, even if not super useful, I'm fairly happy with how it's been coming out since it seems fairly usable for its purpose.