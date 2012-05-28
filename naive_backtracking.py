import puzzle

class NaiveBacktracking:
    
    answer = False
    ships_to_place = []
    ship_col = []
    ship_row = []
    ship_orien = []
    
    def __init__(self, p_instance):
        self.p = p_instance
        self.ships_to_place = p_instance.ships[:]
        self.ships_to_place.sort(reverse=True)
        self.answer = self.backtrack()

    def backtrack(self):
        # base case, use certifier and
        # check that all conditions are met
        if self.ships_to_place == []:
            if(self.p.respects_indicators() == False):
                return False
            elif(self.no_adjacent_ships() == False):
                return False
            else:
                return True
        for i in range(len(self.ships_to_place)):
            size = self.ships_to_place[i]
            for row in range(0,self.p.m):
                for col in range(0,self.p.n):
                    for orien in range(0, 2):
                        placed = self.p.place_ship(row,col,size,orien)
                        if placed == True:
                            self.ship_row.append(row)
                            self.ship_col.append(col)
                            self.ship_orien.append(orien)
                            self.ships_to_place.pop(i)
                            result = self.backtrack()
                            if result == True:
                                return True
                            else:
                                self.ships_to_place.insert(i,size)
                                pRow = self.ship_row.pop()
                                pCol = self.ship_col.pop()
                                pOrien = self.ship_orien.pop()
                                self.p.remove_ship(pRow,pCol,size,pOrien)
        return False

    def no_adjacent_ships(self):
    	# Return true if all adjacent cells are empty
        for i in range(0,len(self.p.ships)):
            size = self.p.ships[i]
            row = self.ship_row[i]
            col = self.ship_col[i]
            orien = self.ship_orien[i]
            if orien == 0:
                if self.p.get_node(row,col+size) != self.p.empty:
                    return False
                if self.p.get_node(row,col-1) != self.p.empty:
                    return False
                for j in range(-1,size+1):
                        if self.p.get_node(row+1,col+j) != self.p.empty:
                            return False
                        if self.p.get_node(row-1,col+j) != self.p.empty:
                            return False
            else:
                if self.p.get_node(row+size,col) != self.p.empty:
                    return False
                if self.p.get_node(row-1,col) != self.p.empty:
                    return False
                for i in range(-1,size+1):
                        if self.p.get_node(row+i,col+1) != self.p.empty:
                            return False
                        if self.p.get_node(row+i,col-1) != self.p.empty:
                            return False
        return True
