import sys
import time
import os
import random
import pickle
import datetime


class player:
    def __init__(self):
        self.name=""
        self.gender=""
        self.hp=10
        self.potion=0
        self.location = 'shack'
        self.game_over = False
        self.playing = False
        self.i=1
        self.chapter1=False
        
my_player = player()
################################################################################### MAP CONNECTIONS ####################################################################################
ZONENAME = "location"
DESCRIPTION = "description"
DESCRIPTION2 = "description2"
EXAMINE = "examine"
EXAMINE2 = "examine2"
SOLVED = False
NORTH = 'north', 'n'
EAST = 'east', 'e'
SOUTH = 'south', 's'
WEST = 'west', 'w'
BLOCKADE = ''

zone_map = {                                                                   ###### MIDDLE OF THE MAP ######  
    "shack": {
        ZONENAME: "Shack",
        DESCRIPTION: "A simple wooden shack, looks like the only way in and out is a single door.",
        EXAMINE: "You wonder how and why you woke up here.",
        SOLVED: False,
        NORTH: 'Front of shack',
        EAST: '', #Can't go that way
        SOUTH: '', #Can't go that way
        WEST: '', #Can't go that way
        BLOCKADE: 'There is a wall there.',
    },
    "Front of shack": {
        ZONENAME: "Front of shack",
        DESCRIPTION: "The only thing that can be seen from here is a path that leads north.",
        EXAMINE: "You look around but can see nothing of use.",
        SOLVED: False,
        NORTH: 'Path',
        EAST: 'East of shack',
        SOUTH: 'shack',
        WEST: 'West of shack',
        BLOCKADE: '',
    },
    "West of shack": {
        ZONENAME: "West of shack",
        DESCRIPTION: "Jungle surrounds the areas but a clearing can be seen further west.",
        EXAMINE: "You look around but can see nothing of use.",
        SOLVED: False,
        NORTH: 'Front of shack',
        EAST: '', #Can't go that way
        SOUTH: 'Behind the shack',
        WEST: 'Clearing',
        BLOCKADE: 'There is no door on this side of the shack.',
    },
    "East of shack": {
        ZONENAME: "East of shack",
        DESCRIPTION: "Between the shack and the jungle, the only thing that can be seen are two out of place trees further east.",
        EXAMINE: "You look around but can see nothing of use.",
        SOLVED: False,
        NORTH: 'Front of shack',
        EAST: 'Arched trees',
        SOUTH: 'Behind the shack',
        WEST: '', #Can't go that way
        BLOCKADE: 'There is no door on this side of the shack.',
    },                                                                             ###### BOTTOM OF THE MAP ######
    "Behind the shack": {
        ZONENAME: "Behind the shack",
        DESCRIPTION: "There seems to be a path further south that leads into the jungle.",
        EXAMINE: "You look around but can see nothing of use.",
        SOLVED: False,
        NORTH: '', #Can't go that way
        EAST: 'East of shack',
        SOUTH: 'Jungle path 1',
        WEST: 'West of shack',
        BLOCKADE: 'There is no door on this side of the shack.',
    },
    "Jungle path 1": {
        ZONENAME: "Jungle path",
        DESCRIPTION: "A path leads through the dense jungle.",
        EXAMINE: "It might be useful to follow the path.",
        SOLVED: False,
        NORTH: 'Behind the shack',
        EAST: 'Jungle 3',
        SOUTH: 'Jungle path 2',
        WEST: 'Jungle 1',
        BLOCKADE: '',
    },
    "Jungle path 2": {
        ZONENAME: "Jungle path",
        DESCRIPTION: "The path seems to bend around a corner and continue east.",
        EXAMINE: "It might be useful to follow the path.",
        SOLVED: False,
        NORTH: 'Jungle path 1',
        EAST: 'Jungle path 3',
        SOUTH: '', #Can't go that way
        WEST: 'Jungle 2',
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },
    "Jungle path 3": {
        ZONENAME: "Jungle path",
        DESCRIPTION: "The path continues through the jungle.",
        EXAMINE: "You wonder if the path might actually be useful at all.",
        SOLVED: False,
        NORTH: 'Jungle 3',
        EAST: 'Giant boulder',
        SOUTH: '', #Can't go that way
        WEST: 'Jungle path 2',
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },
    "Giant boulder": {
        ZONENAME: "Giant boulder",
        DESCRIPTION: """The path is holted by what can only be considered a giant boulder. The boulder sits in the way,
almost embeded into the vines and trees.""",
        EXAMINE: """The boulder looks almost perfectly round, could it have been put here?
You look closer and see an engraving...
Jay.go_to_starbucks""",
        SOLVED: False,
        NORTH: 'Dense jungle 3',
        EAST: '', #Can't go that way
        SOUTH: 'Dense jungle 4',
        WEST: 'Jungle path 3',
        BLOCKADE: 'There is a giant boulder in the way.',
    },
    "Jungle 1": {
        ZONENAME: "Jungle",
        DESCRIPTION: "Jungle trees and vines surround you. The sound of exotic birds fills your head.",
        EXAMINE: "There is nothing of use here.",
        SOLVED: False,
        NORTH: '', #Can't go that way
        EAST: 'Jungle path 1',
        SOUTH: 'Jungle 2',
        WEST: 'Dense jungle 1',
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },
    "Jungle 2": {
        ZONENAME: "Jungle",
        DESCRIPTION: "Jungle trees and vines surround you. The sound of exotic birds fills your head.",
        EXAMINE: "You look around but can see nothing of use.",
        SOLVED: False,
        NORTH: 'Jungle 1',
        EAST: 'Jungle path 2',
        SOUTH: 'Lantern creature',
        WEST: 'Dense jungle 2',
        BLOCKADE: '',
    },
    "Jungle 3": {
        ZONENAME: "Jungle",
        DESCRIPTION: "Jungle trees and vines surround you. The sound of exotic birds fills your head.",
        EXAMINE: "You look around but can see nothing of use.",
        SOLVED: False,
        NORTH: '', #Can't go that way
        EAST: 'Dense jungle 3',
        SOUTH: 'Jungle path 3',
        WEST: 'Jungle path 1',
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },
    "Dense jungle 1": {
        ZONENAME: "Dense jungle",
        DESCRIPTION: "You couldn't even get through this with a weed wacker. You can't continue this way.",
        EXAMINE: "It's almost like it's grown to not allow entry or exit.",
        SOLVED: False,
        NORTH: '', #Can't go that way
        EAST: 'Jungle 1',
        SOUTH: '', #Can't go that way
        WEST: '', #Can't go that way
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },
    "Dense jungle 2": {
        ZONENAME: "Dense jungle",
        DESCRIPTION: "You couldn't even get through this with a weed wacker. You can't continue this way.",
        EXAMINE: "It's almost like it's grown to not allow entry or exit.",
        SOLVED: False,
        NORTH: '', #Can't go that way
        EAST: 'Jungle 2',
        SOUTH: '', #Can't go that way
        WEST: '', #Can't go that way
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },
    "Dense jungle 3": {
        ZONENAME: "Dense jungle",
        DESCRIPTION: "You couldn't even get through this with a weed wacker. You can't continue this way.",
        EXAMINE: "It's almost like it's grown to not allow entry or exit.",
        SOLVED: False,
        NORTH: '', #Can't go that way
        EAST: '', #Can't go that way
        SOUTH: 'Giant boulder',
        WEST: 'Jungle 3',
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },
    "Dense jungle 4": {
        ZONENAME: "Dense jungle",
        DESCRIPTION: "You couldn't even get through this with a weed wacker. You can't continue this way.",
        EXAMINE: "It's almost like it's grown to not allow entry or exit.",
        SOLVED: False,
        NORTH: 'Giant boulder',
        EAST: '', #Can't go that way
        SOUTH: '', #Can't go that way
        WEST: '', #Can't go that way
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },
    "Lantern creature": {
        ZONENAME: "Torch",
        DESCRIPTION: "Jungle surrounds the area. A torch sits at the foot of one of the trees.\n(Inspect/Examine)",
        DESCRIPTION2: "A wolf corpse lies, surrounded by jungle",
        EXAMINE: "You walk towards the torch with a reached out hand.",
        SOLVED: False,
        NORTH: 'Jungle 2',
        EAST: '', #Can't go that way
        SOUTH: '', #Can't go that way
        WEST: '', #Can't go that way
        BLOCKADE: "The jungle is too dense to transverse in that direction.",
    },                                                                             ####### LEFT OF THE MAP #######
    "Clearing": {
        ZONENAME: "Clearing",
        DESCRIPTION: """You reach a clearing with the jungle to the north and south of you. The ground is covered with leaves
the size of a human torso.""",
        EXAMINE: "You listen carefully and can hear the sound of waves.",
        SOLVED: False,
        NORTH: 'Dense jungle 6',
        EAST: 'West of shack',
        SOUTH: 'Dense jungle 5',
        WEST: 'Rocky cove',
        BLOCKADE: '',
    },
    "Rocky cove": {
        ZONENAME: "Rocky cove",
        DESCRIPTION: "There is a beautiful sight of a cove, however the rocks look sharp enough to pierce the sky.",
        EXAMINE: "Thoughts of escape fill your head until you quickly realise that trying to climb down could only result in a swift death.",
        SOLVED: False,
        NORTH: 'Dense jungle 6',
        EAST: 'Clearing',
        SOUTH: 'Dense jungle 5',
        WEST: '', #Can't go that way
        BLOCKADE: 'The rocks are too sharp and the sea is too strong, you would probably die.',
    },
    "Dense jungle 5": {
        ZONENAME: "Dense jungle",
        DESCRIPTION: "You couldn't even get through this with a weed wacker. You can't continue this way.",
        EXAMINE: "It's almost like it's grown to not allow entry or exit.",
        SOLVED: False,
        NORTH: 'Rocky cove',
        EAST: '', #Can't go that way
        SOUTH: '', #Can't go that way
        WEST: '', #Can't go that way
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },
    "Dense jungle 6": {
        ZONENAME: "Dense jungle",
        DESCRIPTION: "You couldn't even get through this with a weed wacker. You can't continue this way.",
        EXAMINE: "It's almost like it's grown to not allow entry or exit.",
        SOLVED: False,
        NORTH: '', #Can't go that way
        EAST: 'Path',
        SOUTH: 'Rocky cove',
        WEST: '', #Can't go that way
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },                                                                             ###### RIGHT OF THE MAP ######
    "Arched trees": {
        ZONENAME: "Arched trees",
        DESCRIPTION: """Two trees arch over the top of you making it look like the doorway to a new land disconnected
from reality""",
        EXAMINE: """These trees aren't going to fall... 
right?""",
        SOLVED: False,
        NORTH: 'Dense jungle 7',
        EAST: 'Cave entrance', 
        SOUTH: 'Dense jungle 8', 
        WEST: 'East of shack', 
        BLOCKADE: '',
    },
    "Cave entrance": {
        ZONENAME: "Cave entrance",
        DESCRIPTION: "At the foot of a small cliff outside the entrance to a cave.",
        EXAMINE: "It seems pretty dark in there.",
        SOLVED: False,
        NORTH: 'Dense jungle 7',
        EAST: 'Cave', 
        SOUTH: 'Dense jungle 8', 
        WEST: 'Arched trees', 
        BLOCKADE: '',
    },
    "Dense jungle 7": {
        ZONENAME: "Dense jungle",
        DESCRIPTION: "You couldn't even get through this with a weed wacker. You can't continue this way.",
        EXAMINE: "It's almost like it's grown to not allow entry or exit.",
        SOLVED: False,
        NORTH: '',#Can't go that way
        EAST: '', #Can't go that way
        SOUTH: 'Cave entrance', 
        WEST: 'Path', 
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },
    "Dense jungle 8": {
        ZONENAME: "Dense jungle",
        DESCRIPTION: "You couldn't even get through this with a weed wacker. You can't continue this way.",
        EXAMINE: "It's almost like it's grown to not allow entry or exit.",
        SOLVED: False,
        NORTH: 'Cave entrance',
        EAST: '', #Can't go that way
        SOUTH: '', #Can't go that way
        WEST: '', #Can't go that way
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },                                                                         ###### CAVE ######
    "Cave": {
        ZONENAME: "Cave",
        DESCRIPTION: "It's way too dark to see anything in here. Continuing could be dangerous.",
        DESCRIPTION2: "A narrow cave that seems to go deeper than visible.",
        EXAMINE: "You'll need a light source to go deeper, overwise you might end up falling or being attacked.",
        SOLVED: False,
        NORTH: '',#Can't go that way
        EAST: 'Boss lair', 
        SOUTH: '', #Can't go that way
        WEST: 'Cave entrance', 
        BLOCKADE: 'The passage within the cave only leads east.',
    },
    "Boss lair": {
        ZONENAME: "Boss lair",
        DESCRIPTION: "A wide cavern, high ceilingand jagged walls. A monsterous sized tiger stands menecingly...\n(Inspect/Examine)",
        DESCRIPTION2: "The tiger's body lies like the rest of the putrid animal carcasses in one coner of the lair.",
        EXAMINE: "",
        SOLVED: False,
        NORTH: '',#Can't go that way
        EAST: '', #Can't go that way
        SOUTH: '', #Can't go that way
        WEST: 'Cave', 
        BLOCKADE: 'There is only one entrance/exit in this lair.',
    },                                                                         ###### Top of map ######     
    "Path": {
        ZONENAME: "Path",
        DESCRIPTION: "A rocky path leading towards the shore.",
        EXAMINE: "This path could lead somewhere.",
        SOLVED: False,
        NORTH: 'Vines',
        EAST: 'Dense jungle 7', 
        SOUTH: 'Front of shack', 
        WEST: 'Dense jungle 6', 
        BLOCKADE: '',
    },
    "Vines": {
        ZONENAME: "Stretched vines",
        DESCRIPTION: "Tightly stretched vines across the trees. Less dense that the rest of the jungle.\n(Inspect/Examine)",
        DESCRIPTION2: "Broken vines allow you to exit the jungle.",
        EXAMINE: """The shore can be seen in the distance, beyond the vines. You could probably break through if you had
a sharp tool of some kind.""",
        EXAMINE2: "You slash at the vines until you're able to rip through all of them clearing the rest of the path.",
        SOLVED: False,
        NORTH: 'Shore',
        EAST: '', #Can't go that way
        SOUTH: 'Path', 
        WEST: '', #Can't go that way
        BLOCKADE: 'The jungle is too dense to transverse in that direction.',
    },
    "Shore": {
        ZONENAME: "Shore",
        DESCRIPTION: "Golden sands meet with the ocean waves. A boat sits on the edge of the water as if it was meant for you.\n(Inspect/Examine)",
        EXAMINE: "You get in the boat as your heart explodes with joy.",
        SOLVED: False,
        NORTH: '', #Can't go that way
        EAST: '', #Can't go that way
        SOUTH: 'Vines', 
        WEST: '', #Can't go that way
        BLOCKADE: 'Where are you going? The boat is right there!',
    },
}

############################################################################### NAVIGATION & ACTIONS ##################################################################################
def print_location():
    print("========================================")
    print (zone_map[my_player.location][ZONENAME].upper())
    print (zone_map[my_player.location][DESCRIPTION])
    print("========================================")

def prompt():
    print("\nWhat would you like to do?")
    action = input("> ")
    acceptable_actions = ["move", "go", "map", "look around", "map", "hint", "save", "quit", "restart", "status", "potion", "examine", "inspect", "help"]
    while action.lower().strip() not in acceptable_actions:
        print("I do not know the term '{}', try again".format(action))
        action = input("> ")
    if action.lower().strip() in ["move", "go"]:
        player_move(action.lower().strip())
    elif action.lower().strip() in ["examine", "inspect"]:
        player_examine(action)
    elif action.lower().strip() == "look around":
        print_location()
    elif action.lower().strip() == "quit":
        quit_confirm()
    elif action.lower().strip() == "save":
        save_game()
    elif action.lower().strip() == "map":
        os.system("cls")
        map_select()
    elif action.lower().strip() == "hint":
        hint()
    elif action.lower().strip() == "restart":
        restart_confirm()
    elif action.lower().strip() == "status":
        player_status()
    elif action.lower().strip() == "potion":
        potion_use()
    elif action.lower().strip() == "help":
        print('Your available actions are ["move", "go", "map", "look around", "map", "hint", "save", "quit", "restart", "status", "examine", "inspect", "help"]')
        print("The available directions are ['north', 'n', 'east', 'e', 'south', 's', 'west', 'w']")

################################################################################## MOVEMENT ACTIONS ###################################################################################
def player_move(action):
    move_ask = "Where would you like to move to?\n"
    move_dest = input(move_ask)
    
    while move_dest.lower().strip() not in ['north', 'n', 'east', 'e', 'south', 's', 'west', 'w']:
        print("'{}' is not a direction I understand.".format(move_dest))
        print("The available directions are ['north', 'n', 'east', 'e', 'south', 's', 'west', 'w']")
        move_ask = "Where would you like to move to?\n"
        move_dest = input(move_ask)
        
    if move_dest.lower().strip() in ['north', 'n']:
        destination = zone_map[my_player.location][NORTH]
        movement_handler(destination)
    elif move_dest.lower().strip() in ['east', 'e']:
        destination = zone_map[my_player.location][EAST]
        movement_handler(destination)
    elif move_dest.lower().strip() in ['south', 's']:
        destination = zone_map[my_player.location][SOUTH]
        movement_handler(destination)
    elif move_dest.lower().strip() in ['west', 'w']:
        destination = zone_map[my_player.location][WEST]
        movement_handler(destination)

def movement_handler(destination):
    if destination == "Boss lair" and zone_map["Lantern creature"][SOLVED] == False:
        died_cave = """\nAs you wade through the dark you suddenly feel cold as you are knocked to the ground.
You feel the teeth of an animal pierce your neck as your conscience fades...\n""" #Death message
        for i in died_cave:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(2)
        my_player.game_over = True
        return
    if destination == "Shore" and zone_map["Boss lair"][SOLVED] == False:
        print("\nYou'll need to use a sharp too of some sort before you can continue that way.")
        return
    if destination == "Shore" and zone_map["Vines"][SOLVED] == False:
        print("\nYou should probably use that machete to cut through the vines first.")
        return
    if zone_map["Boss lair"][SOLVED] == True:
        zone_map["Vines"][EXAMINE] = zone_map["Vines"][EXAMINE2]
    if zone_map["Lantern creature"][SOLVED] == True:
        zone_map["Cave"][DESCRIPTION] = zone_map["Cave"][DESCRIPTION2]

    if destination == '':
        print("\n" + zone_map[my_player.location][BLOCKADE])
    else:
        my_player.location = destination
        print("You have moved to {}.\n".format(zone_map[my_player.location][ZONENAME]))
        print_location()

############################################################################### EXAMINE & PUZZLE ACTIONS ##############################################################################
def player_examine(action):
    if zone_map[my_player.location][ZONENAME] == "Torch" and zone_map[my_player.location][SOLVED] == False: #Wolf puzzle
        wolf1_examine = ("\n" + zone_map[my_player.location][EXAMINE] + "\n")
        for i in wolf1_examine:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        os.system("cls")
        wolf_design()
        time.sleep(1)

        wolf1_line1 = "\nSuddenly, a wolf jumps out of nowhere and positions itself between you and the torch.\n"
        for i in wolf1_line1:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        wolf1_line2 = "You will have to kill the wolf to obtain the torch.\n"
        for i in wolf1_line2:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        wolf1_line9 = "Answer the riddles to attack the beast.\n"
        for i in wolf1_line9:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        wolf1_line3 = "\nWhat can you catch but never throw?\n"
        for i in wolf1_line3:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        wolf1_answer = input("> ")
        while wolf1_answer.lower().strip() not in ["cold", "a cold",]:
            wolf1_line5 = "\nThe wolf attacked you!\n"
            for i in wolf1_line5:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1)
            wolf1_dmg = random.randint(1, 3)
            my_player.hp -= wolf1_dmg
            wolf1_line5 = "You lost {} hp.\n".format(wolf1_dmg)
            for i in wolf1_line5:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1)
            wolf1_line8 = "You now have {}/10 hp.\n".format(my_player.hp)
            for i in wolf1_line8:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1)
            if my_player.hp <= 0:
                my_player.game_over = True
                return
            print("Try again")
            wolf1_answer = input("> ")
        if wolf1_answer.lower().strip() in ["cold", "a cold",]:#########################
            wolf2_correct1 = "\nYou attacked the wolf for 5 damage\n"
            for i in wolf2_correct1:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1)
            wolf2_health1 = "The wolf now has 5/10 hp\n"
            for i in wolf2_health1:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1)
            Wolf2_line1 = "\nWhat runs around the whole garden without moving?\n"
            for i in Wolf2_line1:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1)
            wolf2_answer = input("> ")
            while wolf2_answer.lower().strip() not in ["fence", "a fence",]:
                wolf2_line2 = "\nThe wolf attacked you!\n"
                for i in wolf2_line2:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(1)
                wolf2_dmg = random.randint(1, 3)
                my_player.hp -= wolf2_dmg
                wolf2_line3 = "You lost {} hp.\n".format(wolf2_dmg)
                for i in wolf2_line3:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(1)
                wolf2_line4 = "You now have {}/10 hp.\n".format(my_player.hp)
                for i in wolf2_line4:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(1)
                if my_player.hp <= 0:
                    my_player.game_over = True
                    return
                print("Try again")
                wolf2_answer = input("> ")
            if wolf2_answer.lower().strip() in ["fence", "a fence",]:
                zone_map[my_player.location][ZONENAME] = "Dead wolf"
                zone_map[my_player.location][SOLVED] = True
                zone_map[my_player.location][DESCRIPTION] = zone_map[my_player.location][DESCRIPTION2]
                wolf2_line5 = "\nYou attacked the wolf for 5 more damage.\n"
                wolf2_line6 = "The wolf now has 0/10 hp\n"
                wolf2_line7 = "The wolf died. You then walk around the body and pick up the torch.\n"
                for i in wolf2_line5:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(1)
                for i in wolf2_line6:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(1)
                for i in wolf2_line7:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(2)
                os.system("cls")
                torch_design()
                time.sleep(3)
                os.system("cls")
                return
    ################################
    if zone_map[my_player.location][ZONENAME] == "Boss lair" and zone_map[my_player.location][SOLVED] == False:
        os.system("cls")
        tiger_design()
        tiger1_line0 = "\nThe tiger is clearly injured. A machete protrudes from the tiger's stomach.\n"
        tiger1_line1 = "That machete might be able to break through some of the jungle vines around here.\n"
        tiger1_line2 = "The tiger takes a step back... Being injured is making it defensive.\n"
        tiger1_line3 = "It's waiting for you to make the first move.\n"
        tiger1_line4 = "Answer these hard riddles to attack.\n"
        tiger1_riddle1 = "\nI have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?\n"
        for i in tiger1_line0:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        for i in tiger1_line1:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        for i in tiger1_line2:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        for i in tiger1_line3:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        for i in tiger1_line4:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        for i in tiger1_riddle1:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        tiger1_answer = input("> ")

        while tiger1_answer.lower().strip() not in ["map", "a map", "you are a map", "you're a map",]:
            tiger1_wrong = "\nThe tiger attacked you!\n"
            tiger1_dmg = random.randint(3, 5)
            my_player.hp -= tiger1_dmg
            tiger1_line5 = "You lost {} hp\n".format(tiger1_dmg)
            tiger1_line6 = "You now have {}/10 hp\n".format(my_player.hp)
            for i in tiger1_wrong:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1)
            for i in tiger1_line5:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1)
            for i in tiger1_line6:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1)
            if my_player.hp <= 0:
                my_player.game_over = True
                return
            print("Try again")
            tiger1_answer = input("> ")

        if tiger1_answer.lower().strip() in ["map", "a map", "you are a map", "you're a map", ]:
            tiger1_correct = "\nYou attack the tiger for 10 damage.\n"
            tiger2_line1 = "The tiger now has 20/40 hp.\n"
            tiger2_riddle2 = "\nIt has a long neck, a name of a bird, feeds on cargo of ships, it's not alive. What is it?\n"
            for i in tiger1_correct:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1)
            for i in tiger2_line1:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(2)
            for i in tiger2_riddle2:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1)
            tiger2_answer = input("> ")
            while tiger2_answer.lower().strip() not in ["crane", "a crane"]:
                tiger2_wrong = "\nThe tiger attacked you!\n"
                tiger2_dmg = random.randint(3, 5)
                my_player.hp -= tiger2_dmg
                tiger2_line2 = "You lost {} hp\n".format(tiger2_dmg)
                tiger2_line3 = "You now have {}/10 hp\n".format(my_player.hp)
                for i in tiger2_wrong:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(1)
                for i in tiger2_line2:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(1)
                for i in tiger2_line3:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(1)
                if my_player.hp <= 0:
                    my_player.game_over = True
                    return
                print("Try again")
                tiger2_answer = input("> ")
            if tiger2_answer.lower().strip() in ["crane", "a crane"]:
                tiger2_correct = "\nYou attack the tiger for 10 damage.\n"
                tiger3_line1 = "The tiger now has 10/40 hp.\n"
                tiger3_riddle3 = """\nA word in the English language does the following: the first two letters signify a male, 
the first three letters signify a female, the first four letters signify a great person, while the entire world signifies a great woman.
What is the word?\n"""
                for i in tiger2_correct:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(1)
                for i in tiger3_line1:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(2)
                for i in tiger3_riddle3:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(1)
                tiger3_answer = input("> ")
                while tiger3_answer.lower().strip() != "heroine":
                    tiger3_wrong = "\nThe tiger attacked you!\n"
                    tiger3_dmg = random.randint(3, 5)
                    my_player.hp -= tiger3_dmg
                    tiger3_line2 = "You lost {} hp\n".format(tiger3_dmg)
                    tiger3_line3 = "You now have {}/10 hp\n".format(my_player.hp)
                    for i in tiger3_wrong:
                        sys.stdout.write(i)
                        sys.stdout.flush()
                        time.sleep(0.05)
                    time.sleep(1)
                    for i in tiger3_line2:
                        sys.stdout.write(i)
                        sys.stdout.flush()
                        time.sleep(0.05)
                    time.sleep(1)
                    for i in tiger3_line3:
                        sys.stdout.write(i)
                        sys.stdout.flush()
                        time.sleep(0.05)
                    time.sleep(1)
                    if my_player.hp <= 0:
                        my_player.game_over = True
                        return
                    print("Try again")
                    tiger3_answer = input("> ")
                if tiger3_answer.lower().strip() == "heroine":
                    tiger3_correct = "\nYou attack the tiger for 10 damage.\n"
                    tiger3_line4 = "The tiger now has 0/40 hp.\n"
                    tiger3_line5 = "The tiger falls to the ground...\n"
                    tiger3_line6 = "You walk over to the body and remove the machete\n"
                    for i in tiger3_correct:
                        sys.stdout.write(i)
                        sys.stdout.flush()
                        time.sleep(0.05)
                    time.sleep(1)
                    for i in tiger3_line4:
                        sys.stdout.write(i)
                        sys.stdout.flush()
                        time.sleep(0.05)
                    time.sleep(1)
                    for i in tiger3_line5:
                        sys.stdout.write(i)
                        sys.stdout.flush()
                        time.sleep(0.05)
                    time.sleep(1)
                    for i in tiger3_line6:
                        sys.stdout.write(i)
                        sys.stdout.flush()
                        time.sleep(0.05)
                    time.sleep(2)
                    os.system("cls")
                    machete_design()
                    time.sleep(3)
                    os.system("cls")
                    zone_map[my_player.location][ZONENAME] = "Lifeless lair"
                    zone_map[my_player.location][SOLVED] = True
                    zone_map[my_player.location][DESCRIPTION] = zone_map[my_player.location][DESCRIPTION2]
                    return
    if zone_map[my_player.location][ZONENAME] == "Lifeless lair" and zone_map[my_player.location][SOLVED] == True:
        lifeless_examine = "\nThere is nothing left to do here.\n"
        for i in lifeless_examine:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        return
    if zone_map["Vines"][SOLVED] == False and zone_map["Boss lair"][SOLVED] == True:
        os.system("cls")
        vines_design()
        examine_vines_false = "\n" + zone_map["Vines"][EXAMINE2] + "\n"
        for i in examine_vines_false:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(3)
        os.system("cls")
        zone_map["Vines"][SOLVED] = True
        zone_map["Vines"][ZONENAME] = "Broken vines"
        zone_map["Vines"][DESCRIPTION] = zone_map["Vines"][DESCRIPTION2]
        
        return
    if zone_map[my_player.location][ZONENAME] == "Shore":
        os.system("cls")
        shore_design()
        shore_examine = ("\n" + zone_map[my_player.location][EXAMINE] + "\n")
        end1 = "You start the boat and ride off, sure to find mainland soon enough\n"
        end2 = "CONGRATULATION!\n"
        end3 = "You beat the game!\n"
        end4 = "Thank you for playing and we hope you had fun!\n"
        for i in shore_examine:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        for i in end1:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(3)
        for i in end2:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        for i in end3:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
        for i in end4:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(3)
        sys.exit()
    if zone_map[my_player.location][SOLVED] == True:
        examine_true = "\nThere is nothing left to do here.\n"
        for i in examine_true:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)
    else:
        examine_flase = ("\n" + zone_map[my_player.location][EXAMINE] + "\n")
        for i in examine_flase:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)

def hint():
    if zone_map["Lantern creature"][SOLVED] == False:
        print("\nYou should look around the south.")
        print("You might be able to find a torch to enter the caves.")
        return
    elif zone_map["Boss lair"][SOLVED] == False:
        print("\nYou should head to the east side of the map.")
        print("You could probably aquire a new item.")
        return
    elif zone_map["Vines"][SOLVED] == False:
        print("\nPart of the jungle north is less dense than the rest")
        print("You could probably put that machete to good use")
        return
    else:
        print("\nA new area is accessible north after using that machete")
        return

def map_select():
    if my_player.location in ["Jungle path 1", "Jungle path 2", "Jungle path 3", "Giant boulder", "Jungle 1", "Jungle 2", "Jungle 3", "Dense jungle 1", "Dense jungle 2", "Dense jungle 3", "Dense jungle 4", "Lantern creature"]:
        map_jungle()
        return
    elif my_player.location == "shack":
        map_shack()
    elif my_player.location == "Front of shack":
        map_north()
    elif my_player.location == "East of shack":
        map_east()
    elif my_player.location == "Behind the shack":
        map_south()
    elif my_player.location == "West of shack":
        map_west()
    elif my_player.location in ["Cave entrance", "Cave", "Boss lair"]:
        map_cave()
    elif my_player.location == "Arched trees":
        map_trees()
    elif my_player.location == "Dense jungle 7":
        map_east_up()
    elif my_player.location == "Dense jungle 8":
        map_east_down()
    elif my_player.location == "Clearing":
        map_clearing()
    elif my_player.location == "Dense jungle 5":
        map_west_down()
    elif my_player.location == "Dense jungle 6":
        map_west_up()
    elif my_player.location == "Rocky cove":
        map_cove()
    elif my_player.location in ["Path", "Vines"]:
        map_vines()
    elif my_player.location == "Shore":
        map_shore()
    
        return

def player_status():
    if zone_map["Boss lair"][SOLVED] == True:
        print("\n[Name: {}]".format(my_player.name))
        print("[Gender: {}]".format(my_player.gender))
        print("[You have {}/10 hp]\n".format(my_player.hp))
        print("Items:")
        print("[Potions: {}]".format(my_player.potions))
        print("[Map]")
        print("[Key to the shack]")
        print("[Torch]")
        print("[Machete]")
    elif zone_map["Lantern creature"][SOLVED] == True:
        print("\n[Name: {}]".format(my_player.name))
        print("[Gender: {}]".format(my_player.gender))
        print("[You have {}/10 hp]\n".format(my_player.hp))
        print("Items:")
        print("[Potions: {}]".format(my_player.potions))
        print("[Map]")
        print("[Key to the shack]")
        print("[Torch]")
    elif zone_map["Lantern creature"][SOLVED] == False:
        print("\n[Name: {}]".format(my_player.name))
        print("[Gender: {}]".format(my_player.gender))
        print("[You have {}/10 hp]\n".format(my_player.hp))
        print("Items:")
        print("[Potions: {}]".format(my_player.potions))
        print("[Map]")
        print("[Key to the shack]")
        

def potion_use():
    heal = random.randint(1, 3)
    hp_cap = my_player.hp + heal
    if my_player.potions > 0:
        if my_player.hp == 10:
            print("\nYou already have full hp")
        elif hp_cap > 10:
            my_player.hp += heal
            total_hp = my_player.hp
            total_hp -= 10
            my_player.hp -= total_hp
            my_player.potions -= 1
            print("\nYou have healed to full")
        elif hp_cap == 10:
            my_player.hp += heal
            my_player.potions -= 1
            print("\nYou have healed to full")
        else:
            my_player.hp += heal
            my_player.potions -= 1
            print("\nYou healed +{} hp".format(heal))

    else:
        print("\nYou do not have any potions left")

############################################################################### GAME FUNCTIONALITY #####################################################################################
# def start_game():
#     os.system("cls")
#     print("Play")
#     print("Load")
#     print("Quit")
#     menu_loop()
    
# def menu_loop():
#     while my_player.playing == False:
#         choice = input("> ")
#         while choice.lower().strip() not in ["play", "load", "quit"]:
#             print("Invalid input")
#             choice = input("> ")
#         if choice.lower().strip() == "play":
#             if os.path.exists("gamefile.dat") == True:
#                 print("Saving in a new game will overwrite previous game save.")
#                 print("Do you still you wish to continue? (y/n)")
#                 choice2 = input("> ")
#                 while choice2.lower().strip() not in ["yes", "y", "no", "n"]:
#                     print("Invalid input")
#                     choice2 = input("> ")
#                 if choice2.lower().strip() in ["yes", "y"]:
#                     my_player.playing = True
#                     os.system("cls")
#                     new_game()
#                     main_game_loop()
#                 else:
#                     os.system("cls")
#                     start_game()
#             else:
#                 main_game_loop()
#         elif choice.lower().strip() == "load":
#             load()
#         else:
#             sys.exit()

def new_game():
    my_player.name = "Player 1"
    my_player.gender = "Male"
    my_player.hp = 10
    my_player.potions = 0
    my_player.location = 'shack'
    my_player.game_over = False
    my_player.playing = False
    my_player.i=1
    my_player.chapter1=False

def load():
    if os.path.exists("gamefile.dat") == True:
        os.system("cls")
        with open("gamefile.dat", "rb") as sf:
            global my_player
            my_player = pickle.load(sf)
            zone_map["shack"][SOLVED] = pickle.load(sf)
            zone_map["Lantern creature"][SOLVED] = pickle.load(sf)
            zone_map["Lantern creature"][DESCRIPTION] = pickle.load(sf)
            zone_map["Lantern creature"][ZONENAME] = pickle.load(sf)
            zone_map["Boss lair"][SOLVED] = pickle.load(sf)
            zone_map["Boss lair"][DESCRIPTION] = pickle.load(sf)
            zone_map["Boss lair"][ZONENAME] = pickle.load(sf)
            zone_map["Vines"][SOLVED] = pickle.load(sf)
            zone_map["Vines"][ZONENAME] = pickle.load(sf)
            zone_map["Vines"][DESCRIPTION] = pickle.load(sf)


        main_game_loop()
    else:
        print("There is no save file for this game.")
        time.sleep(2)
        return

def save_game():
    with open("gamefile.dat", "wb") as sf:
        pickle.dump(my_player, sf)
        pickle.dump(zone_map["shack"][SOLVED], sf)
        pickle.dump(zone_map["Lantern creature"][SOLVED], sf)
        pickle.dump(zone_map["Lantern creature"][DESCRIPTION], sf)
        pickle.dump(zone_map["Lantern creature"][ZONENAME], sf)
        pickle.dump(zone_map["Boss lair"][SOLVED], sf)
        pickle.dump(zone_map["Boss lair"][DESCRIPTION], sf)
        pickle.dump(zone_map["Boss lair"][ZONENAME], sf)
        pickle.dump(zone_map["Vines"][SOLVED], sf)
        pickle.dump(zone_map["Vines"][ZONENAME], sf)
        pickle.dump(zone_map["Vines"][DESCRIPTION], sf)
    print("\nYour game has been saved\n")
    
def quit_confirm():
    print("\nAre you sure you wish to quit? (y/n)")
    quit_confirm1 = input("> ")
    while quit_confirm1.lower().strip() not in ["yes", "y", "no", "n"]:
        print("Invalid input")
        quit_confirm1 = input("> ")
    if quit_confirm1.lower().strip() in ["yes", "y"]:
        quit_save()
    else:
        return

def restart_confirm():
    print("Are you sure you wish to restart? (y/n)")
    restart_y = input("> ")
    while restart_y not in ["yes", "y", "no", "n"]:
        print("Invalid input")
        restart_y = input("> ")
    if restart_y.lower().strip() in ["yes", "y"]:
        restart()
    elif restart_y.lower().strip() in ["no", "n"]:
        return

def quit_save():
    print("Do you wish to save before exiting? (y/n)")
    quit_save1 = input("> ")
    while quit_save1.lower().strip() not in ["yes", "y", "no", "n"]:
        print("Invalid input")
        quit_save1 = input("> ")
    if quit_save1.lower().strip() in ["yes", "y"]:
        save_game()
        my_player.playing = False
        game()
    else:
        my_player.playing = False
        game()

def restart():
    my_player.game_over = False
    my_player.location = 'shack'
    my_player.name = ""
    my_player.hp = 10
    my_player.potions = 0
    zone_map["Lantern creature"][SOLVED] = False
    zone_map["Boss lair"][SOLVED] = False
    zone_map["Vines"][SOLVED] = False
    main_game_loop()

        
def main_game_loop():
    print_location()
    while my_player.game_over == False:
        prompt()
    if my_player.hp <= 0:
        my_player.game_over = True
    if my_player.game_over == True:
        os.system("cls")
        death_design()
        game_over_text = "\nYOU DIED!\nGAME OVER\n"
        play_again = "Do you wish to play again? (y/n)\n"
        for i in game_over_text:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.1)
        time.sleep(3)
        os.system("cls")
        for i in play_again:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        play_again_answer = input("> ")
        while play_again_answer.lower().strip() not in ["yes", "y", "no", "n"]:
            print("Invalid input")
            play_again_answer = input("> ")
        if play_again_answer.lower().strip() == "yes" or play_again_answer.lower() == "y":
            restart()
        else:
            print("I hope you enjoyed! Goodbye!")
            time.sleep(1)
            sys.exit()
    
#################################################################################### Maps #############################################################################################
def map_shack():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |              Dark Cave :     |
|             .-' ,----------------| ║ x ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |                        /     |
|          Cove|                   '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_east():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |              Dark Cave :     |
|             .-' ,----------------| ║   ║ x--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |                        /     |
|          Cove|                   '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_south():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |              Dark Cave :     |
|             .-' ,----------------| ║   ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |                        /     |
|          Cove|                   '---x---'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_west():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |              Dark Cave :     |
|             .-' ,----------------x ║   ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |                        /     |
|          Cove|                   '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_north():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'x---.                      \\       |
|                .'                | ╔═ ═╗ |              Dark Cave :     |
|             .-' ,----------------| ║   ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |                        /     |
|          Cove|                   '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_jungle():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |              Dark Cave :     |
|             .-' ,----------------| ║   ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |                        /     |
|          Cove|                   '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.    |.x.* Jungle               |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_cave():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |              Dark Cave :     |
|             .-' ,----------------| ║   ║ |---------------------x* ;     |
|       Rocky\\ *'                  | ╚═══╝ |                        /     |
|          Cove|                   '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_cove():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |              Dark Cave :     |
|             .-' x----------------| ║   ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |                        /     |
|          Cove|                   '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_vines():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*x,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |              Dark Cave :     |
|             .-' ,----------------| ║   ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |                        /     |
|          Cove|                   '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_east_up():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/          x        \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |        ||    Dark Cave :     |
|             .-' ,----------------| ║   ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |       ||               /     |
|          Cove|                   '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_trees():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |        ||    Dark Cave :     |
|             .-' ,----------------| ║   ║ |--------x------------ * ;     |
|       Rocky\\ *'                  | ╚═══╝ |       ||               /     |
|          Cove|                   '-------'                       /      |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_east_down():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |        ||    Dark Cave :     |
|             .-' ,----------------| ║   ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |       ||               /     |
|          Cove|                   '-------'                        /     |
|              \\         __.--._      |              x            /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_clearing():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |        ||    Dark Cave :     |
|             .-' ,-----x----------| ║   ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |       ||               /     |
|          Cove|                   '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_west_up():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /   x           .--'----.                      \\       |
|                .'                | ╔═ ═╗ |        ||    Dark Cave :     |
|             .-' ,----------------| ║   ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |       ||               /     |
|          Cove|                   '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_west_down():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x           / ?? |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |        ||    Dark Cave :     |
|             .-' ,----------------| ║   ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |       ||               /     |
|          Cove|      x            '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")
def map_shore():
    print("""+ ----------------------------------------------------------------------- +
|  Riddle Island Map              _,__       .:--------------.            |
|  Player position = x      shore/ x  |      |               \\            |
|      N             .---------./-----|.     :                 :,         |
|    W + E          /    Vine Yard*.,  '-._/                   \\_         |
|      S           /               .--'----.                      \\       |
|                .'                | ╔═ ═╗ |        ||    Dark Cave :     |
|             .-' ,----------------| ║   ║ |--------------------- * ;     |
|       Rocky\\ *'                  | ╚═══╝ |       ||               /     |
|          Cove|      x            '-------'                        /     |
|              \\         __.--._      |                           /       |
|               \\     _.'      \\:.   |...* Jungle                |        |
|                \\__,-'           \\________________________/',_.-'        |
+ ----------------------------------------------------------------------- +
|                                                                         |
|                                                                         |
|                 DIRECTIONS: NORTH, SOUTH, WEST, EAST                    |
|                                                                         |
|                                                                         |
|                                                                         |
+ ----------------------------------------------------------------------- +""")

def wolf_design():
    print("+ ----------------------------------------------------------------------- +")
    print("|                                           ,     ,                       |")
    print("|                                           |\\---/|                       |")
    print("|                                          /  , , |                       |")
    print("|                                     __.-'|   /\\ /                       |")
    print("|                            __ ___.-'        ._O|                        |")
    print("|                         .-'  '        :      _/                         |")
    print("|                        / ,    .        .     |                          |")
    print("|                       :  ;    :        :   _/                           |")
    print("|                       |  |   .'     __:   /                             |")
    print("|                       |  :   /'----'|\\   |                              |")
    print("|                       \\  |\\  |      | /| |                              |")
    print("|\\_//_\\//\\/\\//_\\_//__\'.'| /_//_\\_||\\ |\\_//_\\_//_\\_//_\\/. \\//\\//_\\_//_\\//_\\|")
    print("+ ----------------------------------------------------------------------- +")

def torch_design():
    print("+ ----------------------------------------------------------------------- +")
    print("|                                                                         |")
    print("|                                                                         |")
    print("|                                                                         |")
    print("|                                       _.----.                           |")
    print("|                     .----------------' /  /  \\                          |")
    print("|                    ( |           O  | |   |) |                          |")
    print("|                     `----------------._\\  \\  /                          |")
    print("|                                        '----'                           |")
    print("|                                                                         |")
    print("|                         Found Torch Light!                              |")
    print("|                                                                         |")
    print("|                                                                         |")
    print("+ ----------------------------------------------------------------------- +")

def machete_design():
    print("""+ -------------------------------------------------------------------------------------------- +
|                                  _____________________________                               |
|                           _.-''``------------------------|`. |``''--..__                     |
|                      _.-'` ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' | : |          ``'';';--..__        |
|                 _.-'`                                    | : |         '   :';       ```';   |
|            _.-'`                           ________/\\_/\\_|.'_|_       '   :';           /    |
|       _.-'`                         _.-''``                    ``''--:.__;';           _|    |
|     .'`                        _.-'`                                     `'`''-._     /      |
|   .`                       _.-'                                                  `'-./       |
| .'                    _.-'`           Found Machete!                                         |
|/               __..-'`                                                                       |
|``'''----'''````                                                                              |
+ -------------------------------------------------------------------------------------------- +\n""")            

def death_design():
    print("+ ---------------------------------------------------------------------------- +")
    print("|                                     ____                                 |")
    print("|                              __,---'     `--.__                          |")
    print("|                           ,-'                ; `.                        |")
    print("|                          ,'                  `--.`--.                    |")
    print("|                         ,'                       `._ `-.                 |")
    print("|                         ;                     ;     `-- ;                |")
    print("|                       ,-'-_       _,-~~-.      ,--      `.               |")
    print("|                       ;;   `-,;    ,'~`.__    ,;;;    ;  ;               |")
    print("|                       ;;    ;,'  ,;;      `,  ;;;     `. ;               |")
    print("|                       `:   ,'    `:;     __/  `.;      ; ;               |")
    print("|                        ;~~^.   `.   `---'~~    ;;      ; ;               |")
    print("|                        `,' `.   `.            .;;;     ;'                |")
    print("|                       ,',^. `.  `._    __    `:;     ,'                  |")
    print("|                        `-' `--'    ~`--'~~`--.  ~    ,'                  |")
    print("|                       /;`-;_ ; ;. /. /   ; ~~`-.     ;                   |")
    print("|-._                   ; ;  ; `,;`-;__;---;      `----'                    |")
    print("|   `--.__             ``-`-;__;:  ;  ;__;                                 |")
    print("| ...     `--.__                `-- `-'                                    |")
    print("|`--.:::...     `--.__                ____                                 |")
    print("|    `--:::::--.      `--.__    __,--'    `.                               |")
    print("|    `--:::`;....       `--'       ___  `.                                 |")
    print("|        `--`-:::...     __           )  ;                                 |")
    print("|              ~`-:::...   `---.      ( ,'                                 |")
    print("|                  ~`-:::::::::`--.   `-.                                  |")
    print("|                      ~`-::::::::`.    ;                                  |")
    print("|                          ~`--:::,'   ,'                                  |")
    print("|                               ~~`--'~                                    |")
    print("+ ---------------------------------------------------------------------------- +")

def tiger_design():
    print("+ ----------------------------------------------------------------------- +")
    print("|                                                                         |")
    print("|                                     __,,,,_                             |")
    print("|                      _ __..-;''`--/'/ /.',-`-.                          |")
    print("|                  (`/' ` |  \\ \\ \\ / / / /  .-'/`,_                       |")
    print("|                 /'`\\ \\   |  \\ | \\| // // / -.,/_,'-,                    |")
    print("|                /<7' ;  \\ \\  | ; ||/ /| | \\/    |`-/,/-.,_,/')           |")
    print("|               /  _.-, `,-\\,__|  _-| / \\ \\/|_/  |    '-/.;.\\'            |")
    print("|               `-`  f/ ;      / __/ \\__ `/ |__/ |                        |")
    print("|                    `-'      |  -| =|\\_  \\  |-' |                        |")
    print("|                            /   /_..-' `  ),'  //                        |")
    print("|                          ((__.-'((___..-'' \\__.'                        |")
    print("|                                                                         |")
    print("+ ----------------------------------------------------------------------- +")

def vines_design():
    print("+ ----------------------------------------------------------------------- +")
    print("|    __    __        __          __    __        __          __    __     |")
    print("|   (//    \\\\)    __(//   __    (//    \\\\)    __(//   __    (//    \\\\)    |")
    print("|   /'      / __  \\\\)'    \\\\)_  /'      / __  \\\\)'    \\\\)_  /'      / __  |")
    print("|  '|-..__..-''\\_''-.\\__..-''  '|-..__..-''\\_''-.\\__..-''  '|-..__..-''\\  |")
    print("|  (\\\\  \\_    _(\\\\      _/     (\\\\  \\_    _(\\\\      _/     (\\\\  \\_    //) |")
    print("|   ''  (\\\\  //)''     //)      ''  (\\\\  //)''     //)      ''  (\\\\   ''  |")
    print("|    __  ''__''      __''        __  ''__''      __''        __  ''__     |")
    print("|   (//    \\\\)    __(//   __    (//    \\\\)    __(//   __    (//    \\\\)    |")
    print("|   /'      / __  \\\\)'    \\\\)_  /'      / __  \\\\)'    \\\\)_  /'      / __  |")
    print("|  '|-..__..-''\\_''-.\\__..-''  '|-..__..-''\\_''-.\\__..-''  '|-..__..-''\\  |")
    print("|  (\\\\  \\_    _(\\\\      _/     (\\\\  \\_    _(\\\\      _/     (\\\\  \\_    //) |")
    print("|   ''  (\\\\  //)''     //)      ''  (\\\\  //)''     //)      ''  (\\\\   ''  |")
    print("|    __  ''__''      __''        __  ''__''      __''        __  ''__     |")
    print("+ ----------------------------------------------------------------------- +")

def shore_design():
    print("+ ----------------------------------------------------------------------- +")
    print("|                                      \\        |         /               |")
    print("|                  ,                    .       |        .        .       |")
    print("|               -._-_,-      .           \\              /       .         |")
    print("|              -=_* =-           '  .     \\     |      /      .           |")
    print("|              ,'/'`\\                 ` .  ,+~'`^`'~+,/   , '             |")
    print("|             //                         .'           '.'                 |")
    print("|____________//_________________________/               \\_________________|")
    print("| ~ ____,----/ |_    ~                 ~~            ~          ~         |")
    print("| -'  ________   `-.__     ~                  ~                    _  _/` |")
    print("|   ,',---\\ \\--\\       `-.____        ~~~                 ~   __,-- c'}   |")
    print("|   \\`-____\\ \\__\\             `----.___________________,-----'     ,(_).  |")
    print("|    `~~~~~~~~~~'                                                   -'-   |")
    print("+ ----------------------------------------------------------------------- +")

def potion_design2():
    print("+ ----------------------------------------------------------------------- +")
    print("|                                                                         |")
    print("|                                                                         |")
    print("|                                  :~:                                    |")
    print("|                                  | |                                    |")
    print("|                                 .' `.                                   |")
    print("|                               .'     `.                                 |")
    print("|                               |  HP+  |                                 |")
    print("|                               |       |                                 |")
    print("|                                `.._..'                                  |")
    print("|                                                                         |")
    print("|                             Found POTION!                               |")
    print("|                                                                         |")
    print("+ ----------------------------------------------------------------------- +")

def design_main_screen():
    os.system("cls")
    print("+ ----------------------------------------------------------------------- +")
    print("|                     __     __  __             ___ __                    |")
    print("|      -----         |  |   |  ||  | _____     (_  ( . ) )__   v          |")
    print("|     |  ##  | __  __|  | __|  ||  ||  _  |      '(___(_____)             |")
    print("|     |     / |  ||     ||     ||  ||  ___|                        v      |")
    print("|     |  |\\ \\ |  ||  ## || ##  ||  || |_| |           v                   |")
    print("|     \\__  \\_\\|__||_____||_____||__||_____|                   v           |")
    print("|                          __  _____  __      _______  __   __  ____      |")
    print("|        ________         |  |/  ___||  |    |       ||  \\ |  ||    \\     |")
    print("|______,',---\\ \\--\\_______|  |\\___  \\|  |    |   #   ||   \\|  ||  #  |____|")
    print("|~ ~ ~ \\`-____\\ \\__\\ ~ ~ ~|  | __/  ||  |___ |   _   ||  |\\   ||  #  | ~ ~|")
    print("|~ ~ ~ ~`~~~~~~~~~~' ~ ~ ~|__||_____/|______||__| |__||__| \\__||____/~ ~ ~|")
    print("|~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~|")
    print("+ ----------------------------------------------------------------------- +")
    print("|                                                                         |")
    print("|                                                                         |")
    print("|                               Play                                      |")
    print("|                               Load                                      |")
    print("|                               Help                                      |")
    print("|                               Quit                                      |")
    print("|                                                                         |")
    print("|                                                                         |")
    print("|            Game created by: Tai, Kabir, Mohamed & Damola                |")
    print("+ ----------------------------------------------------------------------- +")
# DICTIONARIUES FOR DECISION MAKING
chap1 = {1:['\nmobile: Check your mobile','sleep: Close your eyes fall back to sleep','shout: Shout out loud for help','help: Help in game play','quit: quit the game'],2:['torch: Turn on your phone torch','candycrush: Play candycrush till your battery runs out','call: Try to call someone','help: Help in game play','quit: quit the game'],3:['drawer: Open the drawer of the table','door: Open the door ','box: Open the box','help: Help in game play','quit: quit the game'],4:['drawer: Open the drawer of the table','box: Open the box','help: Help in game play','quit: quit the game'],5:['drawer: Open the drawer of the table','door: Open the door ','box: Open the box','help: Help in game play','quit: quit the game']}
chap1_print = {1:['Your mobile has a message on it. You open it there is a riddle...','As soon as you close your eyes a siren wakes you up','You shout at the top of your voice but you can not even hear your echo back'],2:['You turn on the torch and see a box, a table with a drawer, a door and a riddle written on the wall','Your battery is dead and now you can not see anything, you starve to death','There is no service'],3:['You try to open the drawer but it is locked','The door is locked','You open the box. There is a transparent box and it contains a key, you need it to solve a riddle to acquire it '],4:['You open the drawer with key from the box and it has another transparent box, you need to solve this riddle to acquire this key...','You are unable to open the door with this key','You already took the key, the box is \n'],5:['The drawer is empty, you already took the key','You need to solve the final riddle to open the door','You already took the key, the box is empty','help: Help in game play','quit: quit the game']}
chap1_choices={1:['mobile','sleep','shout','help','quit'],2:['torch','candycrush','call','help','quit'],3:['drawer','door','box','help','quit'],4:['drawer','door','box','help','quit'],5:['drawer','door','box','help','quit']}
chap1_riddles={1:["I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I","fire"],2:["What gets wetter as it dries?","towel"],3:["What has 88 keys, but cannot open a single door?","piano"],4:["What's black and white and read all over?","newspaper"],5:["What has a face and two hands but no arms or legs?","clock"],6:["What is so fragile that saying its name breaks it?","silence"],7:["What five letter word becomes shorter when you add two letters to it?","short"]}
chap1_riddle_answers={1:"fire",2:"towel",3:"piano",4:"newspaper",5:"clock",6:"silence",7:"short"}
chap1_riddle_or_not={1:{1:True,2:False,3:False},2:{1:True,2:False,3:False,},3:{1:False,2:False,3:True},4:{1:True,2:False,3:False},5:{1:False,2:True,3:False}}
chap1_health_potion={1:{1:False,2:False,3:False},2:{1:False,2:False,3:False},3:{1:False,2:False,3:True},4:{1:False,2:False,3:False},5:{1:False,2:False,3:False}}
chap1_print_design={1:{1:False,2:False,3:False},2:{1:False,2:False,3:False},3:{1:False,2:False,3:False},4:{1:False,2:False,3:False},5:{1:False,2:False,3:False}}
chap1_death={1:{1:False,2:False,3:False},2:{1:False,2:True,3:False},3:{1:False,2:False,3:False},4:{1:False,2:False,3:False},5:{1:False,2:False,3:False}}
#PLAYER CLASS AND INITIALIZATION

#     def use_potion(self):
#         self.potion-=1
#         rnd=random.randint(1,4)
#         self.hp+=rnd
        
def print_question(question):
    for i in question:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(.05)
    print("")
def ask_riddle(lst,i,j,chap1_riddle_or_not,my_player):
    if chap1_riddle_or_not[i][j]==True:
        s=random.choice(lst)
        print_question(chap1_riddles[s][0])
        ans=input("> ")
        
        if ans.lower()==chap1_riddle_answers[s]:
            lst.remove(s)
            print_question("You solved the riddle. Good job\n")
            return 1
        else:
            rnd=random.randint(1,3)
            print_question("Wrong answer")
            print_question("You were shocked.")
            my_player.hp-=rnd
            print_question("You lost {} hp".format(rnd))
            print_question("You now have {}/10 hp]\n".format(my_player.hp))
            return 0
    else:
        return 0
def print_choices(lst):
    for op in lst:
        print_question(op)
def health_potion(chap1_health_potion,i,j,my_player):
    if chap1_health_potion[i][j]==True:
        print("You found a health potion")
        potion_design2()
        #add design health potion
        my_player.potion+=1
        chap1_health_potion[i][j]==False
    
def help(my_player,options):
    print_question("Enter the command before the colon : to select an action you would like to take")
    print_question("one choice will take you to the riddle and a wrong choice may result in your death")
    print_question("You have the following options at this stage")
    print_choices(options)
    print_question("[You have {}/10 hp\n".format(my_player.hp))
# def save_chap1(my_player):
#     name=input("Please select a name with which you would like to save")
#     filename = 'saved.txt'
#     if os.path.exists(filename):
#         append_write = 'a' # append if already exists
#     else:
#         append_write = 'w' # make a new file if not
#     saved = open(filename,append_write)
#     saved.write(name + ','+datetime.datetime.now()+'\n')
#     saved.close()
#     filenamepkl=name+'.pkl'
#     with open(filenamepkl,"wb") as outfile:
#         pickle.dump(my_player,outfile)
#     outfile.close()
def string_parse(text):
    lst=[]
    lst=text.split(',')
    return lst[0]
# def load_chap1():
#     #getting the file name
#     text_data=[]
#     temp=[]
#     num=0
#     name=''
#     c=0
    # if os.path.exists('saved.txt'):
    #     with open('saved.txt') as text_file:
    #         temp=text_file.readlines()
    #     for t in temp:
    #         print(c+': '+t)
    #         text_data.append(string_parse(t))
    #     num=int(input('Please enter the number of file you would like to upload\n'))
    #         #loading the data from file
    #     name=text_data[num-1]
    #     inputfile=open(name,'rb')
    #     my_player=pickle.load(input)
    #     inputfile.close()
    #     if my_player.chapter1==False:
    #         chapter1(my_player)
    #     else:
    #         chapter_2(my_player)
    # else:
    #     print("No saved game")
def chapter1(my_player):
    riddle_progress=list(range(1,8))
    i=my_player.i
    
    while i<=5 and my_player.hp>0:
        print_choices(chap1[i])
        print('Please enter your choice\n')
        choice=input("> ")
        choice=choice.lower()
        while choice not in chap1_choices[i] and my_player.hp>0:
            print('Sorry unable to recognise your response please try again')
            choice=input("> ")
        if choice == chap1_choices[i][0]:
            print_question(chap1_print[i][0])
            if chap1_death[i][1]==True:
                return
            health_potion(chap1_health_potion,i,1,my_player)
            if chap1_print_design[i][1]==True:
                print("print design")
            i+=ask_riddle(riddle_progress,i,1,chap1_riddle_or_not,my_player)
        elif choice == chap1_choices[i][1]:
            print_question(chap1_print[i][1])
            if chap1_death[i][2]==True:
                return
            health_potion(chap1_health_potion,i,2,my_player)
            if chap1_print_design[i][2]==True:
                print("print design")
            i+=ask_riddle(riddle_progress,i,2,chap1_riddle_or_not,my_player)
        elif choice == chap1_choices[i][2]:
            print_question(chap1_print[i][2])
            if chap1_death[i][3]==True:
                return
            health_potion(chap1_health_potion,i,3,my_player)
            if chap1_print_design[i][3]==True:
                print("print design")
            i+=ask_riddle(riddle_progress,i,3,chap1_riddle_or_not,my_player)
        elif choice == choice == chap1_choices[i][3]:
            help(my_player,chap1_choices[i])
        elif choice == choice == chap1_choices[i][4]:
            print("Are you sure? (y/n)")
            sure=input("> ")
            if sure.lower()=='y':
                print("Would you like to save the progress? (y/n)")
                p=input("> ")
                if p.lower().strip()=='y':
                    save_game()
                    game()
                else:
                    return
            else:
                pass
        my_player.i=i
    design_key()
    if my_player.hp>0 and i>5:
        print_question("Making a squeaky sound the door opens")
        my_player.chapter1==True
        print_question("CONGRATULATIONS!!!!")
        print_question("Would you like to continue to next? (y/n)")
        ch=input("> ")
        if ch.lower()=='y':
            main_game_loop()
        elif ch.lower()=='n':
            ("Would you like to save the progress? (y/n)")
            p=input("> ")
            if p.lower=='y':
                zone_map["shack"][SOLVED] = True
                save_game()
                main_game_loop()
                return
            else:
                quit_confirm()
        else:
            print("Invalid input")
            ch = input("> ")
        
    # print("Would you like to progress to next level?")
    # choice='yeha'
    # chapter2(player,chap2)
def player_details():
    print_question("\nPlease enter a name for your character")
    my_player.name=input("> ")
    print_choices(["\nPlease select a gender",'m:male','f:female','o:other'])
    my_player.gender=input(">")

def description(my_player):
    descr="""It is rainy winter night, there are thunder claps and you for driving along the on a dual carriage way....
suddenly you notice the road is blocked, as there has been a wreck over the next hill road is black. 
A sign that you take a side road that detours the wreck.  
You decided to take that road cause .....
On the detour road you see a old woman asking for lift.... You are afraid to give someone lift on this creepy road but then you feel guilty for not helping.
So you decide to stop and let her in.
{}: what are doing alone on this road on this ungodly hour of the night
She: Waiting....
{}: What for what?
She:You""".format(my_player.name,my_player.name)
    print_question(descr)
    if my_player.gender=='m':
        design_male()
    else:
        design_female()
    print_question("""You open your eyes and your head is hurting. You can not see anything, it is completely dark and the 
last thing you can recall is the old lady sitting next to you
You hear a voice .... 
Voice: You have been abducted and taken by the government for human experiment..
Let me explain, you will be asked riddles and by getting them correct.
That is your only chance of making it alive out of here
{}: Government experiment?!?! This cant be real!!!
Voice: The riddles are hidden in this room, find them and solve them if you wish to live

    """.format(my_player.name))
    time.sleep(2)

def help_main():
    print("Please enter on of the following commands to proceed")
    print("PLAY: To start the game and defining your character")
    print("SAVE: Load previous progress")
    print("HELP: See what options you have")
    print("QUIT: Exit the game")
def start_game_chap1():############################################################################################
    player_details()
    intro='o'
    while intro.lower().strip()!='y' and intro.lower().strip()!='n':
        print_question('\nWould you like to skip the intro? (y/n)')
        intro=input("> ")
        if intro.lower()=='n':
            description(my_player)
        elif intro.lower()=='y':
            break
        else:
            print("Couldn't understand your response, please try again")
    chapter1(my_player)

def main_screen():
    design_main_screen()
    while my_player.playing == False:
        option = input(">")
        while option.lower().strip() not in ['play','help','load','quit']:
            print("Invalid input")
            option=input("> ")
        if option.lower().strip()=="play":
            print("Saving in a new game will overwrite the previous game save")
            print("Do you still wish to continue? (y/n)")
            play_choice = input("> ")
            while play_choice.lower().strip() not in ["yes", "y", "no", "n"]:
                print("Invalid input")
                play_choice = input("> ")
            if play_choice.lower().strip() in ["yes", "y"]:
                my_player.playing = True
                new_game()
                start_game_chap1()
            else:
                main_screen()
        elif option.lower().strip()=="help":
            help_main()
        elif option.lower().strip()=="load":
            my_player.playing = True
            load()
        elif option.lower().strip()=="quit":
            sys.exit()


def game():
    main_screen()

def design_male():
    print("+ ----------------------------------------------------------------------- +")
    print("| ╔═══╗                                                                   |")
    print("| ║(O)║ ♫                        _,,,,_                                   |")
    print("| ║(O)║ ♪ ♫                    _.      ._                                 |")
    print("| ╚═══╝ ♫ ♫                   '.-......-.'                                |")
    print("|    ♫ ♫ ♪ ♫                ::            ::                              |")
    print("|                           ::.---    ---.::                              |")
    print("|              ####         ::  O  ::  O  ::         ####                 |")
    print("|              ####         [     (__)     ]         ####                 |")
    print("|              ####__________:     __     :__________####                 |")
    print("|              ###,           :          :           ,###                 |")
    print("|              ##,          _.:''.______.'':._        ,##                 |")
    print("|              #,        _.:::::           :::::._     ,#                 |")
    print("|              ,      .::::::::           :::::::::.    ,                 |")
    print("+ ----------------------------------------------------------------------- +")
def design_female():
    print("+ ----------------------------------------------------------------------- +")
    print("| ╔═══╗                                                                   |")
    print("| ║(O)║ ♫                        ,{{}}}}}.                                |")
    print("| ║(O)║ ♪ ♫                    {{{{{}}}}}}}.                              |")
    print("| ╚═══╝ ♫ ♫                   {{{{   {{{{}}}}                             |")
    print("|    ♫ ♫ ♪ ♫                }}}}}___  ___{{{{{                            |")
    print("|                           }}}}  o :: o   }}}}}                          |")
    print("|               ####       {{{{C   (__)      {{{{      ####               |")
    print("|               ####      }}}}}}:   __     /}}}}}}     ####               |")
    print("|               ####_____{{{{{{{{;.____.;{{{{{{{{{_____####               |")
    print("|               ###,     }}}}}}}}})    (}}}}}}}}}}}    ,###               |")
    print("|               ##,     {{{{}}}}}':   :{{{{{{{{{{{      ,##               |")
    print("|               #,      {{{}}}}}}  '@' {{{}}}}}}}}       ,#               |")
    print("|               ,      {{{{{{{{{{    }}}}}}}}}}}}}}       ,               |")
    print("+ ----------------------------------------------------------------------- +")
def design_key():
    print("+ ----------------------------------------------------------------------- +")
    print("|            +-----------------------------------------+                  |")
    print("|            |                                         | \\                |")
    print("|            |                                         |  |               |")
    print("|            |   8 8 8 8                     ,ooo.     |  |               |")
    print("|            |   8a8 8a8                    oP   ?b    |  |               |")
    print("|            |  d888a888zzzzzzzzzzzzzzzzzzzz8     8b   |  |               |")
    print("|            |   `''^'''                    ?o___oP'   |  |               |")
    print("|            |                                         |  |               |")
    print("|            |                                         |  |               |")
    print("|            |                                         |  |               |")
    print("|            +-----------------------------------------+  |               |")
    print("|             \\__________________________________________\\|               |")
    print("+ ----------------------------------------------------------------------- +")
    
game()