#!/usr/bin/env python3
"""
W1D1 Breakout 2: Personal Python Toolkit
Author: Eric 'Hunter' Petross (@StrayDogSyn)
Title: Applied AI Solutions Engineer
Company: StrayDog Syndications LLC
Date: September 29, 2025

A collection of practical functions to solve real-world daily calculations
"""

import math


def calculate_grade_needed(current_grade, target_grade, final_weight):
    """
    Calculate grade needed on final exam to achieve target grade
    
    Problem it solves: Helps students determine what score they need on their
    final exam to achieve their desired grade in a course.
    
    Args:
        current_grade (float): Current grade percentage (0-100)
        target_grade (float): Desired final grade (0-100)  
        final_weight (float): Weight of final exam as decimal (e.g., 0.3 for 30%)
    
    Returns:
        float: Grade needed on final exam (capped at 100%)
    """
    if final_weight <= 0 or final_weight > 1:
        return "Error: Final weight must be between 0 and 1"
    
    grade_needed = (target_grade - current_grade * (1 - final_weight)) / final_weight
    return min(grade_needed, 100)  # Can't score above 100%


def split_bill_with_tip(total, people, tip_percent=20):
    """
    Calculate bill split including tip
    
    Problem it solves: Quickly calculates how much each person owes when 
    dining out with friends, including tip calculation.
    
    Args:
        total (float): Bill total before tip
        people (int): Number of people splitting the bill
        tip_percent (float): Tip percentage (default 20%)
    
    Returns:
        tuple: (per_person_amount, total_with_tip)
    """
    if people <= 0:
        return "Error: Number of people must be greater than 0"
    
    tip_amount = total * (tip_percent / 100)
    total_with_tip = total + tip_amount
    per_person = total_with_tip / people
    return round(per_person, 2), round(total_with_tip, 2)


def calculate_study_hours_needed(credits, difficulty_multiplier=2.5):
    """
    Calculate recommended study hours per week based on course credits
    
    Problem it solves: Helps students plan their study schedule by estimating
    how many hours they should dedicate to studying per week.
    
    Args:
        credits (int): Number of credit hours for the course
        difficulty_multiplier (float): Multiplier based on course difficulty 
                                     (2.0 = easy, 2.5 = average, 3.0 = hard)
    
    Returns:
        float: Recommended study hours per week
    """
    if credits <= 0:
        return "Error: Credits must be greater than 0"
    
    study_hours = credits * difficulty_multiplier
    return round(study_hours, 1)


def workout_pace_calculator(distance_miles, time_minutes):
    """
    Calculate running/cycling pace per mile
    
    Problem it solves: Converts workout data into pace format that's easy
    to understand and compare with fitness goals.
    
    Args:
        distance_miles (float): Distance covered in miles
        time_minutes (float): Total time in minutes
    
    Returns:
        str: Pace in MM:SS per mile format
    """
    if distance_miles <= 0 or time_minutes <= 0:
        return "Error: Distance and time must be greater than 0"
    
    pace = time_minutes / distance_miles
    minutes = int(pace)
    seconds = int((pace - minutes) * 60)
    return f"{minutes}:{seconds:02d} per mile"


def caffeine_intake_tracker(cups_coffee=0, cups_tea=0, energy_drinks=0):
    """
    Calculate total daily caffeine intake in milligrams
    
    Problem it solves: Helps monitor daily caffeine consumption to stay
    within healthy limits (400mg recommended max for adults).
    
    Args:
        cups_coffee (int): Number of cups of coffee (8oz each)
        cups_tea (int): Number of cups of tea (8oz each)
        energy_drinks (int): Number of energy drinks (8oz each)
    
    Returns:
        dict: Caffeine breakdown and total intake
    """
    # Average caffeine content per 8oz serving
    coffee_mg = cups_coffee * 95    # 95mg per cup of coffee
    tea_mg = cups_tea * 25          # 25mg per cup of tea
    energy_mg = energy_drinks * 80  # 80mg per energy drink
    
    total_caffeine = coffee_mg + tea_mg + energy_mg
    
    return {
        'coffee': coffee_mg,
        'tea': tea_mg,
        'energy_drinks': energy_mg,
        'total_mg': total_caffeine,
        'under_limit': total_caffeine <= 400,
        'status': 'Safe' if total_caffeine <= 400 else 'Exceeds recommended limit'
    }


def calculate_commute_cost(miles_per_day, days_per_week, mpg, gas_price_per_gallon):
    """
    Calculate weekly and monthly commute costs
    
    Problem it solves: Helps budget for transportation costs and evaluate
    whether remote work or moving closer to work would save money.
    
    Args:
        miles_per_day (float): Round-trip miles to work
        days_per_week (int): Number of commute days per week
        mpg (float): Vehicle's miles per gallon
        gas_price_per_gallon (float): Current gas price per gallon
    
    Returns:
        dict: Weekly and monthly cost breakdown
    """
    if mpg <= 0:
        return "Error: MPG must be greater than 0"
    
    weekly_miles = miles_per_day * days_per_week
    weekly_gallons = weekly_miles / mpg
    weekly_cost = weekly_gallons * gas_price_per_gallon
    monthly_cost = weekly_cost * 4.33  # Average weeks per month
    
    return {
        'weekly_miles': round(weekly_miles, 1),
        'weekly_cost': round(weekly_cost, 2),
        'monthly_cost': round(monthly_cost, 2),
        'yearly_cost': round(monthly_cost * 12, 2)
    }


def main():
    """
    Demonstrate all toolkit functions with realistic examples
    """
    print("🛠️  Personal Python Toolkit Demo")
    print("=" * 50)
    
    # Academic function demo
    print("\n📚 Academic Helper:")
    current = 85.5
    target = 90
    final_weight = 0.25
    grade_needed = calculate_grade_needed(current, target, final_weight)
    print(f"Current grade: {current}%")
    print(f"Target grade: {target}%")
    print(f"Final exam weight: {final_weight*100}%")
    print(f"Grade needed on final: {grade_needed:.1f}%")
    
    # Finance function demo
    print("\n💰 Bill Splitter:")
    bill_total = 127.50
    people = 4
    tip = 18
    per_person, total = split_bill_with_tip(bill_total, people, tip)
    print(f"Bill total: ${bill_total}")
    print(f"People: {people}, Tip: {tip}%")
    print(f"Each person pays: ${per_person}")
    print(f"Total with tip: ${total}")
    
    # Study planning demo
    print("\n📖 Study Hour Calculator:")
    credits = 15
    difficulty = 2.8
    study_hours = calculate_study_hours_needed(credits, difficulty)
    print(f"Total credits: {credits}")
    print(f"Difficulty multiplier: {difficulty}")
    print(f"Recommended study hours/week: {study_hours}")
    
    # Fitness function demo
    print("\n🏃 Workout Pace Tracker:")
    distance = 3.1  # 5K
    time = 28.5
    pace = workout_pace_calculator(distance, time)
    print(f"Distance: {distance} miles")
    print(f"Time: {time} minutes")
    print(f"Pace: {pace}")
    
    # Health tracking demo
    print("\n☕ Caffeine Intake Monitor:")
    caffeine_data = caffeine_intake_tracker(cups_coffee=2, cups_tea=1, energy_drinks=1)
    print(f"Coffee: {caffeine_data['coffee']}mg")
    print(f"Tea: {caffeine_data['tea']}mg") 
    print(f"Energy drinks: {caffeine_data['energy_drinks']}mg")
    print(f"Total caffeine: {caffeine_data['total_mg']}mg")
    print(f"Status: {caffeine_data['status']}")
    
    # Transportation cost demo
    print("\n🚗 Commute Cost Calculator:")
    commute_data = calculate_commute_cost(
        miles_per_day=32, 
        days_per_week=5, 
        mpg=28, 
        gas_price_per_gallon=3.45
    )
    print(f"Weekly miles: {commute_data['weekly_miles']}")
    print(f"Weekly cost: ${commute_data['weekly_cost']}")
    print(f"Monthly cost: ${commute_data['monthly_cost']}")
    print(f"Yearly cost: ${commute_data['yearly_cost']}")
    
    print("\n" + "=" * 50)
    print("✅ Toolkit demo complete! All functions working properly.")


if __name__ == "__main__":
    main()