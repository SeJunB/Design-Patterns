'''
Let's say you have a Duck abstract class and two subclasses,
Rubber Duck and MallardDuck (a real duck), that inherit from the Duck ABC.
How would you implement a quack method ?
- I can think of two approaches:
    - Add `quack` to the Duck class and provide it a default implementation.
    Since a RubberDuck cannot quack, we override the default behavior.
    - Add  `quack` as an abstract method and let the subclasses implement it.

Both solution works but there are a couple of annyoing things:
    - In both cases, if I add a new duck for ex SupermanDuck, then the SupermanDuck
    would have to either use the default quack method or define its own quack method.
    Also, if I wanted to re-use a quack method of another duck class say SuperheroDucker and
    use it in the SupermanDuck class, this would not be possible.

Why is it such a pain ?
- It is such a pain because each class inherits the quack behavior from the parent and
must override it. Since it is inherited, there is no way for each subclasses to access each others
quack method.

Encapsulation to the rescue:
The simple idea behind encapsulation is to take the things that vary in the above example (the behavior
of the ducks) into its own class and require each of the client to uses the encapsulated class
to call the behavior.
In other words, moves the behavior from an inseparable part of the class to something that the
class has, a HAS-A relationship.

How can we implement this idea in the duck class ?
- The `quack` method is likely to vary from each of the Duck's subclass, so we encapsulate it by
creating a `QuackBehavior`. This class is an abstract class and represents the `quack` behavior.
- Then, for each of the specific quack behavior, we create classes that "implements" the `quack` behavior.
For example, Squeak, Quack, LoudQuack, etc.
- Then, update the Duck class to take in a `QuackBehavior` as an instance variable (`quackBehavior`)
and define a `quack` method which simply calls the `quackBehavior.quack`.
- BONUS: `quackBehavior` can be any classes that implement the `QuackBehavior` so
we can create a method called `set_quack_behavior(quackBehavior QuackBehavior)` and call
this method to dynamically update the quackBehavior during run time.

What are the benefits:
    - Each of the subclass of `Duck` do not have to implement a quack method.
    It simply provides the `QuackBehavior` it wants in the constructor and can be changed
    by using the `set_quack_behavior` method.
    - `QuackBehavior` are re-usable. Previously, if a subclass of `Duck` had a `quack` method
    and you wanted to re-use this in another class, this was not easy. But now since that `quack` method
    behavior is in a class, it can easily be re-used.
    - Complys with DI (Dependency Inversion principle - Program to an interface not concrete implementation)
    and more importantly (O - Open for extension, closed for modification).
    If I wanted to add new quack behaviors to the Duck class, I just have to create a `QuackBehavior` class
    and the `Duck` class does not need to be modified.

This pattern is known as the Strategy Pattern, which defines a family of algorithms,
encapsulates each one, and make them interchageable by making each implement a shared interface.

A question to consider:
    - Instead of this, couldn't we have created a Quackable interface and forced the subclasses to
    implement it ?
    Yes, that's a decent idea but a bad solution for the following reasons:
        1. A lot of code duplication. Now each class subclass will have to implement its own
        `quack` method. So for 30 Duck classes potentially 30 `quack` methods.
        2. Related to 1, but with this design, we are not able to re-use `quack`.
        If I want `quack` method in one class in another class, it would be hard.
        Well not really, I could copy and paste it but this is a sign that you should probably
        reconsider your approach.

'''
from abc import ABC, abstractmethod

class QuackBehavior(ABC):
    @abstractmethod
    def quack(self):
        pass

class Squeak(QuackBehavior):
    def quack(self):
        print("Squeak squeak")

class Quack(QuackBehavior):
    def quack(self):
        print("Quack Quack")

class LoudQuack(QuackBehavior):
    def quack(self):
        print("Loud Quack Quack")

class Duck(ABC):
    def __init__(self, quackBehavior:QuackBehavior):
        self.set_quack_behavior(quackBehavior)

    def quack(self):
        self.quackBehavior.quack()

    def set_quack_behavior(self, quackBehavior):
        self.quackBehavior: QuackBehavior = quackBehavior

class MallardDuck(Duck):
    def __init__(self):
        super().__init__(Quack())

class RubberDuck(Duck):
    def __init__(self):
        super().__init__(Squeak())

class SuperHeroDuck(Duck):
    def __init__(self):
        super().__init__(LoudQuack())


if __name__ == '__main__':
    mallardDuck = MallardDuck()
    mallardDuck.quack()
    rubberDuck = RubberDuck()
    rubberDuck.quack()
    superHeroDuck = SuperHeroDuck()
    superHeroDuck.quack()
    # Changing quackBehavior at runtime.
    superHeroDuck.set_quack_behavior(Squeak())
    superHeroDuck.quack()
