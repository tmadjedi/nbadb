import json, fields as f, values as v
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
    message = event[f.EVENT_MESSAGE_TYPE]
    ldescr = str(event[f.HOME_DESCRIPTION]) + str(event[f.NEUTRAL_DESCRIPTION]) + str(event[f.AWAY_DESCRIPTION])
    fmt = "%M:%S"

    # resolve time totals at ends of periods
    if message == v.PERIOD_END:
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
    if event[f.PERSON_1_TYPE] not in [v.HOME_PLAYER, v.AWAY_PLAYER]:
        continue

    if event[f.PLAYER_1_ID]:
        unlogged_time.append(event[f.PLAYER_1_ID])

    if event[f.PLAYER_2_ID]:
        unlogged_time.append(event[f.PLAYER_2_ID])

    if event[f.PLAYER_3_ID]:
        unlogged_time.append(event[f.PLAYER_3_ID])

    # add players if they aren't already there
    for j in [f.PLAYER_1_ID, f.PLAYER_2_ID, f.PLAYER_3_ID]:
        if event[j - 1] in [v.HOME_PLAYER, v.AWAY_PLAYER] and not box.get(event[j]):
            new_player(box, event[j], event[j + 2])

    # field goal make
    if message == v.FIELD_GOAL:
        box[event[f.PLAYER_1_ID]]["fgm"] += 1
        box[event[f.PLAYER_1_ID]]["fga"] += 1

        # check if it's a 3 pointer
        if "3PT" in ldescr:
            box[event[f.PLAYER_1_ID]]["3pm"] += 1
            box[event[f.PLAYER_1_ID]]["3pa"] += 1

        # check if the shot was assisted
        if event[f.PLAYER_2_ID]:
            box[event[f.PLAYER_2_ID]]["ast"] += 1

    # field goal miss
    elif message == v.FIELD_GOAL_MISS:
        box[event[f.PLAYER_1_ID]]["fga"] += 1

        # check if it's a 3 pointer
        if "3PT" in ldescr:
            box[event[f.PLAYER_1_ID]]["3pa"] += 1

        # check if it was blocked
        if event[f.PLAYER_3_ID]:
            box[event[f.PLAYER_3_ID]]["blk"] += 1

    # free throw
    elif message == v.FREE_THROW:
        box[event[f.PLAYER_1_ID]]["fta"] += 1

        # this field is empty if the shot was missed
        if event[f.SCORE]:
            box[event[f.PLAYER_1_ID]]["ftm"] += 1

    # rebounds
    elif message == v.REBOUND:
        box[event[f.PLAYER_1_ID]]["dreb" if event[f.EVENT_ACTION_TYPE] == 0 else "oreb"] += 1

    # turnovers
    elif message == v.TURNOVER:
        box[event[f.PLAYER_1_ID]]["to"] += 1

        if event[f.PLAYER_2_ID]:
            box[event[f.PLAYER_2_ID]]["stl"] += 1

    # fouls
    elif message == v.FOUL:
        box[event[f.PLAYER_1_ID]]["pf"] += 1

    # substitutions
    elif message == v.SUBSTITUTION:
        # sub in
        if not played.get(event[f.PLAYER_2_ID]):
            played[event[f.PLAYER_2_ID]] = { "last" : event[f.PERIOD_TIME],
                                             "state" : "in",
                                             "total" : 0 }

        else:
            played[event[f.PLAYER_2_ID]]["last"] = event[f.PERIOD_TIME]
            played[event[f.PLAYER_2_ID]]["state"] = "in"

        # sub out
        if not played.get(event[f.PLAYER_1_ID]):
            delta = datetime.strptime("12:00", fmt) - datetime.strptime(event[f.PERIOD_TIME], fmt)
            played[event[f.PLAYER_1_ID]] = { "last" : event[f.PERIOD_TIME],
                                             "state" : "out",
                                             "total" : delta.seconds }
            unlogged_time = list(set(unlogged_time))
            unlogged_time.remove(event[f.PLAYER_1_ID])
        else:
            delta = datetime.strptime(played[event[f.PLAYER_1_ID]]["last"], fmt) - datetime.strptime(event[f.PERIOD_TIME], fmt)
            played[event[f.PLAYER_1_ID]]["total"] += delta.seconds
            played[event[f.PLAYER_1_ID]]["last"] = event[f.PERIOD_TIME]
            played[event[f.PLAYER_1_ID]]["state"] = "out"
            unlogged_time = list(set(unlogged_time))
            unlogged_time.remove(event[f.PLAYER_1_ID])

for player in played:
    box[player]["timeplayed"] = played[player]["total"]

for player in box:
    print(player, box[player]["fgm"], box[player]["fga"], box[player]["3pm"], box[player]["3pa"], box[player]["oreb"], box[player]["dreb"], box[player]["ast"], box[player]["blk"], box[player]["timeplayed"])