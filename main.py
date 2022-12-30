import random


class Field:
    def __init__(self, ships):
        self.__one_cell_ships = 0
        self.__two_cell_ships = 0
        self.__three_cell_ships = 0
        self.__field = [[EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace()], [EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace()], [EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace()], [EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace()], [EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace()], [EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace(), EmptySpace()]]
        self.__ships = []
        if not (ships is None):
            if len(ships) > 0:
                for ship in ships:
                    self.add_ship(ship)
            else:
                self.fill_random()


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

    def __is_possible_to_place(self, ship):
        counter = 0

        if ship.is_vertical:
            if ship.position_x + ship.length-1 > 6:
                raise CoordinatesError(ship.position_x + ship.length-1, ship.position_y)
        else:
            if ship.position_y + ship.length-1 > 6:
                raise CoordinatesError(ship.position_x, ship.position_y + ship.length-1)

        while counter < ship.length:
            ship_part_position_x = ship.position_x
            ship_part_position_y = ship.position_y
            if ship.is_vertical:
                ship_part_position_y += counter
            else:
                ship_part_position_x += counter
            if not(isinstance(self.__field[ship_part_position_y - 1][ship_part_position_x - 1], EmptySpace)):
                raise CoordinatesError(ship_part_position_x, ship_part_position_y)
            if ship.position_y > 1:
                if not(isinstance(self.__field[ship_part_position_y - 2][ship_part_position_x - 1], EmptySpace)):
                    raise CoordinatesError(ship_part_position_x, ship_part_position_y)
            if ship.position_y < 6:
                if not(isinstance(self.__field[ship_part_position_y][ship_part_position_x - 1], EmptySpace)):
                    raise CoordinatesError(ship_part_position_x, ship_part_position_y)
            if ship.position_x > 1:
                if not(isinstance(self.__field[ship_part_position_y - 1][ship_part_position_x - 2], EmptySpace)):
                    raise CoordinatesError(ship_part_position_x, ship_part_position_y)
            if ship.position_x < 6:
                if not(isinstance(self.__field[ship_part_position_y - 1][ship_part_position_x], EmptySpace)):
                    raise CoordinatesError(ship_part_position_x, ship_part_position_y)
            counter += 1

    def add_ship(self, ship):
        self.__is_possible_to_place(ship)
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

    def do_shot(self, x, y):
        if x < 1 or x > 6:
            raise ValueError("Координаты X выстрела неверные (Правильно: от 1 до 6)!")
        if y < 1 or y > 6:
            raise ValueError("Координаты Y выстрела неверные (Правильно: от 1 до 6)!")
        aim = self.__field[y-1][x-1]
        if isinstance(aim, EmptySpace):
            self.__field[y-1][x-1] = MissleShell()
        elif isinstance(aim, ShipPart):
            if aim.is_destroyed:
                raise MultiplyShotError()
            aim.destroy()
            return True
        elif isinstance(aim, MissleShell):
            raise MultiplyShotError()
        return False

    def set_cell_value(self, index_x, index_y, value):
        self.__field[index_y][index_x] = value

    def fill_random(self):
        self.__add_random_ship(3, bool(random.getrandbits(1)))
        self.__add_random_ship(2, bool(random.getrandbits(1)))
        self.__add_random_ship(2, bool(random.getrandbits(1)))
        self.__add_random_ship(1, bool(random.getrandbits(1)))
        self.__add_random_ship(1, bool(random.getrandbits(1)))
        self.__add_random_ship(1, bool(random.getrandbits(1)))
        self.__add_random_ship(1, bool(random.getrandbits(1)))

    def __add_random_ship(self, length, is_vertical):
        list_x = [1, 2, 3, 4, 5, 6]
        list_y = [1, 2, 3, 4, 5, 6]
        random.shuffle(list_x)
        random.shuffle(list_y)
        for random_x in list_x:
            for random_y in list_y:
                ship = Ship(random_x, random_y, length, is_vertical)
                try:
                    self.add_ship(ship)
                    return
                except:
                    continue

    def check_game_over(self):
        for ship in self.__ships:
            for ship_part in ship.parts:
                if not (ship_part.is_destroyed):
                    return False

        return True

class FieldObject:
    def __init__(self):
        self.representation = ''
    def __str__(self):
        return self.representation

class EmptySpace(FieldObject):
    def __init__(self):
        self.representation = 'O'

class ShipPart(FieldObject):
    def __init__(self):
        self.representation = "\u25A1"
        self.__is_destroyed = False
    @property
    def is_destroyed(self):
        return self.__is_destroyed
    def destroy(self):
        self.__is_destroyed = True
        self.representation = "X"

class Ship:
    def __init__(self, position_x, position_y, length, is_vertical=False):
        self.__position_check(position_x, position_y)
        self.__length_check(length)
        self.position_x = position_x
        self.position_y = position_y
        self.length = length
        self.is_vertical = is_vertical
        self.parts = []
        for i in range(length):
            self.parts.append(ShipPart())

    @staticmethod
    def __position_check(pos_x, pos_y):
        if pos_x < 1 or pos_x > 6:
            raise ValueError("Неверное значение по координатам X (значение должно быть от 1 до 6)!")
        if pos_y < 1 or pos_y > 6:
            raise ValueError("Неверное значение по координатам Y (значение должно быть от 1 до 6)!")

    @staticmethod
    def __length_check(length):
        if length < 1 or length > 3:
            raise ValueError("Длинна корабля задана неверно (значение должно быть от 1 до 3)!")

class MissleShell(FieldObject):
    def __init__(self):
        self.representation = "T"

class CoordinatesError(Exception):
    def __init__(self, x, y):
        self.txt = f"Неверное значение координат x:{x}, y:{y}!"
    def __str__(self):
        return self.txt

class MultiplyShotError(Exception):
    def __init__(self):
        self.txt = "Выстрел по данным координатам уже произведен!"
    def __str__(self):
        return self.txt

class Enemy:
    def __init__(self):
        self.do_shot = self.__generate_shot()
    def __generate_shot(self):
        list_x = [1, 2, 3, 4, 5, 6]
        list_y = [1, 2, 3, 4, 5, 6]
        random.shuffle(list_x)
        random.shuffle(list_y)
        for random_x in list_x:
            for random_y in list_y:
                yield random_x, random_y


def player_input_shot():
        inp = input("Введите координаты выстрела через запятую (пример: x,y):")
        shot = str.split(inp, ',', 2)
        if not shot[0].isdigit() or not shot[1].isdigit():
            print("Введенные координаты должны быть цифрами!")
            return player_input_shot()
        return (int(shot[0]), int(shot[1]))


def player_do_shot(enemy_hidden_field, enemy_field):
    try:
        shot = player_input_shot()
        shot_result = enemy_hidden_field.do_shot(shot[0], shot[1])
        if shot_result:
            destroyed_ship_part = ShipPart()
            destroyed_ship_part.destroy()
            enemy_field.set_cell_value(shot[0]-1, shot[1]-1, destroyed_ship_part)
        else:
            enemy_field.set_cell_value(shot[0] - 1, shot[1] - 1, MissleShell())
    except Exception as ex:
        print(ex)
        player_do_shot(enemy_hidden_field, enemy_field)


def enemy_do_shot(enemy, player_field):
    shot = next(enemy.do_shot)
    player_field.do_shot(shot[0], shot[1])


enemy = Enemy()

print("Поле игрока:")
player_field = Field([])
player_field.fill_random()
player_field.print()
print("")
print("Поле врага:")
enemy_hidden_field = Field([])
enemy_hidden_field.fill_random()
enemy_field = Field(None)
enemy_field.print()

continue_game = True
while continue_game:

    player_do_shot(enemy_hidden_field, enemy_field)
    if enemy_hidden_field.check_game_over():
        print("Победил игрок!")
        continue_game = False

    enemy_do_shot(enemy, player_field)
    if player_field.check_game_over():
        print("Победил компьютер!")
        continue_game = False

    print("Поле игрока:")
    player_field.print()
    print("")
    print("Поле врага:")
    enemy_field.print()
