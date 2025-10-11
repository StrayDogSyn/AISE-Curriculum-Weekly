class ParkingSystem:
    def __init__(self, big: int, medium: int, small: int):
        """
        Initialize the parking system with fixed number of slots.
        Think of this like setting up three separate parking areas,
        each with a different capacity.
        
        Args:
            big: Number of big parking slots
            medium: Number of medium parking slots
            small: Number of small parking slots
        """
        # Store available slots for each type
        # Using a list where index represents car type: [unused, big, medium, small]
        # This allows direct access using carType as index
        self.slots = [0, big, medium, small]
    
    def addCar(self, carType: int) -> bool:
        """
        Attempt to park a car of the given type.
        
        Args:
            carType: 1 (big), 2 (medium), or 3 (small)
        
        Returns:
            True if car was parked successfully, False otherwise
        
        Approach:
            1. Check if there's an available slot for this car type
            2. If yes, decrement the counter (car takes the spot)
            3. Return whether parking was successful
        """
        # Check if slots are available for this car type
        if self.slots[carType] > 0:
            # Park the car by decrementing available slots
            self.slots[carType] -= 1
            return True
        
        # No available slots for this car type
        return False


# Alternative implementation using a dictionary (more readable):
class ParkingSystemDict:
    def __init__(self, big: int, medium: int, small: int):
        """
        Alternative approach using a dictionary for clearer mapping.
        """
        self.available = {
            1: big,     # big cars
            2: medium,  # medium cars
            3: small    # small cars
        }
    
    def addCar(self, carType: int) -> bool:
        """
        Check and park car using dictionary lookup.
        """
        if self.available[carType] > 0:
            self.available[carType] -= 1
            return True
        return False
    
def test_parking_system():
    """
    Test cases to verify the parking system works correctly.
    """
    
    # Test Case 1: Original example from LeetCode
    print("Test Case 1: Original Example")
    ps1 = ParkingSystem(1, 1, 0)
    print(f"addCar(1): {ps1.addCar(1)}")  # Expected: True (big car parks)
    print(f"addCar(2): {ps1.addCar(2)}")  # Expected: True (medium car parks)
    print(f"addCar(3): {ps1.addCar(3)}")  # Expected: False (no small slots)
    print(f"addCar(1): {ps1.addCar(1)}")  # Expected: False (big slot full)
    print()
    
    # Test Case 2: All slots full scenario
    print("Test Case 2: Multiple cars filling all slots")
    ps2 = ParkingSystem(2, 2, 2)
    print(f"addCar(1): {ps2.addCar(1)}")  # Expected: True
    print(f"addCar(1): {ps2.addCar(1)}")  # Expected: True
    print(f"addCar(1): {ps2.addCar(1)}")  # Expected: False (big slots full)
    print(f"addCar(2): {ps2.addCar(2)}")  # Expected: True
    print(f"addCar(3): {ps2.addCar(3)}")  # Expected: True
    print()
    
    # Test Case 3: Only one type available
    print("Test Case 3: Only small cars allowed")
    ps3 = ParkingSystem(0, 0, 5)
    print(f"addCar(1): {ps3.addCar(1)}")  # Expected: False (no big slots)
    print(f"addCar(2): {ps3.addCar(2)}")  # Expected: False (no medium slots)
    print(f"addCar(3): {ps3.addCar(3)}")  # Expected: True
    print(f"addCar(3): {ps3.addCar(3)}")  # Expected: True
    print(f"addCar(3): {ps3.addCar(3)}")  # Expected: True
    print()
    
    # Test Case 4: Empty parking lot
    print("Test Case 4: No parking slots available")
    ps4 = ParkingSystem(0, 0, 0)
    print(f"addCar(1): {ps4.addCar(1)}")  # Expected: False
    print(f"addCar(2): {ps4.addCar(2)}")  # Expected: False
    print(f"addCar(3): {ps4.addCar(3)}")  # Expected: False
    print()
    
    # Test Case 5: Large parking lot stress test
    print("Test Case 5: Large parking lot")
    ps5 = ParkingSystem(100, 50, 25)
    # Park 100 big cars
    big_results = [ps5.addCar(1) for _ in range(101)]
    print(f"First 100 big cars: {all(big_results[:100])}")  # Expected: True
    print(f"101st big car: {big_results[100]}")  # Expected: False
    print()
    
    # Test Case 6: Alternating car types
    print("Test Case 6: Alternating car types")
    ps6 = ParkingSystem(3, 3, 3)
    sequence = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1]  # One extra big car
    results = [ps6.addCar(car_type) for car_type in sequence]
    print(f"Parking sequence {sequence}")
    print(f"Results: {results}")
    print(f"Expected: [True, True, True, True, True, True, True, True, True, False]")
    print()

# Run all tests
if __name__ == "__main__":
    test_parking_system()    