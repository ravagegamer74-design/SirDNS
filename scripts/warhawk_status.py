import json
import re
import urllib.request
from datetime import datetime, timezone

URL = "https://warhawk.gg/"

req = urllib.request.Request(
    URL,
    headers={"User-Agent": "SirDNS-Status/1.0"}
)

try:
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode("utf-8", errors="ignore")

    players_match = re.search(
        r'Online now.*?(\d+)',
        html,
        re.IGNORECASE | re.DOTALL
    )

    games_match = re.search(
        r'Active games.*?(\d+)',
        html,
        re.IGNORECASE | re.DOTALL
    )

    players = int(players_match.group(1)) if players_match else None
    games = int(games_match.group(1)) if games_match else None

    data = {
        "Warhawk": {
            "online": True,
            "players": players,
            "games": games,
            "updated": datetime.now(timezone.utc).isoformat()
        }
    }

except Exception as e:
    data = {
        "Warhawk": {
            "online": False,
            "players": None,
            "games": None,
            "updated": datetime.now(timezone.utc).isoformat(),
            "error": str(e)
        }
    }

with open("status.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(json.dumps(data, indent=2))
