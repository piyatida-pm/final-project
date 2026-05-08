import pygame
import library
import draw
import random
import csv
import os
from datetime import datetime

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Sound path
SOUND_PATH = os.path.join(os.path.dirname(__file__), "sound")

def load_sound(filename):
    """Load a sound file safely"""
    filepath = os.path.join(SOUND_PATH, filename)
    try:
        if os.path.exists(filepath):
            return pygame.mixer.Sound(filepath)
    except:
        pass
    return None

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
        self.game_state = "playing"  # playing, upgrade, stats
        self.prev_game_state = "playing"
        
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
        
        # Sound effects
        self.sound_add_topping = load_sound("add_topping.mp3")
        self.sound_add_topping2 = load_sound("add_topping2.mp3")
        self.sound_add_drink = load_sound("add_drink.mp3")
        self.sound_create_pizza = load_sound("create_new_pizza.mp3")
        self.sound_send_order = load_sound("send_order.mp3")
        self.sound_upgrade = load_sound("upgrade.mp3")
        self.sound_end_day = load_sound("end_day.mp3")
        self.sound_music = load_sound("game_music.mp3")
        self.topping_sound_count = 0
        self.sound_enabled = True  # Track sound on/off state
        
        # CSV file for stats - save to collecting_data folder
        self.data_folder = os.path.join(os.path.dirname(__file__), "collecting_data")
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        self.csv_filename = os.path.join(self.data_folder, f"pizza_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        self.cached_stats = None
        self.stats_tab = 0
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
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            # Resume music if it was playing
            if self.sound_music:
                self.sound_music.play(-1)
        else:
            # Stop all sounds
            pygame.mixer.stop()
    
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
        if self.sound_enabled and self.sound_end_day:
            self.sound_end_day.play()
        
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
        if self.sound_enabled and self.sound_create_pizza:
            self.sound_create_pizza.play()
    
    def add_topping_to_pizza(self, topping_index):
        """Add topping to player's pizza"""
        if self.player_pizza is not None:
            topping = self.restaurant.topping_lst[topping_index]
            # Check if topping already exists on pizza
            topping_names = [t.name for t in self.player_pizza.pizza_lst]
            if topping.name not in topping_names:
                self.restaurant.topping_lst[topping_index].add_topping(self.player_pizza)
                self.player_pizza.cal_topping()
                
                # Play alternating topping sounds
                if self.sound_enabled:
                    if self.topping_sound_count % 2 == 0:
                        if self.sound_add_topping:
                            self.sound_add_topping.play()
                    else:
                        if self.sound_add_topping2:
                            self.sound_add_topping2.play()
                self.topping_sound_count += 1
    
    def add_drink_to_order(self, drink_index):
        """Add drink to current order"""
        if self.current_order is not None:
            drink = self.restaurant.drinks_lst[drink_index]
            drink.add_drink(self.current_order)
            self.player_drink = drink
            
            # Play drink sound
            if self.sound_enabled and self.sound_add_drink:
                self.sound_add_drink.play()
    
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
            # Record incorrect attempt to CSV
            self.orders_failed += 1
            self._record_accuracy("Incorrect")
            return False
        
        # Play order submission sound
        if self.sound_enabled and self.sound_send_order:
            self.sound_send_order.play()
        
        # Order is correct - award money and complete the order
        money_earned = self.player_pizza.pizza_price + self.player_drink.price
        self.restaurant.money += money_earned
        self.orders_completed += 1
        
        # Record to CSV
        self.record_order_stats(self.player_pizza.pizza_price)
        self._record_accuracy("Correct")
        
        # Reset for next customer
        self.player_pizza = None
        self.player_drink = None
        self.current_order = None
        self.next_customer()
        return True
    
    def _record_accuracy(self, result):
        """Append a row recording only the accuracy outcome for this submission."""
        topping_names = ";".join(t.name for t in self.player_pizza.pizza_lst) if self.player_pizza else ""
        drink_type    = self.player_drink.name if self.player_drink else "None"
        price         = self.player_pizza.pizza_price if self.player_pizza else 0
        with open(self.csv_filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.day,
                self.orders_completed + self.orders_failed,
                price,
                topping_names,
                drink_type,
                result,
                random.randint(10, 60)
            ])

    def record_order_stats(self, price):
        """Record order statistics to CSV"""
        topping_names = ";".join(t.name for t in self.player_pizza.pizza_lst) if self.player_pizza else ""
        drink_type = self.player_drink.name if self.player_drink else "None"
        
        with open(self.csv_filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.day,
                self.orders_completed + self.orders_failed,
                price,
                topping_names,
                drink_type,
                "Correct",
                random.randint(10, 60)  # Placeholder for time taken
            ])
    
    def load_all_stats(self):
        """Read all CSV files in collecting_data and return aggregated stats."""
        drink_counts   = {}
        topping_counts = {}
        accuracy_counts = {}
        prices    = []
        order_ids = []
        times     = []
        global_id = 0
        try:
            for fname in sorted(os.listdir(self.data_folder)):
                if fname.endswith('.csv'):
                    fpath = os.path.join(self.data_folder, fname)
                    with open(fpath, 'r', newline='') as f:
                        for row in csv.DictReader(f):
                            global_id += 1
                            drink = row.get('DrinkType', 'Unknown')
                            drink_counts[drink] = drink_counts.get(drink, 0) + 1
                            try:
                                raw = row.get('ToppingsUsed', '')
                                for name in raw.split(';'):
                                    name = name.strip()
                                    if name and not name.isdigit():
                                        topping_counts[name] = topping_counts.get(name, 0) + 1
                            except (ValueError, KeyError):
                                pass
                            try:
                                prices.append(float(row['ItemPrice']))
                                order_ids.append(global_id)
                            except (ValueError, KeyError):
                                pass
                            try:
                                times.append(int(row['TimeTaken']))
                            except (ValueError, KeyError):
                                pass
                            accuracy = row.get('OrderAccuracy', '').strip()
                            if accuracy:
                                accuracy_counts[accuracy] = accuracy_counts.get(accuracy, 0) + 1
        except OSError:
            pass

        # ── Per-tab summary tables ─────────────────────────────────────────
        total = global_id or 1

        # Tab 0 — Drinks: rows = (Drink, Count, %)
        drink_table = [
            ("Drink", "Orders", "Share %")
        ] + [
            (name, str(cnt), f"{cnt / total * 100:.1f}%")
            for name, cnt in sorted(drink_counts.items(), key=lambda x: -x[1])
        ]

        # Tab 1 — Toppings: rows = (Topping, Orders, %)
        topping_total = sum(topping_counts.values()) or 1
        topping_table = [
            ("Topping", "Orders", "Share %")
        ] + [
            (name, str(cnt), f"{cnt / topping_total * 100:.1f}%")
            for name, cnt in sorted(topping_counts.items(), key=lambda x: -x[1])
        ]

        # Tab 2 — Price: summary statistics
        if prices:
            avg_p  = sum(prices) / len(prices)
            price_table = [
                ("Statistic", "Value"),
                ("Orders recorded",  str(len(prices))),
                ("Min price",        f"${min(prices):.2f}"),
                ("Max price",        f"${max(prices):.2f}"),
                ("Mean price",       f"${avg_p:.2f}"),
                ("Total revenue",    f"${sum(prices):.2f}"),
            ]
        else:
            price_table = [("Statistic", "Value")]

        # Tab 3 — Time: summary statistics
        if times:
            avg_t  = sum(times) / len(times)
            sorted_t = sorted(times)
            median_t = sorted_t[len(sorted_t) // 2]
            time_table = [
                ("Statistic", "Value"),
                ("Orders recorded", str(len(times))),
                ("Min time",        f"{min(times)}s"),
                ("Max time",        f"{max(times)}s"),
                ("Mean time",       f"{avg_t:.1f}s"),
                ("Median time",     f"{median_t}s"),
            ]
        else:
            time_table = [("Statistic", "Value")]

        # Tab 4 — Accuracy: pie chart data
        acc_total = sum(accuracy_counts.values()) or 1
        accuracy_table = [
            ("Result", "Count", "Share %")
        ] + [
            (name, str(cnt), f"{cnt / acc_total * 100:.1f}%")
            for name, cnt in sorted(accuracy_counts.items(), key=lambda x: -x[1])
        ]

        return {
            'drink_counts':   drink_counts,
            'topping_counts': topping_counts,
            'prices':         prices,
            'order_ids':      order_ids,
            'times':          times,
            'total_orders':   global_id,
            'drink_table':    drink_table,
            'topping_table':  topping_table,
            'price_table':    price_table,
            'time_table':     time_table,
            'accuracy_counts': accuracy_counts,
            'accuracy_table':  accuracy_table,
        }

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

                # Toggle stats screen
                if event.key == pygame.K_m:
                    if self.game_state == "stats":
                        self.game_state = self.prev_game_state
                    else:
                        self.prev_game_state = self.game_state
                        self.game_state = "stats"
                        self.cached_stats = self.load_all_stats()

                # Tab navigation for stats screen
                if self.game_state == "stats":
                    if event.key in (pygame.K_TAB, pygame.K_RIGHT):
                        self.stats_tab = (self.stats_tab + 1) % 5
                    elif event.key == pygame.K_LEFT:
                        self.stats_tab = (self.stats_tab - 1) % 5

            # Mouse click handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Stats screen tab clicks
                if self.game_state == "stats":
                    tab_w = (SCREEN_WIDTH - 32) // 5
                    if 62 <= mouse_y <= 98:
                        for i in range(5):
                            tx = 16 + i * tab_w
                            if tx <= mouse_x <= tx + tab_w - 4:
                                self.stats_tab = i
                                break

                # Gameplay clicks only fire when stats screen is not open
                if self.game_state == "stats":
                    continue

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
                
                # Check sound toggle button (bottom right)
                sound_button_width = 80
                sound_button_height = 50
                sound_button_x = SCREEN_WIDTH - sound_button_width - 20
                sound_button_y = SCREEN_HEIGHT - sound_button_height - 20
                if sound_button_x < mouse_x < sound_button_x + sound_button_width and sound_button_y < mouse_y < sound_button_y + sound_button_height:
                    self.toggle_sound()
            
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
                        if self.sound_enabled and self.sound_upgrade:
                            self.sound_upgrade.play()
                    
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
                        if self.sound_enabled and self.sound_upgrade:
                            self.sound_upgrade.play()
                    
                    drink_y += 60
                
                # Check Continue button
                continue_x = SCREEN_WIDTH//2 - 75
                continue_y = SCREEN_HEIGHT - 80
                continue_width = 150
                continue_height = 50
                
                if continue_x < mouse_x < continue_x + continue_width and continue_y < mouse_y < continue_y + continue_height:
                    self.start_next_day()
                
                # Check sound toggle button (bottom right)
                sound_button_width = 80
                sound_button_height = 50
                sound_button_x = SCREEN_WIDTH - sound_button_width - 20
                sound_button_y = SCREEN_HEIGHT - sound_button_height - 20
                if sound_button_x < mouse_x < sound_button_x + sound_button_width and sound_button_y < mouse_y < sound_button_y + sound_button_height:
                    self.toggle_sound()
    
    def update(self):
        """Update game state"""
        pass
    
    def draw(self):
        """Draw game"""
        self.screen.fill(CREAM)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw background
        draw.draw_kitchen_background(self.screen)
        
        # Draw restaurant state
        draw.draw_stats(self.screen, self.restaurant.money, self.orders_completed, self.day)
        
        # Use the underlying state when the stats overlay is active
        base_state = self.prev_game_state if self.game_state == "stats" else self.game_state

        if base_state == "upgrade":
            # Draw upgrade screen
            draw.draw_upgrade_screen(self.screen, self.restaurant, self.restaurant.money, mouse_pos)
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
            draw.draw_topping_options(self.screen, self.restaurant.topping_lst, mouse_pos)
            draw.draw_drink_options(self.screen, self.restaurant.drinks_lst, mouse_pos)
            
            # Draw hint text
            draw.draw_hint_text(self.screen)
        
        # Draw instructions
        draw.draw_controls(self.screen, mouse_pos)
        
        # Draw sound toggle button
        draw.draw_sound_toggle_button(self.screen, self.sound_enabled, mouse_pos)

        # Stats overlay (drawn on top of everything)
        if self.game_state == "stats" and self.cached_stats is not None:
            draw.draw_stats_screen(self.screen, self.cached_stats, self.stats_tab, mouse_pos)

        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        # Play background music on loop
        if self.sound_music:
            self.sound_music.play(-1)  # -1 means loop indefinitely
        
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