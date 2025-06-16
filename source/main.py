import csv
import random
import webbrowser

WatchLater = 'Watch Later-videos.csv'

# Reads the CSV file and stores it in a dictionary
with open(WatchLater, mode='r') as file:
    csv_reader = csv.DictReader(file)
    data_list = []
    # Stores each dictionary in a list
    for row in csv_reader:
        data_list.append(row)

# Chooses random dictionary off list
RandomValue = random.choice(data_list)
# Gets Video ID from dictionary
RandomVideo = RandomValue.get('Video ID')

webbrowser.open_new_tab('https://www.youtube.com/watch?v='+RandomVideo)