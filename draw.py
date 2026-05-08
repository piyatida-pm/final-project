import pygame
import os
import math

# ── Color palette ─────────────────────────────────────────────────────────────
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
CREAM        = (255, 248, 230)
PANEL_BG     = (255, 244, 218)
PANEL_BORDER = (160, 108,  55)
BROWN_DARK   = ( 75,  42,  14)
BROWN_MED    = (155, 108,  62)
BROWN_LIGHT  = (208, 172, 118)
BRICK_MAIN   = (182,  98,  68)
BRICK_MORTAR = (218, 193, 168)
GOLD         = (218, 172,  38)
WARM_GOLD    = (252, 198,  48)
LIGHT_YELLOW = (255, 248, 178)
PIZZA_RED    = (198,  52,  38)
DARK_RED     = (148,  28,  18)
ORANGE       = (232, 128,  28)
GREEN        = ( 58, 162,  68)
DARK_GREEN   = ( 38, 112,  48)
GRAY         = (148, 148, 148)
LIGHT_GRAY   = (212, 212, 212)

# ── Fonts ─────────────────────────────────────────────────────────────────────
pygame.font.init()
FONT_LARGE  = pygame.font.Font(None, 48)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_SMALL  = pygame.font.Font(None, 28)
FONT_TINY   = pygame.font.Font(None, 22)

# ── Paths ─────────────────────────────────────────────────────────────────────
ASSET_PATH          = os.path.join(os.path.dirname(__file__), "asset")
CUSTOMER_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "customer_image")

# ── Image loaders ─────────────────────────────────────────────────────────────
def load_image(filename, width=None, height=None):
    filepath = os.path.join(ASSET_PATH, filename)
    try:
        img = pygame.image.load(filepath)
        if width and height:
            img = pygame.transform.scale(img, (width, height))
        return img
    except:
        return None

def get_customer_image_files():
    try:
        if os.path.exists(CUSTOMER_IMAGE_PATH):
            return [f for f in os.listdir(CUSTOMER_IMAGE_PATH)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    except:
        pass
    return []

def load_customer_image(filename, width=200, height=200):
    filepath = os.path.join(CUSTOMER_IMAGE_PATH, filename)
    try:
        img = pygame.image.load(filepath)
        return pygame.transform.scale(img, (width, height))
    except:
        return None

# ── Sprite assets ─────────────────────────────────────────────────────────────
pizza_base = load_image("pizza.PNG", 100, 100) or load_image("pizza.png", 100, 100)
topping_images = {
    "Pesto Sauce": load_image("toppesto.PNG", 100, 100) or load_image("pesto.PNG", 100, 100),
    "Mushroom":    load_image("topmushroom.PNG", 100, 100) or load_image("mushroom.PNG", 100, 100),
    "Cheese":      load_image("topcheese.PNG", 100, 100) or load_image("cheese.PNG", 100, 100),
    "Pepperoni":   load_image("toppeperroni.PNG", 100, 100) or load_image("peperoni.PNG", 100, 100),
    "Bacon":       load_image("topbacon.PNG", 100, 100) or load_image("bacon.PNG", 100, 100),
    "Pineapple":   load_image("toppineapple.PNG", 100, 100) or load_image("pineapple.PNG", 100, 100),
}
topping_menu_images = {
    "Pesto Sauce": load_image("pesto.PNG", 50, 50) or load_image("pesto.png", 50, 50),
    "Mushroom":    load_image("mushroom.PNG", 50, 50) or load_image("mushroom.png", 50, 50),
    "Cheese":      load_image("cheese.PNG", 50, 50) or load_image("cheese.png", 50, 50),
    "Pepperoni":   load_image("peperoni.PNG", 50, 50) or load_image("peperoni.png", 50, 50),
    "Bacon":       load_image("bacon.PNG", 50, 50) or load_image("bacon.png", 50, 50),
    "Pineapple":   load_image("pineapple.PNG", 50, 50) or load_image("pineapple.png", 50, 50),
}
drink_images = {
    "Coke":      load_image("coke.PNG", 100, 100) or load_image("coke.png", 100, 100),
    "Sprite":    load_image("sprite.PNG", 100, 100) or load_image("sprite.png", 100, 100),
    "Water":     load_image("water.PNG", 100, 100) or load_image("water.png", 100, 100),
    "Milkshake": load_image("milkshake.PNG", 100, 100) or load_image("milkshake.png", 100, 100),
}

# ── Drawing helpers ───────────────────────────────────────────────────────────
def _shadow(screen, x, y, w, h, radius=12):
    """Drop-shadow using a shifted dark rectangle."""
    pygame.draw.rect(screen, (68, 38, 12), (x + 5, y + 5, w, h), border_radius=radius)

def draw_panel(screen, x, y, w, h, bg=PANEL_BG, border=PANEL_BORDER, radius=14):
    """Rounded panel with a drop-shadow."""
    _shadow(screen, x, y, w, h, radius)
    pygame.draw.rect(screen, border, (x, y, w, h), border_radius=radius)
    pygame.draw.rect(screen, bg, (x + 3, y + 3, w - 6, h - 6), border_radius=max(radius - 3, 0))

def draw_button(screen, x, y, w, h, text, font,
                bg=PANEL_BG, border=PANEL_BORDER, fg=BROWN_DARK,
                radius=10, mouse_pos=None):
    """Rounded button with mouse-hover highlight."""
    hovered = (mouse_pos is not None
               and x <= mouse_pos[0] <= x + w
               and y <= mouse_pos[1] <= y + h)
    fill = tuple(min(c + 30, 255) for c in bg) if hovered else bg
    _shadow(screen, x, y, w, h, radius)
    pygame.draw.rect(screen, border, (x, y, w, h), border_radius=radius)
    pygame.draw.rect(screen, fill, (x + 2, y + 2, w - 4, h - 4), border_radius=max(radius - 2, 0))
    if text:
        surf = font.render(text, True, fg)
        screen.blit(surf, surf.get_rect(center=(x + w // 2, y + h // 2)))

# ── Background (cached so brick/tile only render once) ────────────────────────
_bg_cache: dict = {}

def draw_kitchen_background(screen):
    width, height = screen.get_size()
    key = (width, height)
    if key not in _bg_cache:
        surf = pygame.Surface((width, height))
        cy = height // 2

        # Wall — warm sandstone base
        surf.fill((232, 212, 188))

        # Brick rows
        bw, bh, m = 78, 28, 3
        for row in range(cy // bh + 2):
            off = bw // 2 if row % 2 else 0
            ry  = row * bh
            for col in range(-1, width // bw + 2):
                bx = col * bw + off
                tile_h = min(bh, cy - ry) - m
                if tile_h > 2 and bx + bw > 0:
                    pygame.draw.rect(surf, BRICK_MAIN,
                                     (bx + m, ry + m, bw - m * 2, tile_h),
                                     border_radius=2)

        # Counter top — warm wood
        ch = 44
        pygame.draw.rect(surf, (188, 138, 88), (0, cy, width, ch))
        pygame.draw.line(surf, (228, 188, 138), (0, cy + 1), (width, cy + 1), 3)
        pygame.draw.line(surf, (118,  78,  38), (0, cy + ch), (width, cy + ch), 2)
        for i in range(6):
            pygame.draw.line(surf, (158, 108, 58),
                             (0, cy + 8 + i * 5), (width, cy + 8 + i * 5), 1)

        # Floor — terracotta tiles
        fy = cy + ch
        surf.fill((138, 98, 62), pygame.Rect(0, fy, width, height - fy))
        ts = 52
        for row in range((height - fy) // ts + 2):
            for col in range(width // ts + 2):
                tx, ty = col * ts, fy + row * ts
                pygame.draw.rect(surf, (128, 90, 55), (tx, ty, ts - 2, ts - 2))
                pygame.draw.rect(surf, (105, 70, 40), (tx, ty, ts - 2, ts - 2), 1)

        # Money box outline (static frame, text drawn each frame)
        pygame.draw.rect(surf, GOLD,         (948, 13, 214, 94), border_radius=12)
        pygame.draw.rect(surf, LIGHT_YELLOW, (951, 16, 208, 88), border_radius=10)

        _bg_cache[key] = surf

    screen.blit(_bg_cache[key], (0, 0))

# ── HUD / stats ───────────────────────────────────────────────────────────────
def draw_stats(screen, money, orders_completed, day):
    # Left info bar
    draw_panel(screen, 28, 12, 270, 44, radius=10)
    screen.blit(FONT_SMALL.render(f"Orders: {orders_completed}", True, BROWN_DARK), (44, 22))
    screen.blit(FONT_SMALL.render(f"Day {day}", True, PIZZA_RED), (200, 22))

    # Money (overlaid on the pre-drawn gold box)
    screen.blit(FONT_MEDIUM.render(f"${money:.2f}", True, DARK_RED), (962, 30))
    screen.blit(FONT_TINY.render("Money", True, BROWN_DARK), (982, 68))

# ── Customer order panel ──────────────────────────────────────────────────────
def draw_customer_order(screen, order):
    draw_panel(screen, 48, 98, 310, 220)

    # Coloured header strip
    pygame.draw.rect(screen, PIZZA_RED, (51, 101, 304, 40), border_radius=11)
    pygame.draw.rect(screen, PIZZA_RED, (51, 128, 304, 13))   # square off bottom
    screen.blit(FONT_MEDIUM.render(f"{order.customer_name}'s Order", True, WHITE), (68, 108))

    y = 155
    if order.lst_order:
        pizza = order.lst_order[0]
        screen.blit(FONT_SMALL.render("Pizza with:", True, BROWN_DARK), (68, y)); y += 28
        for topping in pizza.pizza_lst:
            screen.blit(FONT_TINY.render(f"• {topping.name}", True, DARK_RED), (85, y)); y += 22
        y += 6
        if len(order.lst_order) > 1:
            screen.blit(FONT_SMALL.render(f"+ {order.lst_order[1].name}", True, ORANGE), (68, y))

# ── Player pizza panel ────────────────────────────────────────────────────────
def draw_player_pizza(screen, player_pizza, player_drink=None):
    draw_panel(screen, 398, 98, 292, 220)

    # Panel header strip
    pygame.draw.rect(screen, BROWN_MED, (401, 101, 286, 40), border_radius=11)
    pygame.draw.rect(screen, BROWN_MED, (401, 128, 286, 13))
    screen.blit(FONT_MEDIUM.render("Your Pizza", True, WHITE), (420, 108))

    # Pizza base image
    px, py = 528, 138
    if pizza_base:
        screen.blit(pizza_base, (px, py))
    else:
        pygame.draw.circle(screen, ORANGE, (px + 50, py + 50), 50)

    for topping in player_pizza.pizza_lst:
        img = topping_images.get(topping.name)
        if img:
            screen.blit(img, (px, py))

    # Topping list (left column of panel)
    y = 155
    for topping in player_pizza.pizza_lst:
        screen.blit(FONT_TINY.render(f"+ {topping.name}", True, BROWN_DARK), (408, y))
        y += 20

    # Price
    screen.blit(FONT_SMALL.render(f"${player_pizza.pizza_price:.2f}", True, DARK_RED), (548, 268))

    # Drink display
    if player_drink:
        # White rounded background
        pygame.draw.rect(screen, PANEL_BORDER, (692, 72, 116, 116), border_radius=16)
        pygame.draw.rect(screen, WHITE,        (695, 75, 110, 110), border_radius=14)
        img = drink_images.get(player_drink.name)
        if img:
            screen.blit(img, (700, 80))
        screen.blit(FONT_SMALL.render(player_drink.name, True, BROWN_DARK), (720, 195))

# ── Topping buttons ───────────────────────────────────────────────────────────
def draw_topping_options(screen, toppings, mouse_pos=None):
    width, height = screen.get_size()
    cy = height // 2

    # Section label
    pygame.draw.rect(screen, BROWN_DARK, (width // 2 - 72, cy + 5, 144, 34), border_radius=8)
    screen.blit(FONT_MEDIUM.render("Toppings", True, WHITE), (width // 2 - 60, cy + 8))

    tx, ty, col = width // 2 - 90, cy + 80, 0
    for topping in toppings:
        draw_button(screen, tx, ty, 180, 70, "", FONT_TINY, mouse_pos=mouse_pos)
        img = topping_menu_images.get(topping.name)
        if img:
            screen.blit(img, (tx + 10, ty + 10))
        screen.blit(FONT_TINY.render(topping.name, True, BROWN_DARK), (tx + 68, ty + 10))
        screen.blit(FONT_SMALL.render(f"${topping.price:.2f}", True, DARK_RED), (tx + 68, ty + 38))
        col += 1
        if col == 3:
            ty += 80; tx = width // 2 - 90; col = 0
        else:
            tx += 210

# ── Drink buttons ─────────────────────────────────────────────────────────────
def draw_drink_options(screen, drinks, mouse_pos=None):
    height = screen.get_height()
    cy = height // 2

    # Section label
    pygame.draw.rect(screen, BROWN_DARK, (18, cy + 5, 108, 34), border_radius=8)
    screen.blit(FONT_MEDIUM.render("Drinks", True, WHITE), (22, cy + 8))

    dx, dy, col = 20, cy + 80, 0
    for drink in drinks:
        draw_button(screen, dx, dy, 180, 70, "", FONT_TINY, mouse_pos=mouse_pos)
        img = drink_images.get(drink.name)
        if img:
            screen.blit(pygame.transform.scale(img, (50, 50)), (dx + 10, dy + 10))
        screen.blit(FONT_TINY.render(drink.name, True, BROWN_DARK), (dx + 68, dy + 10))
        screen.blit(FONT_SMALL.render(f"${drink.price:.2f}", True, DARK_RED), (dx + 68, dy + 38))
        col += 1
        if col == 2:
            dy += 80; dx = 20; col = 0
        else:
            dx += 220

# ── Customer image ────────────────────────────────────────────────────────────
def draw_customer_image(screen, customer_image):
    width, height = screen.get_size()
    if customer_image:
        screen.blit(customer_image, (width - 320, height // 2 - 350))

# ── Hint text ─────────────────────────────────────────────────────────────────
def draw_hint_text(screen):
    width, height = screen.get_size()
    surf = FONT_TINY.render(
        "Tip: If you added the wrong topping, press New Pizza to start over", True, DARK_RED)
    screen.blit(surf, (width // 2 - surf.get_width() // 2, height - 52))

# ── Controls bar (New Pizza button + instruction strip) ───────────────────────
def draw_controls(screen, mouse_pos=None):
    width, height = screen.get_size()

    # Translucent bottom strip
    strip = pygame.Surface((width, 24))
    strip.set_alpha(180)
    strip.fill((30, 15, 5))
    screen.blit(strip, (0, height - 24))
    instr = FONT_TINY.render(
        "Click Toppings & Drinks  |  ENTER: Submit  |  M: Stats  |  ESC: Quit", True, WHITE)
    screen.blit(instr, (width // 2 - instr.get_width() // 2, height - 20))

    # New Pizza button — hit-area matches main.py: x=530–670, y=20–55
    draw_button(screen, width // 2 - 70, 20, 140, 35, "New Pizza", FONT_SMALL,
                bg=WARM_GOLD, border=GOLD, fg=BROWN_DARK, radius=10, mouse_pos=mouse_pos)

# ── Sound toggle button ───────────────────────────────────────────────────────
def draw_sound_toggle_button(screen, sound_enabled, mouse_pos=None):
    width, height = screen.get_size()
    bw, bh = 80, 50
    bx = width  - bw - 20   # 1100
    by = height - bh - 20   # 730

    bg     = GREEN      if sound_enabled else PIZZA_RED
    border = DARK_GREEN if sound_enabled else DARK_RED
    label  = "ON"       if sound_enabled else "OFF"

    draw_button(screen, bx, by, bw, bh, label, FONT_MEDIUM,
                bg=bg, border=border, fg=WHITE, mouse_pos=mouse_pos)
    lbl = FONT_TINY.render("SOUND", True, BROWN_DARK)
    screen.blit(lbl, (bx + (bw - lbl.get_width()) // 2, by - 20))

# ── Upgrade screen ────────────────────────────────────────────────────────────
def draw_upgrade_screen(screen, restaurant, money, mouse_pos=None):
    width, height = screen.get_size()

    # Dark overlay
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(215)
    overlay.fill((38, 18, 8))
    screen.blit(overlay, (0, 0))

    # Title panel
    draw_panel(screen, width // 2 - 245, 18, 490, 68, bg=(50, 22, 6), border=GOLD, radius=14)
    title = FONT_LARGE.render("UPGRADES — Day Complete!", True, GOLD)
    screen.blit(title, (width // 2 - title.get_width() // 2, 30))

    # Money display
    draw_panel(screen, width // 2 - 125, 98, 250, 52, radius=10)
    money_surf = FONT_MEDIUM.render(f"Money: ${money:.2f}", True, DARK_RED)
    screen.blit(money_surf, (width // 2 - money_surf.get_width() // 2, 110))

    # Toppings section
    screen.blit(FONT_MEDIUM.render("Upgrade Toppings", True, ORANGE), (50, 162))
    ty = 200
    for topping in restaurant.topping_lst:
        can   = money >= topping.current_upgrade_price
        bg_c  = (235, 252, 235) if can else LIGHT_GRAY
        bdr_c = GREEN           if can else GRAY
        draw_button(screen, 50, ty, 500, 50,
                    f"{topping.name}  —  ${topping.current_upgrade_price:.2f}",
                    FONT_SMALL, bg=bg_c, border=bdr_c, fg=BROWN_DARK,
                    radius=10, mouse_pos=mouse_pos)
        ty += 60

    # Drinks section
    screen.blit(FONT_MEDIUM.render("Upgrade Drinks", True, ORANGE), (width // 2 + 50, 162))
    dy = 200
    for drink in restaurant.drinks_lst:
        can   = money >= drink.current_upgrade_price
        bg_c  = (235, 252, 235) if can else LIGHT_GRAY
        bdr_c = GREEN           if can else GRAY
        draw_button(screen, width // 2 + 50, dy, 500, 50,
                    f"{drink.name}  —  ${drink.current_upgrade_price:.2f}",
                    FONT_SMALL, bg=bg_c, border=bdr_c, fg=BROWN_DARK,
                    radius=10, mouse_pos=mouse_pos)
        dy += 60

    # Continue button — hit-area matches main.py: x=525, y=720, 150×50
    draw_button(screen, width // 2 - 75, height - 80, 150, 50,
                "Continue", FONT_MEDIUM,
                bg=WARM_GOLD, border=GOLD, fg=BROWN_DARK,
                radius=12, mouse_pos=mouse_pos)

# ── Statistics screen ─────────────────────────────────────────────────────────
def _chart_panel(screen, x, y, w, h, title):
    """Rounded chart panel with title strip; returns inner plot area (px, py, pw, ph)."""
    draw_panel(screen, x, y, w, h, radius=12)
    pygame.draw.rect(screen, BROWN_MED, (x + 3, y + 3, w - 6, 30), border_radius=9)
    pygame.draw.rect(screen, BROWN_MED, (x + 3, y + 20, w - 6, 13))
    surf = FONT_SMALL.render(title, True, WHITE)
    screen.blit(surf, (x + w // 2 - surf.get_width() // 2, y + 7))
    return x + 52, y + 44, w - 68, h - 72   # px, py, pw, ph

def _chart_axes(screen, px, py, pw, ph):
    pygame.draw.line(screen, BROWN_DARK, (px, py),      (px,      py + ph), 2)
    pygame.draw.line(screen, BROWN_DARK, (px, py + ph), (px + pw, py + ph), 2)

def _no_data_msg(screen, x, y, w, h):
    msg = FONT_SMALL.render("No data yet", True, GRAY)
    screen.blit(msg, (x + w // 2 - msg.get_width() // 2, y + h // 2 - 10))

def _draw_bar_chart(screen, x, y, w, h, title, data_dict, bar_colors):
    px, py, pw, ph = _chart_panel(screen, x, y, w, h, title)
    if not data_dict:
        _no_data_msg(screen, x, y, w, h); return
    labels = list(data_dict.keys())
    values = list(data_dict.values())
    max_v  = max(values) or 1
    n     = len(labels)
    gap   = max(6, pw // max(n * 4, 1))
    bar_w = max(10, (pw - gap * (n + 1)) // max(n, 1))

    # Rotate labels if the longest one won't fit horizontally in its bar slot
    max_lbl_w = max(FONT_TINY.size(lb)[0] for lb in labels) if labels else 0
    rotate_labels = max_lbl_w > bar_w + gap - 4
    label_area = 54 if rotate_labels else 22   # vertical space reserved below axis

    # Shrink the plot height to make room for the labels
    ph = ph - label_area

    # Y gridlines + axis value labels
    for i in range(5):
        frac = i / 4
        yp   = py + ph - int(ph * frac)
        pygame.draw.line(screen, LIGHT_GRAY, (px, yp), (px + pw, yp), 1)
        lbl = FONT_TINY.render(str(int(max_v * frac)), True, GRAY)
        screen.blit(lbl, (px - lbl.get_width() - 4, yp - 7))

    # Bars + value labels + x-axis labels
    for i, (label, val) in enumerate(zip(labels, values)):
        bx = px + gap + i * (bar_w + gap)
        bh = max(2, int(ph * val / max_v))
        by = py + ph - bh
        pygame.draw.rect(screen, bar_colors[i % len(bar_colors)],
                         (bx, by, bar_w, bh), border_radius=5)
        vl = FONT_TINY.render(str(val), True, BROWN_DARK)
        screen.blit(vl, (bx + bar_w // 2 - vl.get_width() // 2, by - 16))

        ll = FONT_TINY.render(label, True, BROWN_DARK)
        if rotate_labels:
            rotated = pygame.transform.rotate(ll, 35)
            cx = bx + bar_w // 2
            screen.blit(rotated, (cx - rotated.get_width() // 2, py + ph + 6))
        else:
            screen.blit(ll, (bx + bar_w // 2 - ll.get_width() // 2, py + ph + 6))

    _chart_axes(screen, px, py, pw, ph)

def _draw_scatter(screen, x, y, w, h, title, xs, ys):
    px, py, pw, ph = _chart_panel(screen, x, y, w, h, title)
    if not xs:
        _no_data_msg(screen, x, y, w, h); return
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    rx = max_x - min_x or 1
    ry = max_y - min_y or 1
    # Y gridlines + price labels
    for i in range(5):
        frac = i / 4
        yp   = py + ph - int(ph * frac)
        val  = min_y + ry * frac
        pygame.draw.line(screen, LIGHT_GRAY, (px, yp), (px + pw, yp), 1)
        lbl = FONT_TINY.render(f"${val:.0f}", True, GRAY)
        screen.blit(lbl, (px - lbl.get_width() - 4, yp - 7))
    # Dots
    for xi, yi in zip(xs, ys):
        sx = px + int((xi - min_x) / rx * pw)
        sy = py + ph - int((yi - min_y) / ry * ph)
        pygame.draw.circle(screen, PIZZA_RED, (sx, sy), 4)
        pygame.draw.circle(screen, DARK_RED,  (sx, sy), 4, 1)
    xl = FONT_TINY.render("Order ID", True, BROWN_DARK)
    screen.blit(xl, (px + pw // 2 - xl.get_width() // 2, py + ph + 6))
    _chart_axes(screen, px, py, pw, ph)

def _draw_histogram(screen, x, y, w, h, title, values, n_bins=7):
    px, py, pw, ph = _chart_panel(screen, x, y, w, h, title)
    if not values:
        _no_data_msg(screen, x, y, w, h); return
    min_v, max_v = min(values), max(values)
    span         = (max_v - min_v) or 1
    bin_size     = span / n_bins
    bins = [0] * n_bins
    for v in values:
        bins[min(int((v - min_v) / bin_size), n_bins - 1)] += 1
    max_b  = max(bins) or 1
    bar_px = pw // n_bins
    hist_colors = [ORANGE, WARM_GOLD, GREEN, PIZZA_RED, BROWN_MED, GOLD, DARK_GREEN]
    # Y gridlines
    for i in range(5):
        frac = i / 4
        yp   = py + ph - int(ph * frac)
        pygame.draw.line(screen, LIGHT_GRAY, (px, yp), (px + pw, yp), 1)
        lbl = FONT_TINY.render(str(int(max_b * frac)), True, GRAY)
        screen.blit(lbl, (px - lbl.get_width() - 4, yp - 7))
    # Bins
    for i, count in enumerate(bins):
        bx = px + i * bar_px + 2
        if count > 0:
            bh = max(2, int(ph * count / max_b))
            by = py + ph - bh
            pygame.draw.rect(screen, hist_colors[i % len(hist_colors)],
                             (bx, by, bar_px - 4, bh), border_radius=4)
            vl = FONT_TINY.render(str(count), True, BROWN_DARK)
            screen.blit(vl, (bx + (bar_px - 4) // 2 - vl.get_width() // 2, by - 16))
        lbl = FONT_TINY.render(f"{int(min_v + i * bin_size)}s", True, BROWN_DARK)
        screen.blit(lbl, (bx + (bar_px - 4) // 2 - lbl.get_width() // 2, py + ph + 6))
    _chart_axes(screen, px, py, pw, ph)

def _draw_pie_chart(screen, x, y, w, h, title, data_dict, colors):
    """Draw a pie chart with a legend for the given data_dict."""
    px, py, pw, ph = _chart_panel(screen, x, y, w, h, title)
    if not data_dict or sum(data_dict.values()) == 0:
        _no_data_msg(screen, x, y, w, h); return

    total  = sum(data_dict.values())
    labels = list(data_dict.keys())
    values = list(data_dict.values())

    # Pie on the left portion; legend on the right
    legend_w   = max(180, pw // 3)
    pie_area_w = pw - legend_w - 20
    cx = px + pie_area_w // 2
    cy = py + ph // 2
    radius = min(pie_area_w, ph) // 2 - 12

    # Draw filled slices as polygons
    start_angle = -90.0   # start from top
    for i, (label, val) in enumerate(zip(labels, values)):
        if val == 0:
            continue
        sweep = 360.0 * val / total
        color = colors[i % len(colors)]

        # Approximate arc with many polygon points
        steps  = max(3, int(abs(sweep)))
        points = [(cx, cy)]
        for step in range(steps + 1):
            angle_rad = math.radians(start_angle + sweep * step / steps)
            points.append((
                cx + int(radius * math.cos(angle_rad)),
                cy + int(radius * math.sin(angle_rad))
            ))

        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, WHITE, points, 1)

        # Percentage label near the middle of the slice
        mid_rad = math.radians(start_angle + sweep / 2)
        lx = cx + int(radius * 0.6 * math.cos(mid_rad))
        ly = cy + int(radius * 0.6 * math.sin(mid_rad))
        pct_surf = FONT_TINY.render(f"{val / total * 100:.1f}%", True, WHITE)
        screen.blit(pct_surf, (lx - pct_surf.get_width() // 2,
                               ly - pct_surf.get_height() // 2))

        start_angle += sweep

    # Outer border circle
    pygame.draw.circle(screen, BROWN_DARK, (cx, cy), radius, 2)

    # Legend
    legend_x = px + pie_area_w + 20
    legend_y = py + ph // 2 - (len(labels) * 30) // 2
    for i, (label, val) in enumerate(zip(labels, values)):
        color = colors[i % len(colors)]
        lx    = legend_x
        ly    = legend_y + i * 30
        pygame.draw.rect(screen, color,      (lx,     ly + 3, 16, 16), border_radius=3)
        pygame.draw.rect(screen, BROWN_DARK, (lx,     ly + 3, 16, 16), 1, border_radius=3)
        txt = FONT_TINY.render(f"{label}: {val}", True, BROWN_DARK)
        screen.blit(txt, (lx + 22, ly + 4))

def _draw_summary_table(screen, x, y, w, h, title, rows):
    """Draw a two- or three-column summary table inside a panel."""
    draw_panel(screen, x, y, w, h, radius=12)
    # Table title strip
    pygame.draw.rect(screen, BROWN_MED, (x + 3, y + 3, w - 6, 28), border_radius=9)
    pygame.draw.rect(screen, BROWN_MED, (x + 3, y + 18, w - 6, 13))
    ts = FONT_SMALL.render(title, True, WHITE)
    screen.blit(ts, (x + w // 2 - ts.get_width() // 2, y + 6))

    if not rows:
        return

    inner_x = x + 10
    inner_y = y + 38
    row_h   = min(28, (h - 48) // max(len(rows), 1))
    n_cols  = len(rows[0])
    col_w   = (w - 20) // n_cols

    for r_idx, row in enumerate(rows):
        ry = inner_y + r_idx * row_h
        # Alternate row shading
        shade = (255, 245, 210) if r_idx % 2 == 0 else (240, 225, 190)
        if r_idx == 0:
            shade = (180, 120, 60)   # header row
        pygame.draw.rect(screen, shade, (inner_x, ry, w - 20, row_h - 2), border_radius=3)

        for c_idx, cell in enumerate(row):
            fg   = WHITE if r_idx == 0 else BROWN_DARK
            font = FONT_SMALL if r_idx == 0 else FONT_TINY
            surf = font.render(str(cell), True, fg)
            cx   = inner_x + c_idx * col_w + 6
            screen.blit(surf, (cx, ry + (row_h - surf.get_height()) // 2))

def draw_stats_screen(screen, stats_data, tab_index=0, mouse_pos=None):
    """Full-screen statistics overlay — chart on the left, summary table on the right."""
    width, height = screen.get_size()

    # Dark overlay
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(230)
    overlay.fill((18, 8, 3))
    screen.blit(overlay, (0, 0))

    # Title + orders count (top-left block)
    draw_panel(screen, 8, 8, 340, 50, bg=(50, 22, 6), border=GOLD, radius=12)
    title_surf = FONT_MEDIUM.render("Game Statistics", True, GOLD)
    screen.blit(title_surf, (18, 18))
    badge = FONT_TINY.render(f"Orders recorded: {stats_data['total_orders']}", True, WARM_GOLD)
    screen.blit(badge, (18, 44))

    # Close / nav hint (top-right)
    hint = FONT_TINY.render("Tab / ← →: switch chart   M: close", True, LIGHT_GRAY)
    screen.blit(hint, (width - hint.get_width() - 12, 22))

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab_labels = ["Drinks", "Toppings", "Price", "Time", "Accuracy"]
    pad   = 8
    tab_y = 62
    tab_h = 36
    tab_w = (width - 2 * pad) // 5

    for i, label in enumerate(tab_labels):
        tx     = pad + i * tab_w
        active = (i == tab_index)
        draw_button(screen, tx, tab_y, tab_w - 4, tab_h, label, FONT_MEDIUM,
                    bg=WARM_GOLD if active else BROWN_MED,
                    border=GOLD if active else BROWN_DARK,
                    fg=BROWN_DARK if active else WHITE,
                    radius=8, mouse_pos=mouse_pos)

    # ── Layout: chart left (65%), table right (35%) ────────────────────────
    content_y = tab_y + tab_h + 8
    content_h = height - content_y - 28
    tbl_w     = int(width * 0.32)
    chart_w   = width - 2 * pad - tbl_w - pad
    chart_x   = pad
    tbl_x     = chart_x + chart_w + pad

    if stats_data['total_orders'] == 0:
        msg = FONT_MEDIUM.render("No data yet — complete some orders first!", True, WHITE)
        screen.blit(msg, (width // 2 - msg.get_width() // 2, content_y + content_h // 2))
        return

    if tab_index == 0:
        _draw_bar_chart(
            screen, chart_x, content_y, chart_w, content_h,
            "Drink Frequency  (Feature 5 — Bar Graph)",
            stats_data['drink_counts'],
            [(58, 90, 200), (70, 200, 80), (100, 180, 230), (240, 160, 210)])
        _draw_summary_table(
            screen, tbl_x, content_y, tbl_w, content_h,
            "Summary", stats_data.get('drink_table', []))

    elif tab_index == 1:
        _draw_bar_chart(
            screen, chart_x, content_y, chart_w, content_h,
            "Topping Frequency  (Feature 3 — Bar Graph)",
            stats_data['topping_counts'],
            [PIZZA_RED, ORANGE, WARM_GOLD, GREEN, BROWN_MED, GOLD])
        _draw_summary_table(
            screen, tbl_x, content_y, tbl_w, content_h,
            "Summary", stats_data.get('topping_table', []))

    elif tab_index == 2:
        _draw_scatter(
            screen, chart_x, content_y, chart_w, content_h,
            "Order Price over Time  (Feature 1 — Scatter Plot)",
            stats_data['order_ids'], stats_data['prices'])
        _draw_summary_table(
            screen, tbl_x, content_y, tbl_w, content_h,
            "Price Summary", stats_data.get('price_table', []))

    elif tab_index == 3:
        _draw_histogram(
            screen, chart_x, content_y, chart_w, content_h,
            "Time per Order in seconds  (Feature 2 — Histogram)",
            stats_data['times'])
        _draw_summary_table(
            screen, tbl_x, content_y, tbl_w, content_h,
            "Time Summary", stats_data.get('time_table', []))

    elif tab_index == 4:
        _draw_pie_chart(
            screen, chart_x, content_y, chart_w, content_h,
            "Order Delivery Accuracy  (Feature 4 — Pie Chart)",
            stats_data.get('accuracy_counts', {}),
            [GREEN, PIZZA_RED, ORANGE, WARM_GOLD])
        _draw_summary_table(
            screen, tbl_x, content_y, tbl_w, content_h,
            "Accuracy Summary", stats_data.get('accuracy_table', []))