import libdw
import random
from libdw import sm


class Char(sm.SM):
    def __init__(self, character, health, mana, health_regen, mana_regen, damage, name):
        self.character = character
        self.health = health
        self.mana = mana
        self.health_regen = health_regen
        self.mana_regen = mana_regen
        self.attack = damage
        self.name = name
    def passive(self):
        if self.character == 'vampire':
            x = self.attack*0.15
            self.health += self.attack*0.15
            if x>0:
                print(self.name+' the vampire heals for '+str(round(x,3)))
            return self
        elif self.character == 'gambler':
            x = random.randint(1,5)
            if x==1:
                self.attack *= 1.5
                if self.attack >0:
                    print(self.name + " Critical HITS!!! for "+str(self.attack))
            return self
        elif self.character == 'tank':
            return self
        else:
            return self
    def damage(self, damage):
        self.health -= damage
        return self
    def attack_roll(self, dice_roll, guess):
        if guess <= dice_roll:
            self.attack = guess*3
        else:
            self.attack = 0 
        return self
    
    def ignite(self):
        self.health -= 5
        return self
    def ignite_cost(self):
        self.mana -= 40
    def extinguish(self):
        #removes ignite
        self.mana -= 40
        return self
    def heal(self):
        #removes debuffs
        self.health += 15
        self.mana -= 60
        return self
    def lightning(self):
        self.attack = 0
        return self
    def lightning_cost(self):
        self.mana -= 60
        return self
    def regen(self):
        self.health += self.health_regen
        self.mana += self.mana_regen
        return self
        
    def get_next_values(self,state,spell):
        if (state == None) and spell == "N":
            next_state = None
        elif (state == None) and spell =="L":
            next_state = 3
            self.lightning()
            print(self.name + " is stunned by lightning and can't attack")
        elif (state == None) and spell == "I":
            next_state = 2
            self.ignite()
            print(self.name + " is set ABLAZE!")
        elif state == None and (spell == "E" or spell == "H"):
            next_state= None
            
        elif state == 2 and (spell == "E" or spell == "H"):
            next_state = None
            print(self.name + " is no longer ablaze!")
        elif state == 2 and spell =="I":
            next_state = 2
            print(self.name + " continues to burn!")
        elif state == 2 and spell =="L":
            next_state = 4
            self.lightning()
            self.ignite()
            print(self.name + " is burned and stunned!")
        elif state == 2 and spell == "N":
            next_state = 2
            self.ignite()
            print(self.name +" burns!")
        elif state == 3 and (spell =="N" or spell =="E"):
            next_state = 3
            self.lightning()
            print(self.name + " is stunned by lightning and can't attack")
        elif state == 3 and spell == "H":
            next_state = None
            print(self.name + " is healed!")
        elif state == 3 and spell == "I":
            next_state = 4
            self.lightning()
            self.ignite()
            print(self.name + " is burned and stunned!")
        elif state == 3 and spell =="L":
            next_state = 3
            print(self.name +' is still stunned!')
        elif state == 4 and spell == "H":
            next_state = None
            print(self.name + " is healed!")
        elif state == 4 and spell == "E":
            next_state =3 
            self.lightning()
            print(self.name + " is stunned by lightning and can't attack but is no longer ablaze")
        elif state == 4 and (spell =="N" or spell == "L" or spell =="I"):
            next_state = 4
            self.ignite()
            self.lightning()
            print(self.name + " is burned and stunned!")
        return next_state, self
            

            
print("Hello, welcome to this two player game!")
player1 = input("What's player 1's name: ")
while player1 == "":
    print("Hi, you didn't Enter your name.")
    player1 = input("What's player 1's name: ")
    
player2 = input("What's player 2's name: ")
while player2 == "":
    print("Hi, you didn't Enter your name.")
    player2 = input("What's player 2's name: ")

Start = input("Do you want to begin [Y/N]?: ").upper()
if not str(Start).isalpha() or (Start != "Y" and Start != "N"):
    Start = "Y"
if Start == "Y":
    
#    rules and game mechanics    
    game_information = """Character Sheet:
All characters have 100 health and 100 mana but different abilities and passives!

vampire:
health regen = 2
mana regen = 10
passive = heals for 15% of damage dealt

tank:
health regen = 3.5
mana regen = 8

gambler:
health regen = 2 
mana regen = 10
passive = has a 20% chance of critical striking for 150% damage

Spell Sheet (Invalid spell entries default to none):

Ignite:
Description: sets opponent ablaze dealing 5 damage per turn
Cost: 40 mana

Lightning:
Description: stuns opponent causing them to be unable to attack (Ignite still goes through)
Cost: 60 mana

Extinguish:
Description: removes Ignite debuff
Cost: 40 mana

Heal:
Description: removes all debuffs
Cost: 60 mana

Rules:
Each turn, players guess a number from 1 to 10, invalid numbers default to 1
then a 10 sided die is rolled.
If the players' guess is less than or equal to the dice roll, damage equal to three times of guess is dealt to the opponent
    """
    print(game_information)



#Choose your character
    character1_chosen = False
    while not character1_chosen:
        character1_choice = input(player1 + " Choose your Character: ")
        if character1_choice.lower() == "vampire":
            character1= Char("vampire",100,100,2,10,0,player1)
            character1.start()
            print(player1+" chooses " + character1.character)
            character1_chosen = True
        elif character1_choice.lower() == "tank":
            character1 = Char("tank",100,100,3.5,8,0,player1)
            character1.start()
            print(player1+" chooses " + character1.character)
            character1_chosen = True
        elif character1_choice.lower()== "gambler":
            character1 = Char("gambler",100,100,2,10,0,player1)
            character1.start()
            print(player1+" chooses " + character1.character)
            character1_chosen = True
        else:
            print("incorrect entry, please try again")
    character2_chosen = False
    while not character2_chosen:
        character2_choice = input(player2 +" Choose your Character: ")
        if character2_choice.lower() == "vampire":
            character2= Char("vampire",100,100,2,10,0,player2)
            character2.start()
            print(player2+" chooses " + character2.character)
            character2_chosen = True
        elif character2_choice.lower() == "tank":
            character2 = Char("tank",100,100,3.5,8,0,player2)
            character2.start()
            print(player2+" chooses " + character2.character)
            character2_chosen = True
        elif character2_choice.lower()== "gambler":
            character2 = Char("gambler",100,100,2,10,0,player2)
            character2.start()
            print(player2+" chooses " + character2.character)
            character2_chosen = True
        else:
            print("incorrect entry, please try again")
### dice roll to see who begins the game
    player1_roll = random.randint(1,10)
    player2_roll = random.randint(1,10)
    print("Both players roll a 10-sided die")
    dice1 = input(player1 + " rolls [Y/N]:").upper()
    if not str(dice1).isalpha() or (dice1 != "Y" and dice1 != "N"):
        dice1 = "N"
    while dice1 == "N":
        dice1 = input(player1+ " please roll [Y/N]:").upper()
        if not str(dice1).isalpha() or (dice1 != "Y" and dice1 != "N"):
            dice1 = "N"
    if dice1 == "Y":
        print(player1 +" rolled a "+str(player1_roll))
    dice2 = input(player2 + " rolls [Y/N]:").upper()
    if not str(dice2).isalpha() or (dice2 != "Y" and dice2 != "N"):
        dice2 = "N"
    while dice2 == "N":
        dice2 = input(player2+ " please roll [Y/N]:").upper()
        if not str(dice2).isalpha() or (dice2 != "Y" and dice2 != "N"):
            dice2 = "N"
    if dice2 == "Y":
        print(player2+" rolled a "+str(player2_roll))
    if player1_roll > player2_roll:
        starter = player1
        print(player1 +" goes first!")
    elif player2_roll > player1_roll:
        starter = player2
        print(player2 +" goes first!")
    else:
        while player1_roll == player2_roll:
            print("it's a draw! please re-roll")
            player1_roll = random.randint(1,10)
            player2_roll = random.randint(1,10)
            print("Both players roll a 10-sided die")
            dice1 = input(player1 + " rolls [Y/N]:").upper()
            if not str(dice1).isalpha() or (dice1 != "Y" and dice1 != "N"):
                dice1 = "N"
            while dice1 == "N":
                dice1 = input(player1+ " please roll [Y/N]:").upper()
                if not str(dice1).isalpha() or (dice1 != "Y" and dice1 != "N"):
                    dice1 = "N"
            if dice1 == "Y":
                print(player1 +" rolled a "+str(player1_roll))
            dice2 = input(player2 + " rolls [Y/N]:").upper()
            if not str(dice2).isalpha() or (dice2 != "Y" and dice2 != "N"):
                dice2 = "N"
            while dice2 == "N":
                dice2 = input(player2 + " please roll [Y/N]:").upper()
                if not str(dice2).isalpha() or (dice2 != "Y" and dice2 != "N"):
                    dice2 = "N"
            if dice2 == "Y":
                print(player2 +" rolled a "+str(player2_roll))
        if player1_roll > player2_roll:
            starter = player1
            print(player1 +" goes first!")
        elif player2_roll > player1_roll:
            starter = player2
    print("In the event of a draw, the person who starts wins!")
        

    
    while character1.health>0 and character2.health>0:
        spell_book= ["N","I","L","E","H"]
        while True:
            try:
                player1_guess = int(input(player1 + ", Guess an integer from 1 to 10 inclusive: "))
                if player1_guess<1 or player1_guess>10:
                    player1_guess = 1
                break
            except ValueError:
                print("Please Enter a number")
                

        while True:
            try:
                player2_guess = int(input(player2 + ", Guess an integer from 1 to 10 inclusive: "))
                if player2_guess<1 or player2_guess>10:
                    player2_guess = 1
                break
            except ValueError:
                print("Please Enter a number")

            
        player1_spell = input(player1 + ", spell choice of heal/ ignite/ extinguish/lightning/ none [H/I/E/L/N]: ").upper()
        

        player2_spell = input(player2 + ", spell choice of heal/ ignite/ extinguish/lightning/ none [H/I/E/L/N]: ").upper()

        dice_roll = random.randint(1,10)
        print("dice rolls: " + str(dice_roll))
        character1.attack_roll(dice_roll, player1_guess)
        character2.attack_roll(dice_roll, player2_guess)
        
        
        if player1_spell == "I" and character1.mana <40:
            player1_spell ="N"
            print(player1 + " does not have enough mana to cast ignite")
        elif player1_spell == "E" and character1.mana <20:
            player1_spell ="N"
            print(player1 + " does not have enough mana to cast extinguish")
        elif player1_spell == "L" and character1.mana <60:
            player1_spell ="N"
            print(player1 + " does not have enough mana to cast lightning")    
        elif player1_spell == "H" and character1.mana <60:
            player1_spell ="N"
            print(player1 + " does not have enough mana to cast heal")
        if player2_spell == "I" and character2.mana <40:
            player2_spell ="N"
            print(player2 + " does not have enough mana to cast ignite")
        elif player2_spell == "E" and character2.mana <20:
            player2_spell ="N"
            print(player2 + " does not have enough mana to cast extinguish")
        elif player2_spell == "L" and character2.mana <60:
            player2_spell ="N"
            print(player2 + " does not have enough mana to cast lightning")    
        elif player2_spell == "H" and character2.mana <60:
            player2_spell ="N"
            print(player2 + " does not have enough mana to cast heal")
        if player1_spell not in spell_book:
            player1_spell = "N"
        if player2_spell not in spell_book:
            player2_spell = "N"
            
        
        if player1_spell == "I" or player1_spell == "L":
            character1.step(player2_spell)
        elif player1_spell == "E" or player1_spell == "H":
            character1.step(player1_spell)
        elif player1_spell == "N" and (player2_spell == "E" or player2_spell =="H" or player2_spell == "N"):
            character1.step(player1_spell)
        elif player1_spell == "N" and (player2_spell == "L" or player2_spell == "I"):
            character1.step(player2_spell)
        
        if player2_spell == "I" or player2_spell == "L":
            character2.step(player1_spell)
        elif player2_spell == "E" or player2_spell == "H":
            character2.step(player2_spell)
        elif player2_spell == "N" and (player1_spell == "E" or player1_spell =="H" or player1_spell == "N"):
            character2.step(player2_spell)
        elif player2_spell == "N" and (player1_spell == "I" or player1_spell =="L"):
            character2.step(player1_spell)    
            
        if player1_spell == "E":
            character1.extinguish()
        elif player1_spell =="H":
            character1.heal()
        elif player1_spell == "L":
            character1.lightning_cost()
        elif player1_spell == "I":
            character1.ignite_cost()
        if player2_spell == "E":
            character2.extinguish()
        elif player2_spell =="H":
            character2.heal()
        elif player2_spell == "L":
            character2.lightning_cost()
        elif player2_spell == "I":
            character2.ignite_cost()
        
        character1.passive()
        character2.passive()
        character1.damage(character2.attack)
        print(player1 +" damaged " + player2 +" for " + str(character1.attack))
        character2.damage(character1.attack)
        print(player2 +" damaged " + player1 +" for " + str(character2.attack))
        character1.regen()
        character2.regen()
        if character1.mana >=100:
            character1.mana = 100
        if character1.health >= 100:
            character1.health = 100
        if character2.mana >=100:
            character2.mana = 100
        if character2.health >= 100:
            character2.health = 100
        print(player1_spell, player2_spell)
        print(round(character1.health,3), character1.mana)
        print(round(character2.health,3), character2.mana)
        
    if character1.health<=0 and character2.health<=0:
        print("it was close but "+ starter + " took the shot first and wins!")
        print("thanks for playing :D")
    elif character1.health >0 and character2.health <=0:
        print(player1 + " WINS!!!!!")
        print("thanks for playing :D")
    elif character1.health <= 0 and character2.health>0:
        print(player2 + " WINS!!!!!")
        print("thanks for playing :D")
        
        
if Start.upper() == "N":
    print("Come back another time!")
