import csv

Output = "WatchNow.csv"


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
    StoreOutputCSV(Output)
