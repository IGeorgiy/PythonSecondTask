class Field:
    def __init__(self, field):
        self.__field = field
    def print(self):
            print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
            for index, value in enumerate(self.__field):
                print(f"{index} {value[0]} {value[1]} {value[2]}")

class FieldObject:
    def __init__(self):
        self.representation = 'O'
    def __str__(self):
        return self.representation

class Ship(FieldObject):
    def __init__(self):
        self.representation = "\u25A1"
        self.is_destroyed = False

    def destroy(self):
        self.is_destroyed = True
        self.representation = "X"


class MissleShell(FieldObject):
    def __init__(self):
        self.representation = "T"