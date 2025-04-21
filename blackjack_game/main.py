import pygame
import random
import os
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
CARD_WIDTH = 100
CARD_HEIGHT = 145
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
GOLD = (218, 165, 32)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("BlackJack")
clock = pygame.time.Clock()

class Card:
    def __init__(self, suit: str, value: str, score: int):
        self.suit = suit
        self.value = value
        self.score = score
        self.image = None
        self.load_image()
    
    def load_image(self):
        # In una versione futura, caricheremo immagini reali delle carte
        self.image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.image.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render(f"{self.value}{self.suit}", True, BLACK)
        text_rect = text.get_rect(center=(CARD_WIDTH/2, CARD_HEIGHT/2))
        self.image.blit(text, text_rect)
        pygame.draw.rect(self.image, BLACK, (0, 0, CARD_WIDTH, CARD_HEIGHT), 2)

class Deck:
    def __init__(self):
        self.cards = []
        self.build()
    
    def build(self):
        suits = ['♠', '♣', '♥', '♦']
        values = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                 '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
        for suit in suits:
            for value, score in values.items():
                self.cards.append(Card(suit, value, score))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self) -> Card:
        return self.cards.pop()

class Hand:
    def __init__(self, bet: int):
        self.cards: List[Card] = []
        self.value = 0
        self.aces = 0
        self.bet = bet
        self.can_double = True
        self.is_done = False
    
    def add_card(self, card: Card):
        self.cards.append(card)
        self.value += card.score
        if card.value == 'A':
            self.aces += 1
        
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
    
    def can_split(self) -> bool:
        return len(self.cards) == 2 and self.cards[0].value == self.cards[1].value

class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hands: List[Hand] = []
        self.current_hand_index = 0
        self.dealer_hand = Hand(0)  # Dealer doesn't bet
        self.game_over = False
        self.player_turn = True
        self.base_bet = 100
        self.player_money = 1000
        self.message = ""
        self.insurance_available = False
        self.insurance_bet = 0
        self.show_options = True
    
    def deal_initial_cards(self):
        initial_hand = Hand(self.base_bet)
        self.player_hands = [initial_hand]
        self.player_money -= self.base_bet
        
        # Deal initial cards
        for _ in range(2):
            self.player_hands[0].add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())
        
        # Check if insurance is available (dealer's up card is an Ace)
        if self.dealer_hand.cards[1].value == 'A':
            self.insurance_available = True
    
    def hit(self):
        if self.player_turn and not self.game_over and not self.player_hands[self.current_hand_index].is_done:
            current_hand = self.player_hands[self.current_hand_index]
            current_hand.add_card(self.deck.deal())
            current_hand.can_double = False
            
            if current_hand.value > 21:
                current_hand.is_done = True
                if self.current_hand_index < len(self.player_hands) - 1:
                    self.current_hand_index += 1
                else:
                    self.end_hand("Hai sballato!")
    
    def stand(self):
        if self.player_turn and not self.game_over:
            current_hand = self.player_hands[self.current_hand_index]
            current_hand.is_done = True
            
            if self.current_hand_index < len(self.player_hands) - 1:
                self.current_hand_index += 1
            else:
                self.player_turn = False
                self.dealer_play()
    
    def double_down(self):
        current_hand = self.player_hands[self.current_hand_index]
        if current_hand.can_double and self.player_money >= current_hand.bet and len(current_hand.cards) == 2:
            self.player_money -= current_hand.bet
            current_hand.bet *= 2
            self.hit()
            if not self.game_over:
                self.stand()
    
    def split(self):
        current_hand = self.player_hands[self.current_hand_index]
        if current_hand.can_split() and self.player_money >= current_hand.bet:
            # Create new hand with second card
            new_hand = Hand(current_hand.bet)
            self.player_money -= current_hand.bet
            new_hand.add_card(current_hand.cards.pop())
            
            # Add a card to each hand
            current_hand.add_card(self.deck.deal())
            new_hand.add_card(self.deck.deal())
            
            # Insert new hand after current hand
            self.player_hands.insert(self.current_hand_index + 1, new_hand)
    
    def insurance(self):
        if self.insurance_available and self.player_money >= self.base_bet // 2:
            self.insurance_bet = self.base_bet // 2
            self.player_money -= self.insurance_bet
            self.insurance_available = False
            
            # Check if dealer has BlackJack
            if self.dealer_hand.cards[0].value in ['10', 'J', 'Q', 'K']:
                self.player_money += self.insurance_bet * 3
                self.end_game("Assicurazione vinta! Dealer ha BlackJack!")
    
    def dealer_play(self):
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal())
        
        # Compare dealer's hand with all player hands
        all_bust = True
        for hand in self.player_hands:
            if hand.value <= 21:
                all_bust = False
                break
        
        if all_bust:
            self.end_game("Tutte le mani hanno sballato! Dealer vince!")
        elif self.dealer_hand.value > 21:
            self.end_game("Il dealer ha sballato! Hai vinto!")
        else:
            # Check each hand
            results = []
            for i, hand in enumerate(self.player_hands):
                if hand.value > 21:
                    results.append(f"Mano {i+1}: Sballato")
                elif hand.value > self.dealer_hand.value:
                    results.append(f"Mano {i+1}: Vinto (${hand.bet * 2})")
                    self.player_money += hand.bet * 2
                elif hand.value < self.dealer_hand.value:
                    results.append(f"Mano {i+1}: Perso")
                else:
                    results.append(f"Mano {i+1}: Pareggio (${hand.bet})")
                    self.player_money += hand.bet
            
            self.end_game("\n".join(results))
    
    def end_hand(self, message: str):
        if self.current_hand_index < len(self.player_hands) - 1:
            self.current_hand_index += 1
        else:
            self.player_turn = False
            self.dealer_play()
    
    def end_game(self, message: str):
        self.game_over = True
        self.message = message
        self.show_options = False

    def draw(self):
        screen.fill(GREEN)
        
        # Draw dealer's cards
        for i, card in enumerate(self.dealer_hand.cards):
            if i == 0 and self.player_turn:
                pygame.draw.rect(screen, RED, (50 + i * (CARD_WIDTH + 10), 50, CARD_WIDTH, CARD_HEIGHT))
            else:
                screen.blit(card.image, (50 + i * (CARD_WIDTH + 10), 50))
        
        # Draw player's hands
        for hand_index, hand in enumerate(self.player_hands):
            y_offset = WINDOW_HEIGHT - 200 - (hand_index * (CARD_HEIGHT + 20))
            # Highlight current hand
            if hand_index == self.current_hand_index and self.player_turn:
                pygame.draw.rect(screen, YELLOW, 
                               (40, y_offset - 5, len(hand.cards) * (CARD_WIDTH + 10) + 20, CARD_HEIGHT + 10),
                               2)
            
            for i, card in enumerate(hand.cards):
                screen.blit(card.image, (50 + i * (CARD_WIDTH + 10), y_offset))
            
            # Draw hand value and bet
            font = pygame.font.Font(None, 36)
            hand_text = font.render(f"Mano {hand_index + 1}: {hand.value} (${hand.bet})", True, WHITE)
            screen.blit(hand_text, (50 + (len(hand.cards) + 1) * (CARD_WIDTH + 10), y_offset + CARD_HEIGHT//2))
        
        # Draw scores and messages
        font = pygame.font.Font(None, 36)
        if not self.player_turn or self.game_over:
            dealer_text = font.render(f"Dealer: {self.dealer_hand.value}", True, WHITE)
        else:
            dealer_text = font.render("Dealer: ?", True, WHITE)
        screen.blit(dealer_text, (50, 20))
        
        money_text = font.render(f"Soldi: ${self.player_money}", True, GOLD)
        screen.blit(money_text, (WINDOW_WIDTH - 200, 20))
        
        # Draw game options
        if self.show_options and self.player_turn and not self.game_over:
            current_hand = self.player_hands[self.current_hand_index]
            options_y = WINDOW_HEIGHT - 60
            
            hit_text = font.render("H - Carta", True, WHITE)
            stand_text = font.render("S - Stai", True, WHITE)
            screen.blit(hit_text, (50, options_y))
            screen.blit(stand_text, (200, options_y))
            
            if current_hand.can_double and self.player_money >= current_hand.bet:
                double_text = font.render("D - Raddoppia", True, WHITE)
                screen.blit(double_text, (350, options_y))
            
            if current_hand.can_split() and self.player_money >= current_hand.bet:
                split_text = font.render("P - Dividi", True, WHITE)
                screen.blit(split_text, (550, options_y))
            
            if self.insurance_available and self.player_money >= self.base_bet // 2:
                insurance_text = font.render("I - Assicurazione", True, WHITE)
                screen.blit(insurance_text, (750, options_y))
        
        if self.game_over:
            lines = self.message.split('\n')
            for i, line in enumerate(lines):
                message_text = font.render(line, True, WHITE)
                screen.blit(message_text, (WINDOW_WIDTH//2 - message_text.get_width()//2, 
                                         WINDOW_HEIGHT//2 + i * 30))
            restart_text = font.render("Premi R per ricominciare", True, WHITE)
            screen.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, 
                                     WINDOW_HEIGHT//2 + len(lines) * 30 + 20))
        
        pygame.display.flip()

def main():
    game = Game()
    game.deal_initial_cards()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_h:  # Hit
                    game.hit()
                elif event.key == pygame.K_s:  # Stand
                    game.stand()
                elif event.key == pygame.K_d:  # Double Down
                    game.double_down()
                elif event.key == pygame.K_p:  # Split
                    game.split()
                elif event.key == pygame.K_i:  # Insurance
                    game.insurance()
            elif event.type == pygame.KEYDOWN and game.game_over:
                if event.key == pygame.K_r:  # Restart
                    game = Game()
                    game.deal_initial_cards()
        
        game.draw()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main() 