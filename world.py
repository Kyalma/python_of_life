import concurrent.futures

import settings

class World(object):

    def __init__(self, **kwargs):
        self.ticks = 0

        self.__tmp = [0 for x in range(settings.CELLS_X)]
        self.map = [list(self.__tmp) for y in range (settings.CELLS_Y)]
        self._next_map = [list(self.__tmp) for y in range(settings.CELLS_Y)]

        ## For threading purpose ##
        self._neighbours_map = [list(self.__tmp) for y in range(settings.CELLS_Y)]
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=settings.THREADS)


    def is_alive(self, cell_status: int):
        return (1 if cell_status else 0)


    def apply_rule(self, x: int, y: int) -> None:
        ## Reset for the current generation ##
        self._neighbours_map[y][x] = 0

        ## Upper neighbours ##
        self._neighbours_map[y][x] += self.is_alive(self.map[(y - 1 if y - 1 >= 0 else settings.CELLS_Y - 1)][(x - 1 if x - 1 >= 0 else settings.CELLS_X - 1)])
        self._neighbours_map[y][x] += self.is_alive(self.map[(y - 1 if y - 1 >= 0 else settings.CELLS_Y - 1)][x])
        self._neighbours_map[y][x] += self.is_alive(self.map[(y - 1 if y - 1 >= 0 else settings.CELLS_Y - 1)][(x + 1 if x + 1 < settings.CELLS_X else 0)])

        ## Left and Right neighbours ##
        self._neighbours_map[y][x] += self.is_alive(self.map[y][(x - 1 if x - 1 >= 0 else settings.CELLS_X - 1)])
        self._neighbours_map[y][x] += self.is_alive(self.map[y][(x + 1 if x + 1 < settings.CELLS_X else 0)])

        ## Lower neighbours ##
        self._neighbours_map[y][x] += self.is_alive(self.map[(y + 1 if y + 1 < settings.CELLS_Y else 0)][(x - 1 if x - 1 >= 0 else settings.CELLS_X - 1)])
        self._neighbours_map[y][x] += self.is_alive(self.map[(y + 1 if y + 1 < settings.CELLS_Y else 0)][x])
        self._neighbours_map[y][x] += self.is_alive(self.map[(y + 1 if y + 1 < settings.CELLS_Y else 0)][(x + 1 if x + 1 < settings.CELLS_X else 0)])

        ## Original Conway's Game of Life rules ##
        if self.map[y][x] != 0 and (self._neighbours_map[y][x] < 2 or self._neighbours_map[y][x] > 3):
            self._next_map[y][x] = 0
        elif self.map[y][x] != 0 and self._neighbours_map[y][x] in (2, 3):
            self._next_map[y][x] = 2
        elif self.map[y][x] == 0 and self._neighbours_map[y][x] == 3:
            self._next_map[y][x] = 1
        else:
            self._next_map[y][x] = self.map[y][x]
        return
        

    def spawn(self, entities: list) -> None:
        for entity, x, y in entities:
            for y2 in range(len(entity)):
                for x2 in range(len(entity[y2])):
                    self.map[y + y2][x + x2] = entity[y2][x2]


    def tick(self):
        print("tack!")
        self.ticks += 1


    def populate(self):
        tasks = [
            self.executor.submit(self.apply_rule, x, y) for x in range(settings.CELLS_X) for y in range(settings.CELLS_Y)
            ]
        concurrent.futures.wait(tasks)
        self.map = [list(col) for col in self._next_map]
        self.ticks += 1