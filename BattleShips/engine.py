import random


class Ship():
    def __init__(self, size):
        self.row = random.randrange(0, 9)
        self.col = random.randrange(0, 9)
        self.size = size
        self.orientation = random.choice(["h", "v"])
        self.indexes = self.compute_indexes()



    def compute_indexes(self):
        start_index = self.row * 10 + self.col
        if self.orientation == "h":
            return [start_index + i for i in range(self.size)]
        elif self.orientation == "v":
            return [start_index + i * 10 for i in range(self.size)]


    def test(self):
        for i in self.indexes:
            if i >= 100:
                possible_placement = False
                break

            new_row = i // 10
            new_col = i % 10
            if new_row != self.row and new_col != self.col:
                print("caca")


s = Ship(size=3)
print(s.size)
print(s.row)
print(s.col)
print(s.orientation)
print(s.indexes)
print(s.test())


# Carrier - 5 squares
# Battleship - 4 squares
# Cruiser - 3 squares
# Submarine - 3 squares
# Destroyer - 2 squares


class Player:
    def __init__(self):
        self.ships = []
        self.search = ["0" for i in range(0, 100)]  # 0 for unknown square
        self.place_ships(sizes=[5, 4, 3, 3, 2])
        list_of_lists = [ship.indexes for ship in self.ships]
        self.indexes = [index for sublist in list_of_lists for index in sublist]

    def neighbours_check(self, ot_ship):
        final_list = set()
        for i in ot_ship.indexes:
            final_list.add(i+10)
            final_list.add(i+10-1)
            final_list.add(i+10+1)
            final_list.add(i-10-1)
            final_list.add(i-10+1)
            final_list.add(i+1)
            final_list.add(i-1)

        return list(final_list)


    def place_ships(self, sizes):
        for size in sizes:
            isPlaced = False
            while not isPlaced:
                # Create a new ship
                ship = Ship(size)

                # check if the placement is possible
                possible_placement = True

                for i in ship.indexes:

                    if i >= 100:
                        possible_placement = False
                        break

                    # if the indexes goes out of bounds
                    new_row = i // 10
                    new_col = i % 10
                    if new_row != ship.row and new_col != ship.col:
                        possible_placement = False
                        break
                    
                    

                    # if ships intersect
                    for ot_ship in self.ships:
                        if i in ot_ship.indexes:
                            possible_placement = False
                            break
                    # if ships are next to each other
                    for ot_ship in self.ships:
                        list_of_neighbours = self.neighbours_check(ot_ship)
                        print(ot_ship.indexes)
                        print(i, " ", list_of_neighbours)
                        print()
                        if i in list_of_neighbours:
                            possible_placement = False
                            break

                # possible to place the ship
                if possible_placement:
                    self.ships.append(ship)
                    isPlaced = True

    def show_ships(self):
        indexes = []


player = Player()
print(player.indexes)

for i in range(0, 100):
    if i % 10 == 0 and i > 9:
        print("\n", end="")
    shipHere = False
    for ship in player.ships:
        for index in ship.indexes:
            if i == index:
                print("x", end=" ")
                shipHere = True
                break
    if not shipHere:
        print(".", end=" ")
