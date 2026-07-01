import json
from flask import Flask, jsonify, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/holland_lop.jpg")
def serve_holland_lop():
    return send_from_directory(".", "holland_lop.jpg")

@app.route("/api/data")
def get_data():
    try:
        with open("scoreboard.json") as f:
            data = json.load(f)
    except Exception:
        return jsonify({"error": "scoreboard.json not found"}), 404

    events = []
    for event in data.get("events", []):
        comp = event.get("competitions", [{}])[0]
        status = event.get("status", {}).get("type", {}).get("name", "STATUS_SCHEDULED")
        teams = []
        for competitor in comp.get("competitors", []):
            team_info = competitor.get("team", {})
            logo = team_info.get("logo")
            # Override Netherlands (Holland) with the Holland Lop bunny image
            if team_info.get("displayName") == "Netherlands" or team_info.get("abbreviation") == "NED" or team_info.get("id") == "449":
                logo = "/holland_lop.jpg"
            
            teams.append({
                "id": team_info.get("id"),
                "name": team_info.get("displayName"),
                "abbr": team_info.get("abbreviation"),
                "logo": logo,
                "score": competitor.get("score"),
                "winner": competitor.get("winner", False)
            })
        
        note = comp.get("altGameNote") or ""
        note = note.replace("FIFA World Cup", "FeeFa Gorg Cup")
        name = event.get("name") or ""
        name = name.replace("FIFA World Cup", "FeeFa Gorg Cup")

        events.append({
            "id": event.get("id"),
            "name": name,
            "stage": event.get("season", {}).get("slug"),
            "status": status,
            "note": note,
            "date": event.get("date"),
            "teams": teams
        })

    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
