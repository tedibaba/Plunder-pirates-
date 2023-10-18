from island import Island
from data_structures.heap import MaxHeap


class Mode2Navigator:
    """
    We use store the islands in a heap due to the ability to create a heap is O(n) time where n is the number of islands
    to add into the heap. We recreate the heap each time the add_islands method is called because it creates a faster time
    complexity than using add for each island to be added. Any islands that have a ratio of money to marines less than 2
    will not be added to the heap due it not being viable for the pirates to raid such an island. Since the pirates are 
    optimal strategists, a ratio of less than 2 means its more worth to not raid and earn the 2 points per crew mate they
    have alive. The islands array keeps track of all the islands that have previously been added.

    In regard to adding islands to the heap, we add them based how much a pirate with a certain crew size could hope to obtain
    by raiding that island. This is distinct from adding the money on the island or using the ratio between the money and marines
    as was done in mode1 because if the crew size is smaller than the number of marines, then the money we can obtain is the ratio
    of crew to marines multiplied by the island's money.   

    In simulate_day, the first pirate will choose to raid the island with the greatest ratio. We find this island by using 
    the get_max method on the heap. The other pirates will also raid the island with the greatest ratio until there are no
    more islands left in the heap. For these pirates, they will choose to not do anything as this is the best way to maximise 
    the points they earn.

    """

    def __init__(self, n_pirates: int) -> None:
        """
        :param n_pirates: number of pirates 
        
        :complexity:
            :best case: O(1)
            :worst case: O(1)
        """
        self.n_pirates = n_pirates
        self.islands = []
        self.island_heap = [] #An empty list is initialsed to handle the case when simulate day is called without adding any islands

    def add_islands(self, islands: list[Island]):
        """
        The function adds islands to a list if their money to marines ratio is greater than 2.

        By extending, we do not need to rerun through the islands which have already been added 
        to the list.
        
        :param islands: The `islands` parameter is a list of `Island` objects

        :complexity:
            :best case: O(I)
            :worst case: O(I)
            where I is the number of islands to be added
        """

        self.islands.extend(islands)


    def simulate_day(self, crew: int) -> list[tuple[Island|None, int]]:
        """
        The 'simulate_day' method is used to simulate a day where each pirate is given 'crew' number
        of members to raid with. This method calculates how each pirate will optimally perform their 
        raid (i.e. which island they will go to and how many members they will send) in order to maximize
        their points. 

        We rewrite every island with the number of crew each pirate attacking the island will have. We do this
        so that every island is able to be placed in the heap in such a order that each time we will be able 
        to find an yield that will maximise the pirates points.

        :param crew: The number of crew members given to each pirate
        :return: A list containing the island each pirate will raid and how many crew members they will send over.
        
        :complexity:
            :best case: O(n + clog(n))
            :worst case: O(n + clog(n))
            where n is the number of islands that can be raided, c is the number of pirates
        """

        self.islands = [island for island in self.islands if island.marines > 0 and island.money/island.marines > 2] #filter out the unusable islands
        for island in self.islands:
            island.attackers = crew
        self.island_heap = MaxHeap.heapify(self.islands)

        res = []
        for _ in range(self.n_pirates):
            if len(self.island_heap) > 0 and crew > 0:
                island = self.island_heap.get_max()
                plunder_amount, fight_crew = int((min((crew * island.money)/ island.marines, island.money)) + 0.5), min(crew, island.marines)
                res.append((island, fight_crew))
                island.money -= plunder_amount 
                island.marines -= fight_crew
                if island.marines > 0 and island.money / island.marines > 2:
                    self.island_heap.add(island)
            else:
                res.append((None, 0))
        return res
    



if __name__ == "__main__":

    print("\nTest Set 1.")
    m2 = Mode2Navigator(3)

    islands = [Island("A", 400, 100), Island("B", 300, 150)]
    more_islands = [Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
 
    m2.add_islands(islands)
    m2.add_islands(more_islands)

    res = []
    for island, sent_crew in m2.simulate_day(100):
        res.append((island.name, sent_crew))

    m2.add_islands([Island("F", 900, 150)])
    for island, sent_crew in m2.simulate_day(100):
        res.append((island.name, sent_crew))
    
    print("Test 1: ", "passed" if len(res)==6 else "failed")
    print("Test 2: ", "passed" if res == [('A', 100), ('D', 90), ('E', 100), ('F', 100), ('F', 50), ('C', 5)]  else "failed")

    print("\nTest Set 2. stupid floating point errors will come up and you will get negative money if not handled (real tests probably wont bother with this)")
    m2 = Mode2Navigator(30)
    ocean = [
        [Island(name='Dawn Island', money=463891799000, marines=198), Island(name='Zou', money=49973040500, marines=159), Island(name='Enies Lobby', money=229621144000, marines=261), Island(name='Sabaody Archipelago', money=1875319370500, marines=162), Island(name='Skypeia', money=398061434000, marines=264), Island(name='Whole Cake Island', money=1779576013000, marines=5), Island(name='Water 7Ohara', money=1625292916500, marines=280), Island(name='Little Garden', money=1547377772000, marines=227), Island(name='Jaya', money=172060744000, marines=255), Island(name='Dawn Island', money=1375255418000, marines=153)],
        [Island(name='Long Ring Long Land', money=453357110000, marines=98), Island(name='Zou', money=1734578774000, marines=204), Island(name='Fish-Man Island', money=1905620583000, marines=183), Island(name='Jaya', money=963313466000, marines=19), Island(name='Water 7Ohara', money=1215311237500, marines=247), Island(name='Dressrosa', money=818944371500, marines=176), Island(name='Loguetown', money=1761861698500, marines=168), Island(name='Drum Island', money=703352173500, marines=162), Island(name='Wano Country', money=897570512500, marines=57), Island(name='Fish-Man Island', money=753472893000, marines=2)],
        [Island(name='Thriller Bark', money=968629852000, marines=178), Island(name='Gecko Islands', money=1326699602500, marines=278), Island(name='Zou', money=844493283500, marines=16), Island(name='Enies Lobby', money=566637240000, marines=164), Island(name='Cactus Island', money=746935278500, marines=179), Island(name='Thriller Bark', money=858159047500, marines=94), Island(name='Cactus Island', money=651464229500, marines=35), Island(name='Punk Hazard', money=1956877887000, marines=123), Island(name='Shimotsuki Village', money=230363344500, marines=243), Island(name='Arabasta Kingdom', money=751432838500, marines=104)],
        [Island(name='Cactus Island', money=2121731340500, marines=250), Island(name='Skypeia', money=1894681033000, marines=225), Island(name='Thriller Bark', money=1462055850500, marines=89), Island(name='Dawn Island', money=1352620981000, marines=22), Island(name='Wano Country', money=580644676000, marines=257), Island(name='Dawn Island', money=1151971893000, marines=106), Island(name='Skypeia', money=1327578209500, marines=101), Island(name='Gecko Islands', money=943988690000, marines=210), Island(name='Zou', money=593785387500, marines=38), Island(name='Baratie', money=309212017500, marines=245)] ,
        [Island(name='Gecko Islands', money=682116009500, marines=181), Island(name='Shimotsuki Village', money=658280893500, marines=182), Island(name='Baratie', money=1195286721500, marines=231), Island(name='Little Garden', money=1135931623500, marines=46), Island(name='Jaya', money=1142950132500, marines=250), Island(name='Skypeia', money=1097665709000, marines=85), Island(name='Impel Down', money=1695109204500, marines=280), Island(name='Water 7Ohara', money=1664376713000, marines=103), Island(name='Gecko Islands', money=7791885000, marines=195), Island(name='Loguetown', money=1044979577500, marines=296)]
    ]
    expected = [[(Island(name='Whole Cake Island', money=0, marines=0), 5), (Island(name='Sabaody Archipelago', money=0, marines=0), 123), (Island(name='Dawn Island', money=0, marines=0), 123), (Island(name='Little Garden', money=0, marines=0), 123), (Island(name='Water 7Ohara', money=0, marines=0), 123), (Island(name='Water 7Ohara', money=0, marines=0), 123), (Island(name='Little Garden', money=0, marines=0), 104), (Island(name='Sabaody Archipelago', money=0, marines=0), 39), (Island(name='Dawn Island', money=0, marines=0), 123), (Island(name='Dawn Island', money=0, marines=0), 30), (Island(name='Water 7Ohara', money=0, marines=0), 34), (Island(name='Skypeia', money=0, marines=0), 123), (Island(name='Skypeia', money=0, marines=0), 123), (Island(name='Dawn Island', money=0, marines=0), 75), (Island(name='Enies Lobby', money=0, marines=0), 123), (Island(name='Enies Lobby', money=0, marines=0), 123), (Island(name='Jaya', money=0, marines=0), 123), (Island(name='Jaya', money=0, marines=0), 123), (Island(name='Zou', money=0, marines=0), 123), (Island(name='Skypeia', money=0, marines=0), 18), (Island(name='Enies Lobby', money=0, marines=0), 15), (Island(name='Zou', money=0, marines=0), 36), (Island(name='Jaya', money=0, marines=0), 9), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0)], [(Island(name='Loguetown', money=0, marines=0), 123), (Island(name='Fish-Man Island', money=0, marines=0), 123), (Island(name='Zou', money=0, marines=0), 123), (Island(name='Jaya', money=0, marines=0), 19), (Island(name='Wano Country', money=0, marines=0), 57), (Island(name='Fish-Man Island', money=0, marines=0), 2), (Island(name='Zou', money=0, marines=0), 81), (Island(name='Fish-Man Island', money=0, marines=0), 60), (Island(name='Water 7Ohara', money=0, marines=0), 123), (Island(name='Water 7Ohara', money=0, marines=0), 123), (Island(name='Dressrosa', money=0, marines=0), 123), (Island(name='Drum Island', money=0, marines=0), 123), (Island(name='Loguetown', money=0, marines=0), 45), (Island(name='Long Ring Long Land', money=0, marines=0), 98), (Island(name='Dressrosa', money=0, marines=0), 53), (Island(name='Drum Island', money=0, marines=0), 39), (Island(name='Water 7Ohara', money=0, marines=0), 1), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0)], [(Island(name='Punk Hazard', money=0.0, marines=0), 123), (Island(name='Thriller Bark', money=0, marines=0), 94), (Island(name='Zou', money=0, marines=0), 16), (Island(name='Arabasta Kingdom', money=0, marines=0), 104), (Island(name='Thriller Bark', money=0, marines=0), 123), (Island(name='Cactus Island', money=0, marines=0), 35), (Island(name='Gecko Islands', money=0, marines=0), 123), (Island(name='Gecko Islands', money=0, marines=0), 123), (Island(name='Cactus Island', money=0, marines=0), 123), (Island(name='Enies Lobby', money=0, marines=0), 123), (Island(name='Thriller Bark', money=0, marines=0), 55), (Island(name='Cactus Island', money=0, marines=0), 56), (Island(name='Gecko Islands', money=0, marines=0), 32), (Island(name='Enies Lobby', money=0, marines=0), 41), (Island(name='Shimotsuki Village', money=0, marines=0), 123), (Island(name='Shimotsuki Village', money=0, marines=0), 120), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0)], [(Island(name='Thriller Bark', money=0, marines=0), 89), (Island(name='Dawn Island', money=0, marines=0), 22), (Island(name='Skypeia', money=0, marines=0), 101), (Island(name='Dawn Island', money=0, marines=0), 106), (Island(name='Cactus Island', money=0, marines=0), 123), (Island(name='Cactus Island', money=0, marines=0), 123), (Island(name='Skypeia', money=0, marines=0), 123), (Island(name='Skypeia', money=0, marines=0), 102), (Island(name='Zou', money=0, marines=0), 38), (Island(name='Gecko Islands', money=0, marines=0), 123), (Island(name='Gecko Islands', money=0, marines=0), 87), (Island(name='Wano Country', money=0, marines=0), 123), (Island(name='Wano Country', money=0, marines=0), 123), (Island(name='Baratie', money=0, marines=0), 123), (Island(name='Baratie', money=0, marines=0), 122), (Island(name='Cactus Island', money=0, marines=0), 4), (Island(name='Wano Country', money=0, marines=0), 11), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0)], [(Island(name='Water 7Ohara', money=0, marines=0), 103), (Island(name='Little Garden', money=0, marines=0), 46), (Island(name='Skypeia', money=0, marines=0), 85), (Island(name='Impel Down', money=0, marines=0), 123), (Island(name='Impel Down', money=0, marines=0), 123), (Island(name='Baratie', money=0, marines=0), 123), (Island(name='Jaya', money=0, marines=0), 123), (Island(name='Jaya', money=0, marines=0), 123), (Island(name='Baratie', money=0, marines=0), 108), (Island(name='Gecko Islands', money=0, marines=0), 123), (Island(name='Shimotsuki Village', money=0, marines=0), 123), (Island(name='Loguetown', money=0, marines=0), 123), (Island(name='Loguetown', money=0, marines=0), 123), (Island(name='Gecko Islands', money=0, marines=0), 58), (Island(name='Shimotsuki Village', money=0, marines=0), 59), (Island(name='Impel Down', money=0, marines=0), 34), (Island(name='Loguetown', money=0, marines=0), 50), (Island(name='Jaya', money=0, marines=0), 4), (Island(name='Gecko Islands', money=0, marines=0), 123), (Island(name='Gecko Islands', money=0, marines=0), 72), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0), (None, 0)]]

    for index, islands in enumerate(ocean):
        for island in islands:
            m2.add_islands([island])
        res = m2.simulate_day(123)
        passed = True
        for i in range(len(res)):
            if res[i][0] == None:
                if expected[index][i][0] != res[i][0]:
                    
                    passed = False
                    continue
            elif res[i][0].name != expected[index][i][0].name or res[i][1] != expected[index][i][1] or res[i][0].money != expected[index][i][0].money or res[i][0].marines != expected[index][i][0].marines:
                # print(res[i], expected[index][i])
                passed = False
        print(f"Test {index+1}: ", "passed" if passed else "failed")


    print("\nTest Set 3.")

    m2 = Mode2Navigator(100)
    islands = [Island("A", 400, 100), Island("B", 300, 150), Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
    for island in islands:
        m2.add_islands([island])
    res = m2.simulate_day(0)
    print("Test 1: ", "passed" if len(res) == 100 else "failed")
    passed = True
    # print(res)
    for r in res:
        if r[0] != None:
            passed = False
            
        if r[1] != 0:
            passed = False
    print("Test 2: ", "passed" if passed else "failed")

    print("\nTest Set 4.")
    m2 = Mode2Navigator(100)
    res = m2.simulate_day(0)
    print("Test 1: ", "passed" if len(res) == 100 else "failed")
    passed = True
    if len(res) != 100:
        passed = False
    for r in res:
        if r[0] != None:
            passed = False
        if r[1] != 0:
            passed = False
    print("Test 2: ", "passed" if passed else "failed")


if __name__ == "__main__":
    def check_islands_same(island1, island2):
        if island1 is None:
            return island2 is None
        return island1.name == island2.name and island1.money == island2.money and island1.marines == island2.marines

    def get_island_details(island):
        if island is None:
            return None, None, None
        return (island.name, island.money, island.marines)
        
    print("\nTest Set 1.")

    m2 = Mode2Navigator(1)
    islands = [Island("A", 400, 100)]
    m2.add_islands(islands)

    expected = [['A', 360.0, 90, 10], 
                ['A', 320.0, 80, 10], 
                ['A', 280.0, 70, 10], 
                ['A', 240.0, 60, 10], 
                ['A', 200.0, 50, 10], 
                ['A', 160.0, 40, 10], 
                ['A', 120.0, 30, 10], 
                ['A', 80.0, 20, 10], 
                ['A', 40.0, 10, 10], 
                ['A', 0.0, 0, 10], 
                [None, None, None, 0]
                ]
    for i in range(11):
        res = m2.simulate_day(10)
        name, money, marines = get_island_details(res[0][0])
        sent = res[0][1]

        print(f"Test {i+1}: ", "pass" if expected[i]==[name, money, marines, sent] else "fail")

    print("\nTest Set 2.")

    m2 = Mode2Navigator(10)
    islands = [Island("A", 400, 100), Island("B", 300, 150), Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
    m2.add_islands(islands)

    expected = [[['C', 0, 0, 5], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10]], 
                [['A', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10]], 
                [['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10]], 
                [[None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0]]]

    got = []
    for i in range(4):
        res = m2.simulate_day(10)
        
        line = []
        for island in res:
            name, money, marines = get_island_details(island[0])
            sent = island[1]
        
            line.append([name, money, marines, sent])

        got.append(line)
        
    for i in range(4):
        print(f"Test {i+1}: ", "pass" if expected[i]==got[i] else "fail")