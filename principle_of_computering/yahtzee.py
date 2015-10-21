"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:            
            for item in range(1, outcomes + 1):
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    max_score = 0
    current_value = 0
    for element1 in hand:
        current_value = element1
        tmp_max_score = 0
        for element2 in hand:
            if element2 == current_value:
                tmp_max_score += element2
        if tmp_max_score > max_score:
            max_score = tmp_max_score
    
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    value_of_held_dice = 0
    if len(held_dice) > 0:       
        value_of_held_dice = held_dice[0]       
        
    expected = 0
    
    if value_of_held_dice == 0:        
        remaining_possible_set = gen_all_sequences(num_die_sides, num_free_dice)
        for seq in remaining_possible_set:            
            expected += score(seq) * ((1. / num_die_sides) ** num_free_dice)
    else:                                              
        remaining_possible_set = gen_all_sequences(num_die_sides, num_free_dice)
        for seq in remaining_possible_set:
            current_dice = tuple(list(held_dice) + list(seq))
            expected += score(current_dice) * ((1. / num_die_sides) ** num_free_dice)
                
    return float(expected)
    
    #return 0.0

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    all_holds_set = []
    for dummy_idx in range(0, len(hand) + 1):        
        #temp = set()
        #all_sequences = gen_all_sequences(hand, dummy_idx)
        answer_set = set([()])
        for dummy_idx in range(dummy_idx):
            temp_set = set()
            for partial_sequence in answer_set:
                for item in hand:
                    sub_outcomes = list(hand)
                    for item_to_remove in partial_sequence:
                        sub_outcomes.remove(item_to_remove)
                    if item in sub_outcomes:                    
                        new_sequence = list(partial_sequence)
                        new_sequence.append(item)
                        temp_set.add(tuple(new_sequence))
            answer_set = temp_set        
        sorted_sequences = [tuple(sorted(sequence)) for sequence in answer_set]
        all_holds_set += sorted_sequences
            
    return set(all_holds_set)            

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    final_holds_decision = tuple()
    largest_expection = 0.
    tmp_largest_expection = 0.
    for hold in gen_all_holds(hand):
        tmp_largest_expection = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if tmp_largest_expection > largest_expection:
            largest_expection = tmp_largest_expection
            final_holds_decision = hold
    
    return (largest_expection, final_holds_decision)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



