import json
from helpers import (
    display_over_details,
    display_player_score_card,
    display_team_score_card,
    get_overs,
    update_score,
    change_strike,
    get_rr,
)


def match_init(format, target=None):
    if target is None:
        innings = 1
    else:
        innings = 2

    if format == "ODI":
        max_balls = 300
    elif format == "T20":
        max_balls = 120
    else:
        print("Invalid Format")
        exit()
    players = [
        "Sudharshan",
        "Santhosh",
        "Manjunath",
        "Sathish",
        "Rahul",
        "Sriram",
        "Mahendra",
        "Bhuvan",
        "Mahadev",
        "Aakash",
        "Aanand",
    ]
    over_details = {}
    for i in range(1, max_balls // 6 + 1):
        over_details[str(i)] = []
    individual_scores = {}
    for player in players:
        individual_scores[player] = {
            "runs": 0,
            "balls": 0,
            "fours": 0,
            "sixes": 0,
            "strike_rate": 0,
            "out": False,
        }
    return {
        "innings": innings,
        "team_balls": 0,
        "team_score": 0,
        "team_wickets": 0,
        "players": players,
        "individual_scores": individual_scores,
        "target": target,
        "striker": players[0],
        "non_striker": players[1],
        "max_balls": max_balls,
        "extras": 0,
        "team_fours": 0,
        "team_sixes": 0,
        "over_details": over_details,
        "just_loaded": False,
    }


def first_innings(match):
    while not match["team_balls"] >= match["max_balls"]:
        # clear the screen
        print("\033c")
        print("First Innings!!!".center(50, "-"))
        display_team_score_card(
            match["team_score"],
            match["team_balls"],
            match["team_wickets"],
            match["team_fours"],
            match["team_sixes"],
            match["extras"],
            match["max_balls"],
        )
        print()
        display_player_score_card(
            match["striker"],
            match["individual_scores"][match["striker"]]["runs"],
            match["individual_scores"][match["striker"]]["balls"],
            match["individual_scores"][match["striker"]]["fours"],
            match["individual_scores"][match["striker"]]["sixes"],
            match["individual_scores"][match["striker"]]["strike_rate"],
            True,
            False,
        )
        print()
        display_player_score_card(
            match["non_striker"],
            match["individual_scores"][match["non_striker"]]["runs"],
            match["individual_scores"][match["non_striker"]]["balls"],
            match["individual_scores"][match["non_striker"]]["fours"],
            match["individual_scores"][match["non_striker"]]["sixes"],
            match["individual_scores"][match["non_striker"]]["strike_rate"],
            False,
            True,
        )
        print()
        score = input("Score: ")
        match = update_score(match, score)
        if (
            match["team_balls"] != 0
            and match["team_balls"] % 6 == 0
            and score not in ["wd", "nb", "s", "o"]
            and not match["just_loaded"]
        ):
            match = change_strike(match)
            file = open("match.json", "w")
            json.dump(match, file)
            file.close()

    print("First Innings Completed")
    print("Target: ", match["team_score"] + 1)
    print("RRR: ", get_rr(match["team_score"] + 1, match["max_balls"]))
    display_over_details(match)
    print("\033c")
    display_team_score_card(
        match["team_score"],
        match["team_balls"],
        match["team_wickets"],
        match["team_fours"],
        match["team_sixes"],
        match["extras"],
        match["max_balls"],
    )
    print()
    display_player_score_card(
        match["striker"],
        match["individual_scores"][match["striker"]]["runs"],
        match["individual_scores"][match["striker"]]["balls"],
        match["individual_scores"][match["striker"]]["fours"],
        match["individual_scores"][match["striker"]]["sixes"],
        match["individual_scores"][match["striker"]]["strike_rate"],
        True,
        False,
    )
    print()
    display_player_score_card(
        match["non_striker"],
        match["individual_scores"][match["non_striker"]]["runs"],
        match["individual_scores"][match["non_striker"]]["balls"],
        match["individual_scores"][match["non_striker"]]["fours"],
        match["individual_scores"][match["non_striker"]]["sixes"],
        match["individual_scores"][match["non_striker"]]["strike_rate"],
        False,
        True,
    )


def second_innings(match):
    while (
        not match["team_balls"] >= match["max_balls"]
        and not match["team_score"] >= match["target"]
    ):
        # clear the screen
        print("\033c")
        print("Second Innings!!!".center(50, "-"))
        print("Target: ", match["target"],
              f"({get_overs(match['max_balls'])})")
        display_team_score_card(
            match["team_score"],
            match["team_balls"],
            match["team_wickets"],
            match["team_fours"],
            match["team_sixes"],
            match["extras"],
            match["max_balls"],
            match["target"],
            True,
        )
        print()
        print(
            f"Required {match['target'] - match['team_score']} runs in {get_overs(match['max_balls'] - match['team_balls'])}"
        )
        print()
        display_player_score_card(
            match["striker"],
            match["individual_scores"][match["striker"]]["runs"],
            match["individual_scores"][match["striker"]]["balls"],
            match["individual_scores"][match["striker"]]["fours"],
            match["individual_scores"][match["striker"]]["sixes"],
            match["individual_scores"][match["striker"]]["strike_rate"],
            True,
            False,
        )
        print()
        display_player_score_card(
            match["non_striker"],
            match["individual_scores"][match["non_striker"]]["runs"],
            match["individual_scores"][match["non_striker"]]["balls"],
            match["individual_scores"][match["non_striker"]]["fours"],
            match["individual_scores"][match["non_striker"]]["sixes"],
            match["individual_scores"][match["non_striker"]]["strike_rate"],
            False,
            True,
        )
        print()
        score = input("Score: ")
        match = update_score(match, score)
        if (
            match["team_balls"] != 0
            and match["team_balls"] % 6 == 0
            and score not in ["wd", "nb", "s", "o"]
            and not match["just_loaded"]
        ):
            match = change_strike(match)
            file = open("match.json", "w")
            json.dump(match, file)
            file.close()

    print("Second Innings Completed")
    if match["team_score"] > match["target"] - 1:
        print("Team Won")
    elif match["team_score"] < match["target"] - 1:
        print("Team Lost")
    else:
        print("Match Tied")
