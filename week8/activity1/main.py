class Pizza:
    def prepare(self):
        print("Cooking Pizza");

class Burger:
    def prepare(self):
        print("Cooking Burger");

class Pasta:
    def prepare(self):
        print("Cooking Pasta");

#Factory
class FoodFactory:
    @staticmethod
    def create(type):
        type_lower = str.lower(type)

        if type_lower == "pizza":
            return Pizza()
        elif type_lower == "burger":
            return Burger()
        elif type_lower == "pasta":
            return Pasta()
        else:
            raise ValueError("Unknown food type")

def main():
    food = FoodFactory.create("Burger")
    food.prepare()

if __name__ == "__main__":
    main()
