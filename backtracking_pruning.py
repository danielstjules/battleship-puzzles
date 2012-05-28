import puzzle

class BacktrackingPruning:
    
    answer = False
    ships_to_place = []
    ship_row = []
    ship_col = []
    ship_orien = []
    
    def __init__(self, p_instance):
        self.p = p_instance
        self.ships_to_place = p_instance.ships[:]
        self.ships_to_place.sort(reverse=True)
        self.current_row_totals = [0 for i in range(self.p.m)]
        self.current_column_totals = [0 for i in range(self.p.n)]
        self.answer = self.backtrack()

    def backtrack(self):
        if self.ships_to_place == []:
            if(self.p.respects_indicators() == False):
                return False
            return True
        for i in range(len(self.ships_to_place)):
            size = self.ships_to_place[i]
            for z in range(0, 2):
                l = self.get_choice_set(size,z)
                for j in range (0, len(l)):
                    row = l[j][0]
                    col = l[j][1]
                    placed = self.p.place_ship(row,col,size,z)
                    if placed == True:
                        self.update_totals(0,row,col,size,z)
                        self.ship_row.append(row)
                        self.ship_col.append(col)
                        self.ship_orien.append(z)
                        self.ships_to_place.pop(i)
                        result = self.backtrack()
                        if result == True:
                            return True
                        else:
                            self.ships_to_place.insert(i,size)
                            pRow = self.ship_row.pop()
                            pCol = self.ship_col.pop()
                            pZ = self.ship_orien.pop()
                            self.p.remove_ship(pRow,pCol,size,pZ)
                            self.update_totals(1,pRow,pCol,size,pZ)
        return False

    def get_choice_set(self,size,orien):
        cells = []
        for row in range(0,self.p.m):
            for col in range(0,self.p.n):
                adjacent = self.p.adjacent_nodes(row,col,size,orien)
                valid = True
                if self.p.row_totals[row] == 0:
                    valid = False
                elif self.p.column_totals[col] == 0:
                    valid = False
                elif adjacent == True:
                    valid = False
                else:
                    try:
                        if orien == 0:
                            for i in range(col, col+size):
                                if self.current_column_totals[i] + 1 > self.p.column_totals[i]:
                                    valid = False
                            if self.current_row_totals[row] + size > self.p.row_totals[row]:
                                valid = False
                        else:
                            for i in range(row, row+size):
                                if self.current_row_totals[i] + 1 > self.p.row_totals[i]:
                                    valid = False
                            if self.current_column_totals[col] + size > self.p.column_totals[col]:
                                valid = False
                    except IndexError:
                        valid = False
                if valid == True:
                    cells.append([row,col])
        return cells
    
    def update_totals(self,add_or_remove,row,col,size,orien):
        # 0 = add, else = remove
        if orien == 0:
            for i in range(col, col+size):
                if  add_or_remove == 0:
                    self.current_column_totals[i] += 1
                else:
                    self.current_column_totals[i] -= 1
            if add_or_remove == 0:
                self.current_row_totals[row] += size
            else:
                self.current_row_totals[row] -= size
        else:
            for i in range(row, row+size):
                if  add_or_remove == 0:
                    self.current_row_totals[i] += 1
                else:
                    self.current_row_totals[i] -= 1
            if add_or_remove == 0:
                self.current_column_totals[col] += size
            else:
                self.current_column_totals[col] -= size
            