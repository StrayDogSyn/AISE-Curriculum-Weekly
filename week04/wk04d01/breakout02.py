"""
Breakout 2: QuickEats Food Delivery System Architecture
Week 4, Day 1 - Design Patterns Integration Challenge

This module implements a food delivery platform using FOUR design patterns:
1. Factory Pattern - Creates different types of restaurants
2. Strategy Pattern - Handles different delivery methods
3. Observer Pattern - Manages real-time notifications
4. Singleton Pattern - Ensures single instance of shopping cart per session

Author: Your Name
Date: October 20, 2025
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum


# ============================================================================
# SINGLETON PATTERN - Shopping Cart (One instance per session)
# ============================================================================

class ShoppingCart:
    """
    Singleton pattern ensures only ONE cart exists per user session.
    This cart syncs across all devices (phone, web, tablet).
    """
    _instance: Optional['ShoppingCart'] = None
    _is_initialized: bool = False
    
    def __new__(cls):
        """Ensures only one instance of ShoppingCart is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize cart only once, even if __init__ is called multiple times."""
        if not ShoppingCart._is_initialized:
            self.items: List[Dict] = []
            self.delivery_address: str = ""
            self.user_preferences: Dict = {}
            ShoppingCart._is_initialized = True
    
    def add_item(self, item: Dict) -> None:
        """Add an item to the cart."""
        self.items.append(item)
        print(f"✓ Added to cart: {item['name']} - ${item['price']:.2f}")
    
    def remove_item(self, item_name: str) -> bool:
        """Remove an item from the cart by name."""
        for item in self.items:
            if item['name'] == item_name:
                self.items.remove(item)
                print(f"✓ Removed from cart: {item_name}")
                return True
        return False
    
    def get_total(self) -> float:
        """Calculate total price of all items in cart."""
        return sum(item['price'] for item in self.items)
    
    def clear(self) -> None:
        """Clear all items from cart."""
        self.items.clear()
        print("✓ Cart cleared")
    
    def get_items_count(self) -> int:
        """Get the number of items in cart."""
        return len(self.items)
    
    def set_delivery_address(self, address: str) -> None:
        """Set delivery address (syncs across all devices)."""
        self.delivery_address = address
        print(f"✓ Delivery address set to: {address}")
    
    @classmethod
    def reset_instance(cls):
        """Reset singleton instance (useful for testing)."""
        cls._instance = None
        cls._is_initialized = False


# ============================================================================
# FACTORY PATTERN - Restaurant Creation
# ============================================================================

class Restaurant(ABC):
    """Abstract base class for all restaurant types."""
    
    def __init__(self, name: str):
        self.name = name
        self.menu: List[Dict] = []
    
    @abstractmethod
    def get_specialty(self) -> str:
        """Get the restaurant's specialty."""
        pass
    
    @abstractmethod
    def get_preparation_time(self) -> int:
        """Get average preparation time in minutes."""
        pass
    
    def display_menu(self) -> None:
        """Display the restaurant's menu."""
        print(f"\n🍽️  {self.name} Menu ({self.get_specialty()})")
        print("-" * 50)
        for item in self.menu:
            print(f"  {item['name']:<30} ${item['price']:>6.2f}")
        print(f"\n⏱️  Avg preparation time: {self.get_preparation_time()} minutes")


class FastFoodRestaurant(Restaurant):
    """Fast food restaurant - quick service, lower prices."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.menu = [
            {"name": "Cheeseburger", "price": 8.99},
            {"name": "French Fries", "price": 3.99},
            {"name": "Chicken Nuggets", "price": 6.99},
            {"name": "Milkshake", "price": 4.99}
        ]
    
    def get_specialty(self) -> str:
        return "Fast Food - Quick & Affordable"
    
    def get_preparation_time(self) -> int:
        return 10  # minutes


class FineDiningRestaurant(Restaurant):
    """Fine dining restaurant - gourmet food, higher prices."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.menu = [
            {"name": "Filet Mignon", "price": 42.99},
            {"name": "Lobster Risotto", "price": 38.99},
            {"name": "Truffle Pasta", "price": 34.99},
            {"name": "Crème Brûlée", "price": 12.99}
        ]
    
    def get_specialty(self) -> str:
        return "Fine Dining - Gourmet Experience"
    
    def get_preparation_time(self) -> int:
        return 35  # minutes


class FoodTruckRestaurant(Restaurant):
    """Food truck - street food, unique flavors."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.menu = [
            {"name": "Gourmet Tacos", "price": 12.99},
            {"name": "Korean BBQ Bowl", "price": 14.99},
            {"name": "Street Burrito", "price": 10.99},
            {"name": "Craft Soda", "price": 3.99}
        ]
    
    def get_specialty(self) -> str:
        return "Food Truck - Street Food Fusion"
    
    def get_preparation_time(self) -> int:
        return 15  # minutes


class CloudKitchenRestaurant(Restaurant):
    """Cloud kitchen - delivery-only, no physical location."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.menu = [
            {"name": "Pizza Margherita", "price": 16.99},
            {"name": "Caesar Salad", "price": 9.99},
            {"name": "Pasta Carbonara", "price": 14.99},
            {"name": "Tiramisu", "price": 7.99}
        ]
    
    def get_specialty(self) -> str:
        return "Cloud Kitchen - Delivery Only"
    
    def get_preparation_time(self) -> int:
        return 20  # minutes


class RestaurantType(Enum):
    """Enum for restaurant types."""
    FAST_FOOD = "fast_food"
    FINE_DINING = "fine_dining"
    FOOD_TRUCK = "food_truck"
    CLOUD_KITCHEN = "cloud_kitchen"


class RestaurantFactory:
    """
    Factory Pattern - Creates different types of restaurants.
    Centralizes restaurant creation logic.
    """
    
    @staticmethod
    def create_restaurant(restaurant_type: RestaurantType, name: str) -> Restaurant:
        """
        Factory method to create a restaurant based on type.
        
        Args:
            restaurant_type: Type of restaurant to create
            name: Name of the restaurant
            
        Returns:
            Restaurant instance
            
        Raises:
            ValueError: If restaurant type is not supported
        """
        if restaurant_type == RestaurantType.FAST_FOOD:
            return FastFoodRestaurant(name)
        elif restaurant_type == RestaurantType.FINE_DINING:
            return FineDiningRestaurant(name)
        elif restaurant_type == RestaurantType.FOOD_TRUCK:
            return FoodTruckRestaurant(name)
        elif restaurant_type == RestaurantType.CLOUD_KITCHEN:
            return CloudKitchenRestaurant(name)
        else:
            raise ValueError(f"Unknown restaurant type: {restaurant_type}")


# ============================================================================
# STRATEGY PATTERN - Delivery Methods
# ============================================================================

class DeliveryStrategy(ABC):
    """Abstract base class for delivery strategies."""
    
    @abstractmethod
    def calculate_cost(self, distance_km: float, order_total: float) -> float:
        """Calculate delivery cost based on distance and order total."""
        pass
    
    @abstractmethod
    def calculate_time(self, distance_km: float, preparation_time: int) -> int:
        """Calculate estimated delivery time in minutes."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get description of the delivery method."""
        pass


class StandardDeliveryStrategy(DeliveryStrategy):
    """Standard delivery - normal speed, normal cost."""
    
    def calculate_cost(self, distance_km: float, order_total: float) -> float:
        """Standard: $2 base + $0.50 per km. Free if order > $30."""
        base_fee = 2.00
        per_km = 0.50
        cost = base_fee + (distance_km * per_km)
        return 0.0 if order_total > 30 else cost
    
    def calculate_time(self, distance_km: float, preparation_time: int) -> int:
        """Standard: prep time + travel time (assumes 30 km/h)."""
        travel_time = int((distance_km / 30) * 60)  # minutes
        return preparation_time + travel_time
    
    def get_description(self) -> str:
        return "🚗 Standard Delivery (45 min avg) - Free over $30"


class ExpressDeliveryStrategy(DeliveryStrategy):
    """Express delivery - fast, premium cost."""
    
    def calculate_cost(self, distance_km: float, order_total: float) -> float:
        """Express: $5 base + $1.00 per km. No free delivery."""
        base_fee = 5.00
        per_km = 1.00
        return base_fee + (distance_km * per_km)
    
    def calculate_time(self, distance_km: float, preparation_time: int) -> int:
        """Express: prep time + faster travel (assumes 45 km/h)."""
        travel_time = int((distance_km / 45) * 60)  # minutes
        return preparation_time + travel_time
    
    def get_description(self) -> str:
        return "⚡ Express Delivery (20 min avg) - Premium Service"


class ScheduledDeliveryStrategy(DeliveryStrategy):
    """Scheduled delivery - pick your time, discounted cost."""
    
    def __init__(self, scheduled_time: Optional[datetime] = None):
        self.scheduled_time = scheduled_time or datetime.now() + timedelta(hours=2)
    
    def calculate_cost(self, distance_km: float, order_total: float) -> float:
        """Scheduled: $1.50 base + $0.40 per km (discounted)."""
        base_fee = 1.50
        per_km = 0.40
        return base_fee + (distance_km * per_km)
    
    def calculate_time(self, distance_km: float, preparation_time: int) -> int:
        """Scheduled: Returns minutes until scheduled time."""
        time_until = (self.scheduled_time - datetime.now()).total_seconds() / 60
        return max(int(time_until), preparation_time)
    
    def get_description(self) -> str:
        time_str = self.scheduled_time.strftime("%I:%M %p")
        return f"📅 Scheduled Delivery ({time_str}) - Save on fees"


class ContactlessDeliveryStrategy(DeliveryStrategy):
    """Contactless delivery - no-contact, standard pricing."""
    
    def calculate_cost(self, distance_km: float, order_total: float) -> float:
        """Contactless: Same as standard pricing."""
        base_fee = 2.00
        per_km = 0.50
        cost = base_fee + (distance_km * per_km)
        return 0.0 if order_total > 30 else cost
    
    def calculate_time(self, distance_km: float, preparation_time: int) -> int:
        """Contactless: Same as standard time + 2 min for safety."""
        travel_time = int((distance_km / 30) * 60)
        return preparation_time + travel_time + 2
    
    def get_description(self) -> str:
        return "🛡️ Contactless Delivery (45 min avg) - Safe & Secure"


class DeliveryContext:
    """
    Context class that uses a delivery strategy.
    Allows switching between different delivery methods at runtime.
    """
    
    def __init__(self, strategy: DeliveryStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: DeliveryStrategy) -> None:
        """Change the delivery strategy at runtime."""
        self._strategy = strategy
        print(f"✓ Delivery method changed to: {strategy.get_description()}")
    
    def calculate_delivery_cost(self, distance_km: float, order_total: float) -> float:
        """Calculate cost using current strategy."""
        return self._strategy.calculate_cost(distance_km, order_total)
    
    def calculate_delivery_time(self, distance_km: float, preparation_time: int) -> int:
        """Calculate time using current strategy."""
        return self._strategy.calculate_time(distance_km, preparation_time)
    
    def get_strategy_description(self) -> str:
        """Get description of current strategy."""
        return self._strategy.get_description()


# ============================================================================
# OBSERVER PATTERN - Real-time Notifications
# ============================================================================

class OrderStatus(Enum):
    """Enum for order status stages."""
    PLACED = "Order Placed"
    PREPARING = "Preparing Food"
    DRIVER_ASSIGNED = "Driver Assigned"
    ON_THE_WAY = "On the Way"
    DELIVERED = "Delivered"


class Observer(ABC):
    """Abstract observer that receives notifications."""
    
    @abstractmethod
    def update(self, order_id: str, status: OrderStatus, message: str) -> None:
        """Receive update notification."""
        pass


class UserNotificationObserver(Observer):
    """Observer for user notifications (phone, web, tablet)."""
    
    def __init__(self, user_name: str, device: str):
        self.user_name = user_name
        self.device = device
    
    def update(self, order_id: str, status: OrderStatus, message: str) -> None:
        """Send notification to user's device."""
        print(f"📱 [{self.device}] Notification to {self.user_name}:")
        print(f"   Order #{order_id}: {status.value}")
        print(f"   {message}\n")


class RestaurantNotificationObserver(Observer):
    """Observer for restaurant notifications."""
    
    def __init__(self, restaurant_name: str):
        self.restaurant_name = restaurant_name
    
    def update(self, order_id: str, status: OrderStatus, message: str) -> None:
        """Send notification to restaurant."""
        print(f"🏪 Restaurant [{self.restaurant_name}] Update:")
        print(f"   Order #{order_id}: {status.value}")
        print(f"   {message}\n")


class DriverNotificationObserver(Observer):
    """Observer for driver notifications."""
    
    def __init__(self, driver_name: str, driver_id: str):
        self.driver_name = driver_name
        self.driver_id = driver_id
    
    def update(self, order_id: str, status: OrderStatus, message: str) -> None:
        """Send notification to driver."""
        print(f"🚗 Driver [{self.driver_name} #{self.driver_id}] Update:")
        print(f"   Order #{order_id}: {status.value}")
        print(f"   {message}\n")


class OrderSubject:
    """
    Subject (Observable) that maintains list of observers and notifies them.
    This is the core of the Observer pattern.
    """
    
    def __init__(self, order_id: str):
        self.order_id = order_id
        self._observers: List[Observer] = []
        self._status: OrderStatus = OrderStatus.PLACED
    
    def attach(self, observer: Observer) -> None:
        """Attach an observer to receive notifications."""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"✓ Observer attached: {observer.__class__.__name__}")
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer from receiving notifications."""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"✓ Observer detached: {observer.__class__.__name__}")
    
    def notify(self, message: str) -> None:
        """Notify all observers about status change."""
        print(f"\n{'='*60}")
        print(f"📢 Broadcasting update for Order #{self.order_id}")
        print(f"{'='*60}")
        for observer in self._observers:
            observer.update(self.order_id, self._status, message)
    
    def update_status(self, new_status: OrderStatus, message: str) -> None:
        """Update order status and notify all observers."""
        self._status = new_status
        self.notify(message)
    
    def get_status(self) -> OrderStatus:
        """Get current order status."""
        return self._status


# ============================================================================
# MAIN APPLICATION - Integrating All Patterns
# ============================================================================

class QuickEatsApp:
    """
    Main application that integrates all four design patterns:
    - Singleton: Shopping cart
    - Factory: Restaurant creation
    - Strategy: Delivery methods
    - Observer: Real-time notifications
    """
    
    def __init__(self):
        self.cart = ShoppingCart()  # Singleton
        self.restaurant_factory = RestaurantFactory()  # Factory
        self.current_restaurant: Optional[Restaurant] = None
        self.delivery_context: Optional[DeliveryContext] = None
        self.order_subject: Optional[OrderSubject] = None
    
    def display_welcome(self) -> None:
        """Display welcome message."""
        print("\n" + "="*60)
        print("🍔 Welcome to QuickEats - Your Food Delivery Platform! 🍕")
        print("="*60)
    
    def select_restaurant(self, restaurant_type: RestaurantType, name: str) -> None:
        """Use Factory to create and select a restaurant."""
        print(f"\n{'='*60}")
        print(f"🏪 Selecting Restaurant...")
        print(f"{'='*60}")
        
        self.current_restaurant = self.restaurant_factory.create_restaurant(
            restaurant_type, name
        )
        print(f"✓ Selected: {self.current_restaurant.name}")
        self.current_restaurant.display_menu()
    
    def add_to_cart(self, item_name: str) -> bool:
        """Add item from current restaurant to cart (Singleton)."""
        if not self.current_restaurant:
            print("❌ Please select a restaurant first!")
            return False
        
        # Find item in restaurant menu
        for item in self.current_restaurant.menu:
            if item['name'].lower() == item_name.lower():
                self.cart.add_item(item)
                return True
        
        print(f"❌ Item '{item_name}' not found in menu!")
        return False
    
    def select_delivery_method(self, strategy: DeliveryStrategy) -> None:
        """Select delivery method (Strategy pattern)."""
        print(f"\n{'='*60}")
        print(f"🚚 Setting up Delivery...")
        print(f"{'='*60}")
        
        if self.delivery_context is None:
            self.delivery_context = DeliveryContext(strategy)
            print(f"✓ Delivery method set: {strategy.get_description()}")
        else:
            self.delivery_context.set_strategy(strategy)
    
    def place_order(self, distance_km: float = 5.0) -> str:
        """Place order and setup observers for notifications."""
        if self.cart.get_items_count() == 0:
            print("❌ Cart is empty! Add items before placing order.")
            return ""
        
        if not self.delivery_context:
            print("❌ Please select a delivery method first!")
            return ""
        
        # Generate order ID
        order_id = f"QE{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        print(f"\n{'='*60}")
        print(f"📦 Processing Order #{order_id}")
        print(f"{'='*60}")
        
        # Calculate costs
        order_total = self.cart.get_total()
        delivery_cost = self.delivery_context.calculate_delivery_cost(
            distance_km, order_total
        )
        total_cost = order_total + delivery_cost
        
        # Calculate delivery time
        prep_time = self.current_restaurant.get_preparation_time()
        delivery_time = self.delivery_context.calculate_delivery_time(
            distance_km, prep_time
        )
        
        # Display order summary
        print(f"\n📋 Order Summary:")
        print(f"   Restaurant: {self.current_restaurant.name}")
        print(f"   Items: {self.cart.get_items_count()}")
        print(f"   Subtotal: ${order_total:.2f}")
        print(f"   Delivery: ${delivery_cost:.2f}")
        print(f"   Total: ${total_cost:.2f}")
        print(f"   Estimated Time: {delivery_time} minutes")
        print(f"   Method: {self.delivery_context.get_strategy_description()}")
        
        # Setup Observer pattern for notifications
        self.order_subject = OrderSubject(order_id)
        
        # Attach observers
        user_observer = UserNotificationObserver("Customer", "iPhone")
        restaurant_observer = RestaurantNotificationObserver(
            self.current_restaurant.name
        )
        driver_observer = DriverNotificationObserver("John Smith", "DRV-1234")
        
        self.order_subject.attach(user_observer)
        self.order_subject.attach(restaurant_observer)
        
        # Initial notification
        self.order_subject.update_status(
            OrderStatus.PLACED,
            f"Your order has been placed! Total: ${total_cost:.2f}"
        )
        
        # Simulate order progression
        self.order_subject.update_status(
            OrderStatus.PREPARING,
            f"{self.current_restaurant.name} is preparing your food..."
        )
        
        # Attach driver observer when assigned
        self.order_subject.attach(driver_observer)
        self.order_subject.update_status(
            OrderStatus.DRIVER_ASSIGNED,
            f"Driver John Smith has been assigned to your order!"
        )
        
        self.order_subject.update_status(
            OrderStatus.ON_THE_WAY,
            f"Your order is on the way! ETA: {delivery_time} minutes"
        )
        
        return order_id
    
    def view_cart(self) -> None:
        """Display cart contents (Singleton)."""
        print(f"\n{'='*60}")
        print(f"🛒 Shopping Cart")
        print(f"{'='*60}")
        
        if self.cart.get_items_count() == 0:
            print("Your cart is empty.")
            return
        
        for i, item in enumerate(self.cart.items, 1):
            print(f"{i}. {item['name']:<30} ${item['price']:>6.2f}")
        
        print(f"\n{'─'*60}")
        print(f"{'Total:':<30} ${self.cart.get_total():>6.2f}")
        print(f"Items: {self.cart.get_items_count()}")


# ============================================================================
# DEMONSTRATION SCENARIOS
# ============================================================================

def demo_scenario_a():
    """
    Scenario A: User Orders Pizza
    Demonstrates all 4 patterns working together.
    """
    print("\n" + "🍕"*30)
    print("SCENARIO A: User Orders Pizza")
    print("🍕"*30)
    
    app = QuickEatsApp()
    app.display_welcome()
    
    # Step 1: Singleton initializes session
    print("\n👤 User opens app on iPhone...")
    
    # Step 2: Factory creates restaurant
    app.select_restaurant(RestaurantType.CLOUD_KITCHEN, "Pizza Palace")
    
    # Step 3: Singleton stores order
    print(f"\n{'='*60}")
    print(f"🛒 Adding items to cart...")
    print(f"{'='*60}")
    app.add_to_cart("Pizza Margherita")
    app.add_to_cart("Caesar Salad")
    app.add_to_cart("Tiramisu")
    
    app.cart.set_delivery_address("123 Main St, Apt 4B")
    
    # Step 4: Strategy calculates cost/time
    app.select_delivery_method(ExpressDeliveryStrategy())
    
    # Step 5: Observer notifies everyone
    order_id = app.place_order(distance_km=3.5)
    
    print(f"\n✅ Order #{order_id} completed successfully!")


def demo_scenario_b():
    """
    Scenario B: Restaurant Confirms Order
    Demonstrates Observer pattern notifications.
    """
    print("\n" + "✅"*30)
    print("SCENARIO B: Restaurant Confirms Order")
    print("✅"*30)
    
    # Create order subject
    order_subject = OrderSubject("QE20251020143000")
    
    # Attach all observers
    user_obs = UserNotificationObserver("Sarah Johnson", "iPad")
    restaurant_obs = RestaurantNotificationObserver("Pizza Palace")
    driver_obs = DriverNotificationObserver("Mike Chen", "DRV-5678")
    
    order_subject.attach(user_obs)
    order_subject.attach(restaurant_obs)
    order_subject.attach(driver_obs)
    
    # Restaurant confirms and updates status
    print("\n🏪 Pizza Palace marks order as 'Preparing'...\n")
    order_subject.update_status(
        OrderStatus.PREPARING,
        "Your pepperoni pizza is being freshly prepared!"
    )
    
    print("📢 All parties notified: User, Restaurant, and Driver!")


def demo_scenario_c():
    """
    Scenario C: User Switches Devices
    Demonstrates Singleton pattern ensuring cart syncs across devices.
    """
    print("\n" + "📱"*30)
    print("SCENARIO C: User Switches Devices")
    print("📱"*30)
    
    app1 = QuickEatsApp()
    
    print("\n📱 User adds items on iPhone...")
    app1.select_restaurant(RestaurantType.FOOD_TRUCK, "Seoul Street Eats")
    app1.add_to_cart("Korean BBQ Bowl")
    app1.add_to_cart("Gourmet Tacos")
    app1.add_to_cart("Craft Soda")
    
    print("\n" + "="*60)
    print("📱 Viewing cart on iPhone...")
    app1.view_cart()
    
    # Simulate switching devices - same cart instance!
    print("\n" + "="*60)
    print("📱 User opens app on iPad...")
    print("="*60)
    app2 = QuickEatsApp()  # Same cart due to Singleton!
    
    print("\n💫 Cart automatically synced!")
    app2.view_cart()
    
    print("\n" + "="*60)
    print("🏠 User changes delivery address on iPad...")
    print("="*60)
    app2.cart.set_delivery_address("456 Oak Avenue, Suite 12")
    
    print("\n✅ Address synced across all devices!")
    print(f"   Current address: {app1.cart.delivery_address}")


def demo_pattern_comparison():
    """
    Demonstrates differences between patterns and when to use each.
    """
    print("\n" + "🎓"*30)
    print("DESIGN PATTERNS COMPARISON")
    print("🎓"*30)
    
    print("\n1️⃣ FACTORY vs STRATEGY:")
    print("   Factory: CREATES different objects (restaurants)")
    print("   Strategy: SWITCHES behavior at runtime (delivery methods)")
    
    print("\n2️⃣ Adding new Drone Delivery:")
    print("   ✓ Use STRATEGY pattern - it handles delivery behavior!")
    print("   ✗ Other patterns don't need changes")
    
    # Demonstrate adding new strategy
    class DroneDeliveryStrategy(DeliveryStrategy):
        """New delivery method - drones!"""
        
        def calculate_cost(self, distance_km: float, order_total: float) -> float:
            return 8.00 + (distance_km * 1.50)  # Premium pricing
        
        def calculate_time(self, distance_km: float, preparation_time: int) -> int:
            travel_time = int((distance_km / 60) * 60)  # 60 km/h drone speed
            return preparation_time + travel_time
        
        def get_description(self) -> str:
            return "🚁 Drone Delivery (15 min avg) - Ultra Fast!"
    
    print("\n   📦 Testing new Drone Delivery...")
    app = QuickEatsApp()
    app.select_restaurant(RestaurantType.FAST_FOOD, "Burger Express")
    app.add_to_cart("Cheeseburger")
    app.select_delivery_method(DroneDeliveryStrategy())
    
    print("\n   ✅ New delivery method added without changing other patterns!")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all demonstration scenarios."""
    print("\n" + "🎯"*30)
    print("QUICKEATS SYSTEM ARCHITECTURE DEMONSTRATION")
    print("Integrating 4 Design Patterns")
    print("🎯"*30)
    
    # Run all scenarios
    demo_scenario_a()
    
    print("\n" + "─"*60 + "\n")
    demo_scenario_b()
    
    print("\n" + "─"*60 + "\n")
    demo_scenario_c()
    
    print("\n" + "─"*60 + "\n")
    demo_pattern_comparison()
    
    print("\n" + "="*60)
    print("✅ All demonstrations completed!")
    print("="*60)
    
    # Show pattern integration summary
    print("\n📊 PATTERN INTEGRATION SUMMARY:")
    print("   🏭 Factory: Creates restaurants (FastFood, FineDining, etc.)")
    print("   🔄 Strategy: Switches delivery methods (Standard, Express, etc.)")
    print("   📢 Observer: Notifies users, restaurants, and drivers")
    print("   ⭐ Singleton: Ensures one cart per session across devices")
    print("\n   All patterns work together to create a cohesive system! 🎉\n")


if __name__ == "__main__":
    main()
