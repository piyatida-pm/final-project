import random

class Food:
    def __init__(self, name, price, base_upgrade):
        self.name = name
        self.price = price
        self.base_upgrade_price = base_upgrade
        self.current_upgrade_price = self.base_upgrade_price

class Topping(Food):
    def __init__(self, name, price, base_upgrade):
        super().__init__(name, price, base_upgrade)
    
    def add_topping(self, pizza):
        if type(pizza) == Pizza:
            pizza.pizza_lst.append(self)
        else:
            print("This one is not a pizza.") 

class Drink(Food):
    def __init__(self, name, price, base_upgrade):
        super().__init__(name, price, base_upgrade)
    
    def add_drink(self, order):
        if type(order) == Order:
            order.lst_complete_order.append(self)
        else:
            print("This one is not an order.")         

class Pizza:
    def __init__(self):
        self.pizza_lst = []
        self.pizza_price = 10

    def cal_topping(self):
        for i in self.pizza_lst:
            if type(i) != Topping:
                pass
            else:
                self.pizza_price += i.price
    
    def del_topping(self):
        self.pizza_lst = []

    def __eq__(self, other):
        if isinstance(other, Pizza):
            # Compare toppings by name, ignoring order
            self_toppings = sorted([t.name for t in self.pizza_lst])
            other_toppings = sorted([t.name for t in other.pizza_lst])
            return self_toppings == other_toppings
        else:
            return False

class Order:
    possible_name = ["Kendo","Jimmy","Shu","Momo","Oliver", "Theodore", "Arthur", "Felix", "Asher", "Eleanor", "Aurora", "Stella", "Chloe", "Luna", "Rowan", "Quinn", "Avery", "Morgan", "Nova", "Eden"]
    def __init__(self):
        self.lst_order = []
        # populate order - do when start pygame
        self.lst_complete_order = []
        self.customer_name = random.choice(self.possible_name)

    def __str__(self):
        return self.customer_name
    
    def add_item_to_order(self,item):
        if type(item) == Pizza or type(item) == Drink:
            self.lst_complete_order.append(item)
        else:
            print("Something went wrong!")

    def check_and_send_order(self):
        for i in self.lst_order:
            for j in self.lst_complete_order:
                if i == j:
                    self.lst_order.remove(i)
                    self.lst_complete_order.remove(j)
                    #add money
    def del_drink(self, order):
        temp = []
        for i in order.lst_complete_order:
            if type(i) != Drink:
                temp.append(i)
        
        order.lst_complete_order = temp

    
class ManagerCustomers:
    def __init__(self):
        self.max_customer = random.randint(20, 30)
        self.orders_per_day = []
        self.populate_customers()
        self.current_customer = len(self.orders_per_day)
    
    def populate_customers(self):
        for i in range(self.max_customer):
            self.orders_per_day.append(Order())

    def del_customer(self):
        if self.current_customer > 0:
            self.orders_per_day.pop(0)
            self.current_customer -= 1
        else:
            print("Don't have customer here!")

    def clear_customer(self):
        self.orders_per_day = []
        self.current_customer = 0


# Topping(name,price,base_upgrade)
topping_pesto = Topping("Pesto Sauce",30,300)
topping_mushroom = Topping("Mushroom",35,200)
topping_cheese = Topping("Cheese",10,150)
topping_pepperoni = Topping("Pepperoni",10,200)
topping_bacon = Topping("Bacon",40,150)
topping_pineapple = Topping("Pineapple",40,100)

drink_coke = Drink("Coke",30,150)
drink_sprite = Drink("Sprite",30,150)
drink_water = Drink("Water",20,100)
drink_milkshake = Drink("Milkshake",40,200)

class Restaurant:
    topping_lst = [topping_pesto,topping_mushroom,topping_cheese,topping_pepperoni,topping_bacon,topping_pineapple]
    drinks_lst = [drink_coke,drink_water,drink_sprite,drink_milkshake]
    money = 0
    
    def upgrade_topping(self, number):
        topp = self.topping_lst[number]
        if number >= 0 and number <= len(self.topping_lst) - 1:
            if self.money >= topp.current_upgrade_price:
                self.money -= topp.current_upgrade_price
                topp.price += topp.price * 0.1
                topp.current_upgrade_price += topp.current_upgrade_price * 0.5
            else:
                print("Not enough money.")
        else:
            print("Not in topping list.")
    
    def upgrade_drink(self, number):
        drinks = self.drinks_lst[number]
        if number >= 0 and number <= len(self.drinks_lst) - 1:
            if self.money >= drinks.current_upgrade_price:
                self.money -= drinks.current_upgrade_price
                drinks.price += drinks.price * 0.1
                drinks.current_upgrade_price += drinks.current_upgrade_price * 0.5
            else:
                print("Not enough money.")
        else:
            print("Not in drink list.")        

        





# order1 = Order()
# order2 = Order()

# print(order1.customer_name)
# print(order2)

# manage = ManagerCustomers()
# for i in manage.orders_per_day:
#     print(i)

# print("\n", len(manage.orders_per_day))

# # DELETE
# manage.DelCustomer()
# for i in manage.orders_per_day:
#     print(i)

# print("\n", len(manage.orders_per_day))

# # CLEAR
# manage.ClearCustomer()
# for i in manage.orders_per_day:
#     print(i)

# print("\n", len(manage.orders_per_day))