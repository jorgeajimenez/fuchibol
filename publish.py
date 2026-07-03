import os
import json
import shutil

def build():
    # 1. Create docs directory
    dist_dir = "docs"
    os.makedirs(dist_dir, exist_ok=True)
    print("Creating 'docs' folder...")

    # 2. Process scoreboard.json exactly like app.py
    try:
        with open("scoreboard.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading scoreboard.json: {e}")
        return

    events = []
    for event in data.get("events", []):
        comp = event.get("competitions", [{}])[0]
        status = event.get("status", {}).get("type", {}).get("name", "STATUS_SCHEDULED")
        teams = []
        for competitor in comp.get("competitors", []):
            team_info = competitor.get("team", {})
            logo = team_info.get("logo")
            # For static hosting, reference the file locally (relative path)
            if team_info.get("displayName") == "Netherlands" or team_info.get("abbreviation") == "NED" or team_info.get("id") == "449":
                logo = "holland_lop.jpg"
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

    # 3. Read templates/index.html
    try:
        with open("templates/index.html", "r") as f:
            html = f.read()
    except Exception as e:
        print(f"Error reading templates/index.html: {e}")
        return

    # 4. Inline JSON into HTML
    json_string = json.dumps(events, indent=2)
    
    # Exact target match for replacement from templates/index.html
    target_fetch = "rawEvents = /*INLINED_DATA_FALLBACK*/ [];"
    replacement = f"rawEvents = /*INLINED_DATA_FALLBACK*/ {json_string};"

    if target_fetch in html:
        html = html.replace(target_fetch, replacement)
        print("Successfully inlined fallback scoreboard data into index.html!")
    else:
        print("Warning: Could not match exact fallback placeholder. Performing flexible fallback...")
        target_marker = "async function loadRealTimeData() {"
        if target_marker in html:
            html = html.replace(
                target_marker, 
                target_marker + f"\n                rawEvents = {json_string};\n                return;"
            )
            print("Successfully inlined scoreboard data via fallback header!")
        else:
            print("Error: Could not locate loadRealTimeData function in HTML!")
            return

    # 5. Write compiled HTML to docs/index.html
    with open(os.path.join(dist_dir, "index.html"), "w") as f:
        f.write(html)
    print("Wrote compiled HTML to docs/index.html")

    # 6. Parse and compile simulator.html with complete inline databases
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
    players_data = {}
    for team_id, players_dict in players_by_team.items():
        players_data[team_id] = list(players_dict.values())

    matches_data = []
    for event in data.get("events", []):
        comp = event.get("competitions", [{}])[0]
        status = event.get("status", {}).get("type", {}).get("name")
        teams = []
        for competitor in comp.get("competitors", []):
            team_info = competitor.get("team", {})
            logo = team_info.get("logo")
            if team_info.get("displayName") == "Netherlands" or team_info.get("abbreviation") == "NED" or team_info.get("id") == "449":
                logo = "holland_lop.jpg"
            
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

        matches_data.append({
            "id": event.get("id"),
            "name": name,
            "date": event.get("date"),
            "status": status,
            "teams": teams,
            "timeline": timeline
        })

    try:
        with open("templates/simulator.html", "r") as f:
            sim_html = f.read()
    except Exception as e:
        print(f"Error reading templates/simulator.html: {e}")
        return

    sim_html = sim_html.replace("let inlineTeams = /*INLINED_TEAMS_FALLBACK*/ null;", f"let inlineTeams = /*INLINED_TEAMS_FALLBACK*/ {json.dumps(events, indent=2)};")
    sim_html = sim_html.replace("let inlinePlayers = /*INLINED_PLAYERS_FALLBACK*/ null;", f"let inlinePlayers = /*INLINED_PLAYERS_FALLBACK*/ {json.dumps(players_data, indent=2)};")
    sim_html = sim_html.replace("let inlineMatches = /*INLINED_MATCHES_FALLBACK*/ null;", f"let inlineMatches = /*INLINED_MATCHES_FALLBACK*/ {json.dumps(matches_data, indent=2)};")

    with open(os.path.join(dist_dir, "simulator.html"), "w") as f:
        f.write(sim_html)
    print("Wrote compiled HTML to docs/simulator.html")

    # 7. Copy assets
    if os.path.exists("holland_lop.jpg"):
        shutil.copy("holland_lop.jpg", os.path.join(dist_dir, "holland_lop.jpg"))
        print("Copied holland_lop.jpg to docs/ folder.")

    # 8. Create .nojekyll to prevent Jekyll build failures
    with open(os.path.join(dist_dir, ".nojekyll"), "w") as f:
        f.write("")
    print("Created .nojekyll file in docs/ folder.")

    print("\n=======================================================")
    print("SUCCESS: Your fully static site is built inside 'docs/'!")
    print("=======================================================")
    print("This folder now contains everything you need to run serverless:")
    print("  - index.html (with scoreboard data completely inlined)")
    print("  - simulator.html (with teams, players, and match databases fully inlined)")
    print("  - holland_lop.jpg (local custom icon)")
    print("\nTo deploy this directly to GitHub Pages:")
    print("1. Commit the 'docs' folder to your main repository and configure your GitHub repository")
    print("   settings to serve pages from the '/docs' directory on the 'main' branch.")
    print("=======================================================")

if __name__ == "__main__":
    build()
