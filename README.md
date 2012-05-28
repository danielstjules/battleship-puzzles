battleship-puzzles
==================

Brief Overview
-------------------------

Classes and algorithms I wrote to solve Battleship Solitaire, 
an NP-Complete problem. Puzzles are displayed using the following
format:

	  2 0 2 1 3 2 0 
	0 - - - - - - - 
	2 - - o - o - - 
	1 - - o - - - - 
	1 o - - - - - - 
	2 - - - - o o - 
	0 - - - - - - - 
	4 o - - o o o - 
	n: 7 m: 7
	battleships: 0
	cruisers: 1
	destroyers: 2
	submarines: 3

The code I wrote does not use hints like the "Fathom it!" variation 
does. The backtracking solutions are completely ineffective at solving 
any reasonable number of instances using a board size greater than 7. 
Without pruning, even less so.

Using backtracking with pruning to solve 50 instances of a 7x7 configuration 
with 1 cruiser, 2 destroyers, and 3 submarines, it averaged 78.385s per instance, 
with a minimum of 0.0017s, and a maximum of 1667.682s. 

Naive backtracking proved to be completely useless, and the first-fit heuristic 
only manages an 80.72% accuracy with a 5x5 board. This sharply drops to 29.07% 
with the 6x6 puzzle configuration I chose. 

Example Use
-------------------------

	import puzzle
	import backtracking_pruning
	
    x = puzzle.Puzzle(7,7,0,1,2,3,0)
    x.print_solution()
    backtracking_pruning.BacktrackingPruning(x)    
    x.print_alg_solution()
    
