import csv
import random
from yt_dlp import YoutubeDL as yt
import webbrowser

Input = "Watch later-videos.csv"
WatchNow = "WatchNow.csv"

## Extract title, duration and upload date.


# Reads the CSV file and stores it in a dictionary
with open(Input, mode="r") as file:
    csv_fields = csv.DictReader(file)
    csv_data = []
    # Stores each dictionary in a list
    for row in csv_fields:
        csv_data.append(row)
# Chooses random dictionary off list
RandomValue = random.choice(csv_data)
# Gets Video ID from dictionary
RandomVideo = RandomValue.get("Video ID")
# Opens Video ID in Browser as Youtube URL
webbrowser.open_new_tab("https://www.youtube.com/watch?v=" + RandomVideo)
