import time
import math

#hi

class Character:
    def __init__(self, name, atk, hp, atkMulti, skillMulti, skillCD, skillRange, skillDur, type, element):
        self.name = name
        self.atk = atk
        self.hp = hp
        self.maxHP = hp
        self.atkMulti = atkMulti
        self.skillMulti = skillMulti
        self.skillCD = skillCD
        self.cdCounter = skillCD
        self.skillCounter = 0
        self.skillRange = skillRange
        self.skillDur = skillDur
        self.res = 0
        self.type = type
        self.element = element
        self.skillTarget = None

    def checkHP(self):
        if self.hp < 0:
            self.hp = 0
        if self.hp > self.maxHP:
            self.hp = self.maxHP

    def takeDMG(self, incomingDMG):
        dmg = incomingDMG * (1 - self.res)
        self.hp -= dmg
        print(self.name + ' takes ' + str(math.ceil(dmg)) + ' DMG!')
        self.checkHP()
        if self.hp <= 0:
            print(self.name + ' has fallen!')
        time.sleep(0.5)


class Enemy:
    def __init__(self, name, atk, hp, res, element):
        self.name = name
        self.atk = atk
        self.hp = hp
        self.maxHP = hp
        self.res = res
        self.element = element
        self.isHealer = False

    def checkHP(self):
        if self.hp < 0:
            self.hp = 0
        if self.hp > self.maxHP:
            self.hp = self.maxHP

    def takeDMG(self, incomingDMG, dmgElement):
        if self.hp > 0:
            if dmgElement == self.element:
                print(self.name + ' is immune to ' + dmgElement + '!')
            else:
                dmg = incomingDMG * (1 - self.res)
                print(self.name + ' takes ' + str(math.ceil(dmg)) + ' DMG', end='')
                self.hp -= dmg
                self.checkHP()
                if self.hp <= 0:
                    print(' and dies', end='')
                print('!')
            time.sleep(0.5)


class Slime(Enemy):
    def __init__(self, element):
        self.atk = 5
        self.hp = 100
        self.res = 0.1
        self.element = element
        self.name = element + ' Slime'
        self.maxHP = 100
        self.isHealer = False


class EnemyHealer(Enemy):
    def __init__(self, name, atk, hp, res, healMulti, element):
        super().__init__(name, atk, hp, res, element)
        self.isHealer = True
        self.healMulti = healMulti

    def heal(self, enemies):
        lowestHP = 999999
        healTarget = None
        for e in enemies:
            if e.hp < lowestHP:
                healTarget = e
                lowestHP = healTarget.hp
        print(self.name + ' heals ' + healTarget.name + ' for ' + str(math.ceil(self.atk * self.healMulti)) + ' HP!')
        healTarget.hp += self.atk * self.healMulti
        healTarget.checkHP()
        time.sleep(0.5)


def display(char):  # display hp
    print('[', end='')
    for x in range(10):
        if char.hp / char.maxHP > x / 10:
            print('x', end='')
        else:
            print('-', end='')
    print('] ' + char.name + ' ' + str(math.ceil(char.hp)) + '/' + str(char.maxHP))


def resetHP(party, enemies):
    for char in party:
        char.hp = char.maxHP
    for e in enemies:
        e.hp = e.maxHP


def inputTarget(enemies, text):
    num = len(enemies)
    if num == 1:
        target = 1
    else:
        while True:
            try:
                target = int(input(text))
                if not 0 < int(target) <= num:
                    print('Invalid input, enter 1-' + str(num))
                else:
                    break
            except ValueError:
                print('Invalid input, enter 1-' + str(num))

    return enemies[int(target) - 1]


def normalAttack(char, enemies):
    target = inputTarget(enemies, 'Normal attack which enemy? ')
    print()
    print(char.name + ' attacks ' + target.name + '!')
    target.takeDMG(char.atk * char.atkMulti, 'Phys')


def skillInput(activeChar, enemies):
    if activeChar.cdCounter == 0:
        activeChar.skillCounter = activeChar.skillDur
        if not activeChar.type == 'healer':
            activeChar.skillTarget = inputTarget(enemies, 'Use skill on which enemy? ')
        else:
            activeChar.skillTarget = None
    else:
        print('Skill on CD for ' + str(activeChar.cdCounter) + ' moves!')
        normalAttack(activeChar, enemies)


def useSkill(char, enemies, party):
    if char.type == 'healer':
        heal = char.atk * char.skillMulti
        for c in party:
            c.hp += heal
            if c.hp > c.maxHP:
                c.hp = c.maxHP
        print(char.name + ' heals the party for ' + str(heal) + ' HP!')
        time.sleep(0.5)
    else:
        time.sleep(0.5)
        for e in enemies:
            if abs(enemies.index(e) - enemies.index(char.skillTarget)) < char.skillRange:
                e.takeDMG(char.atk * char.skillMulti, char.element)
    char.cdCounter = char.skillCD


def battle(party, enemies):
    resetHP(party, enemies)
    activeChar = party[0]
    partyNames = []
    for char in party:
        partyNames.append(char.name)
    enemyNames = []
    for e in enemies:
        enemyNames.append(e.name)

    while True:
        print(', '.join(partyNames) + ' battles ' + ', '.join(enemyNames) + '!')
        print()
        for c in party:
            display(c)
        print()
        for e in enemies:
            display(e)
        print()
        for char in party:
            char.cdCounter = 0

        while True:  # battle moves
            advance = False
            charsAlive = 0
            enemiesAlive = 0
            for char in party:
                if char.hp > 0:
                    charsAlive += 1
            for e in enemies:
                if e.hp > 0:
                    enemiesAlive += 1

            if charsAlive == 0:  # party dead
                input('Your whole party died! Press Enter to revive')
                resetHP(party, enemies)
                activeChar = party[0]
                print()
                break
            elif enemiesAlive == 0:
                advance = True
                break

            print('Moves:')
            print('Switch characters')
            print('Use Skill (', end='')
            if activeChar.cdCounter == 0:
                print('ready!)')
            else:
                print('CD: ' + str(activeChar.cdCounter) + ' turns)')
            print('Attack (press enter)')

            move = input('What is your move? ').lower()

            if move == 'switch':
                for char in party:
                    if char.hp > 0:
                        print(str(party.index(char) + 1) + ': ' + char.name)
                while True:
                    i = 0
                    try:
                        i = int(input('Switch to which character? ')) - 1
                    except ValueError:
                        print('Invalid input, type 1-3')
                        continue
                    if not 0 <= i <= 2:
                        print('Invalid input, type 1-3')
                    elif party[i].hp == 0:
                        print('Character fallen')
                    else:
                        activeChar = party[i]
                        break
                print('Switched to ' + activeChar.name)
                print('Use Skill (', end='')
                if activeChar.cdCounter == 0:
                    print('ready!)')
                else:
                    print('CD: ' + str(activeChar.cdCounter) + ' moves)')
                print('Attack (press enter)')

                move = input('What is your move? ').lower()
                if move == 'skill':
                    skillInput(activeChar, enemies)
                else:
                    normalAttack(activeChar, enemies)

            elif move == 'skill':
                skillInput(activeChar, enemies)

            else:
                normalAttack(activeChar, enemies)

            for c in party:
                if c.skillCounter > 0:
                    print()
                    if not c.type == 'healer':
                        print(c.name + '\'s skill attacks ' + c.skillTarget.name + '!')
                    useSkill(c, enemies, party)
                    if c.skillDur > 1:
                        print('(active for ' + str(c.skillCounter) + ' more turns)')

            for e in enemies:  # enemy attack
                if e.hp > 0:
                    print()
                    print(e.name + ' attacks ' + activeChar.name + '!')
                    activeChar.takeDMG(e.atk)

                    if activeChar.hp == 0:  # switch char if fallen
                        for x in range(3):
                            if party[2-x].hp > 0:
                                activeChar = party[2-x]

                    if e.isHealer:
                        print()
                        e.heal(enemies)

            print()
            for c in party:
                display(c)
            print()
            for e in enemies:
                display(e)
            print()

            for c in party:
                if c.cdCounter != 0:
                    c.cdCounter -= 1
                if c.skillCounter != 0:
                    c.skillCounter -= 1

        if advance:
            input('You won! Press Enter to go to the next floor')
            print()
            time.sleep(1)
            break

# char = Character('Name', atk, hp, AM, SM, CD, SR, SD, type, element)


kokomi = Character('Kokomi', 15, 350, 0.8, 2.5, 6, 3, 3, 'healer', 'Hydro')
diluc = Character('Diluc', 25, 200, 1.3, 2, 3, 2, 1, 'dps', 'Pyro')
fischl = Character('Fischl', 20, 150, 1, 2, 8, 1, 4, 'sub', 'Electro')

# enemy = Enemy('Name', atk, hp, res, element)
hilichurl = Enemy('Hilichurl', 10, 100, 0.1, None)
mitachurl = Enemy('Axe Mitachurl', 15, 300, 0.1, None)


def startAbyss(party, enemyList):
    for enemies in enemyList:
        battle(party, enemies)
    print('There is no next floor L bozo')


while True:
    print('Press Enter to start the battle, type "info" to view character info, or "help" for how to play')
    start = input().lower()

    if start == 'info':
        print('''
Diluc: On field Pyro DPS. Skill does heavy DMG to 3 targets (cd: 3).
Kokomi: Healer. High HP. Skill heals whole party for 3 turns (cd: 6)
Fischl: Off-field Electro Sub DPS. Skill deals sustained single target DMG for 4 turns (cd: 8)
''')
    elif start == 'help':
        print('''How to Play
On each turn, press enter to attack, type "skill" to use your skill, or type "switch" to switch characters.
Type the number corresponding to the enemy you want to attack.''')
    else:
        print()
        startAbyss([diluc, kokomi, fischl],
                   [
                       [Enemy('Hilichurl', 10, 100, 0.1, None)],
                       [Enemy('Hilichurl', 10, 100, 0.1, None), Enemy('Axe Mitachurl', 15, 300, 0.1, None),
                        Enemy('Hilichurl', 10, 100, 0.1, None)],
                       [Slime('Electro'), Slime('Pyro'), Slime('Hydro'), Slime('Cryo'), Slime('Anemo')],
                       [Enemy('Shield Mitachurl', 12, 300, 0.5, None), Enemy('Axe Mitachurl', 15, 300, 0.1, None)],
                       [Enemy('Pyro Specter', 20, 250, 0.1, 'Pyro'),
                        EnemyHealer('Hydro Specter', 20, 250, 0.1, 0.8, 'Hydro')],
                       [Enemy('Ruin Guard', 25, 400, 0.4, None)],
                       [Enemy('Azhdaha', 30, 1000, 0.2, None)],

                   ])
        break
