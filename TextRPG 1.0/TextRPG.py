# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 20:20:28 2023

@author: mdelk
"""

# -*- coding: utf-8 -*-
"""
Wanted to make this game since I was litle. Uses stats and enemies from D&D 5e.

"""
import random
import time
def exploration_tutorial():
    """
    Explains to the user what each the choices given during the exploration phase does
    """
    print ("\nExplore - Look for one of your targets")
    print ("Rest - Heal up to max health but remaining enemies increase by 1")
    print ("Town - Heal to max health and restock potions but remaining enemies increase by 2\n")

def combat_tutorial():
    """
    Explains to the user what each the choices given during the combat phase does
    """
    print ("\nAttack - attack the enemy (damage done will be a random roll from 0-4 plus your attack stat")
    print ("\tNote that enemy attack will be calculated the same way")
    print ("Potion - heals you by 20, will not heal more than max health (You only have 3 so use them wisely)") 
    print ("Escape - Try to run away (35% chance to succeed)\n") 


def player_damage(attack,enemy_health,enemy_name):
    """
    Gets player attack stat, enemy health and the name of the monster
    returns the value of enemy health after damage calculation
    """
    damage = random.randint(0,4) + attack
    enemy_health -= damage
    print("You dealt ",damage, " damage to the "+enemy_name)
    return enemy_health

def enemy_damage(enemy_attack,health,enemy_name):
    """
    Gets enemy attack stat, player health and the name of the monster
    returns the value of player health after damage calculation
    """

    damage = random.randint(0,4) + enemy_attack
    health -= damage
    print (enemy_name+" dealt ",damage, " damage to you")
    return health

def chose_potion(potions,health,max_health):
    """
    Gets number of potions and player health
    Returns new values of potions and player health if condition is true, else informs player that there are no potions remaining.
    """
    if potions > 0:
        health += 20
        if health > max_health:
            health = max_health
        potions -= 1
        print ("Remaining potions: ", potions)
    else:
        print("No potions remaining, enemy attacks while you're looking in your bag")
    return potions,health

def chose_escape():
    """
    Uses a randome value from 0 to 100 to decide if the excape succeeds
    Returns true if value is greater than 50 (50% chance), false if otherwise
    """
    is_successful = False
    escape_roll = random.randint(0,100)
    if escape_roll > 65:
        is_successful = True
    return is_successful()
def Leader():
    #Assigns stats according to current level and stats
    max_health,attack, level = job_level_3()
    health = max_health
    is_alive = True
    potions = 3

    print ("\nYou head to the adventurer's guild to take a job and see a request posted.")
    print ("It is a level 3 quest to hunt The Orc Leader. You gladly take it.")
    print("This is the final stage of the demo!")    
    player_choice = input("Will you take the request to hunt the 'Enemies'? Or do you wish to 'Exit'? Remember your progress is NOT saved!")
        
    #Assigns enemy stats and number of enemies according to selected quest
    if player_choice == "Enemies":
        enemy_max_health = 100
        enemy_attack = 15
        enemies = 1
        enemy_name = "Leader"
    elif player_choice == "Exit":
        print("You say no to an adventure today. Returning to main menu.")
        job_selection()

    #assigns health to enemy for first battle
    enemy_health = enemy_max_health

    #Gives player quick tutorial on what each choice does 
    print ("\nExploration Tutorial:")
    exploration_tutorial()
    print ("\nCombat Tutorial:")
    combat_tutorial()

    print ("\nYou prepare your equipment and enter the forest")
    #Exploration loop continues until the player dies or completes the quest
    while is_alive and enemies > 0:

        #Provides the user with important information at the start of every exploration phase 
        print ("Enemies remaining: ",enemies)
        print ("Current health: ",health)
        print ("Remaing potions: ",potions)

        player_choice = input ("Explore, Rest or Town? (type help if you forgot what these actions do) ")

        if player_choice == "Explore":
            print ("After exploring for a while you encounter the last enemy! The Orc "+enemy_name)
            #Combat loop will continue until either the player or the enemy is slain
            while enemy_health > 0 and health > 0:
                print ("Enemy health: ",enemy_health)
                print ("Your health: ",health)

                player_choice = input("Attack, Potion or Escape? (Type Help if you forgot these actions) ")

                #Calls on the function that corresponds with user input
                if player_choice == "Attack":
                    enemy_health = player_damage(attack, enemy_health, enemy_name)
                elif player_choice == "Potion":
                    potions,health = chose_potion(potions, health,max_health)
                elif player_choice == "Escape":
                    #If escape is successful program exits battle loop, else the loop continues
                    if chose_escape():
                        print("Escaped successfully")
                        break
                    else:
                        print("Failed to escape, the "+enemy_name+" attacks while your back is turned")   
                elif player_choice == "Help":
                    combat_tutorial()
                #If enemy survives after player's turn, enemy will attack player
                if enemy_health > 0:
                    health = enemy_damage(enemy_attack, health,enemy_name)

            #If enemy is defeated player is informed, number of enemies is updated 
            if enemy_health <= 0:
                print("You have defeated the " + enemy_name,"\n")
                enemies -= 1   
            #Resets enemy health value after battle ends
            enemy_health = enemy_max_health

            if health <= 0:
                is_alive = False

        #If player chooses Rest, fully restore health and increase remaining enemies by 1
        elif player_choice == "Rest":
            health = max_health
            enemies += 1
        #If player chooses Town, fully restore health and potions, then increase remaining enemies by 2
        elif player_choice == "Town":
            health = max_health
            potions = 3
            enemies += 2
        elif player_choice == "Help":
            exploration_tutorial()
    #Congratulates player if they are alive at the end, if otherwise displays defeat message
    if is_alive:
        print("Congratulations, you succeeded with your quest! You are now level 4!")
        print("Your health and attack have increased!")
        print('More quests will be available in the next town! Stay tuned!')
        time.sleep(1800)
    else:
        print("Unfortunately you died during your quest, rest in peace.")
        print("You can quit by closing the application at any time. Otherwise, we will be restart.")
        Goblins()
def Orcs():
    #Assigns stats according to current level and stats
    max_health,attack,level = job_level_2()
    health = max_health
    is_alive = True
    potions = 3
    print ("\nYou head to the adventurer's guild to take a job and see a request posted.")
    print ("It is a level 2 quest to hunt Orcs. You should start this next.")
    print("Orcs are much tougher than Goblins, but come in smaller groups.")    
    player_choice = input("Will you take the request to hunt the 'Enemies'? Or do you wish to 'Exit'?")
        
    #Assigns enemy stats and number of enemies according to selected quest
    if player_choice == "Enemies":
        enemy_max_health = 30
        enemy_attack = 6
        enemies = 2
        enemy_name = "Orc"
    elif player_choice == "Exit":
        print("You say no to an adventure today. Returning to main menu.")
        job_selection()

    #assigns health to enemy for first battle
    enemy_health = enemy_max_health

    #Gives player quick tutorial on what each choice does 
    print ("\nExploration Tutorial:")
    exploration_tutorial()
    print ("\nCombat Tutorial:")
    combat_tutorial()

    print ("\nYou prepare your equipment and enter the forest")
    #Exploration loop continues until the player dies or completes the quest
    while is_alive and enemies > 0:

        #Provides the user with important information at the start of every exploration phase 
        print ("Enemies remaining: ",enemies)
        print ("Current health: ",health)
        print ("Remaing potions: ",potions)

        player_choice = input ("Explore, Rest or Town? (type help if you forgot what these actions do) ")

        if player_choice == "Explore":
            print ("After exploring for a while you encounter a lone "+enemy_name)
            #Combat loop will continue until either the player or the enemy is slain
            while enemy_health > 0 and health > 0:
                print ("Enemy health: ",enemy_health)
                print ("Your health: ",health)

                player_choice = input("Attack, Potion or Escape? (Type Help if you forgot these actions) ")

                #Calls on the function that corresponds with user input
                if player_choice == "Attack":
                    enemy_health = player_damage(attack, enemy_health, enemy_name)
                elif player_choice == "Potion":
                    potions,health = chose_potion(potions, health,max_health)
                elif player_choice == "Escape":
                    #If escape is successful program exits battle loop, else the loop continues
                    if chose_escape():
                        print("Escaped successfully")
                        break
                    else:
                        print("Failed to escape, the "+enemy_name+" attacks while your back is turned")   
                elif player_choice == "Help":
                    combat_tutorial()
                #If enemy survives after player's turn, enemy will attack player
                if enemy_health > 0:
                    health = enemy_damage(enemy_attack, health,enemy_name)

            #If enemy is defeated player is informed, number of enemies is updated 
            if enemy_health <= 0:
                print("You have defeated the " + enemy_name,"\n")
                enemies -= 1   
            #Resets enemy health value after battle ends
            enemy_health = enemy_max_health

            if health <= 0:
                is_alive = False

        #If player chooses Rest, fully restore health and increase remainging enemies by 1
        elif player_choice == "Rest":
            health = max_health
            enemies += 1
        #If player chooses Town, fully restore health and potions, then increase remaining enemies by 2
        elif player_choice == "Town":
            health = max_health
            potions = 3
            enemies += 2
        elif player_choice == "Help":
            exploration_tutorial()
    #Congratulates player if they are alive at the end, if otherwise displays defeat message
    if is_alive:
        print("Congratulations, you succeeded with your quest! You are now level 3!")
        print("Your health and attack have increased!")
        print('Your final quest is now available! (This is just a demo version, more will soon be added!)')
        Leader()
    else:
        print("Unfortunately you died during your quest, rest in peace.")
        print("You can quit by closing the application at any time. Otherwise, we will be restart.")
        Goblins()
def Goblins():
    #Assigns stats according to job selected
    max_health,attack, level = job_selection()
    health = max_health
    is_alive = True
    potions = 3

    print ("\nYou head to the adventurer's guild to take a job and see a request posted.")
    print ("It is a level 1 quest to hunt Goblins. You should start this first.")
    print ("Goblins are weak but come in large numbers. They will be a good starting point for your quest.")
    
    player_choice = input("Will you take the request to hunt the 'Enemies'? Or do you wish to 'Exit'?")
        
    #Assigns enemy stats and number of enemies according to selected quest
    if player_choice == "Enemies":
        enemy_max_health = 15
        enemy_attack = 3
        enemies = 4
        enemy_name = "goblin"
    elif player_choice == "Exit":
        print("You say no to an adventure today. Returning to main menu.")
        job_selection()

    #assigns health to enemy for first battle
    enemy_health = enemy_max_health

    #Gives player quick tutorial on what each choice does 
    print ("\nExploration Tutorial:")
    exploration_tutorial()
    print ("\nCombat Tutorial:")
    combat_tutorial()

    print ("\nYou prepare your equipment and enter the forest")
    #Exploration loop continues until the player dies or completes the quest
    while is_alive and enemies > 0:

        #Provides the user with important information at the start of every exploration phase 
        print ("Enemies remaining: ",enemies)
        print ("Current health: ",health)
        print ("Remaing potions: ",potions)

        player_choice = input ("Explore, Rest or Town? (type help if you forgot what these actions do) ")

        if player_choice == "Explore":
            print ("After exploring for a while you encounter a lone "+enemy_name)
            #Combat loop will continue until either the player or the enemy is slain
            while enemy_health > 0 and health > 0:
                print ("Enemy health: ",enemy_health)
                print ("Your health: ",health)

                player_choice = input("Attack, Potion or Escape? (Type Help if you forgot these actions) ")

                #Calls on the function that corresponds with user input
                if player_choice == "Attack":
                    enemy_health = player_damage(attack, enemy_health, enemy_name)
                elif player_choice == "Potion":
                    potions,health = chose_potion(potions, health,max_health)
                elif player_choice == "Escape":
                    #If escape is successful program exits battle loop, else the loop continues
                    if chose_escape():
                        print("Escaped successfully")
                        break
                    else:
                        print("Failed to escape, the "+enemy_name+" attacks while your back is turned")   
                elif player_choice == "Help":
                    combat_tutorial()
                #If enemy survives after player's turn, enemy will attack player
                if enemy_health > 0:
                    health = enemy_damage(enemy_attack, health,enemy_name)

            #If enemy is defeated player is informed, number of enemies is updated 
            if enemy_health <= 0:
                print("You have defeated the " + enemy_name,"\n")
                enemies -= 1   
            #Resets enemy health value after battle ends
            enemy_health = enemy_max_health

            if health <= 0:
                is_alive = False

        #If player chooses Rest, fully restore health and increase remainging enemies by 1
        elif player_choice == "Rest":
            health = max_health
            enemies += 1
        #If player chooses Town, fully restore health and potions, then increase remaining enemies by 2
        elif player_choice == "Town":
            health = max_health
            potions = 3
            enemies += 2
        elif player_choice == "Help":
            exploration_tutorial()
    #Congratulates player if they are alive at the end, if otherwise displays defeat message
    if is_alive:
        print("Congratulations, you succeeded with your quest! You are now level 2!" )
        print("Your health and attack have increased!" )
        print("A new request is available!")
        time.sleep(2)
        Orcs()
    else:
        print("Unfortunately you died during your quest, rest in peace.")
        print("You can quit by closing the application at any time. Otherwise, we will be restart.")
        Goblins()
def job_level_3():
    """
    Takes previous input and levels you up!
    """
    print("You have leveled to 3!")
    print("You can change your class if you'd like, or keep playing your current one!")
    print ("Warrior - High health but low attack")
    print ("Adventurer - Balanced stats")
    print ("Rogue - High attack but low health")
    job3 = input("Choose one of the jobs above:")
    if job3 == "Warrior":
        max_health = 135
        attack = 9
        level = 3
    elif job3 == "Adventurer":
        max_health = 105
        attack = 15
        level = 3
    elif job3 == "Rogue":
        max_health = 75
        attack = 21
        level = 3
    else:
        print("Please choose one of the jobs listed")
        job_level_3()
    return max_health, attack, level
def job_level_2():
    """
    Takes previous input and levels you up!
    """
    print("You have leveled to 2!")
    print("You can change your class if you'd like, or keep playing your current one!")
    print ("Warrior - High health but low attack")
    print ("Adventurer - Balanced stats")
    print ("Rogue - High attack but low health")
    job2 = input("Choose one of the jobs above:")
    if job2 == "Warrior":
        max_health = 90
        attack = 6
        level = 2
    elif job2 == "Adventurer":
        max_health = 70
        attack = 10
        level = 2
    elif job2 == "Rogue":
        max_health = 50
        attack = 14
        level = 2
    else:
        print("Please choose one of the jobs listed")
        job_level_2()
    return max_health, attack, level
def job_selection():
    """
    Takes user input to return stats values according to chosen class
    """
    print ("Warrior - High health but low attack")
    print ("Adventurer - Balanced stats")
    print ("Rogue - High attack but low health")
    job = input("Choose one of the jobs above: ")
    if job == "Warrior":
        max_health = 45
        attack = 3
        level = 1
    elif job == "Adventurer":
        max_health = 35
        attack = 5
        level = 1
    elif job == "Rogue":
        max_health = 25
        attack = 7
        level = 1
    else:
        print("Please choose one of the jobs listed")
        job_selection()
    return max_health, attack, level
Goblins()