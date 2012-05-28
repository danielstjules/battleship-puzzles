import random

class Puzzle:
    
    # grid
    
    grid = None
    populated_grid = None
    row_totals = None
    column_totals = None
    
    n = 10
    m = 10
    
    empty = "-"
    node = "o"

    # ships
    
    battleship_size = 4
    cruiser_size = 3
    destroyer_size = 2
    submarine_size = 1
    
    ships = None
    
    def __init__(self, n, m, battleships, cruisers, destroyers, submarines, genType):
        self.n = n
        self.m = m
        self.battleships = battleships
        self.cruisers = cruisers
        self.destroyers = destroyers
        self.submarines = submarines
        self.grid = [[self.empty for i in range(m)] for j in range(n)]
        self.populated_grid = [[self.empty for i in range(m)] for j in range(n)]
        self.row_totals = [0 for i in range(m)]
        self.column_totals = [0 for i in range(n)]
        self.build_ship_list()
        if genType == 0:
            self.generate()
        else:
            self.randomly_generate()
        self.set_totals()
        self.copy_grid()
        self.erase_grid()
	
    def build_ship_list(self):
        # build list of ships to be placed
        self.ships = []
        for i in range (0, self.battleships):
            self.ships.append(self.battleship_size)
        for i in range (0, self.cruisers):
            self.ships.append(self.cruiser_size)
        for i in range (0, self.destroyers):
            self.ships.append(self.destroyer_size)
        for i in range (0, self.submarines):
            self.ships.append(self.submarine_size)

    def generate(self):
        # Place ships, forcing a yes instance
        while(True):
            for i in range(len(self.ships)):
                placed = False
                size = self.ships[i]
                cells = self.get_empty_cells()
                for j in range (0, len(cells)):
                    row = cells[j][0]
                    col = cells[j][1]
                    orien = random.randint(0,1)
                    adjacent = self.adjacent_nodes(row,col,size,orien)
                    if adjacent == False:
                        placed = self.place_ship(row,col,size,orien)
                    if placed == False:
                        adjacent = self.adjacent_nodes(row,col,size,1-orien)
                        if adjacent == False:
                            placed = self.place_ship(row,col,size,1-orien)
                    if placed == True:
                        break
                if placed == False:
                    break
            if i == (len(self.ships)-1) and placed == True:
                return
            else:
                self.erase_grid()
    
    def randomly_generate(self):
        # Place ships randomly within grid
        # High probability of no instance
        while(True):
            for i in range(len(self.ships)):
                placed = False
                size = self.ships[i]
                cells = self.get_empty_cells()
                for j in range (0, len(cells)):
                    row = cells[j][0]
                    col = cells[j][1]
                    orien = random.randint(0,1)
                    placed = self.place_ship(row,col,size,orien)
                    if placed == False:
                        placed = self.place_ship(row,col,size,1-orien)
                    if placed == True:
                        break
                if placed == False:
                     break
            if i == (len(self.ships)-1) and placed == True:
                return
            else:
                self.erase_grid()

    def get_empty_cells(self):
    	# Return a list of all empty cells
        cells = []
        for i in range(0, self.m):
            for j in range(0,self.n):
                if self.grid[i][j] == self.empty:
                    cells.append([i,j])
        random.shuffle(cells)
        return cells                   
        
    def place_ship(self,row,col,size,orien):
        # Check that placement is within bounds of grid
        # and that ship won't overlap existing nodes
        try:
            if orien == 0:
                for j in range(col, col + size):
                    if self.grid[row][j] != self.empty:
                        return False
                for j in range(col, col + size):
                    self.grid[row][j] = self.node
            else:
                for i in range(row, row + size):
                    if self.grid[i][col] != self.empty:
                        return False
                for i in range(row, row + size):
                    self.grid[i][col] = self.node           
        except IndexError:
            return False
        return True

    def remove_ship(self,row,col,size,orien):
    	# Set nodes to empty
        if orien == 0:
            for j in range(col,col+size):
                self.grid[row][j] = self.empty
        else:
            for i in range(row,row+size):
                self.grid[i][col] = self.empty

    def set_totals(self):
        # Assign row and column totals accordingly
        for i in range(0, self.m):
            self.row_totals[i] = self.get_row_total(i)
        for j in range(0, self.n):
            self.column_totals[j] = self.get_column_total(j)

    def get_row_total(self,row):
    	# Calculate current number of nodes in row
        total = 0
        for i in range(0,self.n):
            if self.grid[row][i] != self.empty:
                total += 1
        return total

    def get_column_total(self,col):
    	# Calculate current number of nodes in column
        total = 0
        for i in range(0,self.m):
            if self.grid[i][col] != self.empty:
                total += 1
        return total

    def erase_grid(self):
        # Must be called prior to solving
        for i in range(0, self.m):
            for j in range(0,self.n):
                self.grid[i][j] = self.empty

    def copy_grid(self):
    	# After generation, use this to store 
    	# the generated solution in populated_grid
        for i in range(0, self.m):
            for j in range(0,self.n):
                self.populated_grid[i][j] = self.grid[i][j]

    def get_node(self,row,col):
    	# Check if node is empty or not
        # Avoid L[-1]
        if row < 0 or col < 0:
            return self.empty
        try:
            value = self.grid[row][col]
        except IndexError:
            value = self.empty
        return value

    def adjacent_nodes(self,row,col,size,orien):
        # Returns True if there are adjacent nodes,
        # False otherwise
        if orien == 0:
            if self.get_node(row,col+size) != self.empty:
                return True
            if self.get_node(row,col-1) != self.empty:
                return True
            for j in range(-1,size+1):
                    if self.get_node(row+1,col+j) != self.empty:
                        return True
                    if self.get_node(row-1,col+j) != self.empty:
                        return True
        else:
            if self.get_node(row+size,col) != self.empty:
                return True
            if self.get_node(row-1,col) != self.empty:
                return True
            for i in range(-1,size+1):
                    if self.get_node(row+i,col+1) != self.empty:
                        return True
                    if self.get_node(row+i,col-1) != self.empty:
                        return True
        return False
        
    def empty_nodes(self,row,col,size,orien):
        # Check if nodes are empty
        try:
            if orien == 0:
                for j in range(col, col + size):
                    if self.grid[row][j] != self.empty:
                        return False
            else:
                for i in range(row, row + size):
                    if self.grid[i][col] != self.empty:
                        return False          
        except IndexError:
            return False
        return True
    
    def respects_indicators(self):
    	# Check that the current placement of nodes 
    	# respects all row/column indicators
        for i in range(0, self.m):
            if self.get_row_total(i) != self.row_totals[i]:
                return False
        for j in range(0, self.n):
            if self.get_column_total(j) != self.column_totals[j]:
                return False
        return True
        
    def print_alg_solution(self):
    	# Output current solution
        column_totals = [" ", " "]
        for j in range(0, self.n):
            column_totals.append(str(self.column_totals[j]))
            column_totals.append(" ")
        print(''.join(column_totals))
        for i in range(0,self.m):
            strList = []
            strList.append(str(self.row_totals[i]))
            strList.append(" ")
            for j in range(0,self.n):
                strList.append(self.grid[i][j])
                strList.append(" ")
            print(''.join(strList))
        print('n: '+ str(self.n) + ' m: ' + str(self.m) + '\n' +
              'battleships: ' + str(self.battleships) + '\n' +
              'cruisers: ' + str(self.cruisers) + '\n' +
              'destroyers: ' + str(self.destroyers) + '\n' +
              'submarines: ' + str(self.submarines) + '\n')

    def print_solution(self):
    	# Output solution given in instance generation
        column_totals = [" ", " "]
        for j in range(0, self.n):
            column_totals.append(str(self.column_totals[j]))
            column_totals.append(" ")
        print(''.join(column_totals))
        for i in range(0,self.m):
            strList = []
            strList.append(str(self.row_totals[i]))
            strList.append(" ")
            for j in range(0,self.n):
                strList.append(self.populated_grid[i][j])
                strList.append(" ")
            print(''.join(strList))
        print('n: '+ str(self.n) + ' m: ' + str(self.m) + '\n' +
              'battleships: ' + str(self.battleships) + '\n' +
              'cruisers: ' + str(self.cruisers) + '\n' +
              'destroyers: ' + str(self.destroyers) + '\n' +
              'submarines: ' + str(self.submarines) + '\n')

    def print_solution_to_file(self):
    	# Print solution given in instance generation to file
        f = open('instances.txt', 'a')
        column_totals = [" ", " "]
        for j in range(0, self.n):
            column_totals.append(str(self.column_totals[j]))
            column_totals.append(" ")
        f.write(''.join(column_totals) + '\n')
        for i in range(0,self.m):
            strList = []
            strList.append(str(self.row_totals[i]))
            strList.append(" ")
            for j in range(0,self.n):
                strList.append(self.populated_grid[i][j])
                strList.append(" ")
            f.write(''.join(strList) + '\n')
        f.write('n: '+ str(self.n) + ' m: ' + str(self.m) + '\n' +
                'battleships: ' + str(self.battleships) + '\n' +
                'cruisers: ' + str(self.cruisers) + '\n' +
                'destroyers: ' + str(self.destroyers) + '\n' +
                'submarines: ' + str(self.submarines) + '\n')
        f.close()
