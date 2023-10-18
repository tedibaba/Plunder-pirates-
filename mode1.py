from island import Island
from algorithms.mergesort import mergesort
from data_structures.bst import BinarySearchTree, ReverseInOrderIterator

class Mode1Navigator:
    """
    We choose to store the islands in a binary tree over the list data structure which offers the same complexities
    in most cases due to the worst case requirement on the update island being O(logn) where n is the number of islands. If
    this complexity requirement did not exist, we could have alternatively used an array. We also store the ratio of 
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
        it = ReverseInOrderIterator(self.islands.root)
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
        of maximal plunder amounts.  
        
        :param crew_numbers: The `crew_numbers` parameter is a list of integers representing the number
        of crew members 
        :return: The function `select_islands_from_crew_numbers` returns a list of floats indicating the amount 
        of money that a crew of that size could plunder.

        :complexity:
            :best case: O(c)
            :worst case: O(n + clog(c))
            where n is the number of islands and c is length of the crew_numbers array.

            In the best case, the crew_numbers are already sorted which gives O(c) to verify the order. Furthermore, in the best case,
            we will need to use all the crew on the first island and hence there is no need to iterate over all of them.

            In both worst case, we sort over the crew_numbers array which yields O(clog(c)). We also 
            iterate over the all the islands and over all the crew numbers which gives the O(n) and O(c) respectively. 
            Hence we get O(n + clog(c))
        """
        if len(crew_numbers) == 0: #Edge case: when the crew_numbers array is empty
            return []

        crew_numbers = [[crew_numbers[i], i] for i in range(len(crew_numbers))] #This is done to keep track of the original index that the array was passed in

        for i in range(len(crew_numbers) -1): #Checking if it is already sorted
            if crew_numbers[i][0] > crew_numbers[i+1][0]:
                crew_numbers = mergesort(crew_numbers, lambda x : x[0])
                break
        
        crew_used = 0 #An accumulator to keep track of the number of crew that have been used.

        it = ReverseInOrderIterator(self.islands.root)
        res = [0]
        i = 0
        complete_break = False #Used to exit the for loop when there are no more crews to iterate over

        for island in it:
            island_money, island_marines= island.item.money, island.item.marines
            while crew_numbers[i][0] >= 0 and island_money > 0:

                plunder_amount, fight_crew= int(min((crew_numbers[i][0] * island_money)/ island_marines, island_money) + 0.5), min(crew_numbers[i][0], island_marines)
                res[i] += plunder_amount
                crew_numbers[i][0] -= fight_crew
                crew_used += fight_crew
                island_marines -= fight_crew
                island_money -= plunder_amount

                if crew_numbers[i][0] <= 0:
                    i += 1 
                   
                    if i >= len(crew_numbers):
                        complete_break = True
                        break

                    res.append(res[-1])
                    crew_numbers[i][0] -= crew_used

            if complete_break:
                break
        
        res += [res[-1] for _ in range(i + 1, len(crew_numbers))] #If we went through all the islands but there are still crew_numbers we have not calculated for, then all the other crew numbers will yield the same value. 

        #Remapping to the original order         
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
        #Update the island's attributes
        island.money = new_money
        island.marines = new_marines
        self.islands[new_money / new_marines] = island





if __name__ == "__main__":
    # islands = [Island("A", 400, 100), Island("B", 300, 150), Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
    # nav = Mode1Navigator(islands, 200)
    # results = nav.select_islands()
    # for i in results:
    #     print(i[0].name, i[1])
    print('\nTest Set 1. select_islands_from_crew_numbers()')
    islands = [Island("A", 400, 100), Island("B", 300, 150), Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
    
    nav = Mode1Navigator(islands, 200)

    test_crew_numbers = [
        [0, 3, 4, 4],
        [0, 3, 4, 4, 5, 6, 7, 8, 9, 10],
        [0, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        [0, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        [0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        [9, 7, 2, 4, 2, 7, 9, 3, 100, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        [6999, 700, 1000000, 2, 3, 4, 6, 8, 1, 252524],
        [],
    ]

    expected = [
        [0.0, 60.0, 80.0, 80.0],
        [0.0, 60.0, 80.0, 80.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0],
        [0.0, 60.0, 80.0, 80.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0, 124.0, 128.0],
        [0.0, 60.0, 80.0, 80.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0, 124.0, 128.0, 132.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 480.0, 0.0, 0.0, 0.0],
        [116.0, 108.0, 40.0, 80.0, 40.0, 108.0, 116.0, 60.0, 480.0, 80.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0, 124.0, 128.0, 132.0], 
        [1450.0, 1450.0, 1450.0, 40.0, 60.0, 80.0, 104.0, 112.0, 20.0, 1450.0],
        [],
    ]

    for i in range(len(test_crew_numbers)):
        print(i)
        res = nav.select_islands_from_crew_numbers(test_crew_numbers[i])
        print(f"Test {i+1}:", "pass" if res == expected[i] else "fail")

    print('\nTest Set 2. select_islands()')
    
    ocean = [
        [Island(name='Dawn Island', money=463891799000, marines=198), Island(name='Zou', money=49973040500, marines=159), Island(name='Enies Lobby', money=229621144000, marines=261), Island(name='Sabaody Archipelago', money=1875319370500, marines=162), Island(name='Skypeia', money=398061434000, marines=264), Island(name='Whole Cake Island', money=1779576013000, marines=5), Island(name='Water 7Ohara', money=1625292916500, marines=280), Island(name='Little Garden', money=1547377772000, marines=227), Island(name='Jaya', money=172060744000, marines=255), Island(name='Dawn Island', money=1375255418000, marines=153)],
        [Island(name='Long Ring Long Land', money=453357110000, marines=98), Island(name='Zou', money=1734578774000, marines=204), Island(name='Fish-Man Island', money=1905620583000, marines=183), Island(name='Jaya', money=963313466000, marines=19), Island(name='Water 7Ohara', money=1215311237500, marines=247), Island(name='Dressrosa', money=818944371500, marines=176), Island(name='Loguetown', money=1761861698500, marines=168), Island(name='Drum Island', money=703352173500, marines=162), Island(name='Wano Country', money=897570512500, marines=57), Island(name='Fish-Man Island', money=753472893000, marines=2)],
        [Island(name='Thriller Bark', money=968629852000, marines=178), Island(name='Gecko Islands', money=1326699602500, marines=278), Island(name='Zou', money=844493283500, marines=16), Island(name='Enies Lobby', money=566637240000, marines=164), Island(name='Cactus Island', money=746935278500, marines=179), Island(name='Thriller Bark', money=858159047500, marines=94), Island(name='Cactus Island', money=651464229500, marines=35), Island(name='Punk Hazard', money=1956877887000, marines=123), Island(name='Shimotsuki Village', money=230363344500, marines=243), Island(name='Arabasta Kingdom', money=751432838500, marines=104)],
        [Island(name='Cactus Island', money=2121731340500, marines=250), Island(name='Skypeia', money=1894681033000, marines=225), Island(name='Thriller Bark', money=1462055850500, marines=89), Island(name='Dawn Island', money=1352620981000, marines=22), Island(name='Wano Country', money=580644676000, marines=257), Island(name='Dawn Island', money=1151971893000, marines=106), Island(name='Skypeia', money=1327578209500, marines=101), Island(name='Gecko Islands', money=943988690000, marines=210), Island(name='Zou', money=593785387500, marines=38), Island(name='Baratie', money=309212017500, marines=245)] ,
        [Island(name='Gecko Islands', money=682116009500, marines=181), Island(name='Shimotsuki Village', money=658280893500, marines=182), Island(name='Baratie', money=1195286721500, marines=231), Island(name='Little Garden', money=1135931623500, marines=46), Island(name='Jaya', money=1142950132500, marines=250), Island(name='Skypeia', money=1097665709000, marines=85), Island(name='Impel Down', money=1695109204500, marines=280), Island(name='Water 7Ohara', money=1664376713000, marines=103), Island(name='Gecko Islands', money=7791885000, marines=195), Island(name='Loguetown', money=1044979577500, marines=296)]
    ]

    res = []
    for islands in ocean:
        m = Mode1Navigator(islands, 100)
        for island, sent in  m.select_islands():
            res.append((island.name, sent))

    expected = [('Whole Cake Island', 5), ('Sabaody Archipelago', 95), ('Fish-Man Island', 2), ('Jaya', 19), ('Wano Country', 57), ('Loguetown', 22), ('Zou', 16), ('Cactus Island', 35), ('Punk Hazard', 49), ('Dawn Island', 22), ('Thriller Bark', 78), ('Little Garden', 46), ('Water 7Ohara', 54)]
    print(f"Test 1: ", "pass" if res == expected else "fail")

    print('\nTest Set 3. update_island()')
    original_islands = [Island("A", 400, 100), Island("B", 300, 150), Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
    islands = [Island("A", 400, 100), Island("B", 300, 150), Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
    
    nav = Mode1Navigator(islands, 200)
    for island in islands:
        nav.update_island(island, island.money, island.marines)
    for island in islands:
        nav.update_island(island, island.money-1, island.marines-1)

    for index, island in enumerate(islands):
        print(f"Test {index+1}: ", "pass" if island.money == original_islands[index].money-1 and island.marines == original_islands[index].marines-1 else "fail")

    print('\nTest Set 4. update_island()')
    for index, island in enumerate(islands):
        print(f"Test {index+1}: ", "pass" if island.money / island.marines == (original_islands[index].money-1)/(original_islands[index].marines-1)  else "fail")

    print()


