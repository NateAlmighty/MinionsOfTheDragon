import os
import random
import time
import pickle

actions = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}

# x = 0  x = 1    x = 2    x = 3      x = 4       x = 5     x = 6
map = [["town", "mayor", "bridge", "plains", "forest", "mountain", "cave"],  # y = 0
       ["shop", "forest", "forest", "forest", "forest", "hills", "mountain"],  # y = 1
       ["bridge", "fields", "plains", "hills", "forest", "hills", "hills"],  # y = 2
       ["plains", "fields", "plains", "hills", "forest", "hills", "mountain"],  # y = 3
       ["plains", "fields", "fields", "plains", "hills", "mountain", "mountain"]]  # y = 4)

y_len = len(map) - 1
x_len = len(map[0]) - 1

biom = {
    "plains": {
        "t": "PLAINS",
        "e": True },
    "forest": {
        "t": "WOODS",
        "e": True },
    "fields": {
        "t": "FIELDS",
        "e": True },
    "bridge": {
        "t": "BRIDGE",
        "e": False },
    "town": {
        "t": "TOWN CENTRE",
        "e": False },
    "shop": {
        "t": "SHOP",
        "e": False },
    "mayor": {
        "t": "MAYOR",
        "e": False },
    "cave": {
        "t": "CAVE",
        "e": False },
    "mountain": {
        "t": "MOUNTAIN",
        "e": True },
    "hills": {
        "t": "HILLS",
        "e": True,
    }
}

x = 0
y = 0
run = True
standing = False
fight = False
player_stats = [
    "name",
    "job",
    "ability",
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    0,
    0
]
pot = 1
elix = 1
gold = 0
quest_stats = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    False],
boss = False
endgame = False
hpmax = 0
hp = 0
at = 0
enemy = "Goblin"
gender = [
    "Nonbinary",
    "They",
    "Them",
    "Themself"
]
pacifist = False
pacifist_ruined = False
gifts = 0
romance = [
    0,
    0,
    0,
    0,
    0,
    0
]

achievements_killer = {
    'Exploration': [
        {'Name': 'Plains Explorer', 'Required': 'Areas Explored Plains', 'Goal': 25, 'MAXHP1 Increase': 10 },
        {'Name': 'Woods Explorer', 'Required': 'Areas Explored Woods', 'Goal': 25, 'MAXHP2 Increase': 10 },
        {'Name': 'Fields Explorer', 'Required': 'Areas Explored Fields', 'Goal': 25, 'MAXHP3 Increase': 10 },
        {'Name': 'Mountain Explorer', 'Required': 'Areas Explored Mountain', 'Goal': 25, 'MAXHP4 Increase': 10 },
        {'Name': 'Hills Explorer', 'Required': 'Areas Explored Hills', 'Goal': 25, 'MAXHP5 Increase': 10 },
        {'Name': 'Bridge Explorer', 'Required': 'Areas Explored Bridge', 'Goal': 25, 'MAXHP6 Increase': 10 },
    ],
    'Slayer': [
        {'Name': 'Goblin Slayer', 'Required': 'Enemies Killed Goblin', 'Goal': 25, 'ATK1 Increase': 10 },
        {'Name': 'Orc Slayer', 'Required': 'Enemies Killed Orc', 'Goal': 25, 'ATK2 Increase': 10 },
        {'Name': 'Slime Slayer', 'Required': 'Enemies Killed Slime', 'Goal': 25, 'ATK3 Increase': 10 },
        {'Name': 'Harpy Slayer', 'Required': 'Enemies Killed Harpy', 'Goal': 25, 'ATK4 Increase': 10 },
        {'Name': 'Minotaur Slayer', 'Required': 'Enemies Killed Minotaur', 'Goal': 25, 'ATK5 Increase': 10 },
        {'Name': "Dragon's Mate Slayer", 'Required': "Enemies Killed Dragon's Mate", 'Goal': 25, 'ATK6 Increase': 10 },
    ],
    'Shopping': [
        {'Name': 'Elixir Enthusiast', 'Required': 'Elixirs Bought', 'Goal': 25, 'MAXMP1 Increase': 10 },
        {'Name': 'Potion Pro', 'Required': 'Potions Bought', 'Goal': 25, 'MAXMP2 Increase': 10 },
        {'Name': 'Weapon Upgrade Specialist', 'Required': 'Weapon Upgrades Bought', 'Goal': 25,
        'MAXMP3 Increase': 10 },
        {'Name': 'Armor Upgrade Ace', 'Required': 'Armor Upgrades Bought', 'Goal': 25, 'MAXMP4 Increase': 10 },
        {'Name': 'Trinket Upgrade Expert', 'Required': 'Trinket Upgrades Bought', 'Goal': 25, 'MAXMP5 Increase': 10 },
    ],
    'Meta': [
        {'Name': 'Master Explorer', 'Required': 'All Exploration achievements completed', 'Goal': 6,
        'All Killer Stats Increase': 100 },
        {'Name': 'Master Slayer', 'Required': 'All Slayer achievements completed', 'Goal': 6,
        'All Killer Stats Increase': 100 },
        {'Name': 'Master Shopper', 'Required': 'All Shopping achievements completed', 'Goal': 5,
        'All Killer Stats Increase': 100 }
    ]
}

achievements_pacifist = {
    'Gift Shopping': [
        {'Name': 'Gift Guru', 'Required': 'Gifts Bought', 'Goal': 5, 'Gift Points Increase': 10 },
        {'Name': 'Present Pro', 'Required': 'Gifts Bought', 'Goal': 10, 'Gift Points Increase': 10 },
        {'Name': 'Gift-giving Great', 'Required': 'Gifts Bought', 'Goal': 15, 'Gift Points Increase': 10 },
    ],
    'Romance': [
        {'Name': 'Goblin Game', 'Required': 'Max Romance Score: Goblin', 'Goal': 6, 'Speech1 Increase': 10 },
        {'Name': 'Orc Admirer', 'Required': 'Max Romance Score: Orc', 'Goal': 6, 'Speech2 Increase': 10 },
        {'Name': 'Slime Smoocher', 'Required': 'Max Romance Score: Slime', 'Goal': 6, 'Speech3 Increase': 10 },
        {'Name': 'Happy with Harpies', 'Required': 'Max Romance Score: Harpy', 'Goal': 6, 'Speech4 Increase': 10 },
        {'Name': 'Minotaur Marriage', 'Required': 'Enemies Killed Minotaur', 'Goal': 6, 'Speech6 Increase': 10 },
        {'Name': "Dragon's Mate", 'Required': "Max Romance Score: Dragon", 'Goal': 6, 'Speech6 Increase': 10 },
    ],
    'Jobs': [
        {'Name': 'Part-time Pro', 'Required': 'Gold Earned from Part-Time Job', 'Goal': 1000, 'Gold1 Increase': 10 },
        {'Name': 'Full-time Finder', 'Required': 'Gold Earned from Full-Time Job', 'Goal': 10000,
        'Gold2 Increase': 10 },
        {'Name': 'Freelance Flourish', 'Required': 'Gold Earned from Freelance', 'Goal': 50000, 'Gold3 Increase': 10 }
    ],
    'Meta': [
        {'Name': 'Master ', 'Required': 'All Shopping achievements completed', 'Goal': 6,
        'All Civilian Stats Increase': 100 },
        {'Name': 'Master Mater', 'Required': 'All Romance achievements completed', 'Goal': 6,
        'All Civilian Stats Increase': 100 },
        {'Name': 'Master Worker', 'Required': 'All Jobs achievements completed', 'Goal': 3,
        'All Civilian Stats Increase': 100 }
    ]
}
progress = {}

tracked = []


def name_color():
    global player_stats
    return f"\033[1;35m{player_stats[0]}\033[1m"


def job_color():
    global player_stats
    return f"\033[1;35m{player_stats[1]}\033[1m"


def ability_color():
    global player_stats
    return f"\033[1;35m{player_stats[2]}\033[1m"


def gold_color():
    global gold
    return f"\033[1;33m{gold}\033[1m"


def level_color():
    global player_stats
    return f"\033[1;33m{player_stats[9]}\033[1m"


def HP_color():
    global player_stats
    return f"\033[1;32m{player_stats[5]}\033[1m"


def speech_color():
    global player_stats
    return f"\033[1;32m{player_stats[10] * player_stats[9]}\033[1m"


def HPMAX_color():
    global player_stats
    return f"\033[1;32m{player_stats[3] * player_stats[9]}\033[1m"


def MP_color():
    global player_stats
    return f"\033[1;34m{player_stats[6]}\033[1m"


def gifting_color():
    global player_stats
    return f"\033[1;34m{player_stats[11]}\033[1m"


def MPMAX_color():
    global player_stats
    return f"\033[1;34m{player_stats[4] * player_stats[9]}\033[1m"


def TATK_color():
    global player_stats
    return f"\033[1;31m{player_stats[8] * player_stats[9]}\033[1m"


def ATK_color():
    global player_stats
    return f"\033[1;31m{player_stats[7] * player_stats[9]}\033[1m"


def work_color():
    global player_stats
    return f"\033[1;31m{player_stats[12]}\033[1m"


def x_color():
    global x
    return f"\033[1;33m{x}\033[1m"


def y_color():
    global y
    return f"\033[1;33m{y}\033[1m"


def typewriter(text):
    for i, char in enumerate(text):
        print(char, end="", flush=True)
        if char == "!" or char == "." or char == "?" and text[i + 1:i + 2] == " " or i == len(text) - 1:
            print("\n")
        time.sleep(0.01)  # print a newline character


class SaveGlobals:
    def __init__(self):
        self.filename_template = 'globals_{}.pkl'
        self.default_vars = {
            "x": 0,
            "y": 0,
            "run": True,
            "standing": True,
            "fight": False,
            "player_stats": [
                "name",
                "job",
                "ability",
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0],
            quest_stats: [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                False
            ],
            "pot": 1,
            "elix": 1,
            "boss": False,
            "gold": 0,
            "quest_stats[12]": False,
            "endgame": False,
            "hpmax": 0,
            "hp": 0,
            "at": 0,
            "enemy": "Goblin",
            "gender": [
                "Nonbinary",
                "They",
                "Them",
                "Themself"
            ],
            "pacifist": False,
            "pacifist_ruined": False,
            "gifts": 0,

        }

    def save(self, slot=0):
        while standing:
            filename = self.filename_template.format(slot)
            with open(filename, 'wb') as f:
                pickle.dump(globals(), f)
            print(f"Game variables saved to slot {slot}.")

    def load(self, slot):
        filename = self.filename_template.format(slot)
        try:
            with open(filename, 'rb') as f:
                global_vars = pickle.load(f)
        except FileNotFoundError:
            with open(filename, 'wb') as f:
                pickle.dump({}, f)
                global_vars = {}

        for var_name, var_value in self.default_vars.items():
            if var_name not in global_vars:
                global_vars[var_name] = var_value

        globals().update(global_vars)
        typewriter(f"Game variables loaded from slot {slot}.")


def load_game():
    typewriter("Enter the save slot to load (0-9):")
    slot = int(input("> "))
    save_globals = SaveGlobals()
    save_globals.load(slot)


def save_game():
    typewriter("Enter the save slot to save to (1-9):")
    if slot > 0:
        slot = int(input("> "))
        save_globals = SaveGlobals()
        save_globals.save(slot)
    else:
        typewriter("That's not a valid save slot!")
        save_game()


def map_menu():
    typewriter('  #x = 0       x = 1       x = 2       x = 3       x = 4       x = 5          x = 6')
    typewriter('[["town"      "mayor"     "bridge"    "plains"    "forest"   "mountain"       "cave"]      y = 0')
    typewriter('["shop",     "forest",    "forest",   "forest",   "forest",   "hills",       "mountain"],  y = 1')
    typewriter('["bridge",   "fields",    "plains",   "hills",    "forest",   "hills",        "hills"  ],  y = 2')
    typewriter('["plains"   ,"fields",    "plains",    "hills",   "forest"  , "hills",       "mountain"],  y = 3')
    typewriter('["plains",   "fields",    "fields",    "plains",   "hills",  "mountain",     "mountain"]   y = 4')


def track_achievement(achievement_name):
    global endgame, pacifist
    if not endgame:
        return
    if not pacifist:
        for category in achievements_killer:
            for achievement in achievements_killer[category]:
                if achievement['Name'] == achievement_name:
                    if len(tracked) < 3:
                        if achievement_name in progress:
                            tracked.append(achievement_name)
                            typewriter(f"{achievement_name} has been added to the tracked achievements.")
                        else:
                            typewriter(f"{achievement_name} can not be tracked.")
                    else:
                        typewriter("You can only track up to 3 achievements at a time.")
    if pacifist:
        for category in achievements_pacifist:
            for achievement in achievements_pacifist[category]:
                if achievement['Name'] == achievement_name:
                    if len(tracked) < 3:
                        if achievement_name in progress:
                            tracked.append(achievement_name)
                            typewriter(f"{achievement_name} has been added to the tracked achievements.")
                        else:
                            typewriter(f"{achievement_name} can not be tracked.")
                    else:
                        typewriter("You can only track up to 3 achievements at a time.")


def print_achievements():
    global endgame, pacifist, achievements_pacifist, achievements_killer
    if endgame is False:
        return

    achievements = achievements_pacifist if pacifist else achievements_killer
    categories = ["Gift Shopping", "Romance", "Jobs", "Meta"] if pacifist else ["Exploration", "Slayer", "Shop", "Meta"]
    typewriter("Categories:")
    category_index = _print_achievements(categories, "Which category would you like to look at? (or 0 to leave)")
    if category_index == -1:
        play()
    elif 0 <= category_index < len(categories):
        category = categories[category_index]
        if category in achievements:
            typewriter(category)
            for achievement in achievements[category]:
                typewriter(f"\t{achievement['Name']} - {achievement['Required']}: {achievement['Goal']}:"
                           f" {achievement['Progress']}")
                typewriter("Do you want to track an achievement (y/n)?")
                track = input("> ").lower()
                if track == "y":
                    typewriter("Which achievement do you want to track?")
                    achievement_name = input("> ").lower()
                    track_achievement(achievement_name)
                else:
                    play()
        else:
            typewriter("This category has no achievements.")
            print_achievements()
    else:
        typewriter("Invalid category selected.")
        print_achievements()


def clear():
    time.sleep(2)
    os.system("cls")


def draw():
    typewriter("xX--------------------xX")


def heal_mana(value, resource, resource_name):
    if resource > 1:
        resource -= 1
        value(20)
    else:
        typewriter(f"No {resource_name}s!")
    clear()


def romance_increase_polly():
    global romance
    romance[3] += 1
    typewriter("You've increased your romance score with Polly!")
    typewriter(f"Your new score is {str(romance[3])}")
    town()


def polly():
    
    global romance, gifts, player_stats
    gift_measurement = gifts * player_stats[11] * player_stats[9]

    polly_texts = [
        [
            "As you walk through the town, you hear a familiar squawking noise.",
            "Polly: SQUAAWK - Wanna cracker - BRAAWK!",
            "You find Polly sitting in a group of pigeons.",
            "Polly: SQUAAWK - If it isn't the adventurer who saved my life - BACKAWW!",
            "Polly: SQUAA - What was your name again?",
            "Tell Polly your name (y/n)?",
        ][
            f"Polly: {str(name_color())}-AWK! Pretty name! Pretty name!",
        ][
            "Polly: Then leave me alone - BRAWWK!",
        ][
            "Polly is still hanging out with the pigeons.",
            "Polly: SQUAAWK - My bird friends need food - BRAWWK!",
            "Polly: SQUAAWK - Bring bird feed and I'll talk to you - SQUAAWK!",
            "Bring Polly a gift from the shop to continue.",
        ][
            "Polly is in her usual pigeon place.",
            "Polly: BRAWWWK - Thank you, thank you!",
            "Polly happily grabs the feed in her beak and spills the entire package on the ground.",
            "Polly: Oh no, I scared them!",
            "Polly: I mean - BRAWWK! Time to fly!",
            "You watch Polly take off and follow the pigeons.",
            "You notice she flies much more gracefully than any bird you've ever seen.",
        ][
            "You find Polly in her usual spot, but this time she looks dejected and you notice 0 pigeons.",
            "Polly: Oh, it's you... Squawk.",
            "Polly: I didn't mean to scare the birds.",
            "Polly: I noticed they were hungry. The people were actively avoiding feeding them...",
            "Polly: They were also too scared of people's wrath to eat when humans were around.",
            "Polly: I just thought they needed a friend - squawk.",
            "Ask Polly if she'll go out with you (y/n)?",
        ][
            "Polly: Me, you, BRAWWK!",
            "Polly: Of course! Polly - BRAWWK - would love to go out!",
            "Polly: Maybe - SQUAWWK - we can look for our pigeon friends - BRAWWK!",
            "Polly: Bring some foodstuffs for the birds and us to nibble - BRAWWK!",
            "Bring Polly some gifts from the shop to continue",
        ][
            "You leave Polly to herself.",
        ][
            "Polly: SQAAWK - Not enough! Not enough - BRAAWK!",
        ][
            "Polly is patiently waiting for you. You notice she's blushing.",
            f"Polly: Brawwk - I mean, hi, {name_color()}.",
            "Polly: I see - brawwk - You have the food - squawk.",
            "You notice she's toning down her Parrot routine this time.",
            "Tell her she's a cute parrot (y/n)?",
        ][
            "Polly's face lights up.",
            "Polly: SQUAAWK - Pretty bird, pretty bird - BRAWWWK!",
        ][
            "Polly half expects you to say something, but you don't.",
            "Polly: Pretty bird?",
            "You catch on, and nod.",
            "Polly's face lights up.",
            "Polly: SQUAAWK - Pretty bird, pretty bird - BRAWWWK!",
        ][
            "You and Polly walk together through the park, spreading bird seeds wherever Polly thinks a bird has been.",
            "Polly: BRAWWK - Bird feathers in the tree above, spread seed here - SQUAAWK!",
            "You mention to Polly that she seems to notice more than typical",
            "Polly: Get to my age, you notice a lot - SQUAWWK!",
            "You start to ask Polly's age, but decide against it.",
            "The two of you walk for some time and finish with a stargazing session in the middle of the park.",
        ][
            "Polly is back to feeding the pigeons, having learned how to properly hold a bag in her beak.",
            "Polly: SQUWRRK - wrn minint!",
            "You can tell she is struggling to talk.",
            "You wait a few minutes for the bag to be emptied and the pigeons to be fed.",
            "Polly: SQUAWWK - Thank you for waiting.",
            "Polly: SQUAWWK - I guess you're wondering why a parrot lives with Harpies - BRAWWK!",
            "You give a little half-nod, understanding now that she needs the encouragement.",
            "Polly: BRAWWK - Well, Harpies are sister-kin to the birds - SQUAWWK",
            "We - BRAWWWK - I mean they - evolved from prehistoric parrots - SQUAWWK!",
            "So when parrot parents abandoned me, the Harpies took me in - BRAWWK!",
            "Ask Polly for her real story (y/n)?",
        ][
            "REAL story? BRAWWK - fine, but you must get me something first - SQUAWWK!",
            "Polly: Polly wants some spray paint bottles from the shop - SQUAWWK!",
            "Get Polly a few gifts from the shop to continue.",
        ][
            "Polly: I can tell you don't believe me - BRAWWK!",
            "Polly: BRAWWK - fine, I tell you the REAL story but you must get me something first - SQUAWWK!",
            "Polly: Polly wants some spray paint bottles from the shop - SQUAWWK!",
            "Get Polly a few gifts from the shop to continue.",
        ][
            "Polly: SQUAWWK - More colors, more colors - BRAWWK!",
        ][
            "You come back to where Polly has been waiting for you.",
            "Polly: SQUAAWK - You got them, you got them!",
            "Polly grabs the canisters of spray paint from you and excitedly starts to spray her feathers.",
            "Polly: SQUAWWK - Now I tell you the real story - BRAWWK!",
            "Polly: ...I guess I'll stop the parrot thing for now.",
            "Polly: So, it's true that Harpies and birds share a descendant, just like all living things do.",
            "Polly: Honestly, though, Harpy society is so restrictive that I can't really have fun in it.",
            "Polly: I'm in my 30s, everyone is saying I should settle down and find a mate.",
            "Polly: Simply put, the parrot thing is my way of keeping my youth alive while I still have it.",
            "Polly: Besides, there is NO way I'm mating with a low-life MALE of any species.",
            "Polly: I'd rather never breed if that's the case.",
            "Polly: I can date, and hang with males...",
            "Polly: But I'm not interested in THAT with them.",
            "You nod in understanding, and realize Polly has transformed herself into a larger version of a parrot.",
            "Polly: Impressive, right? My matriarch helped me learn to use the paint to color my feathers properly.",
            "Polly: She's always been there for me, unlike most others of my kind...",
            "Polly squawks once more, and you sit with her and stroke her beautiful feathers.",
        ][
            "You head to the usual meeting spot with Polly and notice she's not there.",
            "Polly: SQUAWWK - here, pretty bird - BRAWWK!",
            "Looking up, she's flying around happily.",
            "You notice she's displaying her gorgeous colored feathers to a flock of similarly-colored birds.",
            "The parrots seem to be in a sort of mating dance with her.",
            "You watch her happily as she dances with them for a while, before realizing they're all females.",
            "Polly: BRAWWK! Pretty birds, I'm pretty too, SQUAWWK!",
            "Parrots: Pretty-pretty bird!",
            "Interrupt the dance (y/n)?",
        ][
            "You yell up for Polly to come down.",
            "Polly: SQUAWWK - See you later, pretty birds - BRAWWK!",
            "Parrots: Pretty see you!",
        ][
            "You watch them for quite some time until the females get bored and leave.",
            "Polly then notices you and happily swoops back down.",
        ][
            "Polly: BRAWWK -  Hello my darling, I was just thinking about you - SQUAWWK!",
            "Polly: And about how you talked to Dragon, and he was nice - BRAWWK!",
            "Polly: Polly wants to feed Dragon some friendship crackers!",
            "Polly: Bring Polly many Dragon snacks to feed him - SQUAWWK!",
            "Bring Polly some gifts from the shop.",
        ][
            "Polly: More snacks for Dragon - SQUAWWK!",
            "Bring Polly a few more gifts from the shop to continue.",
        ][
            "Polly: You got the Dragon snacks - BRAWWK!",
            "Polly: Dragon said I had to grow up - SQUAWWK!",
            "Polly: But he was always making sure others didn't hurt me for being different - BRAWWK!",
            "Polly: SQUAWWK - Polly hopes he feels better after eating - BRAWWK!",
        ][
            "You find Polly sitting alone, no birds around her.",
            f"Polly: I've been... thinking, {name_color()}.",
            "Polly: Maybe I should grow up... Maybe being a parrot isn't really what I need...",
            "You sit next to her and listen.",
            "Polly: I do want to retain my youth, but you see, I've been struggling to find my place in your society.",
            "Polly: I've had to beg and steal to survive, and I don't have a home.",
            "Polly: I need to become... normal.",
        ][
            "You suggest to Polly that there could be an alternative: Teaching at Willow's school.",
            "Polly: Willow? That... Goblin girl? She's starting a school?",
            "Polly: ...And you think she'd be ok with... parrots?",
            "You tell Polly that Willow is incredibly accepting.",
            "You also mention that since her school will be mostly young kids, she will fit right in with their humor.",
            "Polly smiles wide.",
            "Polly: BRAWWK - Pretty bird go there at once - SQUAWWK!",
        ][
            "You suggest to Polly that there could be an alternative. Something with kids, perhaps?",
            "Polly: Kids?",
            "Her face lights up with an idea."
            "Polly: Polly could be a schoolteacher - BRAWWK!",
            "Polly: Kids love pretty birds - SQUAWWK!",
        ][
            "You tell Polly you'll buy her some supplies to prepare for her job hunt.",
            f"Polly: Pretty bird loves pretty-{gender[0]} - SQUAWWK!",
            "Buy Polly a few gifts from the shop to continue.",
        ][
            "Polly: You're missing, missing - SQUAWWK!",
            "Buy Polly more gifts to continue.",
        ][
            "Polly looks through the items.",
            "Polly: Everything as it should be - BRAWWK - thank you, thank you!",
            "Polly's face then turns serious as she drops the parrot act once more.",
            "Polly: By the way, you can't get anything past me, I hope you understand.",
        ][
            "Polly: I know you wish to date other people.",
            "Polly: I don't mind in the least, but I do wish you were more open about it.",
        ][
            "Polly: I know you're dating other people.",
            "Polly: I don't mind in the least, but I do wish you were more open about it.",
        ][
            "Polly: I even have my eyes on a certain someone as well...",
            "Polly: So please, let us NOT keep these secrets.",
            "Polly: You'll thank me later.",
            "She kisses your cheek and flies off.",
        ][
            "Polly: SQUAWWK! Don't be clingy, meet other people - BRAAWK!",
        ][
            "Polly: SQUAWWK - Dragon's Mate, Dragon's Mate - BRAWWK!",
            "You look at her as if she's discovered a huge secret.",
            "Polly: SQUAWWK - parrots repeat everything - BRAWWK!",
            "You shake your head and chuckle at her silliness. She laughs too.",
            "Polly: Parrot good teacher - BRAWWK!",
            "Polly: Willow hired on the spot - SQUAWWK!",
            "Polly: Gate is the best, makes Polly laugh - BRAWWK!",
            "Polly lays her head on your lap, and sighs happily.",
            "You decide to amuse her and try your best at impersonating a dog, making her laugh.",
            "Polly: Good effort, needs work - BRAWWK - always improving - SQUAWWK!",
            "The two of you go back and forth as you catch up.",
        ]
    ]
    if romance[0] == 0:
        keys = polly_texts[0]
        for key in keys:
            typewriter(key)
            if key == "Tell Polly your name (y/n)?":
                player_input = input("> ").lower()
                if player_input == 'y':
                    keys0 = polly_texts[1]
                    for key in keys0:
                        typewriter(key)
                        romance_increase_polly()
                elif player_input == 'n':
                    keys0 = polly_texts[2]
                    for key in keys0:
                        typewriter(key)
                        town()
    elif romance[3] == 1 and gift_measurement == 0:
        keys = polly_texts[3]
        for key in keys:
            typewriter(key)
            town()
    elif romance[3] == 1 and gift_measurement >= 10:
        gifts = 0
        keys = polly_texts[4]
        for key in keys:
            typewriter(key)
            romance_increase_polly()
    elif romance[3] == 2 and gift_measurement == 0:
        keys = polly_texts[5]
        for key in keys:
            typewriter(key)
            if key == "Ask Polly if she'll go out with you (y/n)?":
                player_input = input("> ").lower()
                if player_input == "y":
                    keys0 = polly_texts[6]
                    for key in keys0:
                        typewriter(key)
                        town()
                elif player_input == "n":
                    keys0 = polly_texts[7]
                    for key in keys0:
                        typewriter(key)
                        town()
    elif romance[3] == 2 and 0 < gift_measurement < 20:
        keys = polly_texts[8]
        for key in keys:
            typewriter(key)
            town()
    elif romance[3] == 2 and gift_measurement >= 20:
        gifts = 0
        keys = polly_texts[9]
        for key in keys:
            typewriter(key)
            player_input = input("> ")
            if player_input == "y":
                keys0 = polly_texts[10]
                for key in keys0:
                    typewriter(key)
            elif player_input == "n":
                keys0 = polly_texts[11]
                for key in keys0:
                    typewriter(key)
            keys1 = polly_texts[12]
            for key in keys1:
                typewriter(key)
                romance_increase_polly()
    elif romance[3] == 3 and gift_measurement == 0:
        keys = polly_texts[13]
        for key in keys:
            typewriter(key)
            player_input = input("> ")
            if player_input == "y":
                keys0 = polly_texts[14]
                for key in keys0:
                    typewriter(key)
                    town()
            elif player_input == "n":
                keys0 = polly_texts[15]
                for key in keys0:
                    typewriter(key)
                    town()
    elif romance[3] == 3 and 0 < gift_measurement < 30:
        keys = polly_texts[16]
        for key in keys:
            typewriter(key)
            town()
    elif romance[3] == 3 and gift_measurement >= 30:
        keys = polly_texts[17]
        for key in keys:
            romance_increase_polly()
    elif romance[3] == 4 and gift_measurement == 0:
        keys = polly_texts[18]
        for key in keys:
            typewriter(key)
            player_input = input("> ")
            if player_input == "y":
                keys0 = polly_texts[19]
                for key in keys0:
                    typewriter(key)
            elif player_input == "n":
                keys0 = polly_texts[20]
                for key in keys0:
                    typewriter(key)
            keys1 = polly_texts[21]
            for key in keys1:
                typewriter(key)
                town()
    elif romance[3] == 4 and 0 < gift_measurement < 40:
        keys = polly_texts[22]
        for key in keys:
            typewriter(key)
            town()
    elif romance[3] == 4 and gift_measurement >= 40:
        keys = polly_texts[23]
        for key in keys:
            typewriter(key)
            romance_increase_polly()
    elif romance[3] == 5 and gift_measurement == 0:
        keys = polly_texts[24]
        for key in keys:
            typewriter(key)
            keys0 = polly_texts[25] if romance[0] >= 4 else polly_texts[26]
            for key in keys0:
                typewriter(key)
            keys1 = polly_texts[27]
            for key in keys1:
                typewriter(key)
                town()
    elif romance[3] == 5 and 0 < gift_measurement < 50:
        keys = polly_texts[28]
        for key in keys:
            typewriter(key)
            town()
    elif romance[3] == 5 and gift_measurement >= 50:
        keys = polly_texts[29]
        for key in keys:
            typewriter(key)
            if romance[0] and romance[1] and romance[2] and romance[4] == 0:
                keys0 = polly_texts[30]
                for key0 in keys0:
                    typewriter(key0)
            elif romance[0] or romance[1] or romance[2] or romance[4] > 0:
                keys0 = polly_texts[31]
                for key0 in keys0:
                    typewriter(key0)
            keys1 = polly_texts[32]
            for key1 in keys1:
                typewriter(key1)
                romance_increase_polly()
    elif romance[3] == 6:
        if romance[5] < 6:
            keys = polly_texts[33]
            for key in keys:
                typewriter(key)
                town()
        elif romance[5] == 6:
            keys = polly_texts[34]
            for key in keys:
                typewriter(key)
                town()




def gate():
    global romance, gifts, player_stats

    gate_texts = { "You notice a group of people crowding around a single spot.": { },
                   "As you go to investigate, you hear a familiar voice yell out from the crowd.": { },
                   "Gate: One at a time, please! I know my cooking is delicious, but ONE AT A TIME!": { },
                   "Push through the crowd to see for yourself (y/n)?":
                       { 'y': { "You push through the crowd where Gate is, quite literally, inside of a cooking pot.",
                                "Gate: Oh! Hi there! You're the adventurer who brought peace to our homes!!",
                                "Gate: Don't worry about me, this is how all Slimes cook!",
                                "Gate: But I will admit I'm getting a little claustrophobic in this crowd.",
                                "Gate: Can you shoo them away for me please?" },
                         'n': { "You leave Gate to their cooking.", town() } },
                   "Help Gate get rid of the crowd (y/n)?": {
                       'y': { "You turn to the crowd and announce that Gate is officially closing shop.",
                              "The crowd, of course, doesn't listen.",
                              "Gate looks at you with amusement in their eyes.", "Gate: That's ok, I can handle it!" },
                       'n': { "They look at you with a frustrated glare", "Gate: Fine, I'll do it myself!" } },
                   "The water around Gate suddenly starts to rapidly boil.": { },
                   "The crowd anxiously backs up, and people slowly start to trickle away..": { },
                   "Gate: Thank you... friend.": { }, "Gate: What's your name again?": { },
                   "You tell Gate your name.": { },
                   f"Gate: Ah, well thank you, {name_color()}!": { }, "Gate: I hope we can chat again soon!": { },
                   "You meet up with Gate as they're reading a book of what looks like a bunch of cooking recipes.": { },
                   f"Gate: Oh, hey there {name_color()}.": { },
                   "Gate: I was just looking at the way you humans cook!": { },
                   "Gate: There seems to be an odd lack of, well, human in it.": { },
                   "Gate: When us Slimes cook, we quite literally put our bodies into it.": { },
                   "Gate: But humans seem to just... replace Slime with some sort of process called...": { },
                   "Gate's face contorts as they try to remember what they read.": { }, "Gate: ...Soogarr?": { },
                   "Gate: Can you explain how to add this... soogarr?": { },
                   "Take the time to explain sugar to Gate (y/n)?": {
                       'y': { "You try to explain how sugar works to Gate, as well as"
                              " the fact that humans aren't made of sweet stuff.",
                              "Gate: That's... fascinating. Odd, but fascinating.",
                              "Gate: Could you possibly get me some of this... sugar stuff... to try?" },
                       'n': { "Gate: Well, I'd still like to try this... soogarr stuff. Could you get me some?" } },
                   "Gate: I would be very grateful!": { }, "Buy Gate a gift from the shop to continue.": { },
                   town(): { },
                   "You find Gate at their usual spot in the town centre happily whisking what looks like cake batter.": { },
                   "Gate: You got the soogar - I mean, sugar?": { }, "Gate: You did! Thank you so much!": { },
                   "They take a sprinkle of sugar and swallow it, then start coughing.": { },
                   "Gate: Gross! You humans EAT this dry stuff?": { },
                   "Gate: No, no way! I will NOT have this be part of my recipes!": { },
                   "Gate then looks at you with a softer expression.": { },
                   f"Gate: Oh, but I do like that you tried to help me, {name_color()}.": { },
                   "Gate: Would you like some of this cake when I'm done with it?": { },
                   "Gate: I usually charge, but for you, it's on the house!": { },
                   "You sit with Gate as they bake, listening to them ramble on about whatever comes to mind.": { },
                   "Gate: ...It's all about making a mess!": { },
                   "Gate: The best cakes - and best cooking in general - is always the messiest!": { },
                   "Gate: The messier it is, the more Slime gets in the cooking, you see.": { },
                   "Gate: And therefore, the sweeter it is!": { },
                   "Gate: But the cake's almost done! Want to try?": { },
                   "You take a bite of Gate's cake. It's one of the best you've ever had!": { },
                   "Gate: I knew you'd like it! It's made with affection!": { },
                   "You sit and talk with Gate or a few more hours, and then head home.": { }, town(): { },
                   "You go to Gate's usual spot, but they aren't there.": { },
                   "You start walking in the direction of the Mayor's house, wondering where they went.": { },
                   "You find them, angrily shouting at the Mayor's closed door.": { },
                   "Gate: I AM NOT A FREAK! I AM A CHEF!": { }, "Ask Gate what happened (y/n)?": {
            'y': { "Gate jolts, and turns around to face you.", f"{name_color()}! Don't scare me like that!",
                   "You ask Gate how you can help.",
                   "Gate: That jerk of a Mayor is sending out propaganda against Slimes!",
                   "Gate: He's saying our bodies are toxic and we're poisoning the humans with our cooking!",
                   "You hear the Mayor's voice from the other side of the door.",
                   "Mayor: I will NOT have SLIME in my FOOD!",
                   "Mayor: You freaks better get out of here immediately!",
                   "Gate: Can you bring me some tools to try and get this door open? I just want to... talk.",
                   "Bring Gate a gift from the shop to continue.", town() },
            'n': { "You leave Gate to themself.", town() } }, "Gate looks through your collection of tools.": { },
                   "Gate: ...You're missing one. Can you go back and get it?": { },
                   "Return when you have one more gift.": { }, town(): { },
                   "Gate: You got them! Perfect, now let me just do this...": { },
                   "They grab the tools and cover the entirety with slime.": { },
                   "Gate: Now we're ready to begin.": { },
                   "Gate takes a lockpick and easily manages to open the door.": { },
                   "Gate: OK Mayor-person! Come out wherever you are!": { },
                   "The Mayor's voice shouts back from inside:": { },
                   "Mayor: Leave me be! Why can't you freaks just let us NORMAL people be ourselves!?": { },
                   "Gate: Why can't you so-called NORMAL people accept that not everyone is the same!?": { },
                   "Stop the argument (y/n)?": {
                       'y': { "You tell Gate it isn't worth the effort. Some people just won't change.",
                              "Gate: ...Yeah, you're right. Let's go home." },
                       'n': { "Gate: This is stupid. I'm not getting arrested today. Let's go home." } },
                   "They lead you to their home in the town.": { },
                   "As you walk, Gate is still seething and mumbling under their breath.": { },
                   "Gate: Mnmnm call us freaks... mmnmmnm I'll show him...": { }, "Gate: ...Jerk.": { },
                   "You get to a small house in a less savory area.": { }, "Gate: This is it...": { },
                   "There's an unusual pause of silence. Gate isn't their normal, talkative self.": { },
                   "Gate: ...": { },
                   "Gate: ...I'm sorry I blew up like that.": { }, "Gate: I just wish...": { },
                   "Gate: Well, would you like to come inside? I can... I can make you something to eat?": { },
                   "You agree, and the two of you spend the evening chatting together.": { },
                   "You find Gate once again happily making food for humans.": { }, f"Gate: Heyy, {name_color()}!": { },
                   "Gate: The Mayor has stopped putting out the propaganda! We're back in business!": { },
                   "Gate: The two of us really scared him, didn't we?": { },
                   "Gate hops out of the pot and saunters over to you, as much as a Slime can.": { },
                   "They turn to the crowd that is eagerly waiting for the soup.": { },
                   f"Gate: This one is on the house, courtesy of {name_color()}!": { },
                   "The crowd cheers, and closes around the pot of Slime soup. Gate leans in and whispers to you.": { },
                   "Gate: Hurry, while they're distracted. Let's go.": { },
                   "The two of you scurry off, leaving the crowd behind.": { },
                   "Gate: I wanted to tell you how I appreciated having my back with the Mayor.": { },
                   "Gate: I also was thinking about Dragon...": { },
                   "Gate: Do you know the history behind Dragons and Slimes?": { }, "Do you know (y/n)?": {
            'y': { "Gate: Oh, so you do know a little about Slimes!" },
            'n': { "Gate: Oh. Well, you see, Dragons are natural predators of Slimes.",
                   "Gate: Since Slimes don't age, or really die of anything else...",
                   "Gate: Dragons have to keep us from dying out by, well, hunting and eating us." } },
                   "When we joined Dragon's army, he outlawed eating Slimes because we were dying out.": { },
                   "Gate: He told me I couldn't be a chef because his Mates might try to eat me instead.": { },
                   "Gate: He always looked out for us... in his own way.": { },
                   "Gate: I wish I had realized it before now...": { },
                   "Gate: Can you help me make a gift basket for Dragon to show my appreciation?": { },
                   "Get some gifts from the shop to continue the story with Gate!": { }, town(): { },
                   "Gate: You got a few gifts, but we need a little more for the basket.": { },
                   "Buy Gate more gifts to continue!": { }, town(): { },
                   "Gate peers with wide eyes at the mound of gifts, then makes a gesture like an evil mastermind.": { },
                   "Gate: ...Excellent.": { }, "Gate: This is the perfect selection to start my evil plan to...": { },
                   "They notice you staring.": { }, "Gate: ..Too much?": { }, "You nod.": { },
                   "Gate: Sorry. Well, anyway, I need to make the gift basket now. Can you help me with it?": { },
                   "You begin to ask why, but then see Gate's Slime body and realize what they meant.": { },
                   "Gate: ...Yeah. Slimy.": { },
                   "You chat with Gate while you make the basket for the rest of the afternoon.": { },
                   "It's later than usual when you arrive in town. You decide to drop by Gate's home to see them.": { },
                   "As you knock on the door, you hear Gate quietly sniffling behind it.": { },
                   "Gate: Go away! I said I wouldn't cook anymore!": { }, "Leave Gate alone (y/n)?": {
            'y': { "You leave Gate's house, wondering what could have happened to make him quit?", town() },
            'n': { "You knock louder.",
                   "Gate: I said go away! What more could you want from me? DO YOU WANT ME TO DIE!?",
                   "The last comment catches you off-guard and you frantically yell for Gate to open the door.",
                   f"Gate: ...{name_color()}?", "The door slowly opens to reveal Gate, but not as you knew them.",
                   "Gate's body, where it was once a gelatinous cube, is now a soppy puddle on the floor.",
                   "You can't even see their mouth or eyes anymore.", "Gate: Look what they did to me!",
                   "Gate: They said I'm a monster! They tore apart all my cookbooks... they...",
                   "Gate: THEY POURED SALT ON ME!!!",
                   "You ask if that's how they ended up like this.",
                   "Gate: Yes, Slimes are made of a special substance that melts when combined with salt.",
                   "Gate: I'll eventually reform, but it will take weeks...",
                   "Gate: ...and all my cookbooks are ruined!",
                   "Gate: I'll never cook again!",
                   "See if you can find a gift from the shop that can cheer Gate up.", town() } },
                   "...You probably want to get a larger selection before returning to Gate.": { }, town(): { },
                   "You find a dejected, but slightly less puddly, Gate still hiding in their house.": { },
                   "Gate: ...What's that you got there?": { },
                   "You hand Gate the empty books you got them.": { },
                   "Gate: ...empty cookbooks? With labels and everything?": { },
                   "Gate: So... I guess this is your way of saying I should write my own recipes?": { },
                   "You confirm their suspicions.": { },
                   "Gate looks at the books, then back at you. There's a long pause as they consider the idea.": { },
                   "Gate: ...Thanks.": { },
                   "They slowly grab a pen from a nearby table and within moments are buried in the pages.": { },
                   "You leave Gate to their work.": { },
                   "It's been quite a few days since you checked on Gate. They should be feeling better now.": { },
                   "As you make your way toward their house, you hear a commotion in a back alley nearby.": { },
                   "Investigate (y/n)?": {
                       'n': { "You decide it isn't your fight and go to Gate's house. They aren't home."
                              "Your gut churns as something inside you says to check the alley." },
                       'y': { } }, "You look down the alley to find Gate cornered by a bunch of city guards!": { },
                   "Gate is trapped. They seem mostly unharmed so far, but the guards are closing in.": { },
                   "Guard: Didn't the Mayor tell you to stop making SLIME GUMP?": { }, "Gate: Let me go!": { },
                   "Acting on instinct alone, your legs propel you forward.": { },
                   "You run between Gate and the guards and draw your sword.": { },
                   "Guard: Look who came to save you, freak!": { },
                   "The guard sneers at you, seemingly unphased by your sharpened blade.": { },
                   "Guard: You're that cowardly adventurer! Do you even know how to USE that, toothpick?": { },
                   "Fight the guards (y/n)?": {
                       'y': { "Five guards. Five strikes. All you needed was to take them down."
                              "The guards lie beaten at your feet. Not dead, but not in great shape either." },
                       'n': { "You take a defensive stance, but do not attack.",
                              "The guards charge you, but you continue to block and parry their attacks.",
                              "Eventually, the guards tire out.",
                              "Guard: Ahh, whatever! You'll get what's coming for ya eventually! All of ya freaks!" } },
                   "You scoop up Gate and take them home.": { }, "Gate: You... saved me...": { },
                   f"Gate: Can I tell you something, {name}?": { },
                   "Gate: But that's ok. Just... please let's not keep it a secret anymore.": { },
                   "Gate: 'Cause I really do love you...": { },
                   "Gate falls asleep in your arms as you walk back to their house.": { },
                   "This time, you stay and take care of them as they recover.": { },
                   "Eventually, the Mayor stops sending guards to harass the two of you.": { },
                   "You leave a few days later, after making sure Gate is fine enough to take care of themselves.": { },
                   town(): { }, "You visit Gate at their house. They greet you with a hug.": { },
                   "Gate: Welcome, welcome! Welcome in!": { },
                   "Gate: Oh, but honestly, I'm fine! You shouldn't keep checking on me!": { },
                   "Gate: There's a whole world of friends to meet!": { },
                   "They do their best impression of a human wink.": { }, "Gate: And more-than-friends, too!": { },
                   "You both laugh, and you leave Gate to their cooking.": { }, town(): { },
                   "Gate: Did you hear the news about me and Polly?": { },
                   "Gate: Or were you too busy canoodling with Dragon?": { },
                   "They laugh at your questioning gaze.": { },
                   "Gate: Oh, you know people are talking up a storm about Dragon's new Mate!": { },
                   "Gate: Don't worry, I'm not angry! I gave you permission, after all!": { },
                   "Gate: Besides, Polly and I have been having a time of it for the last few months!": { },
                   "Gate: And with Sam and Willow getting married soon, I was thinking of proposing, too.": { },
                   "Gate: But, all in due time. They say good things come to those who wait, after all!": { },
                   "Gate: Any-who, what's up with you? Aside from the obvious?": { },
                   "The two of you share stories as the sun goes down.": { }, town(): { },
                   }
    if romance[2] < 1:
        keys = list(gate_texts.keys())[:4]
        for key in keys:
            typewriter(key)
            if key == "Push through the crowd to see for yourself (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in gate_texts[key][player_input]:
                        typewriter(sub_key)
                        keys = list(gate_texts.keys())[5]
                        for key in keys:
                            typewriter(key)
                            player_input = input("> ").lower()
                            if player_input in ['y', 'n']:
                                for sub_key0 in gate_texts[key][player_input]:
                                    typewriter(sub_key0)
                                    keys0 = list(gate_texts.keys())[6:12]
                                    for key in keys0:
                                        typewriter(key)
                                        romance[2] += 1
                                        typewriter("You've increased your romance score with Gate!")
                                        typewriter(f"Your new score is {str(romance[2])}")
                                        town()
    elif romance[2] == 1 and player_stats[11] * gifts * player_stats[9] == 0:
        keys = list(gate_texts.keys())[13:22]
        for key in keys:
            typewriter(key)
            if key == "Take the time to explain sugar to Gate (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in gate_texts[key][player_input]:
                        typewriter(sub_key)
                        keys0 = list(gate_texts.keys())[23:25]
                        for key in keys0:
                            typewriter(key)
    elif romance[2] == 1 and player_stats[11] * gifts * player_stats[9] >= 10:
        gifts = 0
        keys = list(gate_texts.keys())[26:45]
        for key in keys:
            typewriter(key)
            romance[2] += 1
            typewriter("You've increased your romance score with Gate!")
            typewriter(f"Your new score is {str(romance[2])}")
            town()
    elif romance[2] == 2 and player_stats[11] * gifts * player_stats[9] == 0:
        keys = list(gate_texts.keys())[46:50]
        for key in keys:
            typewriter(key)
            if key == "Ask Gate what happened (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in gate_texts[key][player_input]:
                        typewriter(sub_key)
    elif romance[2] == 2 and 0 < player_stats[11] * gifts * player_stats[9] < 20:
        keys = list(gate_texts.keys())[51:54]
        for key in keys:
            typewriter(key)
    elif romance[2] == 2 and player_stats[11] * gifts * player_stats[9] >= 20:
        gifts = 0
        keys = list(gate_texts.keys())[55:63]
        for key in keys:
            typewriter(key)
            if key == "Stop the argument (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in gate_texts[key][player_input]:
                        typewriter(sub_key)
                        keys0 = list(gate_texts.keys())[64:75]
                        for key in keys0:
                            typewriter(key)
                            romance[2] += 1
                            typewriter("You've increased your romance score with Gate!")
                            typewriter(f"Your new score is {str(romance[2])}")
                            town()
    elif romance[2] == 3 and player_stats[11] * gifts * player_stats[9] == 0:
        keys = list(gate_texts.keys())[76:89]
        for key in keys:
            typewriter(key)
            if key == "Do you know (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in gate_texts[key][player_input]:
                        typewriter(sub_key)
                        keys9 = list(gate_texts.keys())[90:96]
                        for key in keys0:
                            typewriter(key)
    elif romance[2] == 4 and 0 < player_stats[11] * gifts * player_stats[9] < 30:
        keys = list(gate_texts.keys())[97:99]
        for key in keys:
            typewriter(key)
    elif romance[2] == 3 and player_stats[11] * gifts * player_stats[9] >= 30:
        gifts = 0
        keys = list(gate_texts.keys())[100:109]
        for key in keys:
            typewriter(key)
            romance[2] += 1
            typewriter("You've increased your romance score with Gate!")
            typewriter(f"Your new score is {str(romance[2])}")
            town()
    elif romance[2] == 4 and player_stats[11] * gifts * player_stats[9] == 0:
        keys = list(gate_texts.keys())[110:113]
        for key in keys:
            typewriter(key)
            if key == "Leave Gate alone (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in gate_texts[key][player_input]:
                        typewriter(sub_key)
    elif romance[2] == 4 and 0 < player_stats[11] * gifts * player_stats[9] < 40:
        keys = list(gate_texts.keys())[114:115]
        for key in keys:
            typewriter(key)
    elif romance[2] == 4 and player_stats[11] * gifts * player_stats[9] >= 40:
        gifts = 0
        keys = list(gate_texts.keys())[116:125]
        for key in keys:
            typewriter(key)
            romance[2] += 1
            typewriter("You've increased your romance score with Gate!")
            typewriter(f"Your new score is {str(romance[2])}")
    elif romance[2] == 5 and player_stats[11] * gifts * player_stats[9] == 0:
        keys = list(gate_texts.keys())[126:128]
        for key in keys:
            typewriter(key)
            if key == "Investigate (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in gate_texts[key][player_input]:
                        typewriter(sub_key)
                        keys0 = list(gate_texts.keys())[129:138]
                        for key in keys0:
                            typewriter(key)
                            if key == "Fight the guards (y/n)?":
                                player_input = input("> ").lower()
                                if player_input in ['y', 'n']:
                                    for sub_key0 in gate_texts[key][player_input]:
                                        typewriter(sub_key0)
                                        keys1 = list(gate_texts.keys())[139:141]
                                        for key in keys1:
                                            typewriter(key)
                                            if romance[0] or romance[1] or romance[3] or romance[4] > 1:
                                                typewriter("I know you're with others...")
                                            else:
                                                typewriter("I know you want to see others...")
                                            keys2 = list(gate_texts.keys())[142:149]
                                            for key in keys2:
                                                typewriter(key)
                                                romance[2] += 1
                                                typewriter("You've increased your romance score with Gate!")
                                                typewriter(f"Your new score is {str(romance[2])}")
                                                town()
    elif romance[2] == 6:
        keys = list(gate_texts.keys())[150:151]
        for key in keys:
            typewriter(key)
        if romance[5] < 6:
            keys0 = list(gate_texts.keys())[152:157]
            for key in keys0:
                typewriter(key)
        elif romance[5] == 6:
            keys0 = list(gate_texts.keys())[158:168]
            for key in keys0:
                typewriter(key)


def sam():
    global player_stats, gifts
    sam_texts = { "The highly masculine Orc is standing alone. She greets you in her usual gruff voice.": { },
                   "Sam: Heya, " + name_color() + "!": { },
                   "Sam: So, the town is saved and Dragon is defeated!": { },
                   "Sam: That leaves one question: Who are you and why are you talking to me?": { },
                   "Tell Sam your name (y/n)?": {
                       'n': {
                           "She looks slightly outraged.",
                           "Sam: Oh well, whatever. I'll be off now.",
                           "She walks away, leaving you wondering if that was the right choice", town()
                       },
                       'y': {
                           "Sam: Oh, " + name_color() + ".  That's a cool name.",
                           "Sam: So... what do you want?" } }, "Ask Sam on a date (y/n)?": {
            'y': { "Sam: A date? W-With me?",
                   "The Orc looks shocked for a moment, before regaining her composure.",
                   "Sam: Yeah, sure! I could use some fresh air. How about we meet at the training camp?",
                   "Sam: We can spar for a bit there.",
                   "Sam: Be sure to get a wooden sword for yourself, though! Your real one won't be allowed in!",
                   "Buy Sam a gift from the shop to continue." },
            'n': {
                "You tell Sam you just wanted to say hi. She looks at you with quiet rage.",
                "Sam: Oh well, hi. I'll be off now.",
                "She walks away, leaving you wondering if that was the right choice", town() } },
                   "Sam: If you don't want to go out, just say so!": { }, "Buy Sam a gift to continue.": { },
                   "You and Sam head to the sparring area of the training camp.": { },
                   "You go at it for hours, Sam continuously impressing you with her speed and agility.": { },
                   "After some time sparring, Sam stops and looks toward the west.": { },
                   "Sam: The sunset is beautiful, isn't it, " + name_color() + "?": { }, "Agree with Sam (y/n)?": {
            'y': "Sam: Beautiful, yes...",
            'n': "Sam laughs. Sam: I guess a hardened adventurer like you can't appreciate beauty."
        },
                   "Sam: Beauty...": { },
                   "She looks down at her masculine frame.": { },
                   "She stares at her large hands and touches her square jaw.": { },
                   "Sam: I wish I was as beautiful as some of the Orc females I've seen...": { },
                   "Sam: I'm sure you've figured it out by now, player, so I need not say it...": { },
                   "Sam: ... and I don't know why you asked me out, but I appreciate your kindness.": { },
                   "Sam: This is the best I could have asked for, as a first date.": { },
                   "The two of you sit and silently watch the sun set.": { },
                   "Sam: Hey, " + name_color() + "!": { }, "Sam: I was just thinking about you.": { },
                   "Sam: I realized after our date that I accidentally kept your fake sword.": { },
                   "Sam: You wouldn't mind if I kept it as a momento?": { }, "Allow Sam to keep the sword (y/n)?": {
            'y': { "Sam: Oh, awesome! Thank you, ", name_color(), "!" },
            'n': { "Sam: Oh. Well, since you don't need it I guess I'll throw it out.",
                   "She looks slightly upset, but contains herself." } },
                   "Sam: Oh, by the way, my brother's in town signing a treaty with the Mayor.": { },
                   "Sam: I feel like all that political nonsense gets more in the WAY of peace than it HELPS.": { },
                   "Sam: Either way, I've been assigned as the Mayor's 'Orc Emissary' or some garbage.": { },
                   "Sam: Problem is, I don't have the money to get a horn and mug for my brother, as is our custom.": { },
                   "Sam: Can you get me one of each from the shop?": { },
                   "Buy a gift from the Shop to continue.": { }, town(): { },
                   "Sam: You got the horn, but we still need the mug!": { }, "Buy Sam another gift to continue.": { },
                   town(): { },
                   "Sam: Great! And just in time, too! The treaty is going to be signed tomorrow.": { },
                   "Sam: Maybe after that I can finally be done with politics and this stupid 'Orc Tribe' nonsense.": { },
                   "Sam: Don't get me wrong, my brother does a great job of leading our tribe.": { },
                   "Sam: I just wish I could have willingly passed it to him earlier.": { },
                   "Sam: You know what I mean?": { },
                   "Ask what Sam means (y/n)?": {
                       'y': { "Sam: Oh, that's right. I may have forgotten not everyone grows up in Orc society.",
                              "Sam: Basically, I was supposed to be the leader when I was born.",
                              "Sam: I was the first son and that made me the heir.",
                              "Sam: But I never wanted to be.",
                              "Sam: I like combat, but politics... well, they aren't my thing.",
                              "Sam: Not that I even thought about that when I told my parents I wanted to be a woman." },
                       'n': { "She chuckles.", "Sam: So you know a little about Orcs, then. That's good." }, },
                   "You ask Sam if that's what Willow meant when she talked about you leading the Orcs.": { },
                   "Sam: Willow? She's... She's alive?": { },
                   "Sam: And... she knows about... me?": { },
                   "You confirm Willow knows about Sam's womanhood, and reassure her that Willow kind of "
                   "figured it out.": { },
                   "Sam: Wow... she was always smarter than she usually let on.": { },
                   "Sam: I should visit her sometime, then.": { },
                   "Sam: My dad thought I was just trying to get an 'easier life.'": { },
                   "She looks at the ground, angry tears welling in her eyes.": { },
                   "Sam: Life isn't easier, though! It's just different.": { },
                   "Sam: It's just... mine.": { }, "You sit with each other in silence.": { },
                   "Sam runs up to you, looking more excited than you've ever seen her.": { },
                   "Sam: " + name_color() + "! Did you hear the news!?": { }, "Did you hear (y/n)?": {
            'y': { "Sam: Oh, you did? It's wonderful isn't it!?" },
            'n': { "Sam: I don't have to be a slave!", "Sam notices your look of confusion.",
                   "Sam: Oh, right, Orc stuff...",
                   "Sam: As an Orc woman in our tribe, I was destined for slavery.",
                   "Sam: When Dragon came and took over, he abolished it and made all of us into soldiers.",
                   "Sam: But with him gone, our tribe was debating whether or not we should keep it that way.",
                   "Sam: The mayor said he would not be opposed to enslaving female Orcs...",
                   "Sam: But my brother put his foot down against it and refused to budge!",
                   "Sam: So now... we're free! We won't have to be slaves! We're equals in both the town and my tribe!" } },
                   "Looking into Sam's eye,you notice for the first time how effeminate she seems when she's happy.": { },
                   "Sam: Can you bring me something so I can cherish this moment forever?": { },
                   "Maybe a few books so that every time I open one, I remember yours and my brother's kindness.": { },
                   "Buy some gifts from the Shop to continue.": { }, town(): { },
                   "Sam: You brought some books!": { },
                   "Sam: Oh, but could you get me some more? Please?": { },
                   "Sam looks at you with puppy-dog eyes until you agree.": { }, town(): { },
                   "Sam: You got the books! Thank you so so much!": { },
                   "Sam: You know, I was always nervous that the Dragon would change the law back after the war.": { },
                   "Sam: But maybe... he wasn't planning to.": { },
                   "Sam: I'll have to think about this some more...": { },
                   "Sam: I was thinking about the slave laws and how Dragon got rid of them.": { },
                   "Sam: He may have messed up a few times, but he seemed to do his best.": { },
                   "Sam: ...He made quite a few changes that helped my sisters-in-arms.": { },
                   "Sam: Leadership is a curse, I know that much. And Dragon was another victim of it.": { },
                   "Sam: Can you bring me something so I can give it to him, to show my appreciation?": { },
                   "Bring Sam some gifts to give to Dragon": { }, town(): { },
                   "Sam: That's a good start, but we'll need more.": { },
                   "Bring Sam more gifts for Dragon!": { }, town(): { },
                   "Sam: Amazing! Thank you so much!": { },
                   "Sam: You know, Dragon would banish or kill anyone who tried to hurt an Orc woman.": { },
                   "Sam: It didn't matter why, or who, he placed strict rules around conduct with the fairer sex.": { },
                   "Sam: I hope this can make up for how I treated him...": { },
                   "Sam: I appreciate everything you've done for me, " + name_color() + ".": { },
                   "Sam: Can you do me a HUGE favor, " + name_color() + "?": { }, "Do a favor for Sam (y/n)?": {
            'y': { "Sam: Thank you! I knew I could count on you!", "Sam: Here's the gist of it:" },
            'n': { "Sam looks at you, exasperated.", "Sam: But you haven't even heard what it is!" } },
                   "Sam: The shop just released a new potion line.": { },
                   "Sam: It lasts for 24 hours and turns you into a woman or man, depending what you started as!": { },
                   "Sam: I could finally be a woman for once!": { },
                   "Sam: Can you run to the shop and PLEASE get me a sample until I can save enough for a sub box?": { },
                   "Bring Sam a few gifts to last her until she can afford it herself.": { }, town(): { },
                   "Sam: Oh, back so soon?": { },
                   "Sam: I don't think that's enough potions to keep me stocked...": { },
                   "Sam: Can you get just a few more, please?": { },
                   "Bring Sam a few more potions to last her a little longer.": { }, town(): { },
                   "Sam: Oh wow! There's so many!": { },
                   "Sam eagerly takes one of the potions from your bag and drinks it.": { },
                   "Sam: I feel... woozy...": { },
                   "Sam passes out.": { },
                   "You wait for a few hours as Sam's body undergoes magical transformations.": { }, "...": { },
                   "Suddenly, she wakes up.": { }, "Sam: Ooh, my head...": { }, "Sam: Wait, I'm...": { },
                   "Sam: I'm... ": { },
                   "Sam's body has completely changed. Her rough lines replaced with curves.": { },
                   "Sam: I'M A WOMAN!!!": { },
                   "Sam's high-pitched squeal of joy echoes through the town.": { },
                   "Her voice is still a little on the deeper side.": { },
                   "However, it's more like the soothing tones of a harp, rather than the gruffness you heard before.": { },
                   "There's no doubt about it, her body, voice, and mind is 100% female now.": { },
                   "Sam: I CAN'T BELIEVE IT! THANK YOU!!!": { }, "Sam kisses you on the cheek, and runs off": { },
                   "Sam: Well, if it isn't my favorite " + gender[0] + "!": { },
                   "Sam: I've been thinking about yoouuu!": { },
                   "Sam: I think we shouldn't be... too... exclusive!": { },
                   "Sam: Go enjoy yourself, and I'll do the same!": { }, town(): { }, "Sam: Well, well, well...": { },
                   "Sam: If it isn't the Dragon's new Mate!": { },
                   "Sam: I'm happy for you two! You seem to really bring out the best in each other!": { },
                   "Sam: Meanwhile, my amazing soon-to-be-wife and I are working together on her school.": { },
                   "Sam: Willow is perfect for me, so funny and kind!": { },
                   "Sam: Though, I will always be willing to make time for you, sweetheart.": { },
                   "Sam: Until then, toodle-oo!": { },
                   "Sam waltzes away, blowing you a kiss as she turns.": { } }

    if romance[1] == 0:
        keys = list(sam_texts.keys())[:5]
        for key in keys:
            typewriter(key)
            if key == "Tell Sam your name (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in sam_texts[key][player_input]:
                        typewriter(sub_key)
                        player_input = input("> ").lower()
                        if player_input in ['y', 'n']:
                            for sub_key0 in sam_texts[key][player_input]:
                                typewriter(sub_key0)
                        else:
                            typewriter("Invalid input.")
                else:
                    typewriter("Invalid input.")
        romance[1] += 1
        typewriter("You've increased your romance score with Sam!")
        typewriter("Your new score is: " + str(romance[1]) + "!")
    elif romance[1] == 1 and player_stats[11] * gifts * player_stats[9] == 0:
        keys = list(sam_texts.keys())[6:8]
        for key in keys1:
            typewriter(key)

    elif romance[1] == 1 and player_stats[11] * gifts * player_stats[9] >= 10:
        keys = list(sam_texts.keys())[9:12]
        for key in keys:
            typewriter(key)
            if key == "Agree with Sam? (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key2 in sam_texts[key][player_input]:
                        typewriter(sub_key2)
        keys1 = list(sam_texts.keys())[13:21]
        for key in keys1:
            typewriter(key)
    elif romance[1] == 2 and player_stats[11] * gifts * player_stats[9] == 0:
        keys = list(sam_texts.keys())[22:26]
        for key in keys:
            typewriter(key)
            if key == "Allow Sam to keep the sword (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in sam_texts[key][player_input]:
                        typewriter(sub_key)
        keys1 = list(sam_texts.keys())[27:33]
        for key in keys1:
            typewriter(key)
    elif romance[1] == 2 and player_stats[11] * gifts * player_stats[9] < 20:
        keys = list(sam_texts.keys())[34:36]
        for key in keys:
            typewriter(key)
    elif romance[1] == 2 and player_stats[11] * gifts * player_stats[9] >= 20:
        gifts = 0
        keys = list(sam_texts.keys())[37:42]
        for key in keys:
            typewriter(key)
            if key == "Ask what Sam means (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in sam_texts[key][player_input]:
                        typewriter(sub_key4)
        if romance[0] == 2:
            keys = list(sam_texts.keys())[43:48]
            for key in keys8:
                typewriter(key)
            keys1 = list(sam_texts.keys())[49:52]
            for key in keys9:
                typewriter(key)
            romance[1] += 1
            typewriter("You've increased your romance score with Sam!")
            typewriter("Your new score is " + str(romance[1]) + "!")
            town()
    elif romance[1] == 3 and gifts == 0:
        keys = list(sam_texts.keys())[53:55]
        for key in keys:
            typewriter(key)
            if key == "Did you hear (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in sam_texts[key][player_input]:
                        typewriter(sub_key)
        keys0 = list(sam_texts.keys())[56:60]
        for key in keys0:
            typewriter(key)
    elif romance[1] == 3 and 0 < player_stats[11] * gifts * player_stats[9] < 30:
        keys = list(sam_texts.keys())[61:64]
        for key in keys:
            typewriter(key)
        town()
    elif romance[1] == 3 and player_stats[11] * gifts * player_stats[9] >= 30:
        gifts = 0
        keys = list(sam_texts.keys())[65:68]
        for key in keys:
            typewriter(key)
        romance[1] += 1
        "You've increased your romance score with Sam!"
        "Your new score is " + str(romance[1])
    elif romance[1] == 4 and player_stats[11] * gifts * player_stats[9] == 0:
        keys = list(sam_texts.keys())[68:73]
        for key in keys:
            typewriter(key)
    elif romance[1] == 4 and 0 < player_stats[11] * gifts * player_stats[9] < 40:
        keys = list(sam_texts.keys())[74:76]
        for key in keys:
            typewriter(key)
    elif romance[1] == 4 and player_stats[11] * gifts * player_stats[9] >= 40:
        gifts = 0
        keys = list(sam_texts.keys())[77:81]
        for key in keys:
            typewriter(key)
        romance[1] += 1
        "You've increased your romance score with Sam!"
        "Your new score is " + str(romance[1])
        town()
    elif romance[1] == 5 and player_stats[11] * gifts * player_stats[9] == 0:
        keys = list(sam_texts.keys())[82:83]
        for key in keys:
            typewriter(key)
            if key == "Do a favor for Sam (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in sam_texts[key][player_input]:
                        typewriter(sub_key)
        keys0 = list(sam_texts.keys())[84:89]
        for key in keys0:
            typewriter(key)
    elif romance[1] == 5 and 0 < player_stats[11] * gifts * player_stats[9] < 50:
        keys = list(sam_texts.keys())[90:94]
        for key in keys:
            typewriter(key)
    elif romance[1] == 5 and player_stats[11] * gifts * player_stats[9] >= 50:
        gifts = 0
        keys = list(sam_texts.keys())[95:112]
        for key in keys:
            typewriter(key)
        romance[1] += 1
        typewriter("You've increased your romance score with Sam!")
        typewriter("Your new score is " + str(romance[1]))
        town()
    elif romance[1] == 6 and romance[5] < 6:
        keys = list(sam_texts.keys())[113:117]
        for key in keys:
            typewriter(key)
    elif romance[5] == 6:
        keys = list(sam_texts.keys())[118:125]
        for key in keys:
            typewriter(key)
        town()


def willow():
    global romance, gifts, player_stats
    willow_texts = { "You come across five Goblins standing in the town centre.": { },
                     "One of them spots you, and turns to his female companion.": { },
                     "Goblin: Look, Willow! It's that " + gender[0] + " that let you go free!": { },
                     "Willow looks at you shyly and starts to speak in a soft voice.": { },
                     "Willow: ...Hi, thanks for letting us come here.": { }, "Willow: What's your name?": { },
                     "Give Willow your name (y/n?)": {
                         'n': { "Willow: ...Oh, I guess you're busy.",
                                "Willow walks away with her friends, looking dejected.",
                                town() },
                         'y': { "Willow perks up.", "Willow: Oh, that's such a lovely name! I could say it all day!"
                                                    "Willow: " + name_color() + ", " + name_color() + ", " + name_color() + "! ",
                                "Willow: That's so fun!",
                                "Willow: I like you, " + name_color() + ", let's grab lunch sometime!" } },
                     "Willow: Did you bring lunch?": { }, "Willow: Oh, but I'm hungry!": { },
                     "Willow: Please can you buy some lunch for me?": { },
                     "Buy Willow a gift in the shop to continue.": { },
                     town(): { }, "Willow: You brought lunch! Yay!": { },
                     "Willow: Why don't you come with me to the park and we'll set up a picnic?": { },
                     "You head to the park, Willow's bubbly personality making you laugh the entire way.": { },
                     "At the park, Willow opens up to you about her feelings on the Goblin society...": { },
                     "Willow: Do you know anything about Goblins and how they work?": { }, "Respond: (y/n)?": {
            'y': { "Willow: Oh, you do? Well, then you'll know we don't really educate ourselves.",
                   "Willow: That's why everyone thinks we're stupid and lesser. Most Goblins are just archers.",
                   "Willow: But I wanted to go to school. I wanted to be a cheerleader.",
                   "Willow: You humans are so lucky to have all these options available to you.",
                   "Willow: Why can't I be human?" },
            'n': { } }, "Willow suddenly perks up.": { },
                     "Willow: But don't let me get you down! It's a beautiful day!": { },
                     "Willow: Let's go play!": { },
                     "Willow grabs your hand and pulls you to the playground where you two spend the rest of the day.": { },
                     town(): { }, "Willow: Hey there, " + name_color() + "!": { },
                     "Willow: I enjoyed our lunch date so, so much!": { },
                     "Willow: Would you like to walk with me?": { },
                     "Willow: Oh, but I left my shoes at home! Can you run to the shop and get me a new pair?": { },
                     "Buy Willow a gift or two from the shop to continue!": { }, town(): { },
                     "Willow: You got the shoes! Thank you so much!": { },
                     "Willow grabs your hand and you both skip through the town, laughing and joking about your pasts...": { },
                     "Willow: ...And then this one time, before Dragon showed up...": { },
                     "Sam hid my arrows, and I couldn't find them for days!": { },
                     "Willow: Actually, I wonder what happened to Sam... he and I were in the same battalion together.": { },
                     "Willow: Dragon separated the Orcs and Goblins and I haven't seen him since.": { },
                     "Willow: He was always more like a boyish sister than a 'brother in arms' to me...": { },
                     "You explain to Willow you've met Sam.": { },
                     "Willow: You did!? How is he? Is he living in the town, too?": { },
                     "You explain to Willow that Sam is safe and is living as herself now.": { },
                     "Willow: ..HERself?": { },
                     "Willow: I KNEW IT!": { },
                     "Willow: Well, if he - I mean, if SHE - ever asks about me, tell her I'd like to see her again!": { },
                     "Willow: Wait, if she's... a she... does that mean she is no longer in line to lead the Orcs?": { },
                     "Willow: Well if it isn't the wonderful " + gender[
                         0] + " that I've been telling EVERYONE about!": { },
                     "Willow: I've been talk-talk-talking up a storm about you to all my friends!": { },
                     "Willow: Like, " + gender[1] + "is the sweetest, kindest, gentlest soul I've ever met!": { },
                     "Willow: And like, " + gender[1] + " should buy " + gender[3] + " a medal for best boo!": { },
                     "Willow: Oh, or " + gender[2] + " eyes are the brightest stars in my daydreams' skies!": { },
                     "Willow: ...I should write a poem about you! Can you get me few parchments from the shop?": { },
                     "Buy Willow gifts from the shop to continue!": { }, town(): { },
                     "Willow: You got the parchment! But... I will admit it was kind of a ploy...": { },
                     "Willow: You see, I'm not writing a poem. I'm writing a business plan.": { },
                     "Willow: I want to open a school for Goblins. The first of its kind.": { },
                     "Willow: I know I'll be laughed at by everyone for this, but I want to give the kids a chance.": { },
                     "Willow: Can you forgive me?": { },
                     "Forgive Willow for deceiving you (y/n)?": {
                         'y': { "Willow: I knew it! You're the best, " + name_color() + "!"
                                                                                        "Willow: I hope I still have time for you after I start my school."
                                                                                        "Willow: If I don't, I hope you'll at least visit me at work, sometime." },
                         'n': { "Willow: You're so mean! I see that smirk on your face!",
                                "Willow: I guess I did ask for it though, heh.",
                                "You both crack up at your joke.",
                                "Willow: I hope I still have time for you after I start my school, " + name_color() + ".",
                                "Willow: If I don't, I hope you'll at least visit me at work, sometime." } },
                     "Willow: I've been thinking about Dragon, recently.": { },
                     "Willow: I mean, about why he never let me open my school...": { },
                     "Willow: I thought he was just being mean, but I thought about what he said.": { },
                     "Willow: Can you bring me some things to make into a gift for him? ": { },
                     "I feel bad for being mean. He's the only reason we survived for so long.": { },
                     "Buy some more gifts from the shop to bring to Willow.": { },
                     town(): { }, "Willow: You got the stuff!": { },
                     "Willow: ...But there's not enough. We need more for a Dragon! They're HUGE!": { },
                     "Willow: Please get some more gifts!": { }, town(): { },
                     "Willow: You got the stuff! Thank you!": { },
                     "Willow: Maybe now Dragon will forgive me for being mean to him.": { },
                     "Willow: He always claimed that the front-line army was short on men.": { },
                     "Willow: And that the archers needed to fill the gap.": { },
                     "Willow: And honestly, it was true, even if I didn't believe it at the time.": { },
                     "Willow: That nasty Mayor was always hunting us down. I'm surprised I lived to see peace!": { },
                     "Willow: I'll go to Dragon's cave and deliver this to him at once!": { },
                     "Willow: Aren't you the cutest Dragon's Mate?": { },
                     "Willow: Yep, news spreads fast here! You and Dragon must be so happy!": { },
                     "Willow: I'm not even mad, because Sam and I are getting married! EEEEEE!": { },
                     "Willow: Don't worry, I'll still make time for you!": { },
                     "Willow: We're still together, but you know how the marriage laws work...": { },
                     "You have a laugh together as the two of you catch up.": { }, town(): { }

                     }
    while romance[0] < 1:
        keys = list(willow_texts.keys())[:7]
        for key in keys:
            typewriter(key)
            if key == "Give Willow your name (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in willow_texts[key][player_input]:
                        typewriter(sub_key)
                        romance[0] += 1
                        "Your romance score with Willow has increased to " + str(romance[0])
                        town()
    if romance[0] == 1 and player_stats[11] * gifts * player_stats[9] == 0:
        keys = list(willow_texts.keys())[8:11]
        for key in keys:
            typewriter(key)
    while romance[0] == 1 and player_stats[11] * gifts * player_stats[9] >= 10:
        gifts = 0
        keys = list(willow_texts.keys())[12:17]
        for key in keys:
            typewriter(key)
            if key == "Respond: (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in sam_texts[key][player_input]:
                        typewriter(sub_key)
                        keys0 = list(willow_texts.keys())[18:22]
                        for key0 in keys0:
                            typewriter(key0)
                            romance[0] += 1
                            "You've increased your romance score with Willow!"
                            "Your new score is " + str(romance[0])
                            town()
    if romance[0] == 2 and player_stats[11] * gifts * player_stats[9] == 0:
        keys = list(willow_texts.keys())[23:28]
        for key in keys:
            typewriter(key)
    if romance[0] == 2 and 0 < player_stats[11] * gifts * player_stats[9] < 20:
        typewriter("Willow: That's only one shoe! I have two feet, silly!")
        town()
    while romance[0] == 2 and player_stats[11] * gifts * player_stats[9] >= 20:
        gifts = 0
        keys = list(willow_texts.keys())[29:42]
        for key in keys:
            typewriter(key)
            if romance[1] >= 3:
                typewriter("You explain to Willow she's happier now, and her brother is doing a good job.")
                typewriter("Willow: Oh, I guess that does make sense. Sam never really liked being in charge.")
            if romance[1] < 3:
                typewriter("You explain you don't know much about Sam, but will ask when you see her.")
                typewriter("Willow: I guess that makes sense. Thank you for telling me, " + name_color() + ".")
            typewriter("You finish your walk and say goodbye.")
            romance[0] += 1
            "You've increased your romance score with Willow!"
            "Your new score is " + str(romance[0])
            town()
    if romance[0] == 3 and gifts * player_stats[11] * player_stats[9] == 0:
        keys = list(willow_texts.keys())[43:50]
        for key in keys:
            typewriter(key)
    elif romance[0] == 3 and 0 < player_stats[11] * gifts * player_stats[9] < 30:
        typewriter("Willow: Nooo! I need more parchments for my MASTERPIECE!")
        town()
    while romance[0] == 3 and gifts * player_stats[11] * player_stats[9] >= 30:
        gifts = 0
        keys = list(willow_texts.keys())[51:56]
        for key in keys:
            typewriter(key)
            if key == "Forgive Willow for deceiving you (y/n)?":
                player_input = input("> ").lower()
                if player_input in ['y', 'n']:
                    for sub_key in sam_texts[key][player_input]:
                        typewriter(sub_key)
                        romance[0] += 1
                        "You've increased your romance score with Willow!"
                        "Your new score is " + str(romance[0])
                        town()
    if romance[0] == 4 and player_stats[11] * gifts * player_stats[9] == 0:
        keys = list(willow_texts.keys())[57:43]
        for key in keys:
            typewriter(key)
    elif romance[0] == 4 and 0 < player_stats[11] * gifts * player_stats[9] < 40:
        keys = list(willow_texts.keys())[44:47]
        for key in keys:
            typewriter(key)
    while romance[0] == 4 and player_stats[11] * gifts * player_stats[9] >= 40:
        gifts = 0
        keys = list(willow_texts.keys())[48:54]
        for key in keys:
            typewriter(key)
        romance[0] += 1
        "You've increased your romance score with Willow!"
        "Your new score is " + str(romance[0])
        town()
    if romance[0] == 5:
        typewriter("Willow: I started my school!")
        typewriter("Willow: I even got a few Harpies to be teachers there!")
        if romance[3] >= 5:
            typewriter("Willow: Oh, and Polly is the favorite among them with her parrot impressions!")
        if romance[2] == 6:
            typewriter("Willow: sam's cooking recipes are also a HUGE hit with the kids!")
            typewriter("Willow: There's... just one thing I wanted to ask...")
        if romance[1] or romance[2] or romance[3] or romance[4] > 1:
            typewriter("Willow: ...I know you've been seeing other people.")
            typewriter("Willow: I wanted to tell you I'm ok with that.")
        else:
            typewriter("Willow: ...I know you've been wanting to see other people.")
            typewriter("Willow: I wanted to tell you I'm ok with that.")
        typewriter("Willow: I also wanted to ask if I can start seeing Sam without going behind your back...")
        typewriter("Willow: Pleeaassee?")
        typewriter("Allow Willow to see Sam?")
        willow_1 = input("> ").lower()
        if willow_1 == "y":
            typewriter("Willow: THANK YOU!! You're the BEST!!!")
            typewriter("Willow kisses you on the cheek and skips away happily.")
            romance[0] += 1
            typewriter("You've increased your romance score with Willow!")
            typewriter("Your new score is " + str(romance[0]))
            town()
        elif willow_1 == "n":
            typewriter("Willow: You're joking again. I'm being serious, though! I really like her!")
            typewriter("Willow: Please reconsider!")
            typewriter("Are you going to break Willow's heart or allow her to be with both you and Sam?")
            willow_2 = input("> ").lower()
            if willow_2 == "y":
                typewriter("Willow: THANK YOU!! You're the BEST!!!")
                typewriter("Willow kisses you on the cheek and skips away happily.")
                romance[0] += 1
                typewriter("You've increased your romance score with Willow!")
                typewriter("Your new score is " + str(romance[0]))
                town()
            elif willow_2 == "n":
                typewriter("Willow: ...Oh. You're serious.")
                typewriter("Willow: Umm... I have to go...")
                typewriter("You broke Willow's heart.")
                typewriter("You can try again by talking to her later.")
                town()

    while romance[0] == 6:
        typewriter("Willow: If it isn't the bestest ever to exist in the world: boo-bear!")
        if romance[5] < 6:
            typewriter("Willow: Honestly, though, I think you should talk to the others!")
            typewriter("Willow: They're awesome, too!")
            town()
        if romance[5] == 6:
            keys1 = list(willow_texts.keys())[55:61]
            for key in keys:
                typewriter(key)


def townwork():
    global player_stats
    clear()
    draw()
    typewriter("Work ethic: " + work_color() + ".")
    typewriter("Gifting: " + gifting_color() + ".")
    typewriter("Speech: " + speech_color() + ".")
    draw()
    typewriter("Would you like to work (y/n)?")
    working = input("> ").lower()
    if working == "y":
        typewriter("Where would you like to work? (PT/FT/FL)")
        worktype = input("> ").upper()
        if worktype == "PT":
            typewriter("You worked Part-Time and earned " + work_color())
            gold += player_stats[12] * player_stats[9]
            townwork()
        elif worktype == "FT":
            typewriter("You worked Full-Time and earned " + 2 * work_color())
            gold += 2 * player_stats[12] * player_stats[9]
            townwork()
        elif worktype == "FL":
            typewriter("You worked Freelance and earned " + 3 * work_color())
            gold += 3 * player_stats[12] * player_stats[9]
            townwork()
    elif working == "n":
        town()


def enemy_convo():
    global enemy, endgame, quest_stats
    clear()
    draw()
    if enemy == "Goblin":
        typewriter("Goblin: I don't want to hurt you. I heard you let Willow go free.")
        typewriter("Respond: (yes/no/who)")
        choice_goblin = input("> ").lower()
        if choice_goblin == "yes":
            typewriter("Goblin: I knew it! Us Goblins don't like the mean, stinky Dragon.")
            typewriter("Goblin: If you convince a few more of us you humans can be nice, we'll join your town!")
            typewriter("Goblin: I'll even help introduce you to Willow, she's single! *wink wink*")
            quest_stats[1] += 1
            if quest_stats[1] == 4:
                quest_stats[12] = True
                player_stats[9] += 1
                typewriter("You completed the quest and gained a player_stats[9]! You are now leve " + level_color())
                typewriter("Return to the mayor with your news of the Goblins joining your side!")
            play()
        elif choice_goblin == "no":
            typewriter("Goblin: Oh... you didn't? Well, you seem like a good " + gender[0] + " anyway...")
            typewriter("Goblin: If you convince a few more of us you humans can be nice, we'll join your town!")
            typewriter("Goblin: I'll even help introduce you to Willow, she's single! *wink wink*")
            quest_stats[1] += 1
            if quest_stats[1] == 4:
                quest_stats[12] = True
                player_stats[9] += 1
                typewriter("You completed the quest and gained a level! You are now level " + level_color())
                typewriter("Return to the mayor with your news of the Goblins joining your side!")
            play()
        elif choice_goblin == "who":
            typewriter("Goblin: Willow! You mean to say you talked to her without asking her name!?")
            typewriter("Goblin: Look, the mean, stinky Dragon isn't liked by anyone here...")
            typewriter("Goblin: If you can convince enough Goblins that you humans aren't all bad, "
                       "we'll join your town!")
            typewriter("Goblin: I'll even help introduce you to Willow, she's single! *wink wink*")
            quest_stats[1] += 1
            if quest_stats[1] == 4:
                quest_stats[12] = True
                player_stats[9] += 1
                typewriter("You completed the quest and gained a level! You are now level " + level_color())
                typewriter("Return to the mayor with your news of the Goblins joining your side!")
            play()
        else:
            typewriter("That's not a valid option!")
            enemy_convo()
    elif enemy == "Orc" and quest_stats[2] == 0:
        typewriter("The female Orc looks you up and down, and in an oddly deep voice, speaks to you.")
        typewriter("Orc: Goblins and Orcs have always been allied. ")
        typewriter("Orc: We bring the front-line soldiers, they bring the archers.")
        typewriter("Orc: However, the Dragon forced our Goblin friends to take up sword and shield")
        typewriter("Orc: He laughs as our friends are sacrificed, seeing them as 'lesser beings.'")
        typewriter("Orc: I will gladly join your side in order to wipe that smug look off his face..")
        typewriter("Orc: Name's Sam. NOT short for Samuel. Short for Samantha.")
        typewriter("Sam: If you find and recruit my brother, our tribe leader, we'll all join your side.")
        quest_stats[2] += 1
        play()
    elif enemy == "Orc" and quest_stats[2] == 1:
        typewriter("The Orc in front of ")
        typewriter("Orc: You're that " + gender[0] + " that Sam wrote to me about...")
        typewriter("Orc: He - she, I mean - made some very good points about the Dragon.")
        typewriter("Orc: You've earned yourself a new ally, but one thing...")
        typewriter("Orc: If you dare hurt Sam, I will BREAK you.")
        typewriter("The Orc Leader pats you on the back and makes his way toward the town.")
        quest_stats[2] += 1
        player_stats[9] += 1
        typewriter("You completed the quest and gained a level! You are now level " + level_color())
        typewriter("Return to the mayor with your news of the Orcs joining your side!")
        play()
    elif enemy == "Slime" and quest_stats[3] == 0:
        typewriter("Slime: Dragon is bad sad!")
        typewriter("Slime: He says Slimes must have genders and breed or else we are freaks!")
        typewriter("Slime: Slimes have no gender! And we reproduce alone!")
        typewriter("Slime: We are still romantically interested, but breeding is gross!")
        typewriter("Slime: Please, please let me join your wonderful town!")
        typewriter("Slime: And tell my family how great you are, too!")
        quest_stats[3] += 1
        play()
    elif enemy == "Slime" and quest_stats[3] > 0:
        typewriter("Slime: I've heard that you let Gate join your town.")
        typewriter("Respond: (yes/no/who)")
        choice_slime = input("> ").lower()
        if choice_slime == "yes":
            typewriter("Slime: I knew it! Gate says they've been so so happy since coming to the town!")
            typewriter("Slime: They also said they wanted to talk a little more after you beat the bad sad Dragon.")
            typewriter("Slime: I thinks they like you! I like you too, but not in that way...")
            typewriter("Slime: If you can convince a few more Slimes to join, everyone will come!")
            quest_stats[3] += 1
            if quest_stats[3] == 4:
                player_stats[9] += 1
                typewriter("You completed the quest and gained a level! You are now level " + level_color())
                typewriter("Return to the Mayor with your news of the Slimes joining your side!")
            play()
        if choice_slime == "no":
            typewriter("Slime: Oh, you're silly! It's obviously you!")
            typewriter("Slime: No other adventurer has taken the time to talk to us!")
            typewriter("Slime: I thinks Gate likes you! I like you too, but not in that way...")
            typewriter("Slime: If you can convince a few more Slimes to join, everyone will come!")
            quest_stats[3] += 1
            if quest_stats[3] == 4:
                typewriter("Return to the Mayor with your news of the Slimes joining your side!")
            play()
        if choice_slime == "who":
            typewriter("Slime: Gate! You mean to tell me you never asked their name!?")
            typewriter("Slime: Well, Gate sure knows you! They've been talking about you ever since you met!")
            typewriter("Slime: If you can convince a few more Slimes to join, everyone will come!")
            quest_stats[3] += 1
            if quest_stats[3] == 4:
                typewriter("Return to the Mayor with your news of the Slimes joining your side!")
            play()
        else:
            typewriter("That's not a valid option!")
            enemy_convo()
    elif enemy == "Harpy" and quest_stats[4] == 0:
        typewriter("The Harpy seems to be imitating a type of bird...")
        typewriter("Harpy: GAWWWK! Evil Draggy man if evil! I hate him! SQUAWK!")
        typewriter("Harpy: He says I can't be a parrot! He says parrots are idiots! GAWWK!")
        typewriter("Harpy: I'll show him! I'll join your town! SQUAWWK!")
        typewriter("Harpy: If you talk to our Matriarch, she'll bring all the other Harpies to your side!")
        typewriter("Harpy: GAWWK!")
        play()
    elif enemy == "Harpy" and quest_stats[4] == 1:
        typewriter("Harpy: So, you've met Polly. She's an... interesting one, to say the least.")
        typewriter("Harpy: I will admit she's one of my most intelligent lieutenants, even with the... parroting.")
        typewriter("Harpy: If she says you're trustworthy, that's good enough for me.")
        typewriter("Harpy: Do me one favor, though, and meet up with her after you defeat the Dragon.")
        quest_stats[4] += 1
        play()
    elif enemy == "Minotaur":
        typewriter("The oddly feminine Minotaur looks at you as if he'd never seen a human before.")
        typewriter("Minotaur: You've managed to impress me with your extreme pacifism.")
        typewriter("Minotaur: Name's Jake. Yes, I know what it looks like, but it's Jake, got it?")
        typewriter("Minotaur: I'm not interested in fighting a losing battle. Us Minotaurs are survivors.")
        typewriter("Minotaur: If you will allow, we will gladly join your side.")
        typewriter("Minotaur: Oh, and here's a key for the Dragon's lair. You've earned it.")
        typewriter("Minotaur: I will admit that the Dragon is a bit of a jerk, but he's been through a lot.")
        typewriter("Minotaur: Please, show him mercy.")
        quest_stats[9] += 1
        play()
    elif enemy == "Dragon":
        typewriter("Dragon: You... you don't want to fight? You're sure?")
        typewriter("Dragon: I'm not sure what to say. It's been ages since someone wanted to... talk.")
        typewriter("Dragon: I'm the last male of my kind, you see.")
        typewriter("Dragon: So many females, so many mates... yet I can not seem to give them a son...")
        typewriter("Dragon: The blasted Mayor of that town hunted my kind to practical extinction.")
        typewriter("Dragon: Has he finally had a change of heart, I wonder?")
        typewriter("Dragon: We never wanted to hurt people. We just want to survive...")
        typewriter("Dragon: Yes, I treated the others as lowlifes. I regret it every day...")
        typewriter("Dragon: It was the only way I knew to control an army.")
        typewriter("Dragon: I'm not a leader. Or a general. I was never meant to be. I was the runt!")
        typewriter("Dragon: Leave me be, for now. I have much to ponder...")
        typewriter("You leave the cave, knowing you should head back to town.")
        endgame = True
        typewriter("Congratulations! You've finished the game!")
        typewriter("This was the pacifist ending, and therefore you've unlocked the Pacifist Achievements tab!")
        typewriter("You've also unlocked Romances and talents to go with those Romances!")
        typewriter("Press enter to continue.")
        input("> ")
        play()


def battle():
    global player_stats, pot, elix, boss, gold, endgame, fight, achievements_killer, hpmax, hp, at, enemy, pacifist, \
        pacifist_ruined, quest_stats
    totem = 0
    Round = 0
    enemy_list = ["Goblin", "Orc", "Slime", "Harpy", "Minotaur", "Dragon's Mate"]
    # Determine the type and stats of the enemy
    if not boss:
        if quest_stats[0] == 0:
            enemy = "Goblin"
        elif quest_stats[0] == 1 and quest_stats[1] < 4:
            enemy = "Goblin"
        elif quest_stats[1] == 4 and quest_stats[2] < 2:
            enemy = "Orc"
        elif quest_stats[2] == 2 and quest_stats[3] < 4:
            enemy = "Slime"
        elif quest_stats[3] == 4 and quest_stats[4] < 2:
            enemy = "Harpy"
        elif quest_stats[4] == 2 and not endgame:
            enemy = "Minotaur"
        elif endgame and not pacifist:
            enemy = random.choice(enemy_list)
    elif boss and not endgame:
        enemy = "Dragon"

    hpmax = (15 * player_stats[9] if enemy == "Goblin" else 35 * player_stats[9] if enemy == "Orc"
    else 30 * player_stats[9] if enemy == "Slime" else 45 * player_stats[9] if enemy == "Harpy"
    else 50 * player_stats[9] if enemy == "Minotaur" else 250 * player_stats[9] if enemy == "Dragon's Mate"
    else 250 * player_stats[9] if enemy == "Dragon" else 0)

    at = (3 * player_stats[9] if enemy == "Goblin" else 4 * player_stats[9] if enemy == "Orc"
    else 5 * player_stats[9] if enemy == "Slime" else 6 * player_stats[9] if enemy == "Harpy"
    else 7 * player_stats[9] if enemy == "Minotaur" else 10 * player_stats[9] if enemy == "Dragon's Mate"
    else 10 * player_stats[9] if enemy == "Dragon" else 0)

    go = (8 * player_stats[9] if enemy == "Goblin" else 10 * player_stats[9] if enemy == "Orc"
    else 13 * player_stats[9] if enemy == "Slime" else 15 * player_stats[9] if enemy == "Harpy"
    else 20 * player_stats[9] if enemy == "Minotaur" else 100 * player_stats[9] if enemy == "Dragon"
    else 100 * player_stats[9] if enemy == "Dragon's Mate" else 0)

    hp = hpmax

    while fight:
        Round += 1
        while not pacifist:
            # Draw the game screen
            clear()
            draw()
            typewriter("Defeat the " + enemy + "!")
            draw()
            typewriter(f"{enemy}'s HP: {hp} / {hpmax}")
            typewriter(enemy + "'s LEVEL: " + level_color())
            typewriter(name_color() + "'s HP: " + HP_color() + "/" + HPMAX_color())
            typewriter(name_color() + "'s MP: " + MP_color() + "/" + MPMAX_color())
            typewriter("POTIONS: " + str(pot))
            typewriter("ELIXIRS: " + str(elix))
            draw()

            # Display options
            if player_stats[1] == "Shaman":
                typewriter("1 - Skip Turn")
            elif player_stats[1] in ["Warrior", "Warlock", "Mage", "Rogue"]:
                typewriter("1 - ATTACK")
            typewriter("2 - ABILITY")
            if pot > 0:
                typewriter("3 - USE POTION " + str(20 * player_stats[9]) + "HP")
            if elix > 0:
                typewriter("4 - USE ELIXIR " + str(20 * player_stats[9]) + "MP")
            typewriter("5 - ATTEMPT FLEE")
            if quest_stats[0] == 0:
                typewriter("6 - TALK")
            draw()
            choice_battle = input()
            clear()
            if choice_battle == "1":
                if player_stats[1] == "Shaman":
                    typewriter("Turn skipped!")
                elif player_stats[1] in ["Warrior", "Warlock", "Mage", "Rogue"]:
                    hp -= player_stats[7] * player_stats[9]
                    typewriter(name_color() + " dealt " + ATK_color() + " damage to the {enemy}.")
            elif choice_battle == "2":
                if player_stats[1] == "Warrior":
                    if player_stats[6] >= 5:
                        hp -= player_stats[7] * player_stats[9] * 2
                        player_stats[6] -= 5
                        typewriter(name_color() + ' used ' + ability_color() + '!')
                        typewriter(name_color() + " hit twice, dealing " + ATK_color() * 2 + " damage to the {enemy}.")
                    else:
                        typewriter(f"You don't have enough mana! The {enemy} attacked you while you were helpless!")
                elif player_stats[1] == "Rogue":
                    if player_stats[6] >= 5 and Round == 1:
                        hp -= player_stats[7] * player_stats[9] * 3
                        player_stats[6] -= 5
                        typewriter(name_color() + " used " + ability_color())
                        typewriter(name_color() + " hit the " + enemy + " from the shadows, dealing " + ATK_color() * 3
                                   + " damage to it.")
                    elif player_stats[6] >= 5 and Round > 1:
                        typewriter("You can only use that ability on the first round! The " + enemy +
                                   " attacked you while you were helpless!")
                    else:
                        typewriter(f"You don't have enough mana! The {enemy} attacked you while you were helpless!")
                elif player_stats[1] == "Mage":
                    if player_stats[6] >= 9:
                        hp -= player_stats[4] * player_stats[9] * 0.5
                        player_stats[6] -= 9
                        typewriter(name_color() + ' used ' + ability_color() + '!')
                        typewriter(name_color() + " threw a massive fireball, dealing "
                                   + str(player_stats[4] * player_stats[9] * 0.5) + " damage to the " + enemy + ".")
                    else:
                        typewriter(f"You don't have enough mana! The {enemy} attacked you while you were helpless!")
                elif player_stats[1] == "Warlock":
                    if player_stats[6] >= 7:
                        hp -= player_stats[3] * player_stats[9] * 0.1
                        HP += player_stats[3] * player_stats[9] * 0.1
                        player_stats[6] -= 7
                        player_stats[5] = min(player_stats[5], player_stats[3] * player_stats[9])
                        typewriter(name_color() + ' used ' + ability_color() + '!')
                        typewriter(
                            name_color() + f" leeched {player_stats[3] * player_stats[9] * 0.1} health from the {enemy}!")
                    else:
                        typewriter(f"You don't have enough mana! The {enemy} attacked you while you were helpless!")
                elif player_stats[1] == "Shaman":
                    if player_stats[6] >= player_stats[9] * totem:
                        player_stats[6] -= player_stats[9] * totem
                        totem += 1 * player_stats[9]
                        typewriter(name_color() + ' used ' + ability_color() + '!')
                        typewriter(name_color() + " summoned another totem to attack the " + enemy + "!")
                        typewriter(name_color() + "'s totems attacked for " + totem * TATK_color() + "!")
            elif choice_battle == "3":
                heal_mana(20, pot, "potion")
            elif choice_battle == "4":
                heal_mana(20, elix, "elixir")
            elif choice_battle == "5":
                typewriter(name_color() + "Attempted to flee...")
                if random.randint(0, 10) > 3:
                    typewriter("...and succeeded!")
                    fight = False
                else:
                    typewriter("...and failed! The " + enemy + " hit them while their back was turned!")
            elif quest_stats[0] == 0 and choice_battle == "6":
                typewriter(+ enemy + ": I wasn't interested in fighting anyway...")
                typewriter("The Goblin walks away.")
                quest_stats[0] += 1
                player_stats[9] += 1
                typewriter("Congratulations, you've finished your quest! Go back to the Mayor for your"
                           " next assignment!")
                typewriter("You leveled up! You are now level " + level_color())
                quest_stats[12] = True
                pacifist = True
            elif quest_stats[0] > 0 and not pacifist_ruined and choice_battle == "6":
                typewriter(+ enemy + ": You killed my friends! I will NEVER forgive you!")
                typewriter("You can not go the pacifist route at this point!")
            elif quest_stats[0] > 0 and pacifist_ruined and choice_battle == "6":
                typewriter(+ enemy + ": You betrayed us! There's NO turning back for you!")
            if int(player_stats[5]) <= 0:
                typewriter(enemy + " defeated " + name_color())
                typewriter("GAME OVER")
                fight = False
                main_menu()
            else:
                player_stats[5] -= at
                typewriter(enemy + " dealt " + str(at) + " damage to " + name_color() + ".")

            if int(hp) <= 0:
                typewriter(name_color() + " defeated the " + enemy + "!")
                fight = False
                gold += go
                typewriter("You've found " + str(go) + " gold!")
                if endgame:
                    if enemy == "Goblin":
                        achievements_killer['Slayer'][0]['Required'] += 1
                        if achievements_killer['Slayer'][0]['Required'] >= achievements_killer['Slayer'][0]['Goal']:
                            if player_stats[1] != "Shaman":
                                player_stats[7] *= achievements_killer['Slayer'][0]['ATK Increase']
                                achievements_killer['Slayer'][0]['Required'] = achievements_killer['Slayer'][0]['Goal']
                                achievements_killer['Meta'][1]['Required'] += 1
                                if achievements_killer['Meta'][1]['Required'] >= achievements_killer['Meta'][1]['Goal']:
                                    achievements_killer['Meta'][1]['Required'] = achievements_killer['Meta'][1]['Goal']
                            else:
                                player_stats[8] *= achievements_killer['Slayer'][0]['ATK Increase']
                                achievements_killer['Slayer'][0]['Required'] = achievements_killer['Slayer'][0]['Goal']
                                achievements_killer['Meta'][1]['Required'] += 1
                                if achievements_killer['Meta'][1]['Required'] >= achievements_killer['Meta'][1]['Goal']:
                                    achievements_killer['Meta'][1]['Required'] = achievements_killer['Meta'][1]['Goal']
                    elif enemy == "Orc":
                        achievements_killer['Slayer'][1]['Required'] += 1
                        if achievements_killer['Slayer'][1]['Required'] >= achievements_killer['Slayer'][1]['Goal']:
                            if player_stats[1] != "Shaman":
                                player_stats[7] *= achievements_killer['Slayer'][1]['ATK2 Increase']
                                achievements_killer['Slayer'][1]['Required'] = achievements_killer['Slayer'][1]['Goal']
                                achievements_killer['Meta'][1]['Required'] += 1
                                if achievements_killer['Meta'][1]['Required'] >= achievements_killer['Meta'][1]['Goal']:
                                    achievements_killer['Meta'][1]['Required'] = achievements_killer['Meta'][1]['Goal']
                            else:
                                player_stats[8] *= achievements_killer['Slayer'][1]['ATK2 Increase']
                                achievements_killer['Slayer'][1]['Required'] = achievements_killer['Slayer'][1]['Goal']
                                achievements_killer['Meta'][1]['Required'] += 1
                                if achievements_killer['Meta'][1]['Required'] >= achievements_killer['Meta'][1]['Goal']:
                                    achievements_killer['Meta'][1]['Required'] = achievements_killer['Meta'][1]['Goal']
                    elif enemy == "Slime":
                        achievements_killer['Slayer'][2]['Required'] += 1
                        if achievements_killer['Slayer'][2]['Required'] >= achievements_killer['Slayer'][2]['Goal']:
                            if player_stats[1] != "Shaman":
                                player_stats[7] *= achievements_killer['Slayer'][2]['ATK3 Increase']
                                achievements_killer['Slayer'][2]['Required'] = achievements_killer['Slayer'][2]['Goal']
                                achievements_killer['Meta'][1]['Required'] += 1
                                if achievements_killer['Meta'][1]['Required'] >= achievements_killer['Meta'][1]['Goal']:
                                    achievements_killer['Meta'][1]['Required'] = achievements_killer['Meta'][1]['Goal']
                            else:
                                player_stats[8] *= achievements_killer['Slayer'][2]['ATK3 Increase']
                                achievements_killer['Slayer'][2]['Required'] = achievements_killer['Slayer'][2]['Goal']
                                achievements_killer['Meta'][1]['Required'] += 1
                                if achievements_killer['Meta'][1]['Required'] >= achievements_killer['Meta'][1]['Goal']:
                                    achievements_killer['Meta'][1]['Required'] = achievements_killer['Meta'][1]['Goal']
                    elif enemy == "Harpy":
                        achievements_killer['Slayer'][3]['Required'] += 1
                        if achievements_killer['Slayer'][3]['Required'] >= achievements_killer['Slayer'][3]['Goal']:
                            if player_stats[1] != "Shaman":
                                player_stats[7] *= achievements_killer['Slayer'][3]['ATK4 Increase']
                                achievements_killer['Slayer'][3]['Required'] = achievements_killer['Slayer'][3]['Goal']
                                achievements_killer['Meta'][1]['Required'] += 1
                                if achievements_killer['Meta'][1]['Required'] >= achievements_killer['Meta'][1]['Goal']:
                                    achievements_killer['Meta'][1]['Required'] = achievements_killer['Meta'][1]['Goal']
                            else:
                                player_stats[8] *= achievements_killer['Slayer'][3]['ATK4 Increase']
                                achievements_killer['Slayer'][3]['Required'] = achievements_killer['Slayer'][3]['Goal']
                                achievements_killer['Meta'][1]['Required'] += 1
                                if achievements_killer['Meta'][1]['Required'] >= achievements_killer['Meta'][1]['Goal']:
                                    achievements_killer['Meta'][1]['Required'] = achievements_killer['Meta'][1]['Goal']
                    elif enemy == "Minotaur":
                        achievements_killer['Slayer'][4]['Required'] += 1
                        if achievements_killer['Slayer'][4]['Required'] >= achievements_killer['Slayer'][4]['Goal']:
                            if player_stats[1] != "Shaman":
                                player_stats[7] *= achievements_killer['Slayer'][4]['ATK5 Increase']
                                achievements_killer['Slayer'][4]['Required'] = achievements_killer['Slayer'][4]['Goal']
                                achievements_killer['Meta'][1]['Required'] += 1
                                if achievements_killer['Meta'][1]['Required'] >= achievements_killer['Meta'][1]['Goal']:
                                    achievements_killer['Meta'][1]['Required'] = achievements_killer['Meta'][1]['Goal']
                            else:
                                player_stats[8] *= achievements_killer['Slayer'][4]['ATK5 Increase']
                                achievements_killer['Slayer'][4]['Required'] = achievements_killer['Slayer'][4]['Goal']
                                achievements_killer['Meta'][1]['Required'] += 1
                                if achievements_killer['Meta'][1]['Required'] >= achievements_killer['Meta'][1]['Goal']:
                                    achievements_killer['Meta'][1]['Required'] = achievements_killer['Meta'][1]['Goal']
                    elif enemy == "Dragon's Mate":
                        achievements_killer['Slayer'][5]['Required'] += 1
                        if achievements_killer['Slayer'][5]['Required'] >= achievements_killer['Slayer'][5]['Goal']:
                            if player_stats[1] != "Shaman":
                                player_stats[7] *= achievements_killer['Slayer'][5]['ATK6 Increase']
                                achievements_killer['Slayer'][5]['Required'] = achievements_killer['Slayer'][5]['Goal']
                                achievements_killer['Meta'][1]['Required'] += 1
                                if achievements_killer['Meta'][1]['Required'] >= achievements_killer['Meta'][1]['Goal']:
                                    achievements_killer['Meta'][1]['Required'] = achievements_killer['Meta'][1]['Goal']
                            else:
                                player_stats[8] *= achievements_killer['Slayer'][5]['ATK6 Increase']
                                achievements_killer['Slayer'][5]['Required'] = achievements_killer['Slayer'][5]['Goal']
                                achievements_killer['Meta'][1]['Required'] += 1
                                if achievements_killer['Meta'][1]['Required'] >= achievements_killer['Meta'][1]['Goal']:
                                    achievements_killer['Meta'][1]['Required'] = achievements_killer['Meta'][1]['Goal']

            if quest_stats[0] < 1:
                quest_stats[0] += 1
                quest_stats[12] = True
            elif quest_stats[1] < 4:
                iquest_stats[1] += 1
            if quest_stats[1] == 4:
                quest_stats[12] = True
            elif quest_stats[2] < 2:
                quest_stats[2] += 1
            if quest_stats[2] == 2:
                quest_stats[12] = True
            elif quest_stats[3] < 4:
                quest_stats[3] += 1
            if quest_stats[3] == 4:
                quest_stats[12] = True
            elif quest_stats[4] < 2:
                quest_stats[4] += 1
            if quest_stats[4] == 4:
                quest_stats[12] = True
            elif quest_stats[5] == 1:
                if random.randint(0, 100) < 30:
                    quest_stats[12] = True
            elif quest_stats[6]:
                if random.randint(0, 100) < 30:
                    quest_stats[12] = True

            elif boss:
                boss = False
                endgame = True
                typewriter("Congratulations, you've finished the game! Achievements are now unlocked!")
                typewriter("You've also gained a talent for completing your first achievement!")
                typewriter("The achievement tab will show you what achievements you're missing... ")
                typewriter("...as well as the talent the achievements will increase!")
                typewriter("Press Enter to continue!")
                input(">")
                draw()
            if quest_stats[12]:
                player_stats[9] += 1
            gold += 100
            typewriter("You've completed your quest and increased your level to " + level_color() + "!")
            typewriter("You received 100 gold for your troubles!")
            typewriter("Go back to the mayor to continue!")

            if not boss:
                draw()
        while pacifist:
            # Draw the game screen
            clear()
            draw()
            typewriter("Defeat the " + enemy + " or try to talk some sense into them!")
            draw()
            typewriter(f"{enemy}'s HP: {hp} / {hpmax}")
            typewriter(enemy + "'s LEVEL: " + level_color())
            typewriter(name_color() + "'s HP: " + HP_color() + "/" + HPMAX_color())
            typewriter(name_color() + "'s MP: " + MP_color() + "/" + MPMAX_color())
            typewriter("POTIONS: " + str(pot))
            typewriter("ELIXIRS: " + str(elix))
            draw()

            # Display options
            if player_stats[1] == "Shaman":
                typewriter("1 - Skip Turn")
            elif player_stats[1] in ["Warrior", "Warlock", "Mage", "Rogue"]:
                typewriter("1 - ATTACK")
            typewriter("2 - ABILITY")
            if pot > 0:
                typewriter("3 - USE POTION " + str(20 * player_stats[9]) + "HP")
            if elix > 0:
                typewriter("4 - USE ELIXIR " + str(20 * player_stats[9]) + "MP")
            typewriter("5 - ATTEMPT FLEE")
            typewriter("6 - TALK")
            draw()
            choice_battle1 = input()
            if choice_battle1 == "6":
                if quest_stats[1] < 4:
                    if Round + player_stats[10] > 1:
                        typewriter("Goblin: What? You want to talk? Ok, well... I guess that's OK...")
                        fight = False
                        enemy_convo()
                    else:
                        typewriter("Goblin: I no wanna!")
                elif quest_stats[2] < 2:
                    if Round + player_stats[10] > 2:
                        typewriter("Orc: I heard you talked my Goblin friends into joining your town... very well.")
                        fight = False
                        enemy_convo()
                    else:
                        typewriter("Orc: TALK?! SMASH!")
                elif quest_stats[3] > 4:
                    if Round + player_stats[10] > 3:
                        typewriter("Slime: Ok, we can talk, but please don't tell the mean Dragon!")
                        fight = False
                        enemy_convo()
                    else:
                        typewriter("Slime: *Slurp slurp*")
                elif quest_stats[4] < 2:
                    if Round + player_stats[10] > 5:
                        typewriter("Harpy: You wish to talk? Ugh, fine...")
                        enemy_convo()
                    else:
                        typewriter("Harpy: NO!")
                elif quest_stats[5] == 0:
                    if Round + player_stats[10] > 6:
                        typewriter("Minotaur: Hmph, I see. Let us talk.")
                        enemy_convo()
                    else:
                        typewriter("Minotaur: MY LIFE FOR THE DRAGON KING!")
                elif boss:
                    if Round + player_stats[10] > 10:
                        typewriter("Dragon: Wait, what? You actually want to... to... talk?")
                        enemy_convo()
                    else:
                        typewriter("Dragon: I will NEVER join the likes of YOU!")
            elif choice_battle == "3":
                heal_mana(20, pot, "potion")
            elif choice_battle == "4":
                heal_mana(20, elix, "elixir")
            else:
                pacifist = False
                pacifist_ruined = True


def shop(buy):
    global gold, pot, elix, player_stats, quest_stats, gifts
    while buy:
        while not pacifist:
            clear()
            draw()
            typewriter("Welcome to the shop!")
            draw()
            typewriter(f"GOLD: " + gold_color())
            typewriter(f"POTIONS: {pot}")
            typewriter(f"ELIXIRS: {elix}")
            if player_stats[1] == "Shaman":
                typewriter(f"TOTEM ATK: " + TATK_color())
            else:
                typewriter(f"ATK: " + ATK_color())
            typewriter(f"MAXHP: " + HPMAX_color())
            typewriter(f"MAXMP: " + MPMAX_color())
            draw()
            typewriter(f"1 - BUY POTION ({20 * player_stats[9]}HP) - 5 GOLD")
            typewriter(f"2 - BUY ELIXIR ({20 * player_stats[9]}MP) - 5 GOLD")
            if player_stats[1] == "Shaman":
                typewriter(f"3 - UPGRADE WEAPON (+{2 * player_stats[9]}TOTEM ATK) - 10 GOLD")
            else:
                typewriter(f"3 - UPGRADE WEAPON (+{2 * player_stats[9]}ATK) - 10 GOLD")
            typewriter(f"4 - UPGRADE ARMOR (+{2 * player_stats[9]}HP) - 10 GOLD")
            typewriter(f"5 - UPGRADE TRINKETS (+{2 * player_stats[9]}MP) - 10 GOLD")
            if quest_stats[6] == 0:
                typewriter("6 - BUY MATERIAL (INSTANT LEVEL-UP) - 100 GOLD")
                typewriter("7 - LEAVE")
            else:
                typewriter("6 - LEAVE")
            draw()
            choice_shop = input("> ")
            draw()

            if choice_shop == "1":
                if gold >= 5:
                    pot += 1
                    gold -= 5
                    typewriter("You've bought a potion!")
                    if endgame:
                        achievements_killer['Shopping'][1]['Required'] += 1
                        if achievements_killer['Shopping'][1]['Required'] >= achievements_killer['Shopping'][1]['Goal']:
                            player_stats[4] *= achievements_killer['Shopping'][1]['MAXMP2 Increase']
                            achievements_killer['Shopping'][1]['Required'] = achievements_killer['Shopping'][1]['Goal']
                            achievements_killer['Meta'][2]['Required'] += 1
                            if achievements_killer['Meta'][2]['Required'] >= achievements_killer['Meta'][2]['Goal']:
                                achievements_killer['Meta'][2]['Required'] = achievements_killer['Meta'][2]['Goal']
                else:
                    typewriter("Not enough gold!")
            elif choice_shop == "2":
                if gold >= 5:
                    elix += 1
                    gold -= 5
                    typewriter("You've bought an elixir!")
                    if endgame:
                        achievements_killer['Shopping'][0]['Required'] += 1
                        if achievements_killer['Shopping'][0]['Required'] >= achievements_killer['Shopping'][0]['Goal']:
                            player_stats[4] *= achievements_killer['Shopping'][0]['MAXMP1 Increase']
                            achievements_killer['Shopping'][0]['Required'] = achievements_killer['Shopping'][0]['Goal']
                            achievements_killer['Meta'][2]['Required'] += 1
                            if achievements_killer['Meta'][2]['Required'] >= achievements_killer['Meta'][2]['Goal']:
                                achievements_killer['Meta'][2]['Required'] = achievements_killer['Meta'][2]['Goal']
                else:
                    typewriter("Not enough gold!")
            elif choice_shop == "3":
                if gold >= 10:
                    if player_stats[1] == "Shaman":
                        player_stats[8] += 2 * player_stats[9]
                    else:
                        player_stats[7] += 2 * player_stats[9]
                        gold -= 10
                        typewriter("Weapon upgraded!")
                        if endgame:
                            achievements_killer['Shopping'][2]['Required'] += 1
                            if achievements_killer['Shopping'][2]['Required'] >= \
                                    achievements_killer['Shopping'][2]['Goal']:
                                player_stats[4] *= achievements_killer['Shopping'][2]['MAXMP1 Increase']
                                achievements_killer['Shopping'][2]['Required'] = \
                                    achievements_killer['Shopping'][2]['Goal']
                                achievements_killer['Meta'][2]['Required'] += 1
                                if achievements_killer['Meta'][2]['Required'] >= \
                                        achievements_killer['Meta'][2]['Goal']:
                                    achievements_killer['Meta'][2]['Required'] = \
                                        achievements_killer['Meta'][2]['Goal']
                else:
                    typewriter("Not enough gold!")
            elif choice_shop == "4":
                if gold >= 10:
                    player_stats[3] += 2 * player_stats[9]
                    gold -= 10
                    typewriter("Armor upgraded!")
                    if endgame:
                        achievements_killer['Shopping'][3]['Required'] += 1
                        if achievements_killer['Shopping'][3]['Required'] >= achievements_killer['Shopping'][3]['Goal']:
                            player_stats[4] *= achievements_killer['Shopping'][3]['MAXMP1 Increase']
                            achievements_killer['Shopping'][3]['Required'] = achievements_killer['Shopping'][3]['Goal']
                            achievements_killer['Meta'][2]['Required'] += 1
                            if achievements_killer['Meta'][2]['Required'] >= achievements_killer['Meta'][2]['Goal']:
                                achievements_killer['Meta'][2]['Required'] = achievements_killer['Meta'][2]['Goal']
                else:
                    typewriter("Not enough gold!")
            elif choice_shop == "5":
                if gold >= 10:
                    player_stats[4] += 2 * player_stats[9]
                    gold -= 10
                    typewriter("Trinkets upgraded!")
                    if endgame:
                        achievements_killer['Shopping'][4]['Required'] += 1
                        if achievements_killer['Shopping'][4]['Required'] >= achievements_killer['Shopping'][4]['Goal']:
                            player_stats[4] *= achievements_killer['Shopping'][4]['MAXMP1 Increase']
                            achievements_killer['Shopping'][4]['Required'] = achievements_killer['Shopping'][4]['Goal']
                            achievements_killer['Meta'][2]['Required'] += 1
                            if achievements_killer['Meta'][2]['Required'] >= achievements_killer['Meta'][2]['Goal']:
                                achievements_killer['Meta'][2]['Required'] = achievements_killer['Meta'][2]['Goal']
                else:
                    typewriter("Not enough gold!")
            elif choice_shop == "6" and quest_stats[6] == 0:
                if gold >= 100:
                    quest_stats[12] = True
                    gold -= 100
                    typewriter("Material bought!")
                else:
                    typewriter("Not enough gold!")
            elif choice_shop == "6" or choice_shop == "7":
                buy = False
            else:
                typewriter("Invalid input!")

        while pacifist:
            clear()
            draw()
            typewriter(f"GOLD: " + gold_color())
            typewriter(f"SPEECH: " + speech_color())
            typewriter(f"WORK ETHIC: " + work_color())
            typewriter(f"GIFT GIVING: " + gifting_color())
            draw()
            typewriter(f"1 - BUY POTION ({20 * player_stats[9]}HP) - 5 GOLD")
            typewriter("2 - UPGRADE HAT (+" + str(2 * player_stats[9]) + " SPEECH) - 10 GOLD")
            typewriter(f"3 - UPGRADE BOOTS (+{2 * player_stats[9]} WORK ETHIC) - 10 GOLD")
            typewriter(f"4 - UPGRADE GLOVES (+{2 * player_stats[9]} GIFT GIVING) - 10 GOLD")
            draw()
            if quest_gifts == 0 and quest_stats[9] == 1:
                typewriter("5 - BUY  GIFT - 100 GOLD")
                typewriter("6 - LEAVE")
            if endgame:
                typewriter("5 - BUY GIFT - 100 GOLD")
                typewriter("6 - LEAVE")
            else:
                typewriter("6 - LEAVE")
            draw()
            choice_shop1 = input("> ")
            if choice_shop1 == "1":
                if gold >= 5:
                    pot += 1
                    gold -= 5
                    typewriter("You've bought a potion!")
                    shop(buy)
                else:
                    typewriter("Not enough gold!")
                    shop(buy)
            elif choice_shop1 == "2":
                if gold >= 10:
                    player_stats[10] += 2 * player_stats[9]
                    gold -= 10
                    typewriter("You've upgraded your hat and increased your speech by " + speech_color() + "!")
                else:
                    typewriter("Not enough gold!")
                    shop(buy)
            elif choice_shop1 == "3":
                if gold >= 10:
                    player_stats[10] += 2 * player_stats[9]
                    gold -= 10
                    typewriter("You've upgraded your hat and increased your work ethic by " + work_color() + "!")
                    shop(buy)
                else:
                    typewriter("Not enough gold!")
                    shop(buy)
            elif choice_shop1 == "4":
                if gold >= 10:
                    player_stats[10] += 2 * player_stats[9]
                    gold -= 10
                    typewriter("You've upgraded your hat and increased your Gift Giving by " + gifting_color() + "!")
                    shop(buy)
                else:
                    typewriter("Not enough gold!")
                    shop(buy)
            elif choice_shop1 == "5" and quest_gifts == 0 and quest_stats[9] == 1:
                if gold >= 100:
                    quest_gifts += 1
                    typewriter("You've bought a gift for Jake!")
                    shop(buy)
                else:
                    typewriter("Oh, no! Not enough gold?")
                    typewriter("Since you haven't unlocked endgame content, you can't work, either!")
                    typewriter("Guess this one's a freebie, then...")
                    quest_gifts += 1
                    shop(buy)
            elif endgame and choice_shop1 == "5":
                if gold >= 100:
                    gifts += 1
                    shop(buy)
                else:
                    typewriter("You don't have enough gold! Go work some more to buy this!")
            elif choice_shop1 == "6":
                play()
            else:
                typewriter("Invalid option!")
            draw()


def mayor():
    global map, biom, y_len, x_len, player_stats, quest_stats, pot, elix, pacifist, pacifist_ruined
    clear()
    draw()

    typewriter("Mayor: Hello there, " + name_color() + "!")

    quest_texts1 = [("Mayor: I hear you're looking for adventure!",
                     "Mayor: How about you go out and kill an enemy for us? Any will do!", "You now have a quest!"),
                    ("Mayor: You've done well! Here's some gold for your troubles. Now, let's get down to business.",
                     "Mayor: You see, we are besieged by so many creatures. The biggest nuisance being the Goblins.",
                     "Mayor: If you can clear out 4 Goblins, we would be grateful.", "You now have a new quest!"),
                    ("Mayor: Amazing! You surprised me!", "Mayor: Now that the Goblins are gone,"
                                                          " the next issue is Orcs.",
                     "Mayor: Please clear out 2 Orcs for us!"),
                    ("Mayor: You're doing so well! Keep it up!",
                     "Mayor: I was going to send you after Harpies next, but Slimes have started getting out of hand!",
                     "Mayor: Please clear out 4 Slimes for us!", "You now have a new quest!"),
                    ("Mayor: Thank goodness you've defeated those dastardly Slimes!",
                     "Mayor: Now, let's move on to Harpies. They are stealing our grain and must be stopped!",
                     "Mayor: Please defeat 2 Harpies for us!", "You now have a new quest!"),
                    ("Mayor: Now you're experienced with the kind of monsters we are facing.",
                     "Mayor: They're all led by the evil dragon that lurks inside his cave.",
                     "Mayor: Unfortunately, this cave is protected by a magical door.", "Mayor: An enchanted key is "
                                                                                        "necessary to open it.",
                     "Mayor: First, we must mold the key.",
                     "Mayor: Go east until you reach the cave, and use this putty to make a key.",
                     "You now have a new quest!"),
                    ("Mayor: Perfect, you've got the key mold!", "Mayor: Now to get the key material.",
                     "You can buy one from the shop to the southeast, or you can possibly find one on an enemy."),
                    ("Mayor: Perfect! You have the material!", "Mayor: Give my blacksmiths a little while to craft the "
                                                               "key.",
                     "Mayor: In the meantime, I want you to buy the materials to enchant the key.",
                     "Mayor: Bring me 10 elixirs and 10 potions. That should provide enough magical energy.",
                     "You now have a new quest!"),
                    ("Mayor: We're so close to ridding ourselves of that terrible dragon!",
                     "Mayor: The final step is to enchant the key",
                     "Mayor: Luckily, the dragon made a mistake as we got closer.",
                     "Mayor: He sent Minotaurs after us!",
                     "Mayor: Minotaurs are his top lieutenants, but killing them is the way to enchanting the key.",
                     "Mayor: Kill Minotaurs until you've unlocked the magic!", "You now have a new quest!"),
                    ("Mayor: It is time to take on the dragon!",
                     "Mayor: Take the finished key with you, but be careful with the beast!",
                     "Your final quest awaits! Find the Cave and take on the Dragon!", "You now have a new quest!")],
    quest_texts2 = [("Mayor: I heard what you did...", "Mayor: Letting the Goblin go was NOT what I asked of you.",
                     "Mayor: Remember that these... creatures are vile, horrid monsters that MUST be stopped!",
                     "Mayor: Kill four Goblins to prove you're up to the task!", "You now have a new quest!"),
                    ("Mayor: You've done exactly what I asked!",
                     "Mayor: You recruited the Goblins, and now our ranks are bolstered!",
                     "Mayor: Why don't you recruit those barbaric - er, lovely Orcs to our side?",
                     "You now have a new quest!"), ("Mayor: I see you've recruited the Orcs!",
                                                    "Mayor: They will make a fine addition to our growing army against the Dragon!",
                                                    "Mayor: Now, Slimes have been popping up everywhere!",
                                                    "Mayor: With their numbers, we'd be unstoppable!",
                                                    "Mayor: Go recruit some Slimes for our army!",
                                                    "You now have a new quest!"),
                    ("Mayor: The slimes have proven excellent chefs!",
                     "Mayor: As you see, every race has a place in our town.", "Mayor: So, go recruit the harpies now!",
                     "You now have a new quest!"),
                    ("Mayor: The harpies have shown themselves to be better medics than any human I've met!",
                     "Mayor: The last race to recruit is the Minotaurs!",
                     "Mayor: These are the Dragon's top lieutenants and master strategists.",
                     "Mayor: Recruit a single Minotaur and the rest should follow suit!"),
                    ("Mayor: THE MINOTAUR JUST GAVE YOU A KEY!?", "Mayor: Amazing! However, the Dragon is no joke!",
                     "Mayor: Let's gather intelligence on him. Go talk to the Minotaur you met earlier."
                     "I think her name was... Jaq? Jane? I can't remember..."),
                    ("Mayor: Oh, you're back! What did she say?",
                     "Mayor: Oh... she's... a he. Named Jake? Could have sworn he had...",
                     "Mayor: Well, never mind. She, he, it, whatever, they're all freaks - er, people anyway.",
                     "Mayor: The good news is that you now know the Dragon's weakness, yes?",
                     "As you start to explain the situation, the Mayor cuts you off.",
                     "Mayor: I see, so we need to do better than just TALK to the beast. Perhaps a gift will do?",
                     "Mayor: Go get a meat stick from the Shop and THEN see what it says."),
                    ("Mayor: Did you find out anything new?",
                     "The Mayor listens as you describe the conversation, scowling.", "Mayor: That no good... URGH!",
                     "Mayor: I'LL HAVE ITS HEAD FOR THAT!", "You unsheathe your sword in a threatening manner.",
                     "Mayor: Fine! Fine... I know when I'm defeated.", "Mayor: Go, try to 'convince' the Dragon...",
                     "Mayor: But when you don't come back, I'm culling the town's population of FREAKS!")]

    if quest_stats[0] == 0:
        for text in quest_texts1[0][0]:
            typewriter(text)
    elif pacifist_ruined:
        typewriter("Mayor: I heard you decided against peace with those vile monsters.")
        typewriter("Mayor: I believe that is for the best. They're all freaks, anyway.")
    elif quest_stats[1] < 4 and not pacifist:
        for text in quest_texts1[0][1]:
            typewriter(text)
    elif quest_stats[1] < 4 and pacifist:
        for text in quest_texts1[0][1]:
            typewriter(text)
    elif quest_stats[2] < 2 and not pacifist:
        for text in quest_texts1[0][2]:
            typewriter(text)
    elif quest_stats[2] < 2 and pacifist:
        for text in quest_texts2[0][1]:
            typewriter(text)
    elif quest_stats[3] < 4 and not pacifist:
        for text in quest_texts1[0][3]:
            typewriter(text)
    elif quest_stats[3] < 4 and pacifist:
        for text in quest_texts2[0][2]:
            typewriter(text)
    elif quest_stats[4] < 2 and not pacifist:
        for text in quest_texts1[0][4]:
            typewriter(text)
    elif quest_stats[4] < 2 and pacifist:
        for text in quest_texts2[0][3]:
            typewriter(text)
    elif quest_stats[4] == 2 and quest_stats[7] == 0 and not pacifist:
        for text in quest_texts1[0][5]:
            typewriter(text)
    elif quest_stats[4] == 2 and pacifist:
        for text in quest_texts2[0][4]:
            typewriter(text)
    elif quest_stats[9] == 1 and pacifist:
        for text in quest_texts2[0][5]:
            typewriter(text)
    elif quest_stats[10] == 1 and pacifist:
        for text in quest_texts2[0][6]:
            typewriter(text)
    elif quest_stats[11] == 1 and pacifist:
        for text in quest_texts2[0][7]:
            typewriter(text)
    elif quest_stats[7] == 1 and quest_stats[6] == 0 and not pacifist:
        for text in quest_texts1[0][6]:
            typewriter(text)
    elif quest_stats[7] == 1 and quest_stats[6] == 1 and quest_stats[8] == 0 and not pacifist:
        if elix < 10:
            typewriter("You don't have enough elixirs!")
        elif pot < 10:
            typewriter("You don't have enough potions!")
        else:
            for text in quest_texts1[0][7]:
                typewriter(text)
            pot -= 10
            elix -= 10
            quest_stats[12] = True
            quest_stats[8] += 1
    elif quest_stats[8] == 1 and not pacifist:
        for text in quest_texts1[0][8] and not pacifist:
            typewriter(text)
    elif quest_stats[5] == 1:
        for text in quest_texts1[0][9]:
            typewriter(text)


def town():
    global quest_stats, pacifist_ruined, pacifist, romance
    clear()
    draw()
    if quest_stats[9] == 1 and quest_stats[10] == 0:
        typewriter("Visit your friend Jake (y/n)?")
        townquest = input("> ").lower()
        if townquest == "n":
            play()
        elif townquest == "y":
            typewriter("Jake: Heyy, if it isn't my favorite human, " + name_color() + "!")
            typewriter("Jake: What can I do for you?")
            typewriter("You explain to Jake that the Mayor wants to kill the Dragon.")
            typewriter("Jake: ...")
            typewriter("Jake: WHAT!?")
            typewriter("Jake: He can't do this! Dragons are going extinct because of this stupid war!")
            typewriter("Jake: Please, try to reason with him, " + name_color() + "!")
            typewriter("Jake: I beg you! At least try!")
            quest_stats[10] += 1
            play()
        else:
            typewriter("That's not a valid input!")
            town()

    if quest_stats[10] == 1 and quest_stats[11] == 1:
        typewriter("Visit your friend Jake (y/n)?")
        giftquest1 = input("> ")
        if giftquest1 == "n":
            play()
        elif giftquest1 == "y":
            typewriter("Jake: Did you convince the Mayor?")
            typewriter("You tell Jake you brought a gift from the Mayor")
            typewriter("Jake: I DON'T WANT HIS STUPID GIFTS!")
            typewriter("Jake: I'm trying to protect my friend and you're trying to kill him!")
            typewriter("Jake: It's time you chose a side, " + name_color() + ", and I hope you choose right.")
            typewriter("Will you: 1 - Stand up to the Mayor, or 2 - attempt to kill the Dragon?")
            ruin = input("> ")
            if ruin == "1":
                typewriter("You agree to stand up to the Mayor. Jake looks relieved.")
                typewriter("Jake: Thank you, thank you so much!")
                typewriter("It's time to return to the Mayor to confront him.")
                quest_stats[11] += 1
            if ruin == "2":
                pacifist_ruined = True
                pacifist = False
                typewriter("Jake: ...I see.")
                typewriter("Jake: I was wrong about you. We'll be meeting each other on the battlefield.")
                typewriter("Jake: Goodbye, " + name_color() + ".")
                typewriter("After all that effort, you just ruined your chance at peace. Proud of yourself?")
                typewriter("Return to the Mayor to continue on the killer route.")
                play()
    elif endgame and pacifist:
        typewriter("Would you like to 1 - work or 2 - visit?")
        workvisit = input("> ")
        if workvisit == "1":
            townwork()
        elif workvisit == "2":
            typewriter("Who will you visit?")
            typewriter("1 - Willow")
            typewriter("2 - Sam")
            typewriter("3 - Gate")
            typewriter("4 - Polly")
            typewriter("5 - Jake")
            if romance[5] < 6:
                typewriter("6 - Dragon")
            else:
                typewriter("6 - Oswald")
            whovisit = input("> ")
            if whovisit == "1":
                willow()
            elif whovisit == "2":
                sam()
            elif whovisit == "3":
                gate()
            elif whovisit == "4":
                polly()
            elif whovisit == "5":
                jake()
            elif whovisit == "6":
                oswald()

    else:
        typewriter("That's not a valid input!")
        town()


def cave():
    global map, biom, y_len, x_len, quest_stats, fight
    clear()
    draw()
    typewriter("Here lies the door to the lair of the dragon. What will you do?")
    if quest_stats[7] == 1:
        typewriter("1 - MAKE KEY MOLD")
    if quest_stats[5] == 1:
        typewriter("1 - USE FINISHED KEY")
    typewriter("2 - TURN BACK")
    draw()
    choice_cave = input("> ")
    clear()
    if choice_cave == "1":
        if quest_stats[7] == 1:
            typewriter("You walk up to the door and make the mold. Time to return to the Mayor.")
            typewriter("Congratulations! You finished the quest and increased your level to " + level_color() + "!")
            player_stats[9] += 1
            quest_stats[7] += 1
        if quest_stats[5] == 2:
            clear()
            fight = True
            battle()
    elif choice_cave == "2":
        clear()


def new_game():
    global player_stats
    clear()
    with open("blacklist.txt", "r") as f:
        blacklist = f.read().splitlines()
        typewriter("To start, what is your name?")
        name = input("> ")
        while name in blacklist:
            typewriter("That name is not allowed.")
            typewriter("Please enter a different name.")
            name = input("> ")
        if name not in blacklist:
            typewriter("Please enter your gender:")
            gender[0] = input("> ")
            while gender[0] in blacklist:
                typewriter("That is not allowed. Be nice.")
                typewriter("Please enter your REAL gender:")
                gender[0] = input("> ")
            if gender not in blacklist:
                typewriter("What is your first pronoun? (she, they, he, etc)")
                gender[1] = input("> ")
                while gender[1] in blacklist:
                    typewriter("That is not allowed. Be nice.")
                    typewriter("Please enter your REAL pronoun:")
                    gender[1] = input("> ")
                if gender[1] not in blacklist:
                    typewriter("Great! Now enter your second pronoun (her, them, him, etc)")
                    gender[2] = input("> ")
                    while gender[2] in blacklist:
                        typewriter("That is not allowed. Be nice.")
                        typewriter("Please enter your REAL pronoun:")
                        gender[2] = input("> ")
                    if gender[2] not in blacklist:
                        typewriter("Great! Now enter your third pronoun (herself, themself, himself, etc")
                        gender[3] = input("> ")
                        while gender[3] in blacklist:
                            typewriter("That is not allowed. Be nice.")
                            typewriter("Please enter your REAL pronoun:")
                            gender[3] = input("> ")
                        if gender[3] not in blacklist:
                            typewriter("Great! Your name is " + name_color() + ", your gender is " + str(gender[0]) +
                                       ", and your pronouns are " + str(gender[1]) + "/" + str(gender[2]) + "/" + str(
                                gender[3]))
            job_options = [
                ("Warrior", "Berserk", 45, 25, 3, 0, 1, 3, 2),
                ("Rogue", "Sneak Attack", 25, 25, 5, 0, 3, 1, 1),
                ("Mage", "Fireball", 25, 45, 3, 0, 2, 2, 3),
                ("Warlock", "Life Leech", 35, 35, 4, 0, 3, 1, 1),
                ("Shaman", "Summon Totem", 35, 45, 0, 1, 3, 3, 3)]
            typewriter(f"Perfect! Welcome, " + name_color() + "!")
            typewriter("Now to pick a job:")
            for i, (player_stats) in enumerate(job_options):
                typewriter(str(i + 1) + "-" + job_color() + ": " + ability_color() + ","
                                                                                     f" HP: " + HP_color() + ", MP: " + MP_color() + ", ATK: " + ATK_color() + ","
                                                                                                                                                               " Gifting: " + gifting_color())
            typewriter("What will your job be?")
            job_choice = int(input("> ")) - 1
            player_stats[1], player_stats[2], player_stats[3], player_stats[4], player_stats[7], player_stats[8], \
                player_stats[10], player_stats[11], player_stats[12] = job_options[job_choice]
            player_stats[5] = player_stats[3]
            player_stats[6] = player_stats[4]

            typewriter(f"Perfect! Your job is " + job_color() + "! Your ability is " + ability_color() + "!")
            typewriter(f"Your HP is " + HP_color() + " and your MP is " + MP_color() + "!")
            typewriter("Now, let's start your adventure!")
            play()


def h2p():
    clear()
    draw()
    typewriter("How to Play:")
    typewriter("This game is about doing quests to level to 10 so you can defeat the Dragon!")
    typewriter("Each quest completed will increase your level by 1")
    typewriter("Use the number keys to change between menus and move around the map.")
    typewriter("You can press 0 at any time to save and return to the main menu.")
    typewriter("Continue (y/n)?")
    cont1 = input("> ").lower()
    if cont1 == "y":
        draw()
        typewriter("You can choose from 4 jobs. Each job starts with a unique ability.")
        typewriter("Warrior - Berserk: Attacks twice.")
        typewriter("Rogue - Sneak Attack: Deals massive damage based on ATK in the first round of each fight.")
        typewriter("Mage - Fireball: Deals damage based on MP")
        typewriter("Warlock - Life Leech: Restores health based on damage output")
        typewriter("Shaman - Summon Totem: Summons Totems that deal Damage Over Time.")
        typewriter("Continue (y/n)?")
        cont2 = input("> ").lower()
        if cont2 == "y":
            draw()
            typewriter("You will start in a Town. Going east will take you to the mayor's house.")
            typewriter("This is where you can pick up quests.")
            typewriter("You can also visit the shop in the southern part of town to upgrade your gear.")
            typewriter("You need to kill enemies in the wilderness to get the gold for upgrades.")
            typewriter("Going south of the shop or east of the Mayor's house will take you to the bridge.")
            typewriter("This bridge will lead you to the wilderness where you can encounter enemies.")
            typewriter("Continue (y/n)?")
            cont3 = input("> ").lower()
            if cont3 == "y":
                draw()
                typewriter("Once you've finished the main story, you will unlock achievements.")
                typewriter("You will no longer gain levels, however you WILL gain something new: talents!")
                typewriter("The talent you get is based on the achievement type.")
                typewriter("For example: 'slayer' achievements give bonus ATK and 'shop' achievements give bonus MP")
                typewriter("Collect all the achievements and send me a screenshot to be added to the Hall of Fame!")
                typewriter("The Hall of Fame can be found on the GitHub page and in the ReadMe. Now go enjoy yourself!")
                typewriter("Would you like a few tips on completing the game (y/n)?")
                cont4 = input("> ").lower()
                if cont4 == "y":
                    draw()
                    typewriter("Warriors will start slow, but can be helped if you upgrade their weapons.")
                    typewriter("Warlocks' Life Leech damage/healing are based on MAXHP, so upgrade your armor!")
                    typewriter("Mages will literally 1-shot everything, including the Dragon...")
                    typewriter("Rogues will also 1-shot everything at first, but will get harder as you go.")
                    typewriter("Shamans are special in that they rely on stacking totems in order to deal"
                               " damage over time.")
                    typewriter("Press 1 when you're ready to go back to the main menu.")
                    back_to_menu = input("> ")
                    if back_to_menu == "1":
                        main_menu()
                        clear()
                    else:
                        typewriter("You're not very good at following directions,are you?")
                        main_menu()
                        clear()
                elif cont4 == "n":
                    main_menu()
                    clear()
            elif cont3 == "n":
                main_menu()
                clear()
        elif cont2 == "n":
            main_menu()
            clear()
    elif cont1 == "n":
        main_menu()
        clear()


def play():
    global standing, x, y, map, biom, endgame, fight
    while run:
        if not standing and biom[map[y][x]]["e"] and random.randint(0, 10) > 3:
            clear()
            fight = True
            battle()
        else:
            clear()
            display_location()
            display_stats()
            display_options()
            dest = input("> ")
            handle_destination(dest)


def display_location():
    typewriter("LOCATION: " + biom[map[y][x]]["t"])
    draw()


def display_stats():
    typewriter("NAME: " + name_color())
    typewriter("JOB: " + job_color())
    typewriter("LEVEL: " + level_color())
    typewriter("HP: " + HP_color() + "/" + HPMAX_color())
    typewriter("MP: " + MP_color() + "/" + MPMAX_color())
    if player_stats[1] == "Shaman":
        typewriter("TOTEM ATK:" + TATK_color())
    else:
        typewriter("ATK: " + ATK_color())
    typewriter("POTIONS: " + str(pot))
    typewriter("ELIXIRS: " + str(elix))
    typewriter("GOLD: " + gold_color())
    typewriter("COORD: " + x_color() + "," + y_color())
    if endgame:
        if len(tracked) > 0:
            typewriter("Tracked achievements: " + str(tracked))


def display_options():
    draw()
    typewriter("0 - SAVE AND QUIT")
    typewriter("1 - MAP")
    if y > 0:
        typewriter("2 - NORTH")
    if x < x_len:
        typewriter("3 - EAST")
    if y < y_len:
        typewriter("4 - SOUTH")
    if x > 0:
        typewriter("5 - WEST")
    if pot > 0:
        typewriter("6 - USE POTION (" + str(20 * player_stats[9]) + "HP)")
    if elix > 0:
        typewriter("7 - USE ELIXIR (" + str(20 * player_stats[9]) + "MP)")
    if map[y][x] == "shop" or map[y][x] == "mayor" or map[y][x] == "cave":
        typewriter("8 - ENTER")
    if endgame:
        typewriter("9 - ACHIEVEMENTS LIST")
    draw()


def handle_destination(dest):
    global pot, elix, standing, map, x, y, endgame, pacifist

    def move(x_offset, y_offset):
        global standing, map, x, y
        x += x_offset
        y += y_offset
        clear()
        standing = False

    if dest == "0":
        save_game()
        exit()
    elif dest == "1":
        clear()
        map_menu()
    elif dest == "2" and y > 0:
        move(0, -1)
    elif dest == "3" and x < x_len:
        move(1, 0)
    elif dest == "4" and y < y_len:
        move(0, 1)
    elif dest == "5" and x > 0:
        move(-1, 0)
    elif dest == "6":
        heal_mana(20, pot, "potion")
        standing = True
    elif dest == "7":
        heal_mana(20, elix, "elixir")
        standing = True
    elif dest == "8":
        if map[y][x] == "shop":
            clear()
            shop(buy=True)
        if map[y][x] == "mayor":
            clear()
            mayor()
        if map[y][x] == "cave":
            clear()
            cave()
        if map[y][x] == "town" and pacifist:
            town()
    elif dest == "9":
        if endgame:
            print_achievements()
        else:
            typewriter("You do not have achievements unlocked!")

    if endgame:
        # Check if the player has entered a new biome
        if map[y][x] == "plains":
            achievements_killer['Exploration'][0]['Required'] += 1
            if achievements_killer['Exploration'][0]['Required'] >= achievements_killer['Exploration'][0]['Goal']:
                player_stats[3] *= achievements_killer['Exploration'][0]['MAXHP1 Increase']
                achievements_killer['Exploration'][0]['Required'] = achievements_killer['Exploration'][0]['Goal']
                achievements_killer['Meta'][0]['Required'] += 1
                if achievements_killer['Meta'][0]['Required'] >= achievements_killer['Meta'][0]['Goal']:
                    achievements_killer['Meta'][0]['Required'] = achievements_killer['Meta'][0]['Goal']
        elif map[y][x] == "woods":
            achievements_killer['Exploration'][1]['Required'] += 1
            if achievements_killer['Exploration'][1]['Required'] >= achievements_killer['Exploration'][1]['Goal']:
                player_stats[3] *= achievements_killer['Exploration'][1]['MAXHP2 Increase']
                achievements_killer['Exploration'][1]['Required'] = achievements_killer['Exploration'][1]['Goal']
                achievements_killer['Meta'][0]['Required'] += 1
                if achievements_killer['Meta'][0]['Required'] >= achievements_killer['Meta'][0]['Goal']:
                    achievements_killer['Meta'][0]['Required'] = achievements_killer['Meta'][0]['Goal']
        elif map[y][x] == "fields":
            achievements_killer['Exploration'][2]['Required'] += 1
            if achievements_killer['Exploration'][2]['Required'] >= achievements_killer['Exploration'][2]['Goal']:
                player_stats[3] *= achievements_killer['Exploration'][2]['MAXHP3 Increase']
                achievements_killer['Exploration'][2]['Required'] = achievements_killer['Exploration'][2]['Goal']
                achievements_killer['Meta'][0]['Required'] += 1
                if achievements_killer['Meta'][0]['Required'] >= achievements_killer['Meta'][0]['Goal']:
                    achievements_killer['Meta'][0]['Required'] = achievements_killer['Meta'][0]['Goal']
        elif map[y][x] == "mountain":
            achievements_killer['Exploration'][3]['Required'] += 1
            if achievements_killer['Exploration'][3]['Required'] >= achievements_killer['Exploration'][3]['Goal']:
                player_stats[3] *= achievements_killer['Exploration'][3]['MAXHP4 Increase']
                achievements_killer['Exploration'][3]['Required'] = achievements_killer['Exploration'][3]['Goal']
                achievements_killer['Meta'][0]['Required'] += 1
                if achievements_killer['Meta'][0]['Required'] >= achievements_killer['Meta'][0]['Goal']:
                    achievements_killer['Meta'][0]['Required'] = achievements_killer['Meta'][0]['Goal']
        elif map[y][x] == "hills":
            achievements_killer['Exploration'][4]['Required'] += 1
            if achievements_killer['Exploration'][4]['Required'] >= achievements_killer['Exploration'][4]['Goal']:
                player_stats[3] *= achievements_killer['Exploration'][4]['MAXHP5 Increase']
                achievements_killer['Exploration'][4]['Required'] = achievements_killer['Exploration'][4]['Goal']
                achievements_killer['Meta'][0]['Required'] += 1
                if achievements_killer['Meta'][0]['Required'] >= achievements_killer['Meta'][0]['Goal']:
                    achievements_killer['Meta'][0]['Required'] = achievements_killer['Meta'][0]['Goal']
        elif map[y][x] == "bridge":
            achievements_killer['Exploration'][5]['Required'] += 1
            if achievements_killer['Exploration'][5]['Required'] >= achievements_killer['Exploration'][5]['Goal']:
                player_stats[3] *= achievements_killer['Exploration'][5]['MAXHP6 Increase']
                achievements_killer['Exploration'][5]['Required'] = achievements_killer['Exploration'][5]['Goal']
                achievements_killer['Meta'][0]['Required'] += 1
                if achievements_killer['Meta'][0]['Required'] >= achievements_killer['Meta'][0]['Goal']:
                    achievements_killer['Meta'][0]['Required'] = achievements_killer['Meta'][0]['Goal']


def main_menu():
    typewriter("This is V2.3 of my text-based RPG!")
    typewriter("I have now added character genders, a pacifist route, and romance options!")
    typewriter("Would you like to load a saved game (y/n)?")
    load_option = input("> ").lower()
    if load_option == "y":
        load_game()
    if load_option == "n":
        typewriter("OK, we'll start a new game! But first, would you like instructions on how to play (y/n)?")
        instruct = input("> ").lower()
        if instruct == "y":
            h2p()
        if instruct == "n":
            typewriter("OK! Let's get into it!!")
            new_game()


while run:
    clear()
    main_menu()
