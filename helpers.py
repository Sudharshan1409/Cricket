import json
from color_helpers import (
    pBold,
    pRed,
    pGreen,
    pYellow,
)


def change_strike(match):
    match["striker"], match["non_striker"] = match["non_striker"], match["striker"]
    return match


def next_batsman(match):
    for player in match["players"]:
        if (
            not match["individual_scores"][player]["out"]
            and player != match["striker"]
            and player != match["non_striker"]
        ):
            match["striker"] = player
            return match
    match["striker"] = None
    return match


def update_strike_rate(match, player):
    if match["individual_scores"][player]["balls"] == 0:
        match["individual_scores"][player]["strike_rate"] = 0
    else:
        match["individual_scores"][player]["strike_rate"] = round(
            match["individual_scores"][player]["runs"]
            / match["individual_scores"][player]["balls"]
            * 100,
            2,
        )
    return match


def display_player_score_card(
    player,
    runs,
    balls,
    fours,
    sixes,
    strike_rate,
    is_striker=False,
    is_non_striker=False,
):
    player_score_card = f"{player} {runs} ({balls}){'*' if is_striker else ''}".ljust(
        42
    )
    player_strike_rate = f"SR: {strike_rate}".ljust(42)
    player_fours = f"Fours: {fours}"
    player_sixes = f"Sixes: {sixes}"
    if is_striker or is_non_striker:
        player_score_card = pYellow(pBold(player_score_card))
    print(player_score_card, player_fours)
    print(
        pRed(player_strike_rate) if strike_rate < 100 else pGreen(
            player_strike_rate),
        player_sixes,
    )


def update_over_details(match, score):
    score = str(score)
    over = get_current_over(match["team_balls"])
    # check if score contains wd or nb in it as a substring
    if (
        ("WD" in score or "NB" in score)
        and match["team_balls"] != 0
        and match["team_balls"] % 6 == 0
    ):
        over += 1
    match["over_details"][str(over)].append(str(score).ljust(4))
    return match


def calculate_over_runs(over):
    runs = 0
    for ball in over:
        if ball.strip() == "W":
            runs += 0
        elif ball.strip() == "NB":
            runs += 1
        elif ball.strip() == "WD":
            runs += 1
        elif ball.strip() == "WD+1":
            runs += 2
        elif ball.strip() == "WD+2":
            runs += 3
        elif ball.strip() == "WD+3":
            runs += 4
        elif ball.strip() == "WD+4":
            runs += 5
        elif ball.strip() == "NB+1":
            runs += 2
        elif ball.strip() == "NB+2":
            runs += 3
        elif ball.strip() == "NB+3":
            runs += 4
        elif ball.strip() == "NB+4":
            runs += 5
        elif ball.strip() == "NB+6":
            runs += 7
        else:
            runs += int(ball.strip())
    return runs


def update_score_nb(match, score):
    if score == "0" or score == ".":
        match["individual_scores"][match["striker"]]["balls"] += 1
        match = update_strike_rate(match, match["striker"])
        match = update_over_details(match, "NB")

    elif score == "1":
        match["team_score"] += 1
        match["individual_scores"][match["striker"]]["runs"] += 1
        match["individual_scores"][match["striker"]]["balls"] += 1
        match = update_strike_rate(match, match["striker"])
        match = change_strike(match)
        match = update_over_details(match, "NB+1")

    elif score == "2":
        match["team_score"] += 2
        match["individual_scores"][match["striker"]]["runs"] += 2
        match["individual_scores"][match["striker"]]["balls"] += 1
        match = update_strike_rate(match, match["striker"])
        match = update_over_details(match, "NB+2")

    elif score == "3":
        match["team_score"] += 3
        match["individual_scores"][match["striker"]]["runs"] += 3
        match["individual_scores"][match["striker"]]["balls"] += 1
        match = update_strike_rate(match, match["striker"])
        match = change_strike(match)
        match = update_over_details(match, "NB+3")

    elif score == "4":
        match["team_score"] += 4
        match["individual_scores"][match["striker"]]["runs"] += 4
        match["individual_scores"][match["striker"]]["balls"] += 1
        match["individual_scores"][match["striker"]]["fours"] += 1
        match = update_strike_rate(match, match["striker"])
        match["team_fours"] += 1
        match = update_over_details(match, "NB+4")

    elif score == "6":
        match["team_score"] += 6
        match["individual_scores"][match["striker"]]["runs"] += 6
        match["individual_scores"][match["striker"]]["balls"] += 1
        match["individual_scores"][match["striker"]]["sixes"] += 1
        match = update_strike_rate(match, match["striker"])
        match["team_sixes"] += 1
        match = update_over_details(match, "NB+6")
    return match


def display_over_details(match):
    # print over details
    print("\033c")
    for over, over_details in match["over_details"].items():
        print()
        if len(over_details) == 0:
            break
        print(f"{over} over:", end=" |".ljust(5))
        for ball in over_details:
            print(ball, end=" ")
        print("|", calculate_over_runs(over_details), "runs")
        print()
    input("Press Enter to Continue")


def update_score(match, score):
    if score == "0" or score == ".":
        match["team_balls"] += 1
        match["individual_scores"][match["striker"]]["balls"] += 1
        match = update_strike_rate(match, match["striker"])
        match = update_over_details(match, 0)
    elif score == "1":
        match["team_balls"] += 1
        match["team_score"] += 1
        match["individual_scores"][match["striker"]]["runs"] += 1
        match["individual_scores"][match["striker"]]["balls"] += 1
        match = update_strike_rate(match, match["striker"])
        match = change_strike(match)
        match = update_over_details(match, 1)
    elif score == "2":
        match["team_balls"] += 1
        match["team_score"] += 2
        match["individual_scores"][match["striker"]]["runs"] += 2
        match["individual_scores"][match["striker"]]["balls"] += 1
        match = update_strike_rate(match, match["striker"])
        match = update_over_details(match, 2)
    elif score == "3":
        match["team_balls"] += 1
        match["team_score"] += 3
        match["individual_scores"][match["striker"]]["runs"] += 3
        match["individual_scores"][match["striker"]]["balls"] += 1
        match = update_strike_rate(match, match["striker"])
        match = change_strike(match)
        match = update_over_details(match, 3)
    elif score == "4":
        match["team_balls"] += 1
        match["team_score"] += 4
        match["individual_scores"][match["striker"]]["runs"] += 4
        match["individual_scores"][match["striker"]]["balls"] += 1
        match["individual_scores"][match["striker"]]["fours"] += 1
        match = update_strike_rate(match, match["striker"])
        match["team_fours"] += 1
        match = update_over_details(match, 4)
    elif score == "6":
        match["team_balls"] += 1
        match["team_score"] += 6
        match["individual_scores"][match["striker"]]["runs"] += 6
        match["individual_scores"][match["striker"]]["balls"] += 1
        match["individual_scores"][match["striker"]]["sixes"] += 1
        match = update_strike_rate(match, match["striker"])
        match["team_sixes"] += 1
        match = update_over_details(match, 6)

    elif score == "w":
        match["team_balls"] += 1
        match["team_wickets"] += 1
        match["individual_scores"][match["striker"]]["out"] = True
        match["individual_scores"][match["striker"]]["balls"] += 1
        match = update_strike_rate(match, match["striker"])
        match = update_over_details(match, "W")
        if match["team_wickets"] == 10:
            match["striker"] = None
        else:
            match = next_batsman(match)
    elif score == "wd":
        match["team_score"] += 1
        wd_score = input("Wide Score: ")
        if wd_score == ".":
            wd_score = "0"
        match["extras"] += int(wd_score) + 1
        match["team_score"] += int(wd_score)
        if wd_score == "0":
            match = update_over_details(match, "WD")
        elif wd_score == "1":
            match = update_over_details(match, "WD+" + wd_score)
            match = change_strike(match)
        elif wd_score == "3":
            match = update_over_details(match, "WD+" + wd_score)
            match = change_strike(match)
        else:
            match = update_over_details(match, "WD+" + wd_score)
    elif score == "nb":
        match["team_score"] += 1
        match["extras"] += 1
        nb_score = input("No Ball Score: ")
        match = update_score_nb(match, nb_score)

    elif score == "s":
        # print score card of all players
        print("\033c")
        for player in match["players"]:
            print()
            display_player_score_card(
                player,
                match["individual_scores"][player]["runs"],
                match["individual_scores"][player]["balls"],
                match["individual_scores"][player]["fours"],
                match["individual_scores"][player]["sixes"],
                match["individual_scores"][player]["strike_rate"],
                True if player == match["striker"] else False,
                True if player == match["non_striker"] else False,
            )
            print()
        input("Press Enter to Continue")
    elif score == "o":
        display_over_details(match)
    elif score == "save" or score == "exit":
        # save the match
        file = open("match.json", "w")
        json.dump(match, file)
        file.close()
        exit()
    elif score == "load":
        # load the match
        file = open("match.json", "r")
        match = json.load(file)
        file.close()
        match["just_loaded"] = True

    return match


def get_current_over(balls):
    if balls == 0:
        return 1
    elif balls % 6 == 0:
        return balls // 6
    return balls // 6 + 1


def get_overs(balls):
    overs = balls // 6
    balls = balls % 6
    return f"{overs}.{balls}"


def get_rr(runs, balls):
    if balls == 0:
        return 0
    crr = runs / balls * 6
    return round(crr, 2)


def display_team_score_card(
    runs,
    balls,
    wickets,
    fours,
    sixes,
    extras,
    max_balls,
    target=None,
    is_second_innings=False,
):
    team_score_card = f"Team Score: {runs}/{wickets}   {get_overs(balls)} ({get_overs(max_balls)})".ljust(
        42
    )
    team_fours = f"Fours: {fours}"
    team_sixes = f"Sixes: {sixes}"
    run_rate = f"CRR: {get_rr(runs, balls)}".ljust(42)
    if get_rr(runs, balls) < 6:
        run_rate = pRed(run_rate)
    else:
        run_rate = pGreen(run_rate)
    print(team_score_card, team_fours)
    print(run_rate, team_sixes)
    if is_second_innings:
        required_run_rate = f"RRR: {get_rr(target - runs, max_balls - balls)}".ljust(
            42)
        if get_rr(target - runs, max_balls - balls) <= 6:
            required_run_rate = pGreen(required_run_rate)
        else:
            required_run_rate = pRed(required_run_rate)
        print(required_run_rate)
    print("Extras: ", extras)
