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

    # 6. Copy assets
    if os.path.exists("holland_lop.jpg"):
        shutil.copy("holland_lop.jpg", os.path.join(dist_dir, "holland_lop.jpg"))
        print("Copied holland_lop.jpg to docs/ folder.")

    # 7. Create .nojekyll to prevent Jekyll build failures
    with open(os.path.join(dist_dir, ".nojekyll"), "w") as f:
        f.write("")
    print("Created .nojekyll file in docs/ folder.")

    print("\n=======================================================")
    print("SUCCESS: Your fully static site is built inside 'docs/'!")
    print("=======================================================")
    print("This folder now contains everything you need to run serverless:")
    print("  - index.html (with scoreboard data completely inlined)")
    print("  - holland_lop.jpg (local custom icon)")
    print("\nTo deploy this directly to GitHub Pages:")
    print("1. Commit the 'docs' folder to your main repository and configure your GitHub repository")
    print("   settings to serve pages from the '/docs' directory on the 'main' branch.")
    print("=======================================================")

if __name__ == "__main__":
    build()
