'''
Problem:
    You are trying to design starbucks. You have a Beverage base class and
    3 beverages (HouseBlend, DarkRoast, Decaf) that extends the beverage base class.
    As you know, you can add condiments (Milk, Sugar, Tea )
    to the your beverage. How would you design this ?
    The design should flexible enough so that it can support new beverages, condiments,
    and different combinations of condiments.

Two ways:
   - Create a a bunch of classes (HouseBlendWithMilk, HouseBlendWithMilkAndSugar)
     -> Obviously, not feasible since it would lead to a very large amount of classes
     as the number of condiments
   - Put all the condiments in the base and logic for computing the condiment cost in the
   base class and each subchild's cost method calls super().cost + self.cost.
     -> A couple of problems:
        -> The classes inherits a lot of methods that they don't need. Sign of a bad
        design.
        -> Adding new condiments would require updating the base class which violates
        Open/Closed principle (open for extension, closed for modification)

Why can inheritance lead to an inflexible design ?
- Behavior is set during compile time i.e the subclass of a parent class either
keeps the parent classes's behavior or overrides it. But once these are coded,
they cannot be changed during run time.
- Can lead to the subclasses inherting a lot of stuff that they don't need.

Decorator pattern to the rescue!
- attaches additional responsibilities to an object dynamically and is a flexible
alternative for subclassing for extending functionality.

Decorators typically is the same type as the decorator is it is wraping (has - a)
and implements most of the same methods as the wrapped class.

At a high level, we wrap the object (in this case Beverage) with Decorators which our condiments.

MILK -> SOY -> (House Blend)

When it's time to compute the cost, we call milk.cost() -> soy.cost() -> houseBlend.cost()
and comes back up. Very similar to recursion.

To implement the decorator pattern,
1. We introduce a CondimentDecorator class that extends the beverage.
    - This class takes a Beverage (could be a beverage or another condiment) and
    implements getDescription/cost method
        - We only implement the methods that we want to extend.
        - For example, here the decorators implement the getDescription and cost method
        because for each condiment, we want to add a cost/description in addition to the
        beverage.
2. Create Decorators
3. Wrap and call cost.

Okay. So composition is all good and stuff but
what allow us to write programs using compositions ?
- Object have a reference to other objects.
- Each of these objects encapsulate some behavior -> Allows for reusability.
- These objects are referenced via the abstract type rather
than a concrete class type. (Dependency Inversion)
- This allows to change the object during run time because it is of an abstract type, so
can be replaced with any object that replace this type.
A good demonstration of this is the Strategy Pattern.
- Additionally because it is an abstract class, if we add new classes in the case of
the Observer pattern new observers, the client (Subject) does not need to be changed so
promote adherence to Open for extension and closed for modification principle. Also,
demonstrate how composition promotes loose coupling.
'''
from abc import ABC, abstractmethod

class Beverage(ABC):
    @abstractmethod
    def get_description(self)->str:
        pass
    @abstractmethod
    def cost(self)->float:
        pass

class HouseHold(Beverage):
    def get_description(self):
        return "House Hold"
    def cost(self):
        return 1.00

class Decaf(Beverage):
    def get_description(self):
        return "Decaf"
    def cost(self):
        return 3.00

class DarkRoast(Beverage):
    def get_description(self):
        return "Dark Roast"
    def cost(self):
        return 2.00

class CondimentDecorator(Beverage):
    def __init__(self, beverage:Beverage):
        self.beverage = beverage

class Milk(CondimentDecorator):
    def __init__(self, beverage:Beverage):
        super().__init__(beverage)

    def get_description(self) -> str:
        return "Milk," + self.beverage.get_description()

    def cost(self) -> float:
        return 0.10 + self.beverage.cost()

class Honey(CondimentDecorator):
    def __init__(self, beverage:Beverage):
        super().__init__(beverage)

    def get_description(self) -> str:
        return "Honey," + self.beverage.get_description()

    def cost(self) -> float:
        return 0.20 + self.beverage.cost()

class Sugar(CondimentDecorator):
    def __init__(self, beverage:Beverage):
        super().__init__(beverage)

    def get_description(self) -> str:
        return "Sugar,"  + self.beverage.get_description()

    def cost(self) -> float:
        return 0.30 + self.beverage.cost()

'''
Modeling a pizza:
    - A pizza can have a lot of different toppings.
    - Using inheritance to model all the different types would be a lot of classes.
    Let's use decorators to solve this issue for us.

    Core Entities:
        Pizza
            - method
                - cost() -> Returns the cost of a basic pizza
                - get_description() -> Just returns pizza (BORING!:())
        PizzaCondimentDecorator
            - method
                - Constructor takes in a Pizza (which can be the actual pizza or
                    a decorator)
                - cost() -> Returns the cost of each condiment + the object it's wrapping
                - get_description() -> Name of the condiment
'''
class IPizza(ABC):
    @abstractmethod
    def cost(self)->float:
        pass
    @abstractmethod
    def get_description(self)->str:
        pass

class Pizza(IPizza):
    def cost(self) -> float:
        return 2.00
    def get_description(self) -> str:
        return "Pizza"

class PizzaCondimentDecorator(IPizza):
    def __init__(self, pizza:IPizza):
        self.pizza = pizza
    @abstractmethod
    def cost(self)->float:
        pass

    @abstractmethod
    def get_description(self)->str:
        pass

class Cheese(PizzaCondimentDecorator):
    def __init__(self, pizza: IPizza):
        super().__init__(pizza)

    def cost(self) -> float:
        return 0.50 + self.pizza.cost()

    def get_description(self) -> str:
        return "Chesse, " + self.pizza.get_description()

class Pepporoni(PizzaCondimentDecorator):
    def __init__(self, pizza: IPizza):
        super().__init__(pizza)

    def cost(self)->float:
        return 0.75 + self.pizza.cost()

    def get_description(self) -> str:
        return "Pepporoni, " + self.pizza.get_description()

if __name__ == '__main__':
    # Just a decaf
    decaf = Decaf()
    print(f"Price of a {decaf.get_description()} is {decaf.cost()}")
    # Decaf with Milk
    decaf = Milk(Decaf())
    print(f"Price of a {decaf.get_description()} is {decaf.cost()}")

    # Decaf with Milk Honey
    decaf = Honey(Milk(Decaf()))
    print(f"Price of a {decaf.get_description()} is {decaf.cost()}")

    # A regular boring pizza
    pizza = Pizza()
    print(f"Price of a {pizza.get_description()} is {pizza.cost()}")
    # A cheese pizza. meh okay.
    pizza = Cheese(Pizza())
    print(f"Price of a {pizza.get_description()} is {pizza.cost()}")
    # A cheese pizza. meh okay.
    pizza = Pepporoni(Cheese(Pizza()))
    print(f"Price of a {pizza.get_description()} is {pizza.cost()}")
