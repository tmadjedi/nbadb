import json, constants as c
from datetime import datetime

file = open('../0041600162_pbp.json')
data = json.load(file)

def new_player(box, pid, tid):
    box[pid] = {"tid" : tid,
                "team" : "",
                "starter" : False,
                "timeplayed" : 0,
                "fgm" : 0,
                "fga" : 0,
                "3pm" : 0,
                "3pa" : 0,
                "ftm" : 0,
                "fta" : 0,
                "oreb" : 0,
                "dreb" : 0,
                "ast" : 0,
                "stl" : 0,
                "blk" : 0,
                "to" : 0,
                "pf" : 0,
                "pts" : 0}

events = data['resultSets'][0]['rowSet']
box = {}
played = {}
unlogged_time = []

# range hardcoded for this pbp file
for i in range(495):
    event = events[i]
    message = event[c.EVENT_MESSAGE_TYPE]
    ldescr = str(event[c.HOME_DESCRIPTION]) + str(event[c.NEUTRAL_DESCRIPTION]) + str(event[c.AWAY_DESCRIPTION])
    fmt = "%M:%S"

    # resolve time totals at ends of periods
    if message == 13:
        for player in played:
            if player in unlogged_time:
                delta = datetime.strptime(played[player]["last"], fmt) - datetime.strptime("00:00", fmt)
                played[player]["total"] += delta.seconds
                played[player]["last"] = "12:00"
                played[player]["state"] = "out"
            else:
                played[player]["last"] = "12:00"

        unlogged_time = []

    # move on if this isn't a player event
    if event[c.PERSON_1_TYPE] not in [c.HOME_PLAYER, c.AWAY_PLAYER]:
        continue

    if event[c.PLAYER_1_ID]:
        unlogged_time.append(event[c.PLAYER_1_ID])

    if event[c.PLAYER_2_ID]:
        unlogged_time.append(event[c.PLAYER_2_ID])

    if event[c.PLAYER_3_ID]:
        unlogged_time.append(event[c.PLAYER_3_ID])

    # add players if they aren't already there
    for j in [c.PLAYER_1_ID, c.PLAYER_2_ID, c.PLAYER_3_ID]:
        if event[j - 1] in [c.HOME_PLAYER, c.AWAY_PLAYER] and not box.get(event[j]):
            new_player(box, event[j], event[j + 2])

    # field goal make
    if message == 1:
        box[event[c.PLAYER_1_ID]]["fgm"] += 1
        box[event[c.PLAYER_1_ID]]["fga"] += 1

        # check if it's a 3 pointer
        if "3PT" in ldescr:
            box[event[c.PLAYER_1_ID]]["3pm"] += 1
            box[event[c.PLAYER_1_ID]]["3pa"] += 1

        # check if the shot was assisted
        if event[c.PLAYER_2_ID]:
            box[event[c.PLAYER_2_ID]]["ast"] += 1

    # field goal miss
    elif message == 2:
        box[event[c.PLAYER_1_ID]]["fga"] += 1

        # check if it's a 3 pointer
        if "3PT" in ldescr:
            box[event[c.PLAYER_1_ID]]["3pa"] += 1

        # check if it was blocked
        if event[c.PLAYER_3_ID]:
            box[event[c.PLAYER_3_ID]]["blk"] += 1

    # free throw
    elif message == 3:
        box[event[c.PLAYER_1_ID]]["fta"] += 1

        # this field is empty if the shot was missed
        if event[c.SCORE]:
            box[event[c.PLAYER_1_ID]]["ftm"] += 1

    # rebounds
    elif message == 4:
        box[event[c.PLAYER_1_ID]]["dreb" if event[c.EVENT_ACTION_TYPE] == 0 else "oreb"] += 1

    # turnovers
    elif message == 5:
        box[event[c.PLAYER_1_ID]]["to"] += 1

        if event[c.PLAYER_2_ID]:
            box[event[c.PLAYER_2_ID]]["stl"] += 1

    # fouls
    elif message == 6:
        box[event[c.PLAYER_1_ID]]["pf"] += 1

    # substitutions
    elif message == 8:
        # sub in
        if not played.get(event[c.PLAYER_2_ID]):
            played[event[c.PLAYER_2_ID]] = { "last" : event[c.PERIOD_TIME],
                                             "state" : "in",
                                             "total" : 0 }

        else:
            played[event[c.PLAYER_2_ID]]["last"] = event[c.PERIOD_TIME]
            played[event[c.PLAYER_2_ID]]["state"] = "in"

        # sub out
        if not played.get(event[c.PLAYER_1_ID]):
            delta = datetime.strptime("12:00", fmt) - datetime.strptime(event[c.PERIOD_TIME], fmt)
            played[event[c.PLAYER_1_ID]] = { "last" : event[c.PERIOD_TIME],
                                             "state" : "out",
                                             "total" : delta.seconds }
            unlogged_time = list(set(unlogged_time))
            unlogged_time.remove(event[c.PLAYER_1_ID])
        else:
            delta = datetime.strptime(played[event[c.PLAYER_1_ID]]["last"], fmt) - datetime.strptime(event[c.PERIOD_TIME], fmt)
            played[event[c.PLAYER_1_ID]]["total"] += delta.seconds
            played[event[c.PLAYER_1_ID]]["last"] = event[c.PERIOD_TIME]
            played[event[c.PLAYER_1_ID]]["state"] = "out"
            unlogged_time = list(set(unlogged_time))
            unlogged_time.remove(event[c.PLAYER_1_ID])

for player in played:
    box[player]["timeplayed"] = played[player]["total"]

for player in box:
    print(player, box[player]["fgm"], box[player]["fga"], box[player]["3pm"], box[player]["3pa"], box[player]["oreb"], box[player]["dreb"], box[player]["ast"], box[player]["blk"], box[player]["timeplayed"])