import os
import random
import sys
import time


run = True
menu = True
play = False
rules = False
key = False
fight = False
standing = True
buy = False
speak = False
boss = False

HP = 50
HPMAX = 50
ATK = 3
pot = 1
elix = 0
gold = 0
x = 0
y = 0

        #  x = 0       x = 1       x = 2       x = 3       x = 4       x = 5         x = 6
map = [["shop",     "mayor",   "bridge",   "plains",   "forest", "mountain",       "cave"],    # y = 0
       ["bridge",   "bridge",   "forest",   "forest",   "forest",    "hills",   "mountain"],    # y = 1
       ["forest",   "fields",   "forest",   "plains",    "hills",   "forest",      "hills"],    # y = 2
       ["plains",   "plains",   "plains",    "fields",   "plains",    "hills",   "mountain"],    # y = 3
       ["plains",   "fields",   "fields",   "plains",    "hills", "mountain",   "mountain"]]    # y = 4

y_len = len(map)-1
x_len = len(map[0])-1

biom = {
    "plains": {
        "t": "PLAINS",
        "e": True},
    "forest": {
        "t": "WOODS",
        "e": True},
    "fields": {
        "t": "FIELDS",
        "e": False},
    "bridge": {
        "t": "BRIDGE",
        "e": False},
    "town": {
        "t": "TOWN CENTRE",
        "e": False},
    "shop": {
        "t": "SHOP",
        "e": False},
    "mayor": {
        "t": "MAYOR",
        "e": False},
    "cave": {
        "t": "CAVE",
        "e": False},
    "mountain": {
        "t": "MOUNTAIN",
        "e": True},
    "hills": {
        "t": "HILLS",
        "e": True,
    }
}

e_list = ["Goblin", "Orc", "Slime"]

mobs = {
    "Goblin": {
        "hp": 15,
        "at": 3,
        "go": 8
    },
    "Orc": {
        "hp": 35,
        "at": 5,
        "go": 18
    },
    "Slime": {
        "hp": 30,
        "at": 2,
        "go": 12
    },
    "Dragon": {
        "hp": 100,
        "at": 8,
        "go": 100
    }
}


def clear():
    os.system("cls")


def typewriter(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
        if char == "! " or char == ". " or char == "? " or char == len(text) - 1:
            typewriter("\n")
        time.sleep(0.01)
        
        
def draw():
    typewriter("xX--------------------xX\n")


def save():
    list = [
        name,
        str(HP),
        str(ATK),
        str(pot),
        str(elix),
        str(gold),
        str(x),
        str(y),
        str(key)
    ]

    file = open("load.txt", "w")

    for item in list:
        file.write(item + "\n")
    file.close()


def heal(amount):
    global HP
    if HP + amount < HPMAX:
        HP += amount
    else:
        HP = HPMAX
    typewriter(name + "'s HP refilled to " + str(HP) + "!")


def battle():
    global fight, play, run, HP, pot, elix, gold, boss

    if not boss:
        enemy = random.choice(e_list)
    else:
        enemy = "Dragon"
    hp = mobs[enemy]["hp"]
    hpmax = hp
    atk = mobs[enemy]["at"]
    g = mobs[enemy]["go"]

    while fight:
        clear()
        draw()
        typewriter("Defeat the " + enemy + "!\n")
        draw()
        typewriter(enemy + "'s HP: " + str(hp) + "/" + str(hpmax) + "\n")
        typewriter(name + "'s HP: " + str(HP) + "/" + str(HPMAX) + "\n")
        typewriter("POTIONS: " + str(pot) + "\n")
        typewriter("ELIXIR: " + str(elix) + "\n")
        draw()
        typewriter("1 - ATTACK\n")
        if pot > 0:
            typewriter("2 - USE POTION (30HP)\n")
        if elix > 0:
            typewriter("3 - USE ELIXIR (50HP)\n")
        draw()

        choice = input("# ")

        if choice == "1":
            hp -= ATK
            typewriter(name + " dealt " + str(ATK) + " damage to the " + enemy + ".\n")
            if hp > 0:
                HP -= atk
                typewriter(enemy + " dealt " + str(atk) + " damage to " + name + ".\n")
            input("> ")

        elif choice == "2":
            if pot > 0:
                pot -= 1
                heal(30)
                HP -= atk
                typewriter(enemy + " dealt " + str(atk) + " damage to " + name + ".\n")
            else:
                typewriter("No potions!\n")
            input("> ")

        elif choice == "3":
            if elix > 0:
                elix -= 1
                heal(50)
                HP -= atk
                typewriter(enemy + " dealt " + str(atk) + " damage to " + name + ".\n")
            else:
                typewriter("No elixirs!\n")
            input("> ")

        if HP <= 0:
            typewriter(enemy + " defeated " + name + "...\n")
            draw()
            fight = False
            play = False
            run = False
            typewriter("GAME OVER\n")
            input("> ")

        if hp <= 0:
            typewriter(name + " defeated the " + enemy + "!\n")
            draw()
            fight = False
            gold += g
            typewriter("You've found " + str(g) + " gold!\n")
            if random.randint(0, 100) < 30:
                pot += 1
                typewriter("You've found a potion!\n")
            if enemy == "Dragon":
                draw()
                typewriter("Congratulations, you've finished the game! ...for now. Come back later for updates!\n")
                boss = False
                play = False
                run = False
            input("> ")
            clear()


def shop():
    global buy, gold, pot, elix, ATK

    while buy:
        clear()
        draw()
        typewriter("Welcome to the shop!\n")
        draw()
        typewriter("GOLD: " + str(gold) + "\n")
        typewriter("POTIONS: " + str(pot) + "\n")
        typewriter("ELIXIRS: " + str(elix) + "\n")
        typewriter("ATK: " + str(ATK) + "\n")
        draw()
        typewriter("1 - BUY POTION (30HP) - 5 GOLD\n")
        typewriter("2 - BUY ELIXIR (MAXHP) - 8 GOLD\n")
        typewriter("3 - UPGRADE WEAPON (+2ATK) - 10 GOLD\n")
        typewriter("4 - LEAVE\n")
        draw()

        choice = input("# ")

        if choice == "1":
            if gold >= 5:
                pot += 1
                gold -= 5
                typewriter("You've bought a potion!\n")
            else:
                typewriter("Not enough gold!\n")
            input("> ")
        elif choice == "2":
            if gold >= 8:
                elix += 1
                gold -= 8
                typewriter("You've bought an elixir!\n")
            else:
                typewriter("Not enough gold!\n")
            input("> ")
        elif choice == "3":
            if gold >= 10:
                ATK += 2
                gold -= 10
                typewriter("You've upgraded your weapon!\n")
            else:
                typewriter("Not enough gold!\n")
            input("> ")
        elif choice == "4":
            buy = False


def mayor():
    global speak, key

    while speak:
        clear()
        draw()
        typewriter("Hello there, " + name + "!\n")
        if ATK < 10:
            typewriter("You're not strong enough to face the dragon yet! Keep practicing and come back later!\n")
            key = False
        else:
            typewriter("You might want to take on the dragon now! Take this key but be careful with the beast!\n")
            key = True

        draw()
        typewriter("1 - LEAVE")
        draw()

        choice = input("# ")

        if choice == "1":
            speak = False


def cave():
    global boss, key, fight

    while boss:
        clear()
        draw()
        typewriter("Here lies the cave of the dragon. What will you do?")
        draw()
        if key:
            typewriter("1 - USE KEY")
        typewriter("2 - TURN BACK")
        draw()

        choice = input("# ")

        if choice == "1":
            if key:
                fight = True
                battle()
        elif choice == "2":
            boss = False



while run:
    while menu:
        typewriter("1: NEW GAME\n")
        typewriter("2: LOAD GAME\n")
        typewriter("3: RULES\n")
        typewriter("4: QUIT GAME\n")

        if rules:
            typewriter("Ok, the rules are simple: Go out, kill enemies, and level up your weapon in the Shop.\n")
            typewriter("Once your weapon reaches level 10, talk to the Mayor to recieve a key to the Dragon's Lair!\n")
            typewriter("Defeat the Dragon and save the town!\n")
            typewriter("Oh, and check back in every now and then for updates to this game!\n")
            typewriter("Now, press any button to return to the main menu.""\n")
            rules = False
            choice = ""
            input("> ")
        else:
            choice = input("# ")

        if choice == "1":
            clear()
            name = input("# What's your name, hero? ")
            menu = False
            play = True
        elif choice == "2":
            try:
                f = open("load.txt", "r")
                load_list = f.readlines()
                if len(load_list) == 9:
                    name = load_list[0][:-1]
                    HP = int(load_list[1][:-1])
                    ATK = int(load_list[2][:-1])
                    pot = int(load_list[3][:-1])
                    elix = int(load_list[4][:-1])
                    gold = int(load_list[5][:-1])
                    x = int(load_list[6][:-1])
                    y = int(load_list[7][:-1])
                    key = bool(load_list[8][:-1])
                    clear()
                    typewriter("Welcome back, " + name + "!")
                    input("> ")
                    menu = False
                    play = True
                else:
                    typewriter("Corrupt save file!")
                    input("> ")
            except OSError:
                typewriter("No loadable save file!")
                input("> ")
        elif choice == "3":
            rules = True
        elif choice == "4":
            quit()

    while play:
        save()  # autosave
        clear()

        if not standing:
            if biom[map[y][x]]["e"]:
                if random.randint(0, 100) < 30:
                    fight = True
                    battle()

        if play:
            draw()
            typewriter("LOCATION: " + biom[map[y][x]]["t"] + "\n")
            draw()
            typewriter("NAME: " + name + "\n")
            typewriter("HP: " + str(HP) + "/" + str(HPMAX) + "\n")
            typewriter("ATK: " + str(ATK) + "\n")
            typewriter("POTIONS: " + str(pot) + "\n")
            typewriter("ELIXIRS: " + str(elix) + "\n")
            typewriter("GOLD: " + str(gold) + "\n")
            typewriter("COORD: " + str(x) + "," + str(y) + "\n")
            draw()

            typewriter("0 - SAVE AND QUIT""\n")
            if y > 0:
                typewriter("1 - NORTH""\n")
            if x < x_len:
                typewriter("2 - EAST""\n")
            if y < y_len:
                typewriter("3 - SOUTH""\n")
            if x > 0:
                typewriter("4 - WEST""\n")
            if pot > 0:
                typewriter("5 - USE POTION (30HP)""\n")
            if elix > 0:
                typewriter("6 - USE ELIXIR (50HP)""\n")
            if map[y][x] == "shop" or map[y][x] == "mayor" or map[y][x] == "cave":
                typewriter("7 - ENTER""\n")
            draw()

            dest = input("# ")

            if dest == "0":
                play = False
                menu = True
                save()
            elif dest == "1":
                if y > 0:
                    y -= 1
                    standing = False
            elif dest == "2":
                if x < x_len:
                    x += 1
                    standing = False
            elif dest == "3":
                if y < y_len:
                    y += 1
                    standing = False
            elif dest == "4":
                if x > 0:
                    x -= 1
                    standing = False
            elif dest == "5":
                if pot > 0:
                    pot -= 1
                    heal(30)
                else:
                    typewriter("No potions!")
                input("> ")
                standing = True
            elif dest == "6":
                if elix > 0:
                    elix -= 1
                    heal(50)
                else:
                    typewriter("No elixirs!")
                input("> ")
                standing = True
            elif dest == "7":
                if map[y][x] == "shop":
                    buy = True
                    shop()
                if map[y][x] == "mayor":
                    speak = True
                    mayor()
                if map[y][x] == "cave":
                    boss = True
                    cave()
            else:
                standing = True
