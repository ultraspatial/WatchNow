import os
import csv
import re
from datetime import datetime
from flask import Flask, render_template_string
import urllib.parse

app = Flask(__name__)

CSV_FILENAME = os.path.join(os.path.dirname(__file__), "WatchNow.csv")

def extract_video_id(value: str):
    """Extract a YouTube video ID from many common formats."""
    if not value:
        return None
    value = value.strip()
    # direct 11-char ID
    m = re.match(r'^[A-Za-z0-9_-]{11}$', value)
    if m:
        return value
    # try parsing as URL
    parsed = urllib.parse.urlparse(value)
    qs = urllib.parse.parse_qs(parsed.query)
    if 'v' in qs and qs['v']:
        return qs['v'][0]
    # youtu.be or /embed/ or last path segment
    path_seg = parsed.path.rstrip('/').split('/')[-1]
    if path_seg and re.match(r'^[A-Za-z0-9_-]{11}$', path_seg):
        return path_seg
    # fallback: find any 11-char token in string
    m2 = re.search(r'([A-Za-z0-9_-]{11})', value)
    return m2.group(1) if m2 else None

def format_duration(seconds: int) -> str:
  """Format seconds as H:MM:SS or M:SS."""
  if seconds is None:
    return ''
  h, rem = divmod(int(seconds), 3600)
  m, s = divmod(rem, 60)
  if h:
    return f"{h}:{m:02}:{s:02}"
  return f"{m}:{s:02}"


def format_upload_date(datestr: str) -> str:
  """Parse dates in YYYYMMDD (or similar) and return a readable date like 'YYYY-MM-DD' or 'Month D, YYYY'."""
  if not datestr:
    return ''
  for fmt in ("%Y%m%d", "%Y-%m-%d", "%Y/%m/%d"):
    try:
      dt = datetime.strptime(datestr, fmt)
      return dt.strftime("%Y-%m-%d")
    except Exception:
      continue
  # fallback: return raw
  return datestr


def load_csv(path):
  entries = []
  if not os.path.exists(path):
    return entries
  with open(path, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
      vid_raw = row.get('VideoID') or row.get('videoid') or row.get('video_id') or ''
      vid = extract_video_id(vid_raw)
      if vid:
        row['youtube_url'] = f'https://www.youtube.com/watch?v={vid}'
        row['embed_url'] = f'https://www.youtube.com/embed/{vid}'
      else:
        row['youtube_url'] = None
        row['embed_url'] = None

      # normalize and create display fields for duration and upload date
      duration_raw = (row.get('duration') or row.get('Duration') or '').strip()
      try:
        duration_secs = int(duration_raw) if duration_raw else None
      except ValueError:
        duration_secs = None
      row['duration_seconds'] = duration_secs
      row['duration_display'] = format_duration(duration_secs) if duration_secs is not None else None

      upload_raw = (row.get('upload_date') or row.get('Upload_Date') or row.get('uploadDate') or '').strip()
      row['upload_date_display'] = format_upload_date(upload_raw) if upload_raw else None

      entries.append(row)
  return entries


ENTRIES = load_csv(CSV_FILENAME)

TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>WatchNow</title>
  <style>
    body{font-family: Arial, sans-serif; margin:20px}
    .item{margin-bottom:24px}
    iframe{max-width:560px; width:100%; height:315px; border:0}
  </style>
</head>
<body>
  <h1>WatchNow</h1>
  {% if entries %}
    {% for e in entries %}
      <div class="item">
        {% set title = e.get('Title') or e.get('title') or e.get('Name') or 'Untitled' %}
        {% if e.youtube_url %}
          <h3><a href="{{ e.youtube_url }}" target="_blank" rel="noopener">{{ title }}</a></h3>
        {% else %}
          <h3>{{ title }}</h3>
        {% endif %}
        <div class="meta">
          {% if e.get('duration_display') %}
            <strong>Duration:</strong> {{ e.get('duration_display') }}
          {% endif %}
          {% if e.get('upload_date_display') %}
            {% if e.get('duration_display') %} &middot; {% endif %}
            <strong>Uploaded:</strong> {{ e.get('upload_date_display') }}
          {% endif %}
        </div>
        {% if not e.youtube_url %}
          <em>No valid VideoID / URL</em>
        {% endif %}
      </div>
    {% endfor %}
  {% else %}
    <p>No entries found (check WatchNow.csv)</p>
  {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE, entries=ENTRIES)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)