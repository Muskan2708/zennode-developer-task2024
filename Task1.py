import math
# Class representing the catalog of products and their prices
class Catalogue:
    def __init__(self):
        self.products_prices = {"Product A": 20, "Product B": 40, "Product C": 50}

# Class representing the shopping cart
class Shopping_Cart:
    def __init__(self, catalog):
        self.catalog = catalog
        self.cart = {}
        self.total_quantity = 0
        self.subtotal = 0
        self.total_cart_value = 0
        self.gift_wrap_total = 0
        self.shipping_fee_total = 0
        self.discount_name = None
        self.order_total = 0

    # Method to add items to the shopping cart
    def add_to_cart(self, product_name, product_quantity, gift_wrap, product_total):
        # Record product details in the cart
        self.cart[product_name] = {"product_quantity": product_quantity, "gift_wrap": gift_wrap, "product_total": product_total}
        # Update total quantity and cart value
        self.total_quantity += product_quantity
        self.total_cart_value += product_total
        self.subtotal = self.total_cart_value

        # Update gift wrap and shipping fees
        if gift_wrap:
            self.gift_wrap_total += product_quantity
        self.shipping_fee_total = math.ceil(self.total_quantity / 10) * 5

        # Calculate applicable discounts
        self.discount()
        # Update the order total
        self.order_total = self.subtotal + self.shipping_fee_total + self.gift_wrap_total

    # Method to calculate discounts based on specific rules
    def discount(self):
        # Store the original subtotal for comparison
        subtotal_after_discount=self.subtotal

        # Check for a flat $10 discount if the total cart value exceeds $200
        if self.total_cart_value > 200:
            subtotal_after_discount = self.total_cart_value - 10
            # Updating the subtotal and discount name if the discount seems maximum of all so far
            if subtotal_after_discount < self.subtotal:
                self.subtotal = subtotal_after_discount
                self.discount_name = "flat_10_discount"

        # Check for a 5% bulk discount on individual products if quantity exceeds 10 units
        subtotal_after_discount = self.total_cart_value
        for product in self.cart:
            if self.cart[product]["product_quantity"] > 10:
                discount_amount = self.cart[product]["product_total"]* 0.05
                self.cart[product]["product_total"]=self.cart[product]["product_quantity"]*self.catalog.products_prices[product]-discount_amount
                subtotal_after_discount -= discount_amount
        # Updating the subtotal and discount name if the discount seems maximum of all so far
        if subtotal_after_discount < self.subtotal:
            self.subtotal = subtotal_after_discount
            self.discount_name = "bulk_5_discount"

        # Check for a 10% bulk discount on the total cart value if quantity exceeds 20 units
        subtotal_after_discount = self.total_cart_value
        if self.total_quantity > 20:
            subtotal_after_discount -= subtotal_after_discount * 0.01
            # Updating the subtotal and discount name if the discount seems maximum of all so far
            if subtotal_after_discount < self.subtotal:
                self.subtotal = subtotal_after_discount
                self.discount_name = "bulk_10_discount"

        # Check for a tiered 50% discount if total quantity exceeds 30 and any product quantity is above 15
        subtotal_after_discount = self.total_cart_value
        if self.total_quantity > 30:
            for product in self.cart:
                if self.cart[product]["product_quantity"] > 15:
                    discount_amount=(self.cart[product]["product_quantity"]-15)*self.catalog.products_prices[product]*0.5
                    self.cart[product]["product_total"] = self.cart[product]["product_quantity"]*self.catalog.products_prices[product]-discount_amount
                    subtotal_after_discount -= discount_amount
            # Updating the subtotal and discount name if the discount seems maximum of all so far
            if subtotal_after_discount < self.subtotal:
                self.subtotal = subtotal_after_discount
                self.discount_name = "tiered_50_discount"

# Class representing the shopping invoice
class Shopping_Invoice:
    def __init__(self, cart):
        self.cart = cart

    # Method to print the shopping invoice
    def print_invoice(self):
        print("Thank You for shopping with us. Following are the details of your order: ")
        for product in self.cart.cart:
            print("Product Name: " + product + "    Product Quantity:" +
                  str(self.cart.cart[product]["product_quantity"]) +
                  "    Product Total :" + str(self.cart.cart[product]['product_total']))
        print(f"Subtotal: {self.cart.subtotal}")
        print(f"Discount Applied : {self.cart.discount_name}    Discount Amount : "
              f"{self.cart.total_cart_value - self.cart.subtotal}")
        print(f"Shipping Fee :{self.cart.shipping_fee_total}    Gift Wrap Fee :{self.cart.gift_wrap_total}")
        print(f"Total :{self.cart.order_total}")

# Initializing the catalog
catalog = Catalogue()
# Initializing the Shopping Cart
cart = Shopping_Cart(catalog)

# User input loop to add items to the cart
while True:
    for product in catalog.products_prices:
        quantity = int(input(f"Enter the purchase quantity of {product} (price ${catalog.products_prices[product]}) : "))
        if quantity > 0:
            gift = input('Do you want a gift wrap also (price:$1 per unit) ? y/n ')
            gift_wrap = True if gift == 'y' else False
            product_total = quantity * catalog.products_prices[product]
            # Add item to the cart
            cart.add_to_cart(product, quantity, gift_wrap, product_total)

    # Generating and displaying the shopping invoice
    invoice = Shopping_Invoice(cart)
    invoice.print_invoice()
    # Asking user if ordering again
    order_again = input("Do you want to order again? y/n ")
    # Finishing the order or exiting the loop
    if order_again=='n':
        break