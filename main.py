import pygame
import library
import draw
import random
import csv
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BROWN = (70, 50, 30)
LIGHT_BROWN = (150, 100, 70)
CREAM = (245, 245, 220)
GOLD = (255, 215, 0)
RED = (220, 50, 50)
GREEN = (50, 180, 50)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Little Pizza House")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "playing"  # playing, pause, upgrade, game_over
        
        # Game objects
        self.restaurant = library.Restaurant()
        self.manager = library.ManagerCustomers()
        self.current_order = None
        self.player_pizza = None
        self.player_drink = None
        self.day = 1
        self.orders_completed = 0
        self.orders_failed = 0
        self.customer_index = 0
        self.customer_image = None
        self.customer_image_files = draw.get_customer_image_files()
        
        # CSV file for stats - save to collecting_data folder
        data_folder = os.path.join(os.path.dirname(__file__), "collecting_data")
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        self.csv_filename = os.path.join(data_folder, f"pizza_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        self.init_csv()
        
    def init_csv(self):
        """Initialize CSV file for data recording"""
        with open(self.csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Day', 'OrderID', 'ItemPrice', 'ToppingsUsed', 'DrinkType', 'OrderAccuracy', 'TimeTaken'])
    
    def cleanup_empty_csv(self):
        """Delete CSV file if it only contains the header and no data"""
        try:
            if os.path.exists(self.csv_filename):
                with open(self.csv_filename, 'r') as f:
                    lines = f.readlines()
                # If only 1 line (header), delete the file
                if len(lines) <= 1:
                    os.remove(self.csv_filename)
        except Exception as e:
            pass  # Silently ignore errors during cleanup
    
    def next_customer(self):
        """Load next customer's order"""
        if self.customer_index < len(self.manager.orders_per_day):
            self.current_order = self.manager.orders_per_day[self.customer_index]
            # Generate random order items for this customer
            self.generate_random_order(self.current_order)
            # Select random customer image
            if self.customer_image_files:
                random_image_file = random.choice(self.customer_image_files)
                self.customer_image = draw.load_customer_image(random_image_file, 250, 350)
            self.customer_index += 1
            self.player_pizza = None
        else:
            # Day complete - go to upgrade screen
            self.game_state = "upgrade"
    
    def start_next_day(self):
        """Initialize the next day"""
        self.day += 1
        self.orders_completed = 0
        self.orders_failed = 0
        self.customer_index = 0
        self.player_pizza = None
        self.player_drink = None
        self.current_order = None
        self.customer_image = None
        self.game_state = "playing"
        self.next_customer()
    
    def generate_random_order(self, order):
        """Generate random pizza and drink for customer"""
        order.lst_order = []
        
        # Random pizza - no duplicate toppings
        pizza = library.Pizza()
        num_toppings = random.randint(1, 3)
        selected_toppings = []
        
        while len(selected_toppings) < num_toppings:
            topping = random.choice(self.restaurant.topping_lst)
            # Only add if not already selected
            if topping.name not in [t.name for t in selected_toppings]:
                selected_toppings.append(topping)
                pizza.pizza_lst.append(topping)
        
        pizza.cal_topping()
        order.lst_order.append(pizza)
        
        # Random drink
        drink = random.choice(self.restaurant.drinks_lst)
        order.lst_order.append(drink)
    
    def create_player_pizza(self):
        """Start creating a new pizza"""
        self.player_pizza = library.Pizza()
    
    def add_topping_to_pizza(self, topping_index):
        """Add topping to player's pizza"""
        if self.player_pizza is not None:
            topping = self.restaurant.topping_lst[topping_index]
            # Check if topping already exists on pizza
            topping_names = [t.name for t in self.player_pizza.pizza_lst]
            if topping.name not in topping_names:
                self.restaurant.topping_lst[topping_index].add_topping(self.player_pizza)
                self.player_pizza.cal_topping()
    
    def add_drink_to_order(self, drink_index):
        """Add drink to current order"""
        if self.current_order is not None:
            drink = self.restaurant.drinks_lst[drink_index]
            drink.add_drink(self.current_order)
            self.player_drink = drink
    
    def is_order_correct(self):
        """Check if player's order matches customer's order exactly"""
        if not self.current_order or self.player_pizza is None or self.player_drink is None:
            return False
        
        pizza_match = False
        drink_match = False
        
        # Check if pizza and drink match customer's order
        for item in self.current_order.lst_order:
            if isinstance(item, library.Pizza):
                if item == self.player_pizza:
                    pizza_match = True
            elif isinstance(item, library.Drink):
                if item.name == self.player_drink.name:
                    drink_match = True
        
        return pizza_match and drink_match
    
    def check_order(self):
        """Check if player's order matches customer's order and process it"""
        if not self.is_order_correct():
            return False
        
        # Order is correct - award money and complete the order
        money_earned = self.player_pizza.pizza_price + self.player_drink.price
        self.restaurant.money += money_earned
        self.orders_completed += 1
        
        # Record to CSV
        self.record_order_stats(self.player_pizza.pizza_price)
        
        # Reset for next customer
        self.player_pizza = None
        self.player_drink = None
        self.current_order = None
        self.next_customer()
        return True
    
    def record_order_stats(self, price):
        """Record order statistics to CSV"""
        toppings_count = len(self.player_pizza.pizza_lst) if self.player_pizza else 0
        drink_type = self.player_drink.name if self.player_drink else "None"
        
        with open(self.csv_filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.day,
                self.orders_completed + self.orders_failed,
                price,
                toppings_count,
                drink_type,
                "Correct",
                random.randint(10, 60)  # Placeholder for time taken
            ])
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # Pizza creation
                if event.key == pygame.K_p:
                    self.create_player_pizza()
                
                # Submit order
                if event.key == pygame.K_RETURN:
                    self.check_order()
            
            # Mouse click handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                # Check topping button clicks (center, 3 per row, 2 rows)
                topping_x_start = SCREEN_WIDTH//2 - 90
                topping_y_start = SCREEN_HEIGHT//2 + 80
                topping_width = 180
                topping_height = 70
                topping_row_spacing = 80
                topping_col_spacing = 210
                
                for row in range(2):
                    for col in range(3):
                        idx = row * 3 + col
                        if idx < 6:
                            topping_x = topping_x_start + (col * topping_col_spacing)
                            topping_y = topping_y_start + (row * topping_row_spacing)
                            if topping_x < mouse_x < topping_x + topping_width and topping_y < mouse_y < topping_y + topping_height:
                                if self.player_pizza:
                                    self.add_topping_to_pizza(idx)
                
                # Check drink button clicks (left side, 2 per row)
                drink_x_start = 20
                drink_y_start = SCREEN_HEIGHT//2 + 80
                drink_width = 180
                drink_height = 70
                drink_row_spacing = 80
                drink_col_spacing = 220
                
                for row in range(2):
                    for col in range(2):
                        idx = row * 2 + col
                        if idx < 4:
                            drink_x = drink_x_start + (col * drink_col_spacing)
                            drink_y = drink_y_start + (row * drink_row_spacing)
                            if drink_x < mouse_x < drink_x + drink_width and drink_y < mouse_y < drink_y + drink_height:
                                self.add_drink_to_order(idx)
                
                # Check "New Pizza" button (center top)
                if SCREEN_WIDTH//2 - 70 < mouse_x < SCREEN_WIDTH//2 + 70 and 20 < mouse_y < 55:
                    self.create_player_pizza()
            
            # Handle upgrade screen clicks
            if self.game_state == "upgrade" and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                # Check topping upgrade buttons (left side)
                topping_y = 200
                for i in range(len(self.restaurant.topping_lst)):
                    button_x = 50
                    button_y = topping_y
                    button_width = 500
                    button_height = 50
                    
                    if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                        self.restaurant.upgrade_topping(i)
                    
                    topping_y += 60
                
                # Check drink upgrade buttons (right side)
                drink_y = 200
                for i in range(len(self.restaurant.drinks_lst)):
                    button_x = SCREEN_WIDTH//2 + 50
                    button_y = drink_y
                    button_width = 500
                    button_height = 50
                    
                    if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                        self.restaurant.upgrade_drink(i)
                    
                    drink_y += 60
                
                # Check Continue button
                continue_x = SCREEN_WIDTH//2 - 75
                continue_y = SCREEN_HEIGHT - 80
                continue_width = 150
                continue_height = 50
                
                if continue_x < mouse_x < continue_x + continue_width and continue_y < mouse_y < continue_y + continue_height:
                    self.start_next_day()
    
    def update(self):
        """Update game state"""
        pass
    
    def draw(self):
        """Draw game"""
        self.screen.fill(CREAM)
        
        # Draw background
        draw.draw_kitchen_background(self.screen)
        
        # Draw restaurant state
        draw.draw_stats(self.screen, self.restaurant.money, self.orders_completed, self.day)
        
        if self.game_state == "upgrade":
            # Draw upgrade screen
            draw.draw_upgrade_screen(self.screen, self.restaurant, self.restaurant.money)
        else:
            # Draw current order
            if self.current_order:
                draw.draw_customer_order(self.screen, self.current_order)
            
            # Draw customer image
            if self.customer_image:
                draw.draw_customer_image(self.screen, self.customer_image)
            
            # Draw player's pizza
            if self.player_pizza:
                draw.draw_player_pizza(self.screen, self.player_pizza, self.player_drink)
            
            # Draw topping and drink options
            draw.draw_topping_options(self.screen, self.restaurant.topping_lst)
            draw.draw_drink_options(self.screen, self.restaurant.drinks_lst)
            
            # Draw hint text
            draw.draw_hint_text(self.screen)
        
        # Draw instructions
        draw.draw_controls(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        self.next_customer()
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Clean up empty CSV files
        self.cleanup_empty_csv()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()