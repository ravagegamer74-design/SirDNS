import json
from datetime import datetime, timezone
from pathlib import Path

import requests


STATUS_FILE = Path("status.json")

NEXUS_STATUS_URL = "https://projectnexus-revival.com/status.json"

NEXUS_GAMES = {
    "2k14-ps3": "WWE 2K14",
    "wwe13-ps3": "WWE '13",
    "wwe12-ps3": "WWE '12",
    "lucha-aaa": "Lucha AAA",
    "tna-impact-ps3": "TNA iMPACT!",
}


def load_status():
    if STATUS_FILE.exists():
        try:
            with STATUS_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return {}


def main():
    status = load_status()

    try:
        response = requests.get(NEXUS_STATUS_URL, timeout=15)
        response.raise_for_status()
        data = response.json()

        now = datetime.now(timezone.utc).isoformat()

        for title in data.get("titles", []):
            title_id = title.get("id")

            if title_id not in NEXUS_GAMES:
                continue

            game_name = NEXUS_GAMES[title_id]
            is_live = title.get("state") == "live"
            players = title.get("players_online", 0)

            status[game_name] = {
                "online": is_live,
                "players": players,
                "games": None,
                "updated": now,
            }

            print(
                f"{game_name}: "
                f"{players} joueur(s), "
                f"{'online' if is_live else 'offline'}"
            )

        with STATUS_FILE.open("w", encoding="utf-8") as f:
            json.dump(
                status,
                f,
                indent=2,
                ensure_ascii=False,
            )

        print("status.json mis à jour.")

    except Exception as exc:
        print(f"Erreur Project NEXUS: {exc}")
        raise


if __name__ == "__main__":
    main()
