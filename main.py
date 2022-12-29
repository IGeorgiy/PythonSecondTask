class Field:
    def __init__(self, objects_collection):
        self.__one_cell_ships = 0
        self.__two_cell_ships = 0
        self.__three_cell_ships = 0
        self.__field = objects_collection
        self.__ships = []
    def print(self):
            print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
            for index, value in enumerate(self.__field):
                print(f"{index + 1} | {value[0]} | {value[1]} | {value[2]} | {value[3]} | {value[4]} | {value[5]} |")

    def __do_limit(self, ship):
        if ship.length == 3:
            if self.__three_cell_ships >= 1:
                raise ValueError("Превышение лимита кораблей (размером 3 ячейки)!")
            self.__three_cell_ships += 1
        elif ship.length == 2:
            if self.__two_cell_ships >= 2:
                raise ValueError("Превышение лимита кораблей (размером 2 ячейки)!")
            self.__two_cell_ships += 1
        else:
            if self.__one_cell_ships >= 4:
                raise ValueError("Превышение лимита кораблей (размером 1 ячейка)!")
            self.__one_cell_ships += 1
    
    def add_ship(self, ship):
        self.__do_limit(ship)
        self.__ships.append(ship)
        counter = 0
        for ship_part in ship.parts:
            if ship.is_vertical:
                self.__field[ship.position_y - 1 + counter][ship.position_x - 1] = ship_part
                counter += 1
            else:
                self.__field[ship.position_y - 1][ship.position_x - 1 + counter] = ship_part
                counter += 1

class FieldObject:
    def __init__(self):
        self.representation = ''
    def __str__(self):
        return self.representation

class EmptySpace(FieldObject):
    def __init__(self):
        self.representation = 'O'

class ShipPart(FieldObject):
    def __init__(self, ship):
        self.__ship = ship
        self.representation = "\u25A1"
        self.is_destroyed = False

    def destroy(self):
        self.is_destroyed = True
        self.representation = "X"

class Ship :
    def __init__(self, position_x, position_y, length, is_vertical=False):
        self.__position_check(position_x, position_y)
        self.__length_check(length)
        self.position_x = position_x
        self.position_y = position_y
        self.length = length
        self.is_vertical = is_vertical
        self.parts = []
        for i in range(length):
            self.parts.append(ShipPart(self))

    @staticmethod
    def __position_check(pos_x, pos_y):
        if pos_x < 1 or pos_x > 6:
            raise ValueError("Не верное значение по координатам X (значение должно быть от 1 до 6!")
        if pos_y < 1 or pos_y > 6:
            raise ValueError("Не верное значение по координатам Y (значение должно быть от 1 до 6!")

    @staticmethod
    def __length_check(length):
        if length < 1 or length > 3:
            raise ValueError("Длинна корабля задана неверно (значение должно быть от 1 до 3!")

class MissleShell(FieldObject):
    def __init__(self):
        self.representation = "T"
