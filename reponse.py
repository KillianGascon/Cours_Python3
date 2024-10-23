from abc import ABC, abstractmethod
from math import pi
import threading
import time
from functools import wraps

# Exercice 1
class Shape(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        area = pi * (self.radius) ** 2
        print(area)
        return area

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        area = self.width * self.height
        print(area)
        return area

# Exo 2
class BankAccount:
    def __init__(self, balance: float):
        self.balance = balance

    def __add__(self, other):
        if isinstance(other, BankAccount):
            return BankAccount(self.balance + other.balance)
        elif isinstance(other, (int, float)):
            return BankAccount(self.balance + other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, BankAccount):
            return BankAccount(self.balance - other.balance)
        elif isinstance(other, (int, float)):
            return BankAccount(self.balance - other)
        return NotImplemented

    def __repr__(self):
        return f"BankAccount(balance={self.balance})"

# Exo 3
def check_positive(func):
    def wrapper(*args):
        if args[0] < 0:
            raise ValueError("Le nombre est négatif")
        return func(*args)
    return wrapper

@check_positive
def add(a, b):
    return a + b

# Exo 4
class Car:
    def __init__(self, speed=0):
        self.__speed = speed

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        if speed <= 0:
            raise ValueError("Vous n'avancez pas")
        elif speed > 200:
            raise ValueError("Vous allez trop vite")
        self.__speed = speed

# Exo 5
class AgeError(Exception):
    pass

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if age < 0 or age > 150:
            raise AgeError("Âge non valide")
        self.__age = age

# Exo 6
class DbContext:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def __enter__(self):
        return self.db_connection

    def __exit__(self, exc_type, exc_value, traceback):
        self.db_connection.flush()

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.data_store = {}
        return cls._instance

    def add_entry(self, entry):
        entry_id = entry["id"]
        data = entry["data"]
        self.data_store[entry_id] = data

    def remove_by_id(self, entry_id):
        if entry_id in self.data_store:
            del self.data_store[entry_id]

    def drop_all(self):
        self.data_store.clear()

    def flush(self):
        pass

    @property
    def entries(self):
        return [{"id": k, "data": v} for k, v in self.data_store.items()]

# Exo 7
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return pi * (self.radius ** 2)

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class ShapeFactory:
    @staticmethod
    def create(shape, **kwargs):
        if shape == "circle":
            return Circle(kwargs.get('radius'))
        elif shape == "rectangle":
            return Rectangle(kwargs.get('width'), kwargs.get('height'))
        else:
            raise ValueError("Shape type not recognized.")

# Exo 8
class TimeoutError(Exception):
    """Exception levée lorsque la limite de temps est dépassée."""
    pass


def timeout_limit(timeout, raise_exception=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Variable pour stocker l'exception
            result = [None]
            exc = [None]

            # Fonction interne exécutée dans un thread séparé
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exc[0] = e

            # Démarrage du thread pour exécuter la fonction
            thread = threading.Thread(target=target)
            thread.start()

            # Attente pendant la durée spécifiée
            thread.join(timeout)

            # Si le thread est toujours actif après le timeout
            if thread.is_alive():
                if raise_exception:
                    raise TimeoutError("Exécution interrompue par raise_exception.")
                else:
                    raise TimeoutError("La limite de temps a été dépassée.")

            # Si une exception a été levée dans le thread, la relancer
            if exc[0]:
                raise exc[0]

            return result[0]

        return wrapper

    return decorator

# Exo 9
class Matrix:
    def __init__(self, data):
        if not all(len(row) == len(data[0]) for row in data):
            raise ValueError("Toutes les lignes doivent avoir la même longueur.")
        self.values = data

    def __add__(self, other):
        if len(self.values) != len(other.values) or len(self.values[0]) != len(other.values[0]):
            raise ValueError("Les matrices doivent avoir les mêmes dimensions pour l'addition.")
        result = [
            [
                self.values[i][j] + other.values[i][j]
                for j in range(len(self.values[0]))
            ]
            for i in range(len(self.values))
        ]
        return Matrix(result)

    def __mul__(self, other):
        if len(self.values[0]) != len(other.values):
            raise ValueError("Le nombre de colonnes de la première matrice doit être égal au nombre de lignes de la deuxième.")
        result = [
            [
                sum(self.values[i][k] * other.values[k][j] for k in range(len(other.values)))
                for j in range(len(other.values[0]))
            ]
            for i in range(len(self.values))
        ]
        return Matrix(result)

# Exo 10
class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Woof"

class Cat(Animal):
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Meow"

class AnimalFactory:
    @staticmethod
    def create(animal_type, name):
        if animal_type == "dog":
            return Dog(name)
        elif animal_type == "cat":
            return Cat(name)
        else:
            raise ValueError("Type d'animal inconnu. Utilisez 'dog' ou 'cat'.")

# Exo 11
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.price == other.price
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Product):
            return self.price < other.price
        return NotImplemented

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        if isinstance(other, Product):
            return self.price > other.price
        return NotImplemented

    def __ge__(self, other):
        return self > other or self == other

    def __ne__(self, other):
        return not self == other

# Exo 12
class Account:
    def __init__(self, initial_balance=0):
        if initial_balance < 0:
            raise ValueError("Le solde initial ne peut pas être inférieur à 0.")
        self._balance = initial_balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Le montant du dépôt ne peut pas être inférieur à 0.")
        self._balance = amount

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Le montant du dépôt ne peut pas être inférieur à 0.")
        self._balance += amount

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Le montant du retrait ne peut pas être inférieur à 0.")
        if self._balance - amount < 0:
            raise ValueError("Solde insuffisant pour effectuer ce retrait.")
        self._balance -= amount

# Exo 13
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


if __name__ == '__main__':
    print("hello world")

