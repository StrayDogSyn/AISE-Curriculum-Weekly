"""
Simple Python Class Inheritance Example - Beginner Friendly
Demonstrates basic inheritance concepts:
- Base class (parent class)
- Derived classes (child classes)
- Method overriding
- The super() function
- Polymorphism basics
"""


class Animal:
    """
    Base class representing a generic animal.
    
    This is the parent class that other animals will inherit from.
    It contains common attributes and methods that all animals share.
    """
    
    def __init__(self, name: str, species: str, age: int):
        """
        Initialize an animal with basic information.
        
        Args:
            name (str): The animal's name
            species (str): What type of animal it is
            age (int): The animal's age in years
        """
        # These are instance attributes - each animal object will have its own copy
        self.name = name
        self.species = species
        self.age = age
        self.is_sleeping = False
        self.energy = 100
    
    def eat(self, food: str) -> str:
        """
        Make the animal eat food.
        
        Args:
            food (str): What the animal is eating
            
        Returns:
            str: A message about eating
        """
        self.energy = min(100, self.energy + 20)  # Cap energy at 100
        return f"{self.name} the {self.species} eats {food} and gains energy!"
    
    def sleep(self) -> str:
        """
        Make the animal sleep.
        
        Returns:
            str: A message about sleeping
        """
        if self.is_sleeping:
            return f"{self.name} is already sleeping!"
        
        self.is_sleeping = True
        self.energy = 100  # Sleeping restores full energy
        return f"{self.name} goes to sleep and feels refreshed!"
    
    def wake_up(self) -> str:
        """
        Wake up the animal.
        
        Returns:
            str: A message about waking up
        """
        if not self.is_sleeping:
            return f"{self.name} is already awake!"
        
        self.is_sleeping = False
        return f"{self.name} wakes up!"
    
    def make_sound(self) -> str:
        """
        Make a generic animal sound.
        
        This method will be overridden by child classes to make specific sounds.
        
        Returns:
            str: A generic animal sound
        """
        return f"{self.name} makes a generic animal sound!"
    
    def get_info(self) -> str:
        """
        Get information about the animal.
        
        Returns:
            str: Formatted information about the animal
        """
        status = "sleeping" if self.is_sleeping else "awake"
        return f"{self.name} is a {self.age}-year-old {self.species} ({status}, energy: {self.energy})"
    
    def __str__(self) -> str:
        """String representation of the animal."""
        return f"{self.name} the {self.species}"


class Dog(Animal):
    """
    Dog class that inherits from Animal.
    
    This is a child class that extends the Animal class with dog-specific behavior.
    Dogs inherit all methods and attributes from Animal, but can also have their own.
    """
    
    def __init__(self, name: str, age: int, breed: str):
        """
        Initialize a dog.
        
        Args:
            name (str): The dog's name
            age (int): The dog's age in years
            breed (str): The dog's breed (e.g., "Golden Retriever")
        """
        # Call the parent class constructor using super()
        # This initializes all the Animal attributes (name, species, age, etc.)
        super().__init__(name, "Dog", age)
        
        # Add dog-specific attributes
        self.breed = breed
        self.is_trained = False
        self.tricks = []  # List of tricks the dog knows
    
    def make_sound(self) -> str:
        """
        Override the parent's make_sound method with dog-specific behavior.
        
        Returns:
            str: Dog barking sound
        """
        return f"{self.name} barks: Woof! Woof!"
    
    def fetch(self, item: str) -> str:
        """
        Dog-specific method: fetch an item.
        
        Args:
            item (str): What the dog is fetching
            
        Returns:
            str: Message about fetching
        """
        if self.is_sleeping:
            return f"{self.name} is sleeping and can't fetch right now!"
        
        if self.energy < 20:
            return f"{self.name} is too tired to fetch!"
        
        self.energy -= 15  # Fetching uses energy
        return f"{self.name} runs and fetches the {item}! Good dog!"
    
    def learn_trick(self, trick: str) -> str:
        """
        Teach the dog a new trick.
        
        Args:
            trick (str): The trick to learn
            
        Returns:
            str: Message about learning the trick
        """
        if trick in self.tricks:
            return f"{self.name} already knows how to {trick}!"
        
        self.tricks.append(trick)
        return f"{self.name} learned to {trick}!"
    
    def perform_trick(self, trick: str) -> str:
        """
        Make the dog perform a trick.
        
        Args:
            trick (str): The trick to perform
            
        Returns:
            str: Message about performing the trick
        """
        if trick not in self.tricks:
            return f"{self.name} doesn't know how to {trick} yet!"
        
        if self.is_sleeping:
            return f"{self.name} is sleeping and can't perform tricks!"
        
        return f"{self.name} performs {trick}! What a good dog!"
    
    def get_info(self) -> str:
        """
        Override parent's get_info to include dog-specific information.
        
        Returns:
            str: Detailed information about the dog
        """
        # Call the parent's get_info method first
        basic_info = super().get_info()
        
        # Add dog-specific information
        trick_info = f"Knows {len(self.tricks)} tricks: {', '.join(self.tricks)}" if self.tricks else "No tricks learned yet"
        
        return f"{basic_info}\nBreed: {self.breed}\n{trick_info}"


class Cat(Animal):
    """
    Cat class that inherits from Animal.
    
    Another child class showing different behavior from the same parent.
    """
    
    def __init__(self, name: str, age: int, color: str):
        """
        Initialize a cat.
        
        Args:
            name (str): The cat's name
            age (int): The cat's age in years
            color (str): The cat's fur color
        """
        # Call parent constructor
        super().__init__(name, "Cat", age)
        
        # Cat-specific attributes
        self.color = color
        self.lives_remaining = 9  # Cats have 9 lives!
        self.is_purring = False
    
    def make_sound(self) -> str:
        """
        Override make_sound with cat-specific behavior.
        
        Returns:
            str: Cat meowing sound
        """
        return f"{self.name} meows: Meow! Meow!"
    
    def purr(self) -> str:
        """
        Cat-specific method: purring.
        
        Returns:
            str: Message about purring
        """
        if self.is_sleeping:
            return f"{self.name} purrs softly while sleeping!"
        
        self.is_purring = True
        return f"{self.name} purrs contentedly: Purrrrr..."
    
    def climb_tree(self) -> str:
        """
        Cat-specific method: climbing trees.
        
        Returns:
            str: Message about tree climbing
        """
        if self.is_sleeping:
            return f"{self.name} is sleeping and can't climb trees right now!"
        
        if self.energy < 30:
            return f"{self.name} is too tired to climb!"
        
        self.energy -= 20
        return f"{self.name} gracefully climbs up a tree!"
    
    def knock_over_object(self, object_name: str) -> str:
        """
        Cat-specific method: knocking things over (because cats do this!).
        
        Args:
            object_name (str): What the cat is knocking over
            
        Returns:
            str: Message about knocking over the object
        """
        if self.is_sleeping:
            return f"{self.name} is sleeping peacefully and not causing trouble!"
        
        return f"{self.name} looks at the {object_name}... and knocks it over! Typical cat behavior!"
    
    def get_info(self) -> str:
        """
        Override parent's get_info to include cat-specific information.
        
        Returns:
            str: Detailed information about the cat
        """
        basic_info = super().get_info()
        purr_status = "purring" if self.is_purring else "not purring"
        
        return f"{basic_info}\nColor: {self.color}\nLives remaining: {self.lives_remaining}\nCurrently {purr_status}"


class Bird(Animal):
    """
    Bird class that inherits from Animal.
    
    Shows another example of inheritance with flying capability.
    """
    
    def __init__(self, name: str, age: int, wing_span: float):
        """
        Initialize a bird.
        
        Args:
            name (str): The bird's name
            age (int): The bird's age in years
            wing_span (float): The bird's wing span in inches
        """
        super().__init__(name, "Bird", age)
        
        self.wing_span = wing_span
        self.is_flying = False
        self.altitude = 0  # Height in feet
    
    def make_sound(self) -> str:
        """
        Override make_sound with bird-specific behavior.
        
        Returns:
            str: Bird chirping sound
        """
        return f"{self.name} chirps: Tweet! Tweet!"
    
    def fly(self, height: int) -> str:
        """
        Bird-specific method: flying.
        
        Args:
            height (int): How high to fly in feet
            
        Returns:
            str: Message about flying
        """
        if self.is_sleeping:
            return f"{self.name} is sleeping and can't fly right now!"
        
        if self.energy < 25:
            return f"{self.name} is too tired to fly!"
        
        self.is_flying = True
        self.altitude = height
        self.energy -= 20
        
        return f"{self.name} spreads its wings and flies up to {height} feet!"
    
    def land(self) -> str:
        """
        Make the bird land.
        
        Returns:
            str: Message about landing
        """
        if not self.is_flying:
            return f"{self.name} is already on the ground!"
        
        self.is_flying = False
        self.altitude = 0
        
        return f"{self.name} gracefully lands on the ground!"
    
    def get_info(self) -> str:
        """
        Override parent's get_info to include bird-specific information.
        
        Returns:
            str: Detailed information about the bird
        """
        basic_info = super().get_info()
        flight_status = f"flying at {self.altitude} feet" if self.is_flying else "on the ground"
        
        return f"{basic_info}\nWing span: {self.wing_span} inches\nCurrently {flight_status}"


def demonstrate_inheritance():
    """
    Function to demonstrate how inheritance works with our animal classes.
    """
    print("=== Python Inheritance Example ===\n")
    
    # Create different animals
    print("Creating animals...")
    buddy = Dog("Buddy", 3, "Golden Retriever")
    whiskers = Cat("Whiskers", 2, "Orange")
    tweety = Bird("Tweety", 1, 8.5)
    
    print(f"Created: {buddy}")
    print(f"Created: {whiskers}")
    print(f"Created: {tweety}")
    print()
    
    # Show basic information
    print("=== Animal Information ===")
    print(buddy.get_info())
    print()
    print(whiskers.get_info())
    print()
    print(tweety.get_info())
    print()
    
    # Demonstrate polymorphism - same method, different behavior
    print("=== Polymorphism - Same Method, Different Sounds ===")
    animals = [buddy, whiskers, tweety]
    
    for animal in animals:
        print(animal.make_sound())  # Each animal makes its own sound!
    print()
    
    # Demonstrate shared methods from parent class
    print("=== Shared Methods from Parent Class ===")
    print(buddy.eat("dog treats"))
    print(whiskers.eat("fish"))
    print(tweety.eat("seeds"))
    print()
    
    # Demonstrate unique methods for each animal type
    print("=== Unique Methods for Each Animal Type ===")
    
    # Dog-specific methods
    print("--- Dog Activities ---")
    print(buddy.learn_trick("sit"))
    print(buddy.learn_trick("roll over"))
    print(buddy.perform_trick("sit"))
    print(buddy.fetch("ball"))
    print()
    
    # Cat-specific methods
    print("--- Cat Activities ---")
    print(whiskers.purr())
    print(whiskers.climb_tree())
    print(whiskers.knock_over_object("vase"))
    print()
    
    # Bird-specific methods
    print("--- Bird Activities ---")
    print(tweety.fly(50))
    print(tweety.land())
    print()
    
    # Show how energy affects behavior
    print("=== Energy System ===")
    print(f"Buddy's energy before activities: {buddy.energy}")
    print(buddy.fetch("stick"))
    print(buddy.fetch("frisbee"))
    print(buddy.fetch("ball"))  # Should be getting tired
    print(f"Buddy's energy after activities: {buddy.energy}")
    print(buddy.sleep())  # Rest to restore energy
    print(f"Buddy's energy after sleeping: {buddy.energy}")
    print()
    
    # Final status
    print("=== Final Status ===")
    for animal in animals:
        print(f"{animal}: {animal.get_info()}")
        print()


if __name__ == "__main__":
    """
    Main execution - run the demonstration when the file is executed directly.
    """
    demonstrate_inheritance()
    
    print("=" * 50)
    print("Key Inheritance Concepts Demonstrated:")
    print("1. Base class (Animal) with common attributes and methods")
    print("2. Child classes (Dog, Cat, Bird) that inherit from Animal")
    print("3. Method overriding (each animal makes different sounds)")
    print("4. Using super() to call parent class methods")
    print("5. Adding unique methods to child classes")
    print("6. Polymorphism (same method name, different behavior)")
    print("=" * 50)