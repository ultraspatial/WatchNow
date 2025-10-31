import csv
import random
import yt_dlp
import webbrowser

Input = "Watch later-videos.csv"
Output = "WatchNow.csv"

ydl_opts = {
    "quiet": True,  # Suppress output to console
    "no_warnings": True,  # Ignore warnings
    "extract_flat": False,  # Extract full info (not just basic metadata)
}


def InputCSVToArray(Input: str):
    # Reads the CSV file and stores it in a dictionary
    with open(Input, mode="r") as file:
        csv_fields = csv.DictReader(file)
        csv_data = []
        # Stores each dictionary in a list
        for row in csv_fields:
            csv_data.append(row)
    print("Converted CSV to Array")
    return csv_data


def ExtractInfoFromID(csv_data):
    extracted_data = []
    for item in csv_data:
        video_id = item["VideoID"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)

                video_info = {
                    "VideoID": video_id,
                    "title": info.get("title"),
                    "duration": info.get("duration"),
                    "upload_date": info.get("upload_date"),
                }
                extracted_data.append(video_info)

        except Exception as e:
            print(f"Error processing {video_id}: {e}")
            # Add entry with None values for failed extraction
            extracted_data.append(
                {
                    "VideoID": video_id,
                    "title": None,
                    "duration": None,
                    "upload_date": None,
                }
            )
    print("Extracted data")
    return extracted_data


def StoreExtractedData(extracted_data):
    keys = extracted_data[0].keys()

    with open(Output, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(extracted_data)
    print(f"Data stored in {Output}")

def StoreOutputCSV(Output):
    # Read the CSV, sort rows by numeric duration (shortest first), and overwrite the file
    with open(Output, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    def _duration_key(row):
        d = row.get("duration")
        if d in (None, "", "None"):
            return float("inf")
        try:
            return int(d)
        except Exception:
            try:
                return int(float(d))
            except Exception:
                return float("inf")

    rows.sort(key=_duration_key)

    if rows:
        fieldnames = rows[0].keys()
        with open(Output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    print(f"Sorted {Output} by duration")


if __name__ == "__main__":
    csv_data = InputCSVToArray(Input)
    extracted_data = ExtractInfoFromID(csv_data)
    StoreExtractedData(extracted_data)
