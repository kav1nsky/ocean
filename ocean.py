import copy
import sys
import argparse


class Unit:
    @staticmethod
    def change_type(x, y, ocean, unit_type):
        ocean[x][y] = unit_type

    @staticmethod
    def count_neighbours_of_type(unit_type, ocean, x, y):
        count = 0
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not i == j == 0 and 0 <= x + i < len(ocean) and 0 <= y + j < len(ocean[0]):
                    neighbours.append(ocean[x + i][y + j])
        for current_unit in neighbours:
            if current_unit is unit_type:
                count += 1
        return count


class Rock:
    symbol = '#'

    @staticmethod
    def turn(x, y, ocean, ocean_b):
        pass


class Free:
    symbol = '.'

    @staticmethod
    def turn(x, y, ocean, ocean_b):
        # здесь в порядке важности по возрастанию, акулу в конец
        for Animal in [CrayFish, Fish]:
            n = Unit.count_neighbours_of_type(Animal, ocean, x, y)
            if n == 3:
                Unit.change_type(x, y, ocean_b, Animal)


class Fish:
    symbol = 'F'

    @staticmethod
    def turn(x, y, ocean, ocean_b):
        n = Unit.count_neighbours_of_type(Fish, ocean, x, y)
        if n < 2 or n > 3:
            Unit.change_type(x, y, ocean_b, Free)


class CrayFish:
    symbol = 'C'

    @staticmethod
    def turn(x, y, ocean, ocean_b):
        n = Unit.count_neighbours_of_type(CrayFish, ocean, x, y)
        if n < 2 or n > 3:
            Unit.change_type(x, y, ocean_b, Free)


class Ocean:
    UNITS = {
        '#': Rock,
        '.': Free,
        'F': Fish,
        'C': CrayFish,
    }

    def read(self, stream):
        self.turns_count = int(stream.readline())
        self.height, self.width = [int(i) for i in stream.readline().split()]
        self.ocean = []
        for i in range(self.height):
            line = stream.readline()
            self.ocean.append([self.UNITS[i] for i in list(line.replace('\n', ''))])

    def __init__(self):
        self.turns_count = 0
        self.width = 0
        self.height = 0
        self.ocean = []


    # std input if file not mentioned
    def ocean_from_file(self, filepath=None):
        if filepath is None:
            self.read(sys.stdin)
        else:
            with open(filepath) as f:
                self.read(f)

    def print(self, io=sys.stdout):
        for line in self.ocean:
            print("".join(([i.symbol for i in line])), file=io)
        print(2 * len( self.ocean[0]) * '-', file=io)

    def execute(self):
        for t in range(self.turns_count):
            ocean_buffer = copy.deepcopy(self.ocean)
            for i in range(self.height):
                for j in range(self.width):
                    self.ocean[i][j].turn(i, j, self.ocean, ocean_buffer)
            self.ocean = ocean_buffer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-file", help='Ocean filepath, else reading from console', default=None)
    parser.add_argument("--out-file", help='Output filepath, else writing to console', default=None)

    args = parser.parse_args()
    my_ocean = Ocean()
    my_ocean.ocean_from_file(filepath=args.in_file)

    try:
        with open(args.out_file, 'w') as f:
            my_ocean.print(f)
            my_ocean.execute()
            my_ocean.print(f)
    except Exception:
        my_ocean.print()
        my_ocean.execute()
        my_ocean.print()

if __name__ == '__main__':
    main()
