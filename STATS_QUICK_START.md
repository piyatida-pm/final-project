# Quick Start Guide - Statistics Visualizer

## How to Use

### 1. During Gameplay
Look for the **"Stats"** button in the **top-left area** of the screen, just below the Orders display.

```
┌─────────────────────────────────────────────────────────┐
│ Orders: X  Day X                          $ X.XX Money   │
│ [Stats]                                                   │
│ ┌─────────────────────────────────────────────────────┐ │
│ │  Customer Order    │  Your Pizza     │               │ │
│ │  ...               │  ...            │   Customer    │ │
│ │                    │                 │   Image       │ │
│ └─────────────────────────────────────────────────────┘ │
│                    Game Area                             │
└─────────────────────────────────────────────────────────┘
```

### 2. Click the Stats Button
Clicking the "Stats" button opens a large popup window showing:

```
╔═══════════════════════════════════════════════════════════╗
║               GAME STATISTICS                      [X]    ║
╠═══════════════════════════════════════════════════════════╣
║ LEFT SIDE                │ RIGHT SIDE                     ║
║                          │                                ║
║ • Total Orders: N        │ Daily Summary                  ║
║ • Total Revenue: $XXX    │ • Day 1: X orders, $XXX        ║
║ • Average Price: $XX     │ • Day 2: X orders, $XXX        ║
║ • Order Accuracy: X%     │ • ...                          ║
║ • Time Statistics        │                                ║
║   - Min/Max/Avg times    │ Topping Statistics            ║
║ • Drink Frequency        │ • Total Toppings Used: N      ║
║   [Bar chart]            │                                ║
╠═══════════════════════════════════════════════════════════╣
║             Click X or press ESC to close                ║
╚═══════════════════════════════════════════════════════════╝
```

### 3. Close the Popup
- **Method 1**: Click the red **X** button in the top-right corner
- **Method 2**: Press **ESC** key
- Game resumes immediately after closing

## What Statistics Are Shown?

### Main Metrics
- **Total Orders**: How many orders you've completed
- **Total Revenue**: Total money earned from all orders
- **Average Price**: Average amount earned per order

### Performance Metrics
- **Order Accuracy**: Percentage of orders delivered correctly
- **Time Statistics**: Min/Max/Average seconds per order

### Item Analysis
- **Drink Frequency**: Which drinks customers order most
- **Topping Statistics**: How many toppings were used in orders
- **Daily Summary**: Performance breakdown by day

## Tips
- You can open the stats popup at any time during gameplay
- Opening stats doesn't pause the game (it's just an overlay)
- Stats update in real-time based on CSV data from completed orders
- First time playing? Stats will show "0" until you complete orders

## Technical Details

### Data Source
Statistics are read from the CSV file saved in `collecting_data/` folder:
- Each row = one completed order
- Columns: Day, OrderID, ItemPrice, ToppingsUsed, DrinkType, OrderAccuracy, TimeTaken

### CSV Columns Explained
- **Day**: Which day of gameplay (1, 2, 3, etc.)
- **OrderID**: Order number (1, 2, 3, etc.)
- **ItemPrice**: Amount earned from that order
- **ToppingsUsed**: Number of toppings on the pizza
- **DrinkType**: Name of drink ordered (Coke, Sprite, Water, Milkshake)
- **OrderAccuracy**: "Correct" if order matched customer request
- **TimeTaken**: Seconds to complete the order
