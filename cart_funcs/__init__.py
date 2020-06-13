import csv

class Cart():
    def __init__(self):
        self.cart = []
        self.itemdb = ItemDB()

    def get_cartitem_ids(self):
        ids = [item.item_id for item in self.cart]
        return ids

    # add CartItem to cart
    def add_item_to_cart(self, id, amount):
        if id in self.get_cartitem_ids():
            idx = self.get_cartitem_ids().index(id)
            self.cart[idx].amt += amount
        else:
            self.cart.append(CartItem(id, amount))
        
    # remove CartItem from cart
    def remove_item_from_cart(self, id, amount):
        if self.cart[id]:
            item = self.cart[id]
            if amount > item.amt:
                print("That's more than you had in cart, so we'll just remove them all.")
                item.amt = 0
            else:
                item.amt -= amount
                # TODO add item name to printout below through itemdb
                print(f"{amount} removed from the cart.")
            self.purge_zero_amt_cartitems()
        else:
            print("Item id not found in cart. Sorry")

    def purge_zero_amt_cartitems(self):
        for idx, item in enumerate(self.cart):
            if item.amt == 0:
                self.cart.pop(idx)
        print("Purged zero amt items")
    
    # show cart total
    def get_cart_total(self):
        total = 0
        for item in self.cart:
            total += self.itemdb.get_item_price(item.item_id) * item.amt
        return total
    # clear cart
    def clear_cart(self):
        self.cart = []

    def show_cart(self):
        print("="*50)
        print("Your cart contains:")
        if len(self.cart) == 0:
            print("Your cart is currently empty.")
            return True
        for idx, cartitem in enumerate(self.cart):
            item_name, item_price = self.itemdb.get_item_info(cartitem.item_id)
            print(f"{idx}: {item_name} X {cartitem.amt} @ ${item_price}")
        print(f"Cart total is: ${self.get_cart_total()}")
        print("="*50)

class CartItem():
    def __init__(self, item_id, amt=1):
        self.item_id = item_id
        self.amt = amt
    # Maintain list of cart items by id and amounts

class ItemDB():
    def __init__(self):
        self.itemdb = {}
        with open('./item_list.csv', newline='') as item_csv:
            item_reader = csv.DictReader(item_csv)
            for row in item_reader:
                self.itemdb[int(row['id'])] = Item(row['id'], row['name'], row['price'])
    # fill items db from csv
    # get item info by id
    def get_item_info(self, id):
        return self.itemdb[id].name, self.itemdb[id].price
    # get item price by id
    def get_item_price(self, id):
        return self.itemdb[id].price


class Item():
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = float(price)

    def get_item_info(self):
        li = f"{self.id}: {self.name} - ${self.price}"
        return li



class App():
    def __init__(self):
        self.cart = Cart()
        self.show_shopper_welcome()
        self.main()
    
    # Show menu
    def main(self):
        while True:
            self.show_cart()
            op = input("What would you like to do? (a)dd item, (r)emove item, (s)how cart, (c)lear cart, or (q)uit?").lower()
            if op not in ["a", "r", "s", "c", "q"]:
                print("Sorry, that's not a valid option. Please try a, r, s, c, or q")
                continue
            if op == "a":
                # show add menu
                self.show_add_menu()
                # do add
                item_to_add = input("Please enter an item id to add. (the id is to the left of each name) ")
                amount_to_add = input("How many of those would you like to add? ")
                if type(int(item_to_add)) == int and int(item_to_add) in self.cart.itemdb.itemdb.keys():
                    self.cart.add_item_to_cart(int(item_to_add), int(amount_to_add))
                    # I'm converting item_to_add to int too often, maybe do it first or use function to check id in itemdb.
            elif op == "r":
                #show remove menu
                self.show_remove_menu()
                item_to_remove = int(input("Please enter the id of the item to remove. (id is left of name) "))
                amount_to_remove = input("How many to remove? (enter a number or 'all' to remove all) ")
                if amount_to_remove.lower() == "all":
                    # Obviously this breaks if the add more than 100000 of an item to cart
                    self.cart.remove_item_from_cart(item_to_remove, 1000000)
                elif int(amount_to_remove) <= 0:
                    print("Okay, why more zero or negative?")
                else:
                    self.cart.remove_item_from_cart(item_to_remove, int(amount_to_remove))
                # do remove
            elif op == "s":
                self.show_cart()
            elif op == "c":
                # show confirmation
                confirm = input("Are you sure you want to clear cart? (Y/n)")
                if confirm.lower() == 'y':
                    # confirmed, clear cart
                    self.cart.clear_cart()
                elif confirm.lower() == 'n':
                    print("Probably a good choice")
                else:
                    print("That's not Y or N, so we'll assume you want to keep your cart.")
            else:
                break

    def show_cart(self):
        self.cart.show_cart()
        print("="*50)

    def show_remove_menu(self):
        print("="*50)
        self.show_cart()


    def show_add_menu(self):
        print("Available Items:")
        print("="*50)
        # TODO I don't like how I'm repeating itemdb, but not sure how to expose it without the extra layer
        for k, v in self.cart.itemdb.itemdb.items():
            print(f"{k}: {v.name} - ${v.price}")
    
    # perform cart actions
    def show_shopper_welcome(self):
        print("="*50)
        print("Welcome to Wally-World.")
        