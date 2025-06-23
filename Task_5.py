"""Задача 5: Система интернет-магазина с миксинами и композицией
Создай систему интернет-магазина, используя миксины для добавления функциональности
скидок и композицию для работы с корзиной.
Каждый товар должен иметь название, цену, категорию. Реализуй миксины для различных типов скидок
(процентная, фиксированная, по количеству).
Корзина должна содержать товары и уметь рассчитывать общую стоимость с учетом скидок"""


class Product:
    """
    Представляет товар в интернет-магазине.
    """

    def __init__(self, name: str, price: float, category: str) -> None:
        self.name = name
        self.price = price
        self.category = category

    def get_info(self) -> str:
        return f"{self.name}: {self.price} руб."


class Discount:
    """
    Базовый интерфейс скидки.
    """

    def apply(self, product: Product, quantity: int = 1) -> float:
        return product.price


class PercentDiscount(Discount):
    """
    Скидка в процентах от цены товара.
    """

    def __init__(self, percent: float) -> None:
        self.percent = percent

    def apply(self, product: Product, quantity: int = 1) -> float:
        return product.price * (1 - self.percent / 100)


class FixedDiscount(Discount):
    """
    Фиксированная скидка в рублях.
    """

    def __init__(self, amount: float) -> None:
        self.amount = amount

    def apply(self, product: Product, quantity: int = 1) -> float:
        return max(0, product.price - self.amount)


class QuantityDiscount(Discount):
    """
    Скидка, зависящая от количества.
    """

    def __init__(self, percent_per_extra: float) -> None:
        self.percent_per_extra = percent_per_extra

    def apply(self, product: Product, quantity: int = 1) -> float:
        if quantity <= 1:
            return product.price
        discount = self.percent_per_extra / 100 * (quantity - 1)
        return product.price * (1 - discount)


class DiscountedProduct:
    """
    Объект товара с применяемой скидкой.
    """

    def __init__(self, product: Product, discount: Discount) -> None:
        self.product = product
        self.discount = discount

    def get_price(self, quantity: int = 1) -> float:
        return self.discount.apply(self.product, quantity)


class ShoppingCart:
    """
    Корзина покупателя
    """

    def __init__(self) -> None:
        self.items = []

    def add_product(self, product, quantity=1):
        self.items.append((product, quantity))

    def get_total(self) -> float:
        total = 0
        for product, quantity in self.items:
            if isinstance(product, DiscountedProduct):
                total += product.get_price(quantity) * quantity
            else:
                total += product.price * quantity
        return total


product1 = Product("Ноутбук", 50000, "Электроника")
product1 = DiscountedProduct(product1, PercentDiscount(10))
product2 = Product("Мышь", 1000, "Электроника")
product2 = DiscountedProduct(product2, FixedDiscount(100))

cart = ShoppingCart()
cart.add_product(product1, 1)
cart.add_product(product2, 2)
print(cart.get_total())
