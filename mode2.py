from island import Island
from data_structures.heap import MaxHeap


class Mode2Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117
    
    We use store the islands in a heap due to the ability to create a heap is O(n) time where n is the number of islands
    to add into the heap. We recreate the heap each time the add_islands method is called because it creates a faster time
    complexity than using add for each island to be added. Any islands that have a ratio of money to marines less than 2
    will not be added to the heap due it not being viable for the pirates to raid such an island. Since the pirates are 
    optimal strategists, a ratio of less than 2 means its more worth to not raid and earn the 2 points per crew mate they
    have alive. The islands array keeps track of all the islands that have previously been added.

    In simulate_day, the first pirate will choose to raid the island with the greatest ratio. We find this island by using 
    the get_max method on the heap. The other pirates will also raid the island with the greatest ratio until there are no
    more islands left in the heap. For these pirates, they will choose to not do anything as this is the best way to maximise 
    the points they earn.

    """

    def __init__(self, n_pirates: int) -> None:
        """
        
        :complexity:
            :best case: O(1)
            :worst case: O(1)
        """
        self.n_pirates = n_pirates
        self.islands = []
        self.island_heap = None

    def add_islands(self, islands: list[Island]):
        """
        The function adds islands to a list if their money to marines ratio is greater than 2.
        
        :param islands: The `islands` parameter is a list of `Island` objects

        :complexity:
            :best case: O(N + I)
            :worst case: O(N + I)
        """

        self.islands += [island for island in islands if island.money/island.marines > 2] 
        self.island_heap = MaxHeap.heapify(self.islands) 

    def simulate_day(self, crew: int) -> list[tuple[Island|None, int]]:
        """
        
        :complexity:
            :best case:
            :worst case: 
        """
        island_copy = self.island_heap #We do not want to modify the original heap
        res = []
        for _ in range(self.n_pirates):
            if len(island_copy) != 0:
                island = island_copy.get_max()
                plunder_amount = int(min((crew * island.money)/ island.marines, island.money))
                fight_crew = min(crew, island.marines)
                res.append((island, fight_crew))
                island.money -= plunder_amount
                island.marines -= fight_crew
                if island.money > 0:
                    island_copy.add(island)
            else:
                res.append((None, 0))
        return res

