import json, constants as c

file = open('0041600162_pbp.json')
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

for i in range(495):
    event = events[i]
    message = event[c.EVENT_MESSAGE_TYPE]

    # move on if this isn't a player event
    if event[c.PERSON_1_TYPE] not in [c.HOME_PLAYER, c.AWAY_PLAYER]:
        continue

    # add players if they aren't already there
    for j in [c.PLAYER_1_ID, c.PLAYER_2_ID, c.PLAYER_3_ID]:
        if message[j - 1] in [4, 5] and not box.get(message[j]):
            new_player(box, message[j], message[j + 2])

    # field goal make
    if message == 1:
        box[message[c.PLAYER_1_ID]]["fgm"] += 1
        box[message[c.PLAYER_1_ID]]["fga"] += 1

        # check if it's a 3 pointer
        if any("3PT" in descr for descr in [str(message[7]), str(message[8]), str(message[9])]):
            box[message[c.PLAYER_1_ID]]["3pm"] += 1
            box[message[c.PLAYER_1_ID]]["3pa"] += 1

        # check if the shot was assisted
        if message[20]:
            box[message[20]]["ast"] += 1

    # field goal miss
    elif message == 2:
        box[message[c.PLAYER_1_ID]]["fga"] += 1

        # check if it's a 3 pointer
        if any("3PT" in descr for descr in [str(message[7]), str(message[8]), str(message[9])]):
            box[message[c.PLAYER_1_ID]]["3pa"] += 1

        # check if it was blocked
        if message[27]:
            box[message[27]]["blk"] += 1

    # free throw
    elif message == 3:
        box[message[c.PLAYER_1_ID]]["fta"] += 1

        # this field is empty if the shot was missed
        if message[10]:
            box[message[c.PLAYER_1_ID]]["ftm"] += 1

    # rebounds
    elif message == 4 and message[12] in [4, 5]:
        box[message[c.PLAYER_1_ID]]["dreb" if message[3] == 0 else "oreb"] += 1

for player in box:
    print(player, box[player]["fgm"], box[player]["fga"], box[player]["3pm"], box[player]["3pa"], box[player]["oreb"], box[player]["dreb"], box[player]["ast"], box[player]["blk"])