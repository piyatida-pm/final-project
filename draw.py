import pygame
import library
import os

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BROWN = (70, 50, 30)
LIGHT_BROWN = (150, 100, 70)
CREAM = (245, 245, 220)
GOLD = (255, 215, 0)
RED = (200, 50, 50)
GREEN = (50, 180, 50)
GRAY = (150, 150, 150)
DARK_RED = (139, 0, 0)
ORANGE = (255, 140, 0)
LIGHT_YELLOW = (255, 255, 150)

# Font
pygame.font.init()
FONT_LARGE = pygame.font.Font(None, 48)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 24)
FONT_TINY = pygame.font.Font(None, 18)

# Asset path
ASSET_PATH = os.path.join(os.path.dirname(__file__), "asset")
CUSTOMER_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "customer_image")

# Load images
def load_image(filename, width=None, height=None):
    """Load and optionally scale an image"""
    filepath = os.path.join(ASSET_PATH, filename)
    try:
        img = pygame.image.load(filepath)
        if width and height:
            img = pygame.transform.scale(img, (width, height))
        return img
    except:
        return None

# Customer image functions
def get_customer_image_files():
    """Get list of all customer image filenames"""
    try:
        if os.path.exists(CUSTOMER_IMAGE_PATH):
            files = [f for f in os.listdir(CUSTOMER_IMAGE_PATH) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            return files
    except:
        pass
    return []

def load_customer_image(filename, width=200, height=200):
    """Load and scale a customer image"""
    filepath = os.path.join(CUSTOMER_IMAGE_PATH, filename)
    try:
        img = pygame.image.load(filepath)
        img = pygame.transform.scale(img, (width, height))
        return img
    except:
        return None

# Load all sprite assets
pizza_base = load_image("pizza.PNG", 100, 100)
topping_images = {
    "Pesto Sauce": load_image("toppesto.PNG", 100, 100) or load_image("pesto.PNG", 100, 100),
    "Mushroom": load_image("topmushroom.PNG", 100, 100) or load_image("mushroom.PNG", 100, 100),
    "Cheese": load_image("topcheese.PNG", 100, 100) or load_image("cheese.PNG", 100, 100),
    "Pepperoni": load_image("toppeperroni.PNG", 100, 100) or load_image("peperoni.PNG", 100, 100),
    "Bacon": load_image("topbacon.PNG", 100, 100) or load_image("bacon.PNG", 100, 100),
    "Pineapple": load_image("toppineapple.PNG", 100, 100) or load_image("pineapple.PNG", 100, 100),
}

topping_menu_images = {
    "Pesto Sauce": load_image("pesto.PNG", 50, 50),
    "Mushroom": load_image("mushroom.PNG", 50, 50),
    "Cheese": load_image("cheese.PNG", 50, 50),
    "Pepperoni": load_image("peperoni.PNG", 50, 50),
    "Bacon": load_image("bacon.PNG", 50, 50),
    "Pineapple": load_image("pineapple.PNG", 50, 50),
}

drink_images = {
    "Coke": load_image("coke.PNG", 100, 100),
    "Sprite": load_image("sprite.PNG", 100, 100),
    "Water": load_image("water.PNG", 100, 100),
    "Milkshake": load_image("milkshake.PNG", 100, 100),
}

def draw_kitchen_background(screen):
    """Draw the kitchen/restaurant background"""
    width, height = screen.get_size()
    
    # Main counter background
    pygame.draw.rect(screen, LIGHT_BROWN, (0, height//2, width, height//2))
    pygame.draw.line(screen, DARK_BROWN, (0, height//2), (width, height//2), 3)
    
    # Wall/upper area
    pygame.draw.rect(screen, (200, 180, 160), (0, 0, width, height//2))
    
    # Money display box
    pygame.draw.rect(screen, GOLD, (950, 20, 200, 80), 3)
    pygame.draw.rect(screen, LIGHT_YELLOW, (955, 25, 190, 70))

def draw_stats(screen, money, orders_completed, day):
    """Draw game statistics"""
    width, height = screen.get_size()
    
    # Money display
    money_text = FONT_MEDIUM.render(f"${money:.2f}", True, DARK_RED)
    screen.blit(money_text, (960, 35))
    
    label = FONT_TINY.render("Money", True, DARK_BROWN)
    screen.blit(label, (980, 70))
    
    # Orders completed
    orders_text = FONT_SMALL.render(f"Orders: {orders_completed}", True, BLACK)
    screen.blit(orders_text, (50, 20))
    
    # Day display
    day_text = FONT_SMALL.render(f"Day {day}", True, BLACK)
    screen.blit(day_text, (300, 20))

def draw_customer_order(screen, order):
    """Draw current customer's order requirements"""
    width, height = screen.get_size()
    
    # Customer order box
    pygame.draw.rect(screen, WHITE, (50, 100, 300, 200), 3)
    pygame.draw.rect(screen, LIGHT_YELLOW, (55, 105, 290, 190))
    
    # Customer name
    name_text = FONT_MEDIUM.render(f"{order.customer_name}'s Order", True, DARK_BROWN)
    screen.blit(name_text, (70, 120))
    
    # Draw order items
    y_pos = 170
    
    # Pizza details
    if order.lst_order:
        pizza = order.lst_order[0]
        pizza_text = FONT_SMALL.render("Pizza with:", True, BLACK)
        screen.blit(pizza_text, (70, y_pos))
        y_pos += 30
        
        # Draw topping names as text
        for topping in pizza.pizza_lst:
            topping_text = FONT_TINY.render(f"- {topping.name}", True, DARK_RED)
            screen.blit(topping_text, (85, y_pos))
            y_pos += 22
        
        y_pos += 10
        
        # Drink
        if len(order.lst_order) > 1:
            drink = order.lst_order[1]
            drink_text = FONT_SMALL.render(f"+ {drink.name}", True, ORANGE)
            screen.blit(drink_text, (70, y_pos))

def draw_player_pizza(screen, player_pizza, player_drink=None):
    """Draw the pizza the player is making"""
    width, height = screen.get_size()
    
    # Player pizza box
    pygame.draw.rect(screen, WHITE, (400, 100, 280, 200), 3)
    pygame.draw.rect(screen, CREAM, (405, 105, 270, 190))
    
    # Title
    title = FONT_MEDIUM.render("Your Pizza", True, DARK_BROWN)
    screen.blit(title, (420, 120))
    
    # Draw pizza with base image
    pizza_x, pizza_y = 520, 140
    if pizza_base:
        screen.blit(pizza_base, (pizza_x, pizza_y))
    else:
        pygame.draw.circle(screen, ORANGE, (pizza_x + 50, pizza_y + 50), 50)  # Fallback
        pygame.draw.circle(screen, ORANGE, (pizza_x + 50, pizza_y + 50), 50, 2)
    
    # Draw toppings stacked in the center of the pizza
    if player_pizza.pizza_lst:
        for topping in player_pizza.pizza_lst:
            topping_img = topping_images.get(topping.name)
            if topping_img:
                screen.blit(topping_img, (pizza_x, pizza_y))
    
    # Toppings list
    y_pos = 160
    for topping in player_pizza.pizza_lst:
        topping_text = FONT_TINY.render(f"+ {topping.name}", True, BLACK)
        screen.blit(topping_text, (420, y_pos))
        y_pos += 20
    
    # Price
    price_text = FONT_SMALL.render(f"Price: ${player_pizza.pizza_price:.2f}", True, DARK_RED)
    screen.blit(price_text, (550, 260))
    
    # Draw drink if selected
    if player_drink:
        drink_box_x = 700
        
        # Draw drink cup with image
        drink_img = drink_images.get(player_drink.name)
        if drink_img:
            screen.blit(drink_img, (drink_box_x, 80))
        else:
            # Fallback: draw colored box
            drink_colors = [(100, 150, 200), (255, 200, 0), (200, 200, 200), (255, 100, 100)]
            pygame.draw.rect(screen, WHITE, (drink_box_x, 80, 100, 180), 3)
            pygame.draw.rect(screen, drink_colors[0], (drink_box_x + 2, 82, 96, 176))
        
        # Drink name
        drink_name = FONT_SMALL.render(player_drink.name, True, BLACK)
        screen.blit(drink_name, (drink_box_x + 20, 185))

def draw_topping_options(screen, toppings):
    """Draw selectable toppings"""
    width, height = screen.get_size()
    
    # Toppings header
    header = FONT_MEDIUM.render("Toppings", True, DARK_BROWN)
    screen.blit(header, (width//2 - 60, height//2 + 30))
    
    # Draw topping options on table, 3 per row
    topping_y = height//2 + 80
    topping_x = width//2 - 90
    row_count = 0
    
    for i, topping in enumerate(toppings):
        # Topping box
        pygame.draw.rect(screen, WHITE, (topping_x, topping_y, 180, 70), 2)
        pygame.draw.rect(screen, LIGHT_YELLOW, (topping_x + 2, topping_y + 2, 176, 66))
        
        # Draw topping image
        topping_img = topping_menu_images.get(topping.name)
        if topping_img:
            screen.blit(topping_img, (topping_x + 15, topping_y + 10))
        
        # Topping name
        name = FONT_TINY.render(topping.name, True, BLACK)
        screen.blit(name, (topping_x + 75, topping_y + 10))
        
        # Price
        price = FONT_SMALL.render(f"${topping.price:.2f}", True, DARK_RED)
        screen.blit(price, (topping_x + 75, topping_y + 40))
        
        row_count += 1
        if row_count == 3:
            topping_y += 80
            topping_x = width//2 - 90
            row_count = 0
        else:
            topping_x += 210

def draw_drink_options(screen, drinks):
    """Draw selectable drinks"""
    width, height = screen.get_size()
    
    # Drinks header
    header = FONT_MEDIUM.render("Drinks", True, DARK_BROWN)
    screen.blit(header, (20, height//2 + 30))
    
    # Draw drink options on left side of table, 2 per row
    drink_y = height//2 + 80
    drink_x = 20
    row_count = 0
    
    for i, drink in enumerate(drinks):
        # Draw drink box background
        pygame.draw.rect(screen, WHITE, (drink_x, drink_y, 180, 70), 2)
        pygame.draw.rect(screen, LIGHT_YELLOW, (drink_x + 2, drink_y + 2, 176, 66))
        
        # Draw drink image
        drink_img = drink_images.get(drink.name)
        if drink_img:
            # Scale down for display in menu
            drink_img_small = pygame.transform.scale(drink_img, (50, 50))
            screen.blit(drink_img_small, (drink_x + 15, drink_y + 10))
        
        # Drink name
        name = FONT_TINY.render(drink.name, True, BLACK)
        screen.blit(name, (drink_x + 75, drink_y + 10))
        
        # Price
        price = FONT_SMALL.render(f"${drink.price:.2f}", True, DARK_RED)
        screen.blit(price, (drink_x + 75, drink_y + 40))
        
        row_count += 1
        if row_count == 2:
            drink_y += 80
            drink_x = 20
            row_count = 0
        else:
            drink_x += 220

def draw_customer_image(screen, customer_image):
    """Draw customer image on the right side spanning over the edge"""
    width, height = screen.get_size()
    
    # Position: right side, spanning over the edge between upper and table areas
    image_x = width - 320
    image_y = height//2 - 350
    
    # Draw the customer image (no background border)
    if customer_image:
        screen.blit(customer_image, (image_x, image_y))

def draw_controls(screen):
    """Draw control instructions"""
    width, height = screen.get_size()
    
    instructions = [
        "Click Toppings & Drinks  |  ENTER: Submit Order  |  ESC: Quit"
    ]
    
    instr_text = FONT_TINY.render(instructions[0], True, BLACK)
    screen.blit(instr_text, (width//2 - 250, height - 20))
    
    # Draw New Pizza button
    button_width = 140
    button_height = 35
    button_x = width//2 - 70
    button_y = 20
    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height), 2)
    pygame.draw.rect(screen, LIGHT_YELLOW, (button_x + 1, button_y + 1, button_width - 2, button_height - 2))
    button_text = FONT_SMALL.render("New Pizza", True, DARK_BROWN)
    screen.blit(button_text, (button_x + 15, button_y + 5))

def draw_hint_text(screen):
    """Draw hint text at bottom of screen"""
    width, height = screen.get_size()
    
    hint_y = height - 50
    hint_text = FONT_SMALL.render("If you click wrong button create a new pizza", True, DARK_RED)
    screen.blit(hint_text, (width//2 - 220, hint_y))

def draw_upgrade_screen(screen, restaurant, money):
    """Draw upgrade menu for toppings and drinks"""
    width, height = screen.get_size()
    
    # Draw semi-transparent overlay
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Title
    title = FONT_LARGE.render("UPGRADES - Day Complete!", True, GOLD)
    screen.blit(title, (width//2 - 200, 30))
    
    # Money display
    money_text = FONT_MEDIUM.render(f"Money: ${money:.2f}", True, GOLD)
    screen.blit(money_text, (width//2 - 100, 100))
    
    # Toppings section
    topping_title = FONT_MEDIUM.render("Upgrade Toppings", True, ORANGE)
    screen.blit(topping_title, (50, 150))
    
    topping_y = 200
    for i, topping in enumerate(restaurant.topping_lst):
        # Button
        button_x = 50
        button_y = topping_y
        button_width = 500
        button_height = 50
        
        # Check if can afford
        can_afford = money >= topping.current_upgrade_price
        button_color = GREEN if can_afford else GRAY
        
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height), 2)
        pygame.draw.rect(screen, LIGHT_YELLOW if can_afford else (200, 200, 200), (button_x + 1, button_y + 1, button_width - 2, button_height - 2))
        
        # Text: name and cost
        text = f"{topping.name} - ${topping.current_upgrade_price:.2f}"
        topping_text = FONT_SMALL.render(text, True, DARK_BROWN)
        screen.blit(topping_text, (button_x + 20, button_y + 12))
        
        topping_y += 60
    
    # Drinks section
    drink_title = FONT_MEDIUM.render("Upgrade Drinks", True, ORANGE)
    screen.blit(drink_title, (width//2 + 50, 150))
    
    drink_y = 200
    for i, drink in enumerate(restaurant.drinks_lst):
        # Button
        button_x = width//2 + 50
        button_y = drink_y
        button_width = 500
        button_height = 50
        
        # Check if can afford
        can_afford = money >= drink.current_upgrade_price
        button_color = GREEN if can_afford else GRAY
        
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height), 2)
        pygame.draw.rect(screen, LIGHT_YELLOW if can_afford else (200, 200, 200), (button_x + 1, button_y + 1, button_width - 2, button_height - 2))
        
        # Text: name and cost
        text = f"{drink.name} - ${drink.current_upgrade_price:.2f}"
        drink_text = FONT_SMALL.render(text, True, DARK_BROWN)
        screen.blit(drink_text, (button_x + 20, button_y + 12))
        
        drink_y += 60
    
    # Continue button
    continue_x = width//2 - 75
    continue_y = height - 80
    continue_width = 150
    continue_height = 50
    
    pygame.draw.rect(screen, WHITE, (continue_x, continue_y, continue_width, continue_height), 3)
    pygame.draw.rect(screen, LIGHT_YELLOW, (continue_x + 1, continue_y + 1, continue_width - 2, continue_height - 2))
    continue_text = FONT_MEDIUM.render("Continue", True, DARK_BROWN)
    screen.blit(continue_text, (continue_x + 25, continue_y + 8))
