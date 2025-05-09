class Coordinata:
    def __init__(self, x: int, y: int, libero: bool = False):
        self.x = x
        self.y = y
        self.libero = libero

    def __eq__(self, other):
        if isinstance(other, Coordinata):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def print(self):
        print(f"x: {self.x}, y: {self.y}")