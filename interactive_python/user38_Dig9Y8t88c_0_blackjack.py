# Mini-project #6 - Blackjack

#import simplegui
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Image._dir_search_first = '../tmp/'
    
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Ready to have a game of BlackJack?"
dealer_score = 0
player_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_cards = []

    def __str__(self):
        str_hand_cards = "Hand contains: "
        for card in self.hand_cards:
            str_hand_cards += card.suit + " " + card.rank + ", "
        return str_hand_cards

    def add_card(self, card):
        self.hand_cards.append(card)

    def get_value(self):
        sum_cards = 0
        has_ace = False
        for card in self.hand_cards:          
            if card.rank == "A":
                has_ace = True
            sum_cards += VALUES[card.rank]
        
        if not has_ace:
            return sum_cards
        else:
            if sum_cards + 10 <= 21:
                return sum_cards + 10
            else:
                return sum_cards
            
    def draw(self, canvas, pos):
        visible = 1
        for card in self.hand_cards:
            if visible <= 5:
                card.draw(canvas, pos)                
                pos[0] += CARD_SIZE[0] + 20
                visible += 1
                           
        
# define deck class 
class Deck:
    
    def __init__(self):        
        self.deck_cards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck_cards.append(card)        
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_cards)

    def deal_card(self):
        return self.deck_cards.pop()
    
    def __str__(self):
        str_deck_cards = "Deck contains: "        
        for card in self.deck_cards:
            str_deck_cards += card.suit + card.rank + " "
        return str_deck_cards        


#define event handlers for buttons
def deal():    
    global outcome, in_play, dealer_score, player_score
    global deck, dealer_hand, player_hand

    if in_play:
        dealer_score += 1
    
    # your code goes here
    outcome = "Hit or Stand?"
    deck = Deck()  
    deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    #print "Dealer "+ str(dealer_hand)
    #print "Player "+ str(player_hand)
    
    in_play = True

def hit(): 
    global outcome, in_play, dealer_score, player_score
    global deck, player_hand
    
    if not in_play:
        return None
    
    # if the hand is in play, hit the player    
    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
    #print "Player "+ str(player_hand) + " = " + str(player_hand.get_value())
    
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        in_play = False
        dealer_score += 1
        outcome = "Try Again???"        
        
def stand():   
    global outcome, in_play, dealer_score, player_score
    global deck, dealer_hand, player_hand
    
    if not in_play:
        return None
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while in_play and dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
    #print "Dealer "+ str(dealer_hand) + " = " + str(dealer_hand.get_value())

    # assign a message to outcome, update in_play and score
    if dealer_hand.get_value() > 21:                
        outcome = "Try Again???"
        in_play = False
        player_score += 1            
    else:
        if dealer_hand.get_value() >= player_hand.get_value():
            in_play = False
            outcome = "Try Again???"
            dealer_score += 1
        else:
            in_play = False
            outcome = "Try Again???"
            player_score += 1            
        
# draw handler    
def draw(canvas):
    global in_play, dealer_score, player_score
    global dealer_hand, player_hand
        
    if outcome != "Ready to have a game of BlackJack?":            
        canvas.draw_text(outcome, [210, 400], 40, "Yellow")        
        canvas.draw_text("Dealer's score: "+str(dealer_score), [215, 200], 30, "Pink")
        canvas.draw_text("Your score: "+str(player_score), [230, 465], 30, "Pink")
        dealer_hand.draw(canvas, [80, 70])
        player_hand.draw(canvas, [80, 480])
        if in_play:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [80 + CARD_BACK_CENTER[0], 70 + CARD_BACK_CENTER[1]], CARD_SIZE)            
        elif dealer_hand.get_value() <= 21 and player_hand.get_value() <= 21:
            if dealer_hand.get_value() >= player_hand.get_value():          
                canvas.draw_text("Dealer wins the game!", [180, 340], 30, "Yellow")                                
            else:
                canvas.draw_text("You win the game!", [200, 340], 30, "Yellow")                          
        if player_hand.get_value() > 21:
            canvas.draw_text("You have busted. Dealer wins the game!", [70, 340], 30, "Yellow")
        if dealer_hand.get_value() > 21:
            canvas.draw_text("Dealer has busted. You win the game!", [80, 340], 30, "Yellow")                
    else:
        canvas.draw_text(outcome, [90, 300], 30, "Blue")
        canvas.draw_text("Please click 'Deal' to start a new game.", [80, 340], 30, "Blue")
        
    canvas.draw_text("= BLACKJACK =", [190, 30], 30, "Black")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
label = frame.add_label('')
label = frame.add_label('ATTENTION:')
label = frame.add_label('if the "Deal" button is clicked during the middle of a round, the program will report that the player lost the round')
frame.set_draw_handler(draw)


# get things rolling
#deal()
frame.start()


# remember to review the gradic rubric
