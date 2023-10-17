import libtorrent as lt
import requests
import tempfile
import os
from tqdm import tqdm
import time

# Create a libtorrent session
ses = lt.session()

# Ask the user for the torrent file URL
torrent_url = input("Enter torrent URL: ")

# Ask the user for the destination path
download_path = input("Enter the path to save: ")

# Ensure the path exists, create it if it doesn't
os.makedirs(download_path, exist_ok=True)

# Download the torrent file
response = requests.get(torrent_url)
if response.status_code == 200:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name
else:
    print("Failed to download the torrent file.")
    sys.exit(1)

# Create a torrent handler from the downloaded file
info = lt.torrent_info(temp_file_path)
os.remove(temp_file_path)  # Remove the temporary file after loading the torrent info
h = ses.add_torrent({'ti': info, 'save_path': download_path})

# Print information about the file
print(f"File Name: {info.name()}")
print(f"File Size: {info.total_size() / 1024:.2f} KB")

# Initialize the progress bar
pbar = tqdm(total=info.total_size(), unit='B', unit_scale=True)

while not h.status().is_seeding:
    s = h.status()
    pbar.update(s.total_download - pbar.n)  # update the progress bar with the current download value
    time.sleep(1)  # wait for 1 second before the next status update

pbar.close()  # close the progress bar after the download is complete
print("\nDownload complete!")
