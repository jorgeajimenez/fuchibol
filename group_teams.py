import json

with open("scoreboard.json") as f:
    data = json.load(f)

groups = {}
for event in data.get("events", []):
    slug = event.get("season", {}).get("slug", "")
    if slug == "group-stage":
        comp = event.get("competitions", [{}])[0]
        note = comp.get("altGameNote", "No Group")
        # Extract group letter, e.g., "Group A"
        group_name = "Unknown Group"
        if "Group" in note:
            group_name = note.split("Group ")[1].strip()
        
        if group_name not in groups:
            groups[group_name] = set()
            
        for competitor in comp.get("competitors", []):
            team_info = competitor.get("team", {})
            team_name = team_info.get("displayName")
            team_abbr = team_info.get("abbreviation")
            if team_name:
                groups[group_name].add(f"{team_name} ({team_abbr})")

print("Group Teams:")
for group, teams in sorted(groups.items()):
    print(f"Group {group}:")
    for t in sorted(teams):
        print(f"  - {t}")
