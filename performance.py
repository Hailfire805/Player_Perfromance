import json
from re import A
import sys
from datetime import datetime
import shutil
import os


def backup_data():
    backup_file = output_file + ".backup"
    try:
        shutil.copy2(output_file, backup_file)
        print(f"Backup created: {backup_file}")
    except FileNotFoundError:
        print(f"No existing file to backup. A new file will be created.")

# Add this function near the top of the file, after the import statements and before the other function definitions


# Calculate performance score
def calc_performance(
    outcome,
    kills,
    deaths,
    assists,
    damagetochamps,
    damagetaken,
    killparticipation,
    damagetostructures,
    index
):
    # Calculate damage per death
    damage_dealt_per_death = (damagetochamps) / (max(deaths, 1))
    damage_taken_per_death = (damagetaken) / (max(deaths, 1))
    damage_to_structures_per_death = (
        damagetostructures) / (max(deaths, 1))
    # Calculate raw score components
    raw_score = (
        ((damage_dealt_per_death * 0.003)
         + (damage_taken_per_death * 0.002)
         + (damage_to_structures_per_death * 0.005)  # Add damage to structures
         ) * (killparticipation / 100) * (1 + ((kills + assists if kills + assists < 20 else 20)/deaths)/100)
    )

    # Define practical max raw scores for normalization
    max_raw_score = 25  # Increased to account for structure damage
    print(raw_score)
    # Normalize the raw score to be between 0 and 1
    normalized_score = raw_score if raw_score < max_raw_score else max_raw_score
    print(normalized_score)
    print(f"{index}: {'Win' if outcome == 1 else 'Loss'}\t {'Exceptional' if normalized_score > 25 else 'Excellent' if normalized_score > 20 else 'Good' if normalized_score > 15 else 'Satisfactory' if normalized_score > 10  else 'Poor' if normalized_score > 5 else 'Very Poor'} ({normalized_score:.2f}) \t\t \n  K: {kills},\t D: {deaths},\t A: {assists},\t DmgOut: {int(damagetochamps)},\t DmgIn: {int(damagetaken)},\t TowerDmg: {int(damagetostructures)},\t KillPart: {int(killparticipation)}\n")

    return normalized_score  # Return the calculated score


players = {}
output_file = "./output/players.json"
# Import and output players to json


def load_players():
    try:
        with open('./output/players.json', 'r') as f:
            data = json.load(f)
            return data.get('players', {})
    except FileNotFoundError:
        return {}


def save_players():
    result = {
        "timestamp": datetime.now().isoformat(),
        "players": players
    }
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)

# Create Data Structure for Player and Games


def create_player(name, index, id, roles, games):
    players[name] = {
        "index": index,
        "id": id,
        "roles": roles,
        "games": games,
        "performance_scores": [],
        "performance_average": 0
    }

    print("\nPlayer #" + str(index) + "\t" + "\t" + "Name: " +
          id + "\t" + "\t" + "Roles: " + ",\t".join(roles) + "\n")

    total_score = 0
    for game, game_data in games.items():
        score = create_game(game_data[0], game_data[1:], game)
        players[name]["performance_scores"].append(score)
        total_score += score

    players[name]["performance_average"] = total_score / len(games)
    print(
        f"\nAverage Performance Score: {players[name]['performance_average']:.2f}")


def create_game(outcome, data, index):
    if len(data) != 7:  # Updated to expect 7 elements
        print(
            f"Warning: Unexpected data format for game. Expected 7 elements, got {len(data)}")
        return
    kills, deaths, assists, damagetochamps, damagetaken, damagetostructures, killparticipation = data
    return calc_performance(outcome, kills, deaths, assists, damagetochamps,
                            damagetaken, killparticipation, damagetostructures, index)


# CLI for user input
def task_decider():
    print("Selection:")
    return input("1. Add Player\n2. Update Player\n3. View Stored Data\n4. Recalculate All Performances\n5. Restore from Backup\n6. Run Test Function\n7. Exit and Save\n")


def add_player_from_cli():
    name = input("Enter player name: ")
    id = input("Enter player id: ")
    roles = input("Enter player roles (comma-separated): ").split(',')
    games = {}
    outcome = int(input("Enter game outcome (1 for win, 0 for loss): "))
    kills = int(input("Enter kills: "))
    deaths = int(input("Enter deaths: "))
    assists = int(input("Enter assists: "))
    damagetochamps = int(input("Enter damage to champions: "))
    damagetaken = int(input("Enter damage taken: "))
    damagetostructures = int(input("Enter damage to structures: "))
    killparticipation = int(input("Enter kill participation: "))
    games[f"Game 1"] = [outcome, kills, deaths, assists,
                        damagetochamps, damagetaken, damagetostructures, killparticipation]
    create_player(name, len(players)+1, id, roles, games)


def update_player_from_cli():
    global players
    # Remove this line to prevent reloading and overwriting existing data

    name = input("Enter player name to update: ")
    matching_player = next(
        (player for player in players.keys() if player.lower() == name.lower()), None)
    if matching_player is None:
        print(f"Player {name} not found.")
        return

    name = matching_player  # Use the exact name from the dictionary
    outcome = int(input("Enter game outcome (1 for win, 0 for loss): "))
    kills = int(input("Enter kills: "))
    deaths = int(input("Enter deaths: "))
    assists = int(input("Enter assists: "))
    damagetochamps = int(input("Enter damage to champions: "))
    damagetaken = int(input("Enter damage taken: "))
    damagetostructures = int(input("Enter damage to structures: "))
    killparticipation = int(input("Enter kill participation: "))
    game_number = len(players[name]["games"]) + 1
    new_game_data = [outcome, kills, deaths, assists, damagetochamps,
                     damagetaken, damagetostructures, killparticipation]
    players[name]["games"][f"Game {game_number}"] = new_game_data

    # Calculate score for new game only
    new_score = create_game(
        new_game_data[0], new_game_data[1:], f"Game {game_number}")
    players[name]["performance_scores"].append(new_score)

    # Update average
    total_score = sum(players[name]["performance_scores"])
    players[name]["performance_average"] = total_score / \
        len(players[name]["games"])

    print(
        f"\nUpdated Average Performance Score: {players[name]['performance_average']:.2f}")
    save_players()


def view_data():
    global players
    players = load_players()

    print("\nData Fields:\t(Kills, Deaths, Assists, Damage To Champions, Damage Taken, Damage To Structures, Kill Participation)")

    for name, player_data in players.items():
        create_player(name, player_data["index"], player_data["id"],
                      player_data["roles"], player_data["games"])

    print("\nPlayer Average Performance Scores:")
    for name, player in players.items():
        print(f"{name}: {player['performance_average']:.2f}")


def recalculate_all_performances():
    global players
    backup_data()  # Create a backup before recalculating

    # Load the players data
    players = load_players()

    if not players:
        print("No player data found. Nothing to recalculate.")
        return

    for name, player_data in players.items():
        total_score = 0
        player_data["performance_scores"] = []
        for game, game_data in player_data["games"].items():
            score = create_game(game_data[0], game_data[1:], game)
            player_data["performance_scores"].append(score)
            total_score += score
        player_data["performance_average"] = total_score / \
            len(player_data["games"])

    print("All player performances have been recalculated.")
    save_players()


def restore_from_backup():
    global players, output_file
    backup_file = output_file + ".backup"
    if os.path.exists(backup_file):
        shutil.copy2(backup_file, output_file)
        players = load_players()
        print("Data restored from backup.")
    else:
        print("No backup file found.")


def test_calc_performance():
    print("\n--- Testing calc_performance function ---\n")

    # Test data for two sample games
    test_data = [
        {
            "outcome": 1,
            "kills": 8,
            "deaths": 3,
            "assists": 12,
            "damagetochamps": 25000,
            "damagetaken": 18000,
            "killparticipation": 65,
            "damagetostructures": 3500,
            "index": "Test Game 1"
        },
        {
            "outcome": 0,
            "kills": 2,
            "deaths": 7,
            "assists": 5,
            "damagetochamps": 12000,
            "damagetaken": 22000,
            "killparticipation": 40,
            "damagetostructures": 1200,
            "index": "Test Game 2"
        }
    ]

    for game in test_data:
        score = calc_performance(**game)
        print(f"Final score for {game['index']}: {score:.2f}\n")

    print("--- End of test ---\n")


# Main execution block
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(" To run with existing players: python performance.py <output_file>")
        print(" To add a new player: python performance.py <output_file> -a")
        print(" To update an existing player: python performance.py <output_file> -u")
        sys.exit(1)

    players = load_players()  # Load players at the start
    exitconfirm = False
    while True:
        action = task_decider()
        if action == "1":
            add_player_from_cli()
        elif action == "2":
            update_player_from_cli()
        elif action == "3":
            view_data()
        elif action == "4":
            recalculate_all_performances()
        elif action == "5":
            restore_from_backup()
        elif action == "6":
            test_calc_performance()
        elif action == "7":
            save_players()
            sys.exit(0)
        if exitconfirm == True:
            sys.exit(0)
        elif action == "":
            exitconfirm = True
            print("No input detected. Program will exit if no input on next action.")
        save_players()  # Save after each action
