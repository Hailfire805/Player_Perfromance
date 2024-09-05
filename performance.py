import json
import sys
from datetime import datetime


def add_player_from_cli():
    name = input("Enter player name: ")
    id = input("Enter player id: ")
    roles = input("Enter player roles (comma-separated): ").split(',')
    count = input("Number of games to add?")
    games = {}
    while True:
        game_index = input("Enter game number (or 'done' to finish): ")
        if game_index.lower() == 'done':
            break
        outcome = int(input("Enter game outcome (1 for win, 0 for loss): "))
        kills = int(input("Enter kills: "))
        deaths = int(input("Enter deaths: "))
        assists = int(input("Enter assists: "))
        damagetochamps = int(input("Enter damage to champions: "))
        damagetaken = int(input("Enter damage taken: "))
        killparticipation = int(input("Enter kill participation: "))
        games[f"Game {game_index}"] = [outcome, kills, deaths,
                                       assists, damagetochamps, damagetaken, killparticipation]
        count = int(count) - 1
        if count == 0:
            break
    create_player(name, len(players)+1, id, roles, games)


def calc_performance(
    outcome,
    kills,
    deaths,
    assists,
    damagetochamps,
    damagetaken,
    killparticipation,
    index
):
    # Calculate damage per death
    damage_dealt_per_death = (damagetochamps * 1000) / (1 + max(
        deaths, 1
    ))  # Avoid division by zero
    damage_taken_per_death = (damagetaken * 1000) / (1 + max(
        deaths, 1
    ))  # Avoid division by zero

    # Calculate raw score components
    # Combined metric includes kills, assists, damage per death, and kill participation
    raw_score = (
        ((kills + assists) + (damage_dealt_per_death * 0.03)
         + (damage_taken_per_death * 0.005)) * (1 + (killparticipation / 100))
    )  # Adjust scaling factors as needed

    # Define practical min and max raw scores for normalization
    min_raw_score = 0  # Minimum observed raw score
    max_raw_score = 25  # Estimated practical upper limit; adjust based on context

    # Normalize the raw score to be between 0 and 1

    normalized_score = (raw_score - min_raw_score) / \
        (max_raw_score - min_raw_score)
    print(f"{index}: Score: {normalized_score:.2f} \t Outcome: {'Win' if outcome == 1 else 'Loss'}\t Data: ({kills},{deaths},{assists},{damagetochamps},{damagetaken},{killparticipation})")

    return normalized_score  # Return the calculated score


players = {}


def create_player(name, index, id, roles, games):
    players[name] = {
        "index": index,
        "id": id,
        "roles": roles,
        "games": games,
        "performance_scores": [],
        "performance_average": 0
    }

    print(f"\nPlayer #{index} \t Name: {id} \t Roles: {', '.join(roles)}")

    total_score = 0
    for game, game_data in games.items():
        score = make_game(game_data[0], game_data[1:], game)
        players[name]["performance_scores"].append(score)
        total_score += score

    players[name]["performance_average"] = total_score / len(games)
    print(
        f"\nAverage Performance Score: {players[name]['performance_average']:.2f}")


def make_game(outcome, data, index):
    if len(data) != 6:
        print(
            f"Warning: Unexpected data format for game. Expected 6 elements, got {len(data)}")
        return 0
    kills, deaths, assists, damagetochamps, damagetaken, killparticipation = data
    return calc_performance(outcome, kills, deaths, assists, damagetochamps / 1000,
                            damagetaken / 1000, killparticipation, index)


def main(out_file):
    print("\nData Fields:(Kills, Deaths, Assists, Damage To Champions, Damage Taken, Kill Participation)")

    create_player("Fire", 1, "Fire", ["ADC", "Top", "Mid"], {
        "Game 1": [2, 11, 8, 7, 29000, 31000, 56],
        "Game 2": [2, 1, 4, 1, 12000, 11000, 22],
        "Game 3": [1, 9, 0, 4, 11000, 11000, 54],
        "Game 4": [1, 6, 0, 3, 11000, 41000, 50],
        "Game 5": [1, 5, 1, 7, 11000, 11000, 38],
        "Game 6": [2, 10, 18, 11, 44000, 71000, 40],
        "Game 7": [1, 17, 8, 12, 64000, 55000, 76],
        "Game 8": [1, 4, 5, 26, 19000, 37000, 59],
        "Game 9": [2, 2, 5, 1, 10000, 15000, 38],
        "Game 10": [1, 1, 8, 2, 14000, 22000, 27],
        "Game 11": [1, 2, 13, 3, 9000, 20000, 38]
    })

    create_player("Satanas", 2, "Satanas", ["Support"], {
        "Game 1": [1, 6, 2, 4, 9000, 6000, 40],
        "Game 2": [1, 4, 4, 24, 16000, 20000, 78],
        "Game 3": [1, 5, 8, 21, 27000, 23000, 55],
        "Game 4": [2, 4, 7, 20, 47000, 24000, 63],
        "Game 5": [2, 6, 9, 28, 35000, 29000, 65],
        "Game 6": [2, 2, 5, 2, 4000, 9000, 36],
        "Game 7": [1, 2, 1, 17, 6000, 8000, 76],
        "Game 8": [2, 3, 11, 14, 6000, 35000, 68]
    })

    create_player("Alex", 3, "Ginger Elvis", ["Mid"], {
        "Game 1": [2, 7, 4, 12, 27000, 32000, 53],
        "Game 2": [2, 9, 3, 9, 27000, 23000, 78],
        "Game 3": [2, 6, 4, 9, 26000, 18000, 48],
        "Game 4": [1, 18, 2, 8, 39000, 27000, 62]
    })

    create_player("Aleks", 4, "AleksIRL", ["Mid"], {
        "Game 1": [2, 14, 6, 10, 37000, 24000, 67],
        "Game 2": [2, 2, 5, 1, 8000, 11000, 33],
        "Game 3": [2, 17, 4, 5, 58000, 30000, 58]
    })

    create_player("Cameron", 5, "SadTomato1", ["Top"], {
        "Game 1": [2, 10, 7, 2, 34000, 40000, 43],
        "Game 2": [2, 7, 6, 0, 16000, 24000, 50],
        "Game 3": [2, 12, 7, 5, 13000, 19000, 55],
        "Game 4": [2, 11, 11, 8, 31000, 50000, 79],
        "Game 5": [1, 9, 3, 5, 18000, 38000, 54],
        "Game 6": [1, 14, 1, 7, 37000, 49000, 57]
    })

    create_player("Juan", 6, "XCrossBlade", ["Top"], {
        "Game 1": [2, 11, 6, 8, 35000, 34000, 46],
        "Game 2": [2, 4, 9, 9, 35000, 32000, 48],
        "Game 3": [2, 6, 5, 7, 18000, 32000, 62],
        "Game 4": [1, 6, 0, 19, 42000, 19000, 66]
    })
    print("\nPlayer Average Performance Scores:")
    for name, player in players.items():
        print(f"{name}: {player['performance_average']:.2f}")

    result = {
        "timestamp": datetime.now().isoformat(),
        "players": {}
    }
    for name, player in players.items():
        result["players"][name] = {
            "index": player["index"],
            "id": player["id"],
            "roles": player["roles"],
            "games": player["games"],
            "performance_scores": player["performance_scores"],
            "performance_average": player["performance_average"]
        }
    with open(out_file, "w") as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(" To run with existing players: python performance.py <output_file>")
        print(" To add a new player: python performance.py <output_file> -a")
        sys.exit(1)
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[2] == "-a":
        add_player_from_cli()
        main(sys.argv[1])
    else:
        print("Invalid arguments")
        sys.exit(1)
