"""
Class definition
"""

import concurrent.futures

import settings

class World(object):
    """
    Game of life content
    """

    def __init__(self):
        """
        init
        """
        self.__tmp = [0 for x in range(settings.CELLS_X)]
        self.map = [list(self.__tmp) for y in range(settings.CELLS_Y)]
        self._next_map = [list(self.__tmp) for y in range(settings.CELLS_Y)]

        ## For threading purpose ##
        self._neighbours = [list(self.__tmp) for y in range(settings.CELLS_Y)]
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=settings.THREADS)

        ## else ##
        self.value = dict()
        self.value[0] = 0
        self.value[1] = 1
        self.value[2] = 1
        self.paused = True
        self.ticks = 0


    def apply_rule(self, x: int, y: int) -> None:
        """
        apply the game of life rules at a given position
        """
        ## Upper neighbours ##
        self._neighbours[y][x] = self.value[self.map[y - 1][x - 1]]
        self._neighbours[y][x] += self.value[self.map[y - 1][x]]
        self._neighbours[y][x] += self.value[self.map[y - 1][(x + 1) % settings.CELLS_X]]

        ## Left and Right neighbours ##
        self._neighbours[y][x] += self.value[self.map[y][x - 1]]
        self._neighbours[y][x] += self.value[self.map[y][(x + 1) % settings.CELLS_X]]

        ## Lower neighbours ##
        self._neighbours[y][x] += self.value[self.map[(y + 1) % settings.CELLS_Y][x - 1]]
        self._neighbours[y][x] += self.value[self.map[(y + 1) % settings.CELLS_Y][x]]
        self._neighbours[y][x] += self.value[self.map[(y + 1) % settings.CELLS_Y][(x + 1) % settings.CELLS_X]]

        ## Original Conway's Game of Life rules ##
        if self.map[y][x] != 0:
            if self._neighbours[y][x] not in (2, 3):
                self._next_map[y][x] = 0
            elif self._neighbours[y][x] in (2, 3):
                self._next_map[y][x] = 2
        elif self._neighbours[y][x] == 3:
            self._next_map[y][x] = 1
        else:
            self._next_map[y][x] = self.map[y][x]


    def spawn(self, entities: list) -> None:
        """
        insert an entity at the given position
        """
        for entity, x, y in entities:
            if entity['size'][0] + x > settings.CELLS_X or \
                entity['size'][1] + y > settings.CELLS_Y:
                print("Cannot spawn a {}, too large".format(
                    entity['name']))
            else:
                for y2 in range(entity['size'][1]):
                    for x2 in range(entity['size'][0]):
                        self.map[y + y2][x + x2] = entity['body'][y2][x2]


    def tick(self):
        """
        count ticks
        """
        print("tack!")
        self.ticks += 1


    def populate(self):
        """
        Generate the next iteration of population
        """
        tasks = [
            self.executor.submit(self.apply_rule, x, y) for x in range(settings.CELLS_X) for y in range(settings.CELLS_Y)
            ]
        concurrent.futures.wait(tasks)
        self.map = [list(col) for col in self._next_map]
        self.ticks += 1
