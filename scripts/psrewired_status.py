import json
from datetime import datetime, timezone
from pathlib import Path

import requests


STATUS_FILE = Path("status.json")

PSREWIRED_GAMES = {
    "Killzone 2": 21784,
    # On ajoutera les autres jeux ici après validation.
}

PLAYERS_URL = "https://api.psrewired.com/us/api/universes/players"
ROOMS_URL = "https://api.psrewired.com/us/api/rooms"


def load_status():
    if STATUS_FILE.exists():
        try:
            with STATUS_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return {}


def get_game_status(application_id):
    try:
        players_response = requests.get(
            PLAYERS_URL,
            params={"applicationId": application_id},
            timeout=15,
        )
        players_response.raise_for_status()

        rooms_response = requests.get(
            ROOMS_URL,
            params={"applicationId": application_id},
            timeout=15,
        )
        rooms_response.raise_for_status()

        players_data = players_response.json()
        rooms_data = rooms_response.json()

        player_count = len(players_data) if isinstance(players_data, list) else 0

        active_rooms = 0

        if isinstance(rooms_data, list):
            active_rooms = sum(
                1
                for room in rooms_data
                if isinstance(room, dict)
                and room.get("playerCount", 0) > 0
            )

        return {
            "online": True,
            "players": player_count,
            "games": active_rooms,
            "updated": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as exc:
        print(f"Erreur PS Rewired applicationId={application_id}: {exc}")

        return {
            "online": False,
            "players": 0,
            "games": 0,
            "updated": datetime.now(timezone.utc).isoformat(),
        }


def main():
    status = load_status()

    for game_name, application_id in PSREWIRED_GAMES.items():
        print(f"Lecture de {game_name} ({application_id})...")

        game_status = get_game_status(application_id)

        status[game_name] = game_status

        print(
            f"{game_name}: "
            f"{game_status['players']} joueur(s), "
            f"{game_status['games']} partie(s)"
        )

    with STATUS_FILE.open("w", encoding="utf-8") as f:
        json.dump(
            status,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print("status.json mis à jour.")


if __name__ == "__main__":
    main()
