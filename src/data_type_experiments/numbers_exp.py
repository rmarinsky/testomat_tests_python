# - int, float; operations; math; string to number

index = 10
print(index)

price = 10.99
print(price)

price_from_text = float("10.98")
print(price_from_text + 4.02)

index_of_page = "2"
print(int(index_of_page) + 1)

actual_prices: list[str] = ["10.99", "99.43", "12.02"]

print(actual_prices)
print(max(actual_prices))


def is_first_price_the_highest(t_prices: list[str]):
    popo = "poposd"
    return t_prices[0] == max(t_prices)


print(is_first_price_the_highest(actual_prices))

actual_prices.sort(reverse=True)
print(actual_prices)

print(is_first_price_the_highest(actual_prices))

print(int(index_of_page) + 909898)


class Popo:

    def __init__(self, name: str):
        self.name = name
        self.ueryueyr = name

    def prinooo(self):
        print(self.name)

    def asdlkfjds(self):
        print(self.name)
        print(self.ueryueyr)

    def get_popo_name(self):
        return self.name

    def print_popo_name(self):
        print(self.get_popo_name())


Popo("Popovko").print_popo_name()
