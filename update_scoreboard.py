import urllib.request
import json
import os

def update():
    url = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates=20260611-20260719&limit=1000"
    print(f"Fetching latest tournament data from ESPN API: {url}")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        # Verify it has some events
        if "events" in data:
            num_events = len(data["events"])
            print(f"Successfully fetched {num_events} events.")
            with open("scoreboard.json", "w") as f:
                json.dump(data, f, indent=2)
            print("Successfully updated scoreboard.json!")
            return True
        else:
            print("Error: Fetched data does not contain 'events' field.")
            return False
    except Exception as e:
        print(f"Error fetching data: {e}")
        return False

if __name__ == "__main__":
    update()
