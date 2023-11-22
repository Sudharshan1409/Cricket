# state = int(input("Enter the State:\n1--> 1st Innings\n2--> 2nd Innings\nState: "))
# matchType = int(input("Enter the Match Type:\n1--> ODI\n2--> T20\nMatch Type: "))

def getBalls(overs):
    import math
    decimal, overs = math.modf(overs)
    balls = round(decimal, 1) * 10 + overs * 6
    return int(balls)


def getCRR(score, overs):
    balls = getBalls(overs)
    crr = round(score / balls * 6, 2)
    return crr


def getRR(score, overs, target, matchType):
    balls = getBalls(overs)
    if matchType == 1:
        rr = round((target - score) / (300 - balls) * 6, 2)
    elif matchType == 2:
        rr = round((target - score) / (120 - balls) * 6, 2)
    else:
        return -1
    return rr


def getRemainingOvers(overs, matchType):
    balls = getBalls(overs)
    if matchType == 1:
        remainingBalls = 300 - balls
    elif matchType == 2:
        remainingBalls = 120 - balls
    else:
        return -1
    remainingOvers = remainingBalls // 6 + (remainingBalls % 6 / 10)
    return remainingOvers


def getProjectedScores(score, overs, matchType):
    crr = getCRR(score, overs)
    remainingOvers = getRemainingOvers(overs, matchType)
    remainingBalls = getBalls(remainingOvers)
    projectedScore = (score + round(crr * remainingBalls / 6),
                      score + round(6 * remainingBalls / 6),
                      score + round(7 * remainingBalls / 6),
                      score + round(8 * remainingBalls / 6),
                      score + round(10 * remainingBalls / 6),
                      score + round(12 * remainingBalls / 6),
                      score + round(14 * remainingBalls / 6))
    return projectedScore


def firstInnings(matchType):
    return()
    score = int(input("Enter the Score: "))
    overs = float(input("Enter the Overs: "))
    if str(overs).split(".")[1] > "5":
        return("Invalid Overs")
        return
    if (matchType == 1 and overs > 50) or (matchType == 2 and overs > 20):
        return("Invalid Overs")
        return
    crr = getCRR(score, overs)
    remainingOvers = getRemainingOvers(overs, matchType)
    return("Current Run Rate:", crr)
    return("Remaining Overs:", remainingOvers)
    projectedScores = getProjectedScores(score, overs, matchType)
    return()
    return("Projected Scores:")
    return("At {} RPO:".format(crr), projectedScores[0])
    return("At 6 RPO:", projectedScores[1])
    return("At 7 RPO:", projectedScores[2])
    return("At 8 RPO:", projectedScores[3])
    return("At 10 RPO:", projectedScores[4])
    return("At 12 RPO:", projectedScores[5])
    return("At 14 RPO:", projectedScores[6])


def secondInnings(target, matchType):
    return()
    score = int(input("Enter the Score: "))
    overs = float(input("Enter the Overs: "))
    if str(overs).split(".")[1] > "5":
        return("Invalid Overs")
        return
    if (matchType == 1 and overs > 50) or (matchType == 2 and overs > 20):
        return("Invalid Overs")
        return
    crr = getCRR(score, overs)
    rr = getRR(score, overs, target, matchType)
    return("Current Run Rate:", crr)
    return("Required Run Rate:", rr)
    if matchType == 1:
        remainingOvers = 50 - overs
    elif matchType == 2:
        remainingOvers = 20 - overs
    return("{} Runs Required in {} balls".format(
        target - score, getBalls(remainingOvers)))


matchType = int(
    input("Enter the Match Type:\n1--> ODI\n2--> T20\nMatch Type: "))
state = int(
    input("Enter the State:\n1--> 1st Innings\n2--> 2nd Innings\nState: "))

if state == 1:
    while True:
        firstInnings(matchType)
elif state == 2:
    # target = int(input("Enter the Target: "))
    target = int(input("Enter the Target: "))
    while True:
        secondInnings(target, matchType)
