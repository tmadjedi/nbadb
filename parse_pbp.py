import json, constants as c

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

# range hardcoded for this pbp file
for i in range(495):
    event = events[i]
    message = event[c.EVENT_MESSAGE_TYPE]
    ldescr = str(event[c.HOME_DESCRIPTION]) + str(event[c.NEUTRAL_DESCRIPTION]) + str(event[c.AWAY_DESCRIPTION])

    # move on if this isn't a player event
    if event[c.PERSON_1_TYPE] not in [c.HOME_PLAYER, c.AWAY_PLAYER]:
        continue

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

for player in box:
    print(player, box[player]["fgm"], box[player]["fga"], box[player]["3pm"], box[player]["3pa"], box[player]["oreb"], box[player]["dreb"], box[player]["ast"], box[player]["blk"])