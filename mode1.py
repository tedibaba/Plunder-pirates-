from island import Island
from algorithms.mergesort import mergesort
from algorithms.binary_search import binary_search
from data_structures.bst import BinarySearchTree, ReverseIterator

class Mode1Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117

    We choose to store the islands in a binary tree over the list data structure which offers the same complexities
    in most cases due to the worst case requirement on the update island being O(logn) where n is the number of islands. We also store the ratio of 
    money to marines as the key for each island in the binary tree. This is because the ratio dictates which islands
    should be prioritized for raids as the ratio shows how much money per marine can be earned. 

    To achieve the required worst case complexity in select islands for crew members, we first sort the crew numbers. This 
    is an important optimization because for a crew that has more members than another one, it is optimal that it follows
    the smaller crews' attack path and then continue onward by raiding the next highest money to marine island. 

    We also define another method for iterating over a binary tree that follows the right - node - left pattern. By doing this, 
    we are able to get a descending order for the keys in the binary tree. This is essential for both the select_islands and 
    select_islands_from_crew_numbers methods. 

    In the select_islands_from_crew_numbers method, we need to create a mapping for the crew numbers passed in because when they are sorted,
    they lose the original order they are meant to be returned in. This mapping helps to regenerate the intended ordering
    of the return.
    """

    def __init__(self, islands: list[Island], crew: int) -> None:
        """
        The function initializes an object with a given list of islands and crew, and creates a binary
        search tree with the islands' money divided by marines as the key.
        
        :param islands: The `islands` parameter is a list of `Island` objects
        :param crew: The `crew` parameter represents the number of crew members on a ship

        :complexity:
            :best case: O(nlog(n))
            :worst case: O(nlog(n))
            where n is the number of islands
        """
 
        self.crew = crew
        self.islands = BinarySearchTree()
        for island in islands:
            self.islands[island.money/ island.marines] = island
        

    def select_islands(self) -> list[tuple[Island, int]]:
        """
        The function "select_islands" selects islands based on the available crew and the number of
        marines on each island.
        :return: a list of tuples, where each tuple contains an Island object and an integer
        representing the number of crew members to take from that island.

        :complexity:
            :best case: O(logn)
            :worst case: O(n)
            In the best case, we only need to do log(n) traversals to get to the greatest ratio. When we get to this island,
            in the best case, all the crew members attack this island and so there are no more crew members to attack other islands.

            In the worst case, every island needs to be traversed through. 
        """
   
        temp_crew = self.crew #Make a copy so we dont change the intial amount of crew
        it = ReverseIterator(self.islands.root)
        res = []
        for island in it:
            crew_to_take = min(temp_crew, island.item.marines)
            res.append((island.item, crew_to_take))
            temp_crew -= crew_to_take
            if temp_crew <= 0:
                break
        return res

        
    def select_islands_from_crew_numbers(self, crew_numbers: list[int]) -> list[float]:
        """
        The function `select_islands_from_crew_numbers` takes a list of crew numbers and returns a list
        of plunder amounts for each crew member based on their assigned islands.
        
        :param crew_numbers: The `crew_numbers` parameter is a list of integers representing the number
        of crew members on each ship
        :type crew_numbers: list[int]
        :return: The function `select_islands_from_crew_numbers` returns a list of floats.

        :complexity:
            :best case: O(n + clog(c))
            :worst case: O(n + clog(c))
            where n is the number of islands and c is length of the crew_numbers array.
        """
   
        crew_numbers = [[crew_numbers[i], i] for i in range(len(crew_numbers))]
        crew_numbers = mergesort(crew_numbers, lambda x : x[0])
        crew_shadow = [elem[0] for elem in crew_numbers]

        it = ReverseIterator(self.islands.root)
        res = [0]
        i = 0
        for island in it:
            island_money, island_marines= island.item.money, island.item.marines
            while crew_numbers[i][0] >= 0 and island_money > 0 :
                plunder_amount = int(min((crew_numbers[i][0] * island_money)/ island_marines, island_money))
                res[i] += plunder_amount
                fight_crew = min(crew_numbers[i][0], island_marines)
                crew_numbers[i][0] -= fight_crew
                island_marines -= fight_crew
                island_money -= plunder_amount
                if crew_numbers[i][0] <= 0:
                    i += 1
                    if i > len(crew_numbers) -1:
                        break
                    res.append(res[-1])
                    crew_numbers[i][0] -= crew_shadow[i-1]

                    
        final_res = [0 for _ in range(len(res))]
        i=0
        for _, j in crew_numbers:
            final_res[j] = res[i]
            i+=1

        return final_res
            

    def update_island(self, island: Island, new_money: float, new_marines: int) -> None:
        """
        The function updates the island's money and marines and updates the island's position in the
        dictionary based on the new money per marine ratio.
        
        :param island: The island parameter represents the island object that needs to be updated
        :param new_money: The new amount of money on the island
        :param new_marines: The parameter "new_marines" is an integer representing the new number of
        marines on the island

        :complexity:
            :best case: O(log(n))
            :worst case: O(log(n))
            where n is the number of islands 
            Deleting a node takes log(n) time and inserting takes log(n) time as well.        
        """

        del self.islands[island.money / island.marines]
        self.islands[new_money / new_marines] = island


