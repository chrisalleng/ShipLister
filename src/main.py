import argparse
import csv
from Costs import Costs
from operator import itemgetter


def create_ship_build(split_string):
    faction = split_string[4]
    split_string = split_string[9:]
    split_string.insert(0, faction)
    split_string = filter(None, split_string)
    cards = [card.replace('[,]', '') for card in split_string]
    return cards


def get_ship_cost(ship):
    total = 0
    for card in ship:
        total += costs[card]
    return total


def fix_advanced_cost(ship):
    adjust = 0
    if 'TIE Advanced' in ship:
        if 'Enhanced Scopes' in ship:
            adjust = -1
        elif 'Fire-Control System' in ship:
            adjust= -2
        elif 'Accuracy Corrector' in ship:
            adjust = -3
        elif 'Advanced Sensors' in ship:
            adjust = -3
        elif 'Reinforced Deflectors' in ship:
            adjust = -3
        elif 'Sensor Jammer' in ship:
            adjust = -4
        elif 'Advanced Targeting Computer' in ship:
            adjust = -4
    return adjust



def fix_crew_cost(ship):
    adjust_cost = 0
    upgrades = ship[3:]
    if 'Chewbecca' in upgrades:
        adjust_cost -= 38
    if 'Luke Skywalker' in upgrades:
        adjust_cost -= 21
    if 'Darth Vader' in upgrades:
        adjust_cost -= 26
    if 'Han Solo' in upgrades:
        adjust_cost -= 44
    if 'Jan Ors' in upgrades:
        adjust_cost -= 23
    if 'Kyle Katarn' in upgrades:
        adjust_cost -= 18
    if 'Lando Calrissian' in upgrades:
        adjust_cost -= 41
    if 'Dash Rendar' in upgrades:
        adjust_cost -= 34
    if 'Leebo' in upgrades:
        adjust_cost -= 32
    return adjust_cost


def append_unique(self, ship):
    if ship not in self:
        self.append(ship)
    return self


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="path to ListJuggler CSV")
    args = parser.parse_args()
    print(args.file)
    rebel_ships = []
    empire_ships = []
    scum_ships = []
    with open(args.file, newline='\n') as csvfile:
        lists = csv.reader(csvfile, delimiter=',')
        for row in lists:
            if (row[7] != "None") & (row[7] != "elim_standing"):
                ship = create_ship_build(row)

                cost = get_ship_cost(ship[2:])
                cost += fix_advanced_cost(ship)
                cost += fix_crew_cost(ship)

                ship.insert(0, cost)
                if ship[0] != 0:
                    if ship[1] == 'Rebel Alliance':
                        rebel_ships = append_unique(rebel_ships, ship)
                    elif ship[1] == 'Galactic Empire':
                        empire_ships = append_unique(empire_ships, ship)
                    else:
                        scum_ships = append_unique(scum_ships, ship)

        sorted_rebel_ships = sorted(rebel_ships, key=itemgetter(0))
        sorted_empire_ships = sorted(empire_ships, key=itemgetter(0))
        sorted_scum_ships = sorted(scum_ships, key=itemgetter(0))

        for ship in sorted_rebel_ships:
            print(ship)
        for ship in sorted_empire_ships:
            print(ship)
        for ship in sorted_scum_ships:
            print(ship)

costs = Costs().card_list
main()
