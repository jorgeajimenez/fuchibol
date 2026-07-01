import urllib.request
import json

url = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates=20260611-20260719&limit=950"
try:
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode())
    with open("scoreboard.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Downloaded successfully! Found {len(data.get('events', []))} events.")
except Exception as e:
    print(f"Error downloading: {e}")
