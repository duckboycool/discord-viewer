// This file is required by the index.html file and will
// be executed in the renderer process for that window.

/* Potential TODO
 * Allow for local emoji to be displayed
 * Allow for local user/channel data to fill in ids
 * General markdown support
 * Other search options (filters/non-exact query)
 */

// Some of this should probably be in main but whatver
const fs = require('fs');

// Icon start path
const cdn = "https://cdn.discordapp.com/";
const channel = ""
const local = "file://" + __dirname + "/fetch/" + channel + '/';

const avatars = fs.existsSync(__dirname + "/fetch/" + channel + "/avatars");
const attachments = fs.existsSync(__dirname + "/fetch/" + channel + "/attachments");

// Read message data from local file
var messageData = JSON.parse(fs.readFileSync('fetch/' + channel + '/messages.json', 'utf8'));

var messages = document.getElementById('messages');
var searchoutput = document.getElementById('searchout');

// Event to jump to the associated message
jump = (event) => {
    var id = event.target.id;

    if (id == '') {
        id = event.target.parentNode.id;
    }
    if (id == '') {
        id = event.target.parentNode.parentNode.id;
    }

    var reps = 1;

    for (var j = 0; j < messageData.length; j++) {
        if (messageData[j]['id'] == id) {
            break;
        }

        if (messageData[j]['referenced_message']) {
            reps++;
        }
    }

    while (i <= Math.min((j + 20), messageData.length)) {
        addMessage(i);
        i++;
    }

    messages.childNodes[j + reps].scrollIntoView();
};

/* Function that adds a message to the list of nodes in an element
 * Currently nodes are never removed and stay loaded
 * Jumpable means that the message will jump when clicked, and only had content
 */
function addMessage(index, dst = messages, jumpable = false) {
    m = messageData[index];
    
    // Create elements of message
    var message = document.createElement("div");

    var icon = document.createElement("img");
    var content = document.createElement("span");

    var name = document.createElement("h3");
    var time = document.createElement("h5");
    var text = document.createElement("p");

    // Combine elements
    message.appendChild(icon);
    message.appendChild(content);

    content.appendChild(name);
    content.appendChild(time);
    content.appendChild(text);

    // Message content field
    if (m['content']) {
        text.textContent = m['content'];
    }

    /* Attachment field
     * Loop through message attachments and add the appropriate type
     */
    if (m['attachments'].length && !jumpable) {
        m['attachments'].forEach(attachment => {
            var att;
            var type;

            // Get main type of content (e.g. video/audio/image)
            if (attachment['content_type']) type = attachment['content_type'].split('/')[0];
            else type = "image"; // Sure, good enough

            // Handle type
            if (type == "image") {
                att = document.createElement("img");

                if (attachments) att.src = local + 'attachments/' + encodeURIComponent(encodeURIComponent(attachment['url']));
                else att.src = attachment['url'];
            } else if (type == "video" || type == "audio") {
                att = document.createElement(type);
                att.setAttribute("controls", "");
    
                var media = document.createElement("source");
                
                if (attachments) media.src = local + 'attachments/' + encodeURIComponent(encodeURIComponent(attachment['url']));
                else media.src = attachment['url'];
    
                media.type = attachment['content_type'];
                att.appendChild(media);
            } else {
                att = document.createElement("a");
                att.href = attachment['url'];
                att.textContent = attachment['url'];
                att.target = "_blank";
            }
            
            att.width = Math.min(attachment['width'], 800);
            if (attachment['height'] > 1000) att.width *= 1000/attachment['height'];
            
            att.className = "attachment";
            content.appendChild(att); 
        });
    }

    /* Attachment field
     * Loop through message embeds and add the appropriate type from remote source
     * Images/gifs only currently
     */
    if (m['embeds'].length && !jumpable) {
        m['embeds'].forEach(embed => {
            var emb;

            var type = embed['type'];

            if (type == "gifv") {
                emb = document.createElement("video");
                emb.setAttribute("autoplay", "");
                emb.setAttribute("loop", "");

                var media = document.createElement("source");
                media.src = embed['video']['url'];

                media.type = "video/mp4";
                emb.appendChild(media);
            } else if (type == "image") {
                emb = document.createElement("img");
                emb.src = embed['url'];
            }
            
            if (emb) {
                if (embed['video']) {
                    emb.width = Math.min(embed['video']['width'], 800);
                } else {
                    emb.width = Math.min(embed['thumbnail']['width'], 800);
                }

                emb.className = "embed";
                content.appendChild(emb);
            }
        });
    }

    /* Message reply field
     * Shows message that the current message is a reply to above
     */
    if (m['referenced_message'] && !jumpable) {
        var replied = document.createElement("div");
        var ref = m['referenced_message'];

        var reficon = document.createElement("img");
        var refname = document.createElement("h4");
        var reftext = document.createElement("p");
        
        if (avatars) {
            reficon.src = local + "avatars/" + ref['author']['id'] + ".webp";
        } else {
            if (ref['author']['avatar']) reficon.src = cdn + "avatars/" + ref['author']['id'] + "/" + ref['author']['avatar'] + ".webp?size=80";
            else reficon.src = cdn + "embed/avatars/" + ref['author']['discriminator'] % 5 + ".png"
        }

        reficon.width = 24;

        refname.textContent = ref['author']['username'];

        reftext.textContent = ref['content'];

        reficon.className = 'reply';
        refname.className = 'reply';
        reftext.className = 'reply';

        replied.appendChild(reficon);
        replied.appendChild(refname);
        replied.appendChild(reftext);
        replied.className = 'reply';
        replied.id = ref['id']

        dst.appendChild(replied);

        // Make reply jumpable
        replied.addEventListener("click", jump);
    }

    // Set name, pfp, and time (UTC only currently)
    name.textContent = m['author']['username'];

    ts = m['timestamp'];
    time.textContent = ts.substring(0, 10) + " " + ts.substring(11, 23);

    if (avatars) {
        icon.src = local + "avatars/" + m['author']['id'] + ".webp";
    } else {
        // Get remote avatar if not fetched (custom/default)
        if (m['author']['avatar']) icon.src = cdn + "avatars/" + m['author']['id'] + "/" + m['author']['avatar'] + ".webp?size=80";
        else icon.src = cdn + "embed/avatars/" + m['author']['discriminator'] % 5 + ".png"
    }

    icon.width = 48;

    icon.className = "logo";

    text.className = "content";
    
    message.className = "message";
    dst.appendChild(message);

    // Add jump event if applicable
    if (jumpable) {
        message.id = m['id'];
        message.addEventListener("click", jump);
    }
}

// Load first 100 messages
for (var i = 0; i < Math.min(100, messageData.length); i++) {
    addMessage(i);
}

/* Search function
 * Takes a query and returns index of next message containing an exact match from start
 */
function search(query, start = 0) {
    query = query.toUpperCase();

    for (var i = start; i < messageData.length; i++) {
        var content = messageData[i]['content'].toUpperCase();
        
        if (content.indexOf(query) != -1) {
            return i;
        }
    }

    return null;
}

// Scroll event, load new images when near bottom
window.addEventListener("scroll", () => {
    if ((document.body.clientHeight - 1080) - this.scrollY < 640) {
        for (var j = i; j < (i + 20) && j < messageData.length; j++) {
            addMessage(i);
            j++;
            i++;
        }
    }
});

// Do search when button is clicked
document.querySelector('#searchbutton').addEventListener("click", () => {
    searchoutput.innerHTML = '';

    var query = document.getElementById('searchbox').value;
    var res = parseInt(document.getElementById('startbox').value);
    if (isNaN(res)) res = 0;
    var num = 0;

    while (num < 12) {
        var res = search(query, res);

        if (res != null) {
            addMessage(res, searchoutput, true);
            res++;
            num++;
        } else {
            break;
        }
    }

    document.getElementById('startbox').value = res;
});
