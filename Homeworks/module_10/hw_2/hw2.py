"""
Make it possible to use different discount programs.
Hint: use strategy behavioural OOP pattern.
https://refactoring.guru/design-patterns/strategy

"""


class Order:
    def __init__(self, price, discount_function):
        self.price = price
        self.discount_function = discount_function

    def final_price(self):
        return self.discount_function(self)


def morning_discount(order):
    return order.price / 2


def elder_discount(order):
    return order.price / 10


order_1 = Order(100, morning_discount)
assert order_1.final_price() == 50

order_2 = Order(100, elder_discount)
assert order_2.final_price() == 10
