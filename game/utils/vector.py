from game.common.game_object import GameObject
from game.common.enums import ObjectType
from typing import Self, Tuple


class Vector(GameObject):
    """
    `Vector Class Notes:`

    This class is used universally in the project to handle anything related to coordinates. There are a few useful
    methods here to help in a few situations.

    -----

    Add Vectors Method:
        This method will take two Vector objects, combine their (x, y) coordinates, and return a new Vector object.

        Example:
            vector_1: (1, 1)
            vector_2: (1, 1)

            Result:
            vector_result: (2, 2)

    -----

    Add to Vector method:
        This method will take a different Vector object and add it to the current Self reference; that is, this method
        belongs to a Vector object and is not static.

        Example:
            self_vector: (0, 0)
            vector_1: (1, 3)

            Result:
            self_vector: (1, 3)

    -----

    Add X and Add Y methods:
        These methods act similarly to the ``add_vector()`` method, but instead of changing both the x and y, these
        methods change their respective variables.

        Add X Example:
            self_vector: (0, 0)
            vector_1: (1, 3)

            Result:
            self_vector: (1, 0)

        Add Y Example:
            self_vector: (0, 0)
            vector_1: (1, 3)

            Result:
            self_vector: (0, 3)

    -----

    As Tuple Method:
        This method returns a tuple of the Vector object in the form of (x, y). This is to help with storing it easily
        or accessing it in an immutable structure.
    """

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__()
        self.object_type: ObjectType = ObjectType.VECTOR
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, x: int) -> None:
        if x is None or not isinstance(x, int):
            raise ValueError(f"The given x value, {x}, is not an integer.")
        self.__x = x

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, y: int) -> None:
        if y is None or not isinstance(y, int):
            raise ValueError(f"The given y value, {y}, is not an integer.")
        self.__y = y

    @staticmethod
    def from_xy_tuple(xy_tuple: Tuple[int, int]) -> 'Vector':
        ...

    @staticmethod
    def from_yx_tuple(yx_tuple: Tuple[int, int]) -> 'Vector':
        ...

    @staticmethod
    def add_vectors(vector_1: 'Vector', vector_2: 'Vector') -> 'Vector':
        ...

    def add_to_vector(self, other_vector: Self) -> 'Vector':
        ...

    def add_x_y(self, x: int, y: int) -> 'Vector':
        ...

    def add_x(self, x: int) -> 'Vector':
        ...

    def add_y(self, y: int) -> 'Vector':
        ...

    def as_tuple(self) -> Tuple[int, int]:
        ...

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return hash(self.as_tuple())

    def __eq__(self, other) -> bool:
        return self.as_tuple() == other.as_tuple()
