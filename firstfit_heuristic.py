import puzzle

class FirstfitHeuristic:
    
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
        self.answer = self.run()

    def run(self):
        for i in range(len(self.ships_to_place)):
            size = self.ships_to_place[i]
            l = self.firstFit(size)
            if l == []:
                return False
            else:
                row = l[0]
                col = l[1]
                orien = l[2]
                placed = self.p.place_ship(row,col,size,orien)
                if placed == True:
                    self.update_totals(0,row,col,size,orien)
                    self.ship_row.append(row)
                    self.ship_col.append(col)
                    self.ship_orien.append(orien)
                else:
                    return False
        if(self.p.respects_indicators() == False):
            return False
        return True

    def firstFit(self,size):
        for row in range(0,self.p.m):
            for col in range(0,self.p.n):
                for orien in range(0,2):
                    if self.p.row_totals[row] == 0:
                        break
                    elif self.p.column_totals[col] == 0:
                        break
                    valid = True
                    empty = self.p.empty_nodes(row,col,size,orien)
                    if empty == False:
                        valid = False
                    else:
                        adjacent = self.p.adjacent_nodes(row,col,size,orien)
                        if adjacent == True:
                            valid = False
                        if adjacent == False:
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
                        return [row,col,orien]
        return []
    
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
            