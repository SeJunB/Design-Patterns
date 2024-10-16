'''
Problem:
    Let's say you have a WeatherData class that gets updated by the system
    by calling the setMeasurement method every hour.
    We want to implement 3 displays (TemperatureDisplay, HumiditiyDisplay, and PressureDisplay).

How would you implement this naively ?
- Create a WeatherData class.
- Create TemperatureDisplay, HumidityDisplay, and PressureDisplay.
  - Since they are all related to display, create an interface called Display with
  one method `display`.
- The WeatherData class would have the three display classes as instance variables
and update the state when measurements are updated.

The main problem with this approach is that the WeatherData is tightly coupled to the
Display classes. As a result, if we need to add a new display, we would have to update the
WeatherData class to support the new display.

Hmm, okay. Then, what's loose coupling ? All loose coupling means is that the two objects
know very little about each other. As a result, this gives us a lot of flexibility and allow
us to modify one without modifying the other and can be re-used.
LOOSE COUPLING DOES NOT MEAN THAT OBJECTS DON'T DEPEND ON EACH OTHER. They still do but
they do not know each other much.

Observer pattern defines a one to many dependency between objects so that when one object
changes state, all of its dependents are notified and updated automatically.
In our example, the observer pattern will allow us to solve our problem using a loosely coupled
design.


2 Entities to the observer pattern
- Subject - The one who has the state and need to notify others (known as observers)
  - methods:
    - registerObserver
    - removeObserver
    - notifyObservers
    - a method for updating the state of the subject and calls notifyObservers
    ... getter for state
- Observer - The one who needs data from the subject
    - update() method

Flow:
    1. Observer register with the subject.
        - Observers typically have a constructor that takes in the Subject.
    2. When subject has new data, it calls the notifyObserver method
    which iterates through all of its observer and calls `update` on each of the
    observer.
    3. In the update method, the observer get the necessary state by using the
    Subject's getter and do any additional work that is necessary.

The above flow is a "pull-based" observer pattern. That is, the subject doesn't send
any data to the observer and the observer "pulls" the data it needs.
The downside of push based pattern is that if we add more stuff to the WeatherData,
the interface would have to be updated and this can be a pain in the butt.

The main benefit of the Observer pattern is two things:
    - We can add new observers without modifying the Subject. A new observer
    can just implement the Observer interface and register itself to the Subject.
    - Pull based observer pattern allow us to update the subject without updating the
    observers. For example, adding pollen levels only require changes to the Subject code.
    - Add/Remove observers during run time.

Another application of observer pattern is designing a button with event listeners.
- The button is the Subject
- The event listeners are the observers.

'''
from abc import ABC, abstractmethod
from enum import IntEnum, auto
from typing import Sequence
from typing_extensions import List

class Observer(ABC):
    @abstractmethod
    def update(self):
        pass

class Subject(ABC):
    @abstractmethod
    def registerObserver(self, observer:Observer):
        pass

    @abstractmethod
    def removeObserver(self, observer:Observer):
        pass
    @abstractmethod
    def notifyObservers(self):
        pass

class Display(ABC):
    @abstractmethod
    def display(self):
        pass

class WeatherData(Subject):
    def __init__(self):
        self.observers: List[Observer] = []
        self.temperature = 0.0
        self.pressure = 0.0
        self.humidity = 0.0
        self.pollen = 0.0
    def get_pollen(self):
        return self.pollen

    def get_temperature(self):
        return self.temperature

    def get_pressure(self):
        return self.pressure

    def get_humidity(self):
        return self.humidity

    def registerObserver(self, observer:Observer):
        self.observers.append(observer)

    def removeObserver(self, observer:Observer):
        self.observers.remove(observer)

    def notifyObservers(self):
        for observer in self.observers:
            observer.update()

    def set_measurements(self, temperature:float, pressure:float, humidity:float, pollen:float):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.pollen = 15
        self.notifyObservers()

class TemperatureDisplay(Display, Observer):
    def __init__(self, subject:WeatherData):
        self.temperature = 0.0
        self.subject = subject

    def display(self):
        print(f"The current temperature is: {self.temperature}")

    def update(self):
        self.temperature = self.subject.get_temperature()
        self.display()

class HumidityDisplay(Display, Observer):
    def __init__(self, subject:WeatherData):
        self.humidity = 0.0
        self.subject = subject

    def display(self):
        print(f"The current humidity is: {self.humidity}")

    def update(self):
        self.humidity= self.subject.get_humidity()
        self.display()

class PressureDisplay(Display, Observer):
    def __init__(self, subject:WeatherData):
        self.pressure = 0.0
        self.subject = subject

    def update(self):
        self.pressure = self.subject.get_pressure()
        self.display()

    def display(self):
        print(f"The current pressure is: {self.pressure}")

class PollenDisplay(Display, Observer):
    def __init__(self, subject:WeatherData):
        self.pollen = 0.0
        self.subject = subject

    def update(self):
        self.pollen = self.subject.get_pollen()
        self.display()

    def display(self):
        print(f"The current pollen is: {self.pollen}")

class ButtonState(IntEnum):
    ON=auto()
    OFF=auto()

class Button(Subject):
    def __init__(self):
        self._state = ButtonState.ON
        self.observers:List[Observer] = []

    def registerObserver(self, observer:Observer):
        self.observers.append(observer)

    def removeObserver(self, observer:Observer):
        self.observers.remove(observer)

    def notifyObservers(self):
        for observer in self.observers:
            observer.update()

    def set_state(self, state:ButtonState):
        self._state = state
        self.notifyObservers()

    def get_state(self)->ButtonState:
        return self._state

class OnEventListener(Observer):
    def __init__(self, subject:Button):
        self.subject = subject

    def update(self):
        if self.subject.get_state() == ButtonState.ON:
            print("THE BUTTON IS ON SO I AM DOING SOMETHING")

class OffEventListener(Observer):
    def __init__(self, subject:Button):
        self.subject = subject

    def update(self):
        if self.subject.get_state() == ButtonState.OFF:
            print("THE BUTTON IS OFF SO I AM DOING SOMETHING")

if __name__ == '__main__':
    weatherData = WeatherData()
    pressureDisplay = PressureDisplay(weatherData)
    temperatureDisplay = TemperatureDisplay(weatherData)
    humidifyDisplay = HumidityDisplay(weatherData)
    weatherData.registerObserver(pressureDisplay)
    weatherData.set_measurements(50.0, 120, 120, 123)
    weatherData.registerObserver(temperatureDisplay)
    weatherData.set_measurements(60.0, 105, 100, 123)
    weatherData.registerObserver(humidifyDisplay)
    weatherData.set_measurements(70.0, 50, 50, 123)
    weatherData.removeObserver(humidifyDisplay)
    weatherData.registerObserver(PollenDisplay(weatherData))
    weatherData.set_measurements(70.0, 50, 50, 123)


    button = Button()
    button.registerObserver(OnEventListener(button))
    # Nothing printed since OnEventListener doesn't do anything when button is on.
    button.set_state(ButtonState.OFF)

    button.registerObserver(OffEventListener(button))
    button.set_state(ButtonState.OFF)
    button.set_state(ButtonState.ON)
