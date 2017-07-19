"""
Class definition
"""

import concurrent.futures


class Pool(object):
    """
    Game of life content
    """

    def __init__(self, cells: tuple, **kwargs):
        """
        init
        """
        self.cells_x = cells[0]
        self.cells_y = cells[1]
        
        self.__tmp = [0 for x in range(self.cells_x)]
        self.map = [list(self.__tmp) for y in range(self.cells_y)]
        self._tmap = [list(self.__tmp) for y in range(self.cells_y)]

        ## For threading purpose ##
        self._nbr = [list(self.__tmp) for y in range(self.cells_y)]
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=kwargs.get('threads', 4))

        ## else ##
        self.val = dict()
        self.val[0] = 0
        self.val[1] = 1
        self.val[2] = 1

        self.opp = dict()
        self.opp[0] = 1
        self.opp[1] = 0
        self.opp[2] = 0

        self.paused = not kwargs.get('force_unpause', False)
        self.ticks = 0

        ## add some entities to the seed ##
        if 'entities' in kwargs:
            self.spawn(kwargs['entities'])


    def apply_rule(self, x: int, y: int) -> None:
        """
        apply the game of life rules at a given position
        """
        ## Upper neighbours ##
        self._nbr[y][x] = self.val[self.map[y - 1][x - 1]]
        self._nbr[y][x] += self.val[self.map[y - 1][x]]
        self._nbr[y][x] += self.val[self.map[y - 1][(x + 1) % self.cells_x]]

        ## Left and Right neighbours ##
        self._nbr[y][x] += self.val[self.map[y][x - 1]]
        self._nbr[y][x] += self.val[self.map[y][(x + 1) % self.cells_x]]

        ## Lower neighbours ##
        self._nbr[y][x] += self.val[self.map[(y + 1) % self.cells_y][x - 1]]
        self._nbr[y][x] += self.val[self.map[(y + 1) % self.cells_y][x]]
        self._nbr[y][x] += self.val[self.map[(y + 1) % self.cells_y][(x + 1) % self.cells_x]]

        ## Original Conway's Game of Life rules ##
        if self.map[y][x] != 0:
            if self._nbr[y][x] not in (2, 3):
                self._tmap[y][x] = 0
            elif self._nbr[y][x] in (2, 3):
                self._tmap[y][x] = 2
        elif self._nbr[y][x] == 3:
            self._tmap[y][x] = 1
        else:
            self._tmap[y][x] = self.map[y][x]


    def spawn(self, entities: list) -> None:
        """
        insert an entity at the given position
        """
        for entity, x, y in entities:
            if entity['size'][0] + x > self.cells_x or \
                entity['size'][1] + y > self.cells_y:
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
            self.executor.submit(self.apply_rule, x, y) \
                for x in range(self.cells_x)            \
                for y in range(self.cells_y)
            ]
        concurrent.futures.wait(tasks)
        self.map = [list(col) for col in self._tmap]
        self.ticks += 1


    def pause(self):
        self.paused = not self.paused


    def save_seed(self):
        pass


    def restore_seed(self):
        pass