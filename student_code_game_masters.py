from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        peg_list = ["peg1", "peg2", "peg3"]
        peg_disk_list = []
        for pegs in peg_list:
            ask1 = parse_input("fact: (on ?x "+pegs+")")
            disks_helper = self.kb.kb_ask(ask1)
            disk_helper = str(disks_helper)
            disk_ints = []
            peg_disk = []
            temp_disk_list = []
            disk_list = []
            final_d_list = []
            if disk_helper != False:
                temp_disk_list = disk_helper.split()
                for strin in temp_disk_list:
                    if strin == "disk1":
                        disk_list.append("1")
                    elif strin == "disk2":
                        disk_list.append("2")
                    elif strin == "disk3":
                        disk_list.append("3")
                    elif strin == "disk4":
                        disk_list.append("4")
                    elif strin == "disk5":
                        disk_list.append("5")
                for num in disk_list:
                    if final_d_list.__contains__(num) == False:
                        final_d_list.append(num)
                    

            if final_d_list.__len__() > 0:
                for disks in final_d_list:
                    disk_ints.append(int(disks))
                disk_ints.sort()
            peg_disk_list.append(tuple(disk_ints))
        return(tuple(peg_disk_list))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        statement = movable_statement
        move_disk = str(statement.terms[0])
        curr_peg = str(statement.terms[1])
        to_peg = str(statement.terms[2])

        # question_above = parse_input("fact: (above " + move_disk + ") + ?y")
        # disks_below = self.kb.kb_ask(question_above)
        # disks_below_string = str(disks_below)
        # disks_below = disks_below_string.split()

        # if disks_below.__len__ == 0:
        #     current_peg = False
        # else:
        #     current_peg = True
        
        statement_new_destination_ask = parse_input("fact: (empty " + to_peg +")")
        statement_new_destination_empty = self.kb.kb_ask(statement_new_destination_ask)
        if statement_new_destination_empty == False:
            move_to_peg = False
        else:
            move_to_peg = True
        
        
        if move_to_peg == False:
            #means that there is a peg where we are moving to
            # find_what_peg = parse_input("fact: (on "+ move_disk + " ?x)")
            # which_peg = kb.kb_ask(find_what_peg)
            # old_pegs_new_top_fact =  parse_input("fact: (onTopOf "+ move_disk +" "+curr_below+")")
            #could be used now retract_on = parse_input("fact: (onTopOf "+ move_disk +" "+curr_below+")")
            move_to_current_top_ask = parse_input("fact: (top ?x " + to_peg + ")")
            move_to_current_top = self.kb.kb_ask(move_to_current_top_ask)
            current_top_disk = str(move_to_current_top[0].bindings[0].constant)
            question_is_current_top_smaller_than_moving_disk_ask = parse_input("fact: (lessThan "+move_disk+" "+current_top_disk+")")
            question_is_current_top_smaller_than_moving_disk = self.kb.kb_ask(question_is_current_top_smaller_than_moving_disk_ask)
            if question_is_current_top_smaller_than_moving_disk == False:
                return
            remove_disk_from_top = parse_input("fact: (top "+current_top_disk+ " " + to_peg + ")")
            self.kb.kb_remove(remove_disk_from_top)
           

            #this stuff isnt needed because I forgot it was already a legal move
            #new_ask = parse_input("fact: (largerthan " + move_disk + curr_top_disk + ")")
            #move_to_curr_top_question = self.kb.kb_ask(new_ask)
            #if move_to_curr_top_question == False:
        
        retract_on = parse_input("fact: (on "+ move_disk +" "+ curr_peg+")")    
        retract_top = parse_input("fact: (top "+ move_disk +" "+curr_peg+")")
        old_pegs_new_top_ask =  parse_input("fact: (onTopOf "+ move_disk +" ?x)")
        old_pegs_new_top_fact = self.kb.kb_ask(old_pegs_new_top_ask)
        old_pegs_new_top = str(old_pegs_new_top_fact[0].bindings[0].constant)
        adding_old_new_top_statement = parse_input("fact: (top "+ old_pegs_new_top +" "+curr_peg+")")

        self.kb.kb_retract(retract_top)
        self.kb.kb_retract(retract_on)
        self.kb.kb_assert(adding_old_new_top_statement)


        final_move_top = parse_input("fact: (top "+ move_disk +" "+to_peg+")")
        final_move_on = parse_input("fact: (on "+ move_disk +" "+to_peg+")")
        self.kb.kb_assert(final_move_on)
        #final_move_on = will be a series to see what it should be on top off
        self.kb.kb_assert(final_move_top)
        #current problem is that you arent setting the new one as the top

        # for bfs, go up to required next state, you need the previous game state to know that you can reach that move, thats the first condition, the second condition is going going to the next sibling, you can move from a parent to a sibling, if the those nodes have children, you can populate the tree with its children, 
        # go up to find required next state, 
        # go to sibling 
        # go down and add required node

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        x_coor = ["pos1", "pos2", "pos3"]
        y_coor = ["pos1", "pos2", "pos3"]
        tile_list_final = []
        for y in y_coor:
            list_helper = []
            for x in x_coor:
                ask1 = parse_input("fact: (coordinate ?x " + x +" "+y+")")
                tile_helper = self.kb.kb_ask(ask1)
                tile_string = str(tile_helper[0].bindings[0].constant)
                if tile_string == "empty":
                    list_helper.append(-1)
                else:
                    list_helper.append(int(tile_string[4]))
            tile_list_final.append(tuple(list_helper))
        return tuple(tile_list_final)
            

        
    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        statement = movable_statement
        move_disk = str(statement.terms[0])
        curr_x = str(statement.terms[1])
        curr_y = str(statement.terms[2])
        move_x = str(statement.terms[3])
        move_y = str(statement.terms[4])

        adjacent_tile_ask = parse_input("fact: (coordinate ?x "+ move_x + " "+move_y+")")
        adjacent_tile = self.kb.kb_ask(adjacent_tile_ask)
        name_of_adjacent_tile = str(adjacent_tile[0].bindings[0].constant)
        if name_of_adjacent_tile == "empty":
            value_x = int(curr_x[3])
            value_y = int(curr_y[3])
            x_lister = [value_x - 1, value_x, value_x + 1]
            y_lister = [value_y - 1, value_y, value_y + 1]
            list_of_adj = []
            for x in x_lister:
                for y in y_lister:
                    ad_q = parse_input("fact: (coordinate ?x pos" +str(x) + " pos"+str(y) +")")
                    result_ask = self.kb.kb_ask(ad_q)
                    if result_ask != False:
                        result = str(result_ask[0].bindings[0].constant)
                        list_of_adj.append(result)
            for adj in list_of_adj:
                remove_q_1 = parse_input("fact: (adjancent " + move_disk +" "+ adj+")")
                remove_q_2 = parse_input("fact: (adjancent " + adj +" "+ move_disk+")")
                remove_1 = self.kb.kb_ask(remove_q_1)
                remove_2 = self.kb.kb_ask(remove_q_2)
                if remove_1 != False:
                    self.kb.kb_remove(remove_1)
                if remove_2 != False:
                    self.kb.kb_remove(remove_2)
            #need to remove empty
            #need to remove current
            #need to place current
            #need to place empty

            empty_fact_remove = parse_input("fact: (coordinate empty "+move_x+" "+move_y+")")
            self.kb.kb_remove(empty_fact_remove)
            non_empty_remove = parse_input("fact: (coordinate "+move_disk+ " "+curr_x+" "+curr_y+")")
            self.kb.kb_remove(non_empty_remove)
            non_empty_assert = parse_input("fact: (coordinate "+move_disk+ " "+move_x+" "+move_y+")")
            self.kb.kb_assert(non_empty_assert)
            empty_assert = parse_input("fact: (coordinate empty "+curr_x+" "+curr_y+")")
            self.kb.kb_assert(empty_assert)

        # question_above = parse_input("fact: (above " + move_disk + ") + ?y")
        # disks_below = self.kb.kb_ask(question_above)
        # disks_below_string = str(disks_below)
        # disks_below = disks_below_string.split()

        # if disks_below.__len__ == 0:
        #     current_peg = False
        # else:
        #     current_peg = True
        
        

         
    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
