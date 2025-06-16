"""
Задача 5: Система интернет-магазина с миксинами и композицией
Создай систему интернет-магазина, используя миксины для добавления функциональности
скидок и композицию для работы с корзиной.
Каждый товар должен иметь название, цену, категорию. Реализуй миксины для различных типов скидок
(процентная, фиксированная, по количеству).
Корзина должна содержать товары и уметь рассчитывать общую стоимость с учетом скидок
"""


class Product:
    def __init__(self, name, price, chapter):
        self.name = name
        self.price = price
        self.chapter = chapter

    def get_info(self):
        return f"{self.name}: {self.price} руб."


class PercentDiscountMixin:
    def set_percent_discount(self, discount):
        self.price -= self.price * (discount / 100)


class FixedDiscountMixin:
    def set_fixed_discount(self, discount):
        self.price -= discount


class QuantityDiscountMixin:
    def set_quantity_discount(self, quantity, discount):
        if quantity >= 1:
            self.price -= self.price * (discount / 100) * (quantity - 1)


class DiscountedProduct(Product, PercentDiscountMixin, FixedDiscountMixin):
    def __init__(self, name, price, chapter):
        Product.__init__(self, name, price, chapter)


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        self.items.append(product)

    def get_total(self):
        return sum(item.price for item in self.items)


class OnlineStore:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)


product1 = DiscountedProduct("Ноутбук", 50000, "Электроника")
product1.set_percent_discount(10)
product2 = DiscountedProduct("Мышь", 1000, "Электроника")
product2.set_fixed_discount(100)

cart = ShoppingCart()
cart.add_product(product1, 1)
cart.add_product(product2, 2)
print(cart.get_total())
