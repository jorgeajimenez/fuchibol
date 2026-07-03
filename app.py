import json
from flask import Flask, jsonify, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/simulator")
def simulator():
    return render_template("simulator.html")

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
        note = note.replace("FIFA World Cup", "Fuchibol Cup")
        name = event.get("name") or ""
        name = name.replace("FIFA World Cup", "Fuchibol Cup")

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

@app.route("/api/players")
def get_players():
    try:
        with open("scoreboard.json") as f:
            data = json.load(f)
    except Exception:
        return jsonify({"error": "scoreboard.json not found"}), 404

    players_by_team = {}
    for event in data.get("events", []):
        comp = event.get("competitions", [{}])[0]
        for detail in comp.get("details", []):
            for ath in detail.get("athletesInvolved", []):
                team_info = ath.get("team", {})
                team_id = team_info.get("id")
                ath_id = ath.get("id")
                if team_id and ath_id:
                    if team_id not in players_by_team:
                        players_by_team[team_id] = {}
                    players_by_team[team_id][ath_id] = {
                        "id": ath_id,
                        "name": ath.get("displayName"),
                        "jersey": ath.get("jersey"),
                        "position": ath.get("position"),
                    }
                    
    result = {}
    for team_id, players_dict in players_by_team.items():
        result[team_id] = list(players_dict.values())
        
    return jsonify(result)

@app.route("/api/previous_matches")
def get_previous_matches():
    try:
        with open("scoreboard.json") as f:
            data = json.load(f)
    except Exception:
        return jsonify({"error": "scoreboard.json not found"}), 404

    matches = []
    for event in data.get("events", []):
        comp = event.get("competitions", [{}])[0]
        status = event.get("status", {}).get("type", {}).get("name")
        teams = []
        for competitor in comp.get("competitors", []):
            team_info = competitor.get("team", {})
            logo = team_info.get("logo")
            if team_info.get("displayName") == "Netherlands" or team_info.get("abbreviation") == "NED" or team_info.get("id") == "449":
                logo = "/holland_lop.jpg"
            
            stats = {}
            for stat in competitor.get("statistics", []):
                stats[stat.get("name")] = {
                    "abbreviation": stat.get("abbreviation"),
                    "displayValue": stat.get("displayValue")
                }

            teams.append({
                "id": team_info.get("id"),
                "name": team_info.get("displayName"),
                "abbr": team_info.get("abbreviation"),
                "logo": logo,
                "score": competitor.get("score"),
                "winner": competitor.get("winner", False),
                "stats": stats
            })

        timeline = []
        for d in comp.get("details", []):
            ath_list = []
            for ath in d.get("athletesInvolved", []):
                ath_list.append({
                    "name": ath.get("displayName"),
                    "position": ath.get("position")
                })
            timeline.append({
                "type": d.get("type", {}).get("text"),
                "clock": d.get("clock", {}).get("displayValue"),
                "teamId": d.get("team", {}).get("id"),
                "athletes": ath_list
            })

        name = event.get("name") or ""
        name = name.replace("FIFA World Cup", "Fuchibol Cup")

        matches.append({
            "id": event.get("id"),
            "name": name,
            "date": event.get("date"),
            "status": status,
            "teams": teams,
            "timeline": timeline
        })
    return jsonify(matches)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
