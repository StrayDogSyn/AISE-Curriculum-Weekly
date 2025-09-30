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


def sleep_vs_energy_calculator(hours_slept, sleep_quality=7, stress_level=5):
    """
    Calculate energy level based on sleep hours, quality, and stress
    
    Problem it solves: Helps optimize sleep patterns by understanding how
    different factors affect daily energy levels for better productivity.
    
    Args:
        hours_slept (float): Number of hours slept last night
        sleep_quality (int): Sleep quality rating 1-10 (default: 7)
        stress_level (int): Current stress level 1-10 (default: 5)
    
    Returns:
        dict: Energy analysis with recommendations
    """
    if hours_slept < 0 or hours_slept > 24:
        return "Error: Hours slept must be between 0 and 24"
    if not (1 <= sleep_quality <= 10):
        return "Error: Sleep quality must be between 1 and 10"
    if not (1 <= stress_level <= 10):
        return "Error: Stress level must be between 1 and 10"
    
    # Base energy from sleep duration (optimal: 7-9 hours)
    if 7 <= hours_slept <= 9:
        base_energy = 100
    elif 6 <= hours_slept < 7 or 9 < hours_slept <= 10:
        base_energy = 85
    elif 5 <= hours_slept < 6 or 10 < hours_slept <= 11:
        base_energy = 70
    else:
        base_energy = 50
    
    # Quality modifier (1-10 scale becomes 0.5-1.5 multiplier)
    quality_modifier = 0.5 + (sleep_quality / 10)
    
    # Stress penalty (1-10 scale becomes 0-45 point reduction)
    stress_penalty = (stress_level - 1) * 5
    
    # Calculate final energy level
    energy_level = max(0, min(100, (base_energy * quality_modifier) - stress_penalty))
    
    # Generate recommendations
    recommendations = []
    if hours_slept < 7:
        recommendations.append("Consider going to bed earlier for more sleep")
    elif hours_slept > 9:
        recommendations.append("You might be oversleeping - try a consistent 7-8 hour schedule")
    
    if sleep_quality < 6:
        recommendations.append("Improve sleep environment: dark, cool, quiet room")
    
    if stress_level > 7:
        recommendations.append("Try stress reduction: meditation, exercise, or deep breathing")
    
    if energy_level < 60:
        recommendations.append("Consider a short nap (20-30 min) or light exercise")
    
    return {
        'energy_level': round(energy_level, 1),
        'sleep_hours': hours_slept,
        'quality_rating': sleep_quality,
        'stress_rating': stress_level,
        'status': 'High Energy' if energy_level >= 80 else 'Moderate Energy' if energy_level >= 60 else 'Low Energy',
        'recommendations': recommendations
    }


def ai_project_time_estimator(complexity_level, team_size, experience_level):
    """
    Estimate AI/ML project completion time based on complexity and team factors
    
    Problem it solves: Helps AI engineers like me estimate realistic project
    timelines for client proposals and resource planning.
    
    Args:
        complexity_level (str): 'simple', 'moderate', 'complex', 'research'
        team_size (int): Number of team members
        experience_level (str): 'junior', 'mid', 'senior', 'expert'
    
    Returns:
        dict: Project timeline estimates and recommendations
    """
    complexity_hours = {
        'simple': 80,      # Basic ML model, existing data
        'moderate': 200,   # Custom model, data preprocessing
        'complex': 500,    # Multi-model system, extensive engineering
        'research': 1000   # Novel approach, R&D required
    }
    
    experience_multipliers = {
        'junior': 1.8,     # Learning curve, more debugging
        'mid': 1.3,        # Some efficiency, occasional guidance needed
        'senior': 1.0,     # Baseline efficiency
        'expert': 0.7      # High efficiency, fewer roadblocks
    }
    
    if complexity_level not in complexity_hours:
        return "Error: Complexity must be 'simple', 'moderate', 'complex', or 'research'"
    if experience_level not in experience_multipliers:
        return "Error: Experience must be 'junior', 'mid', 'senior', or 'expert'"
    if team_size < 1:
        return "Error: Team size must be at least 1"
    
    # Base hours for complexity
    base_hours = complexity_hours[complexity_level]
    
    # Apply experience multiplier
    adjusted_hours = base_hours * experience_multipliers[experience_level]
    
    # Team size efficiency (diminishing returns)
    if team_size == 1:
        team_efficiency = 1.0
    elif team_size <= 3:
        team_efficiency = 0.8  # Small team, good coordination
    elif team_size <= 6:
        team_efficiency = 0.9  # Medium team, some overhead
    else:
        team_efficiency = 1.1  # Large team, communication overhead
    
    final_hours = adjusted_hours * team_efficiency
    
    # Convert to weeks (40 hours/week)
    weeks = final_hours / 40
    
    # Generate project phases
    phases = {
        'research_planning': round(final_hours * 0.15),
        'data_preparation': round(final_hours * 0.25),
        'model_development': round(final_hours * 0.35),
        'testing_validation': round(final_hours * 0.15),
        'deployment_docs': round(final_hours * 0.10)
    }
    
    return {
        'total_hours': round(final_hours),
        'estimated_weeks': round(weeks, 1),
        'complexity': complexity_level,
        'team_size': team_size,
        'experience': experience_level,
        'phases': phases,
        'daily_hours_needed': round(final_hours / (weeks * 5), 1) if weeks > 0 else 0
    }


def cryptocurrency_portfolio_tracker(investments, current_prices):
    """
    Track cryptocurrency portfolio performance and calculate gains/losses
    
    Problem it solves: Helps track crypto investments across multiple coins
    with real-time performance analysis for informed trading decisions.
    
    Args:
        investments (dict): {'symbol': {'amount': float, 'buy_price': float}}
        current_prices (dict): {'symbol': float} current price per coin
    
    Returns:
        dict: Portfolio analysis with performance metrics
    """
    if not investments or not current_prices:
        return "Error: Both investments and current prices are required"
    
    portfolio_analysis = {
        'coins': {},
        'total_invested': 0,
        'current_value': 0,
        'total_gain_loss': 0,
        'total_gain_loss_percent': 0
    }
    
    for symbol, investment in investments.items():
        if symbol not in current_prices:
            continue
            
        amount = investment['amount']
        buy_price = investment['buy_price']
        current_price = current_prices[symbol]
        
        invested_amount = amount * buy_price
        current_value = amount * current_price
        gain_loss = current_value - invested_amount
        gain_loss_percent = (gain_loss / invested_amount * 100) if invested_amount > 0 else 0
        
        portfolio_analysis['coins'][symbol] = {
            'amount': amount,
            'buy_price': buy_price,
            'current_price': current_price,
            'invested': round(invested_amount, 2),
            'current_value': round(current_value, 2),
            'gain_loss': round(gain_loss, 2),
            'gain_loss_percent': round(gain_loss_percent, 2),
            'status': 'Profit' if gain_loss > 0 else 'Loss' if gain_loss < 0 else 'Break Even'
        }
        
        portfolio_analysis['total_invested'] += invested_amount
        portfolio_analysis['current_value'] += current_value
    
    portfolio_analysis['total_gain_loss'] = portfolio_analysis['current_value'] - portfolio_analysis['total_invested']
    
    if portfolio_analysis['total_invested'] > 0:
        portfolio_analysis['total_gain_loss_percent'] = round(
            (portfolio_analysis['total_gain_loss'] / portfolio_analysis['total_invested']) * 100, 2
        )
    
    # Round totals
    portfolio_analysis['total_invested'] = round(portfolio_analysis['total_invested'], 2)
    portfolio_analysis['current_value'] = round(portfolio_analysis['current_value'], 2)
    portfolio_analysis['total_gain_loss'] = round(portfolio_analysis['total_gain_loss'], 2)
    
    return portfolio_analysis


def remote_work_productivity_score(work_hours, meetings, deep_work_blocks, distractions):
    """
    Calculate daily productivity score for remote work optimization
    
    Problem it solves: Helps remote workers like me analyze daily productivity
    patterns to optimize work-from-home effectiveness and time management.
    
    Args:
        work_hours (float): Total hours worked today
        meetings (int): Number of meetings attended
        deep_work_blocks (int): Number of uninterrupted work sessions (2+ hours)
        distractions (int): Number of significant interruptions
    
    Returns:
        dict: Productivity analysis with optimization suggestions
    """
    if work_hours < 0 or work_hours > 16:
        return "Error: Work hours should be between 0 and 16"
    if meetings < 0 or deep_work_blocks < 0 or distractions < 0:
        return "Error: All counts must be non-negative"
    
    # Base score from work hours (optimal: 6-8 hours)
    if 6 <= work_hours <= 8:
        hours_score = 40
    elif 4 <= work_hours < 6 or 8 < work_hours <= 10:
        hours_score = 35
    elif work_hours < 4:
        hours_score = 20
    else:  # > 10 hours
        hours_score = 25  # Diminishing returns, potential burnout
    
    # Meeting efficiency (optimal: 2-4 meetings)
    if meetings <= 1:
        meeting_score = 25  # Good focus time
    elif 2 <= meetings <= 4:
        meeting_score = 30  # Balanced collaboration
    elif 5 <= meetings <= 6:
        meeting_score = 20  # Meeting-heavy day
    else:
        meeting_score = 10  # Meeting overload
    
    # Deep work bonus (each block worth 10 points, max 30)
    deep_work_score = min(deep_work_blocks * 10, 30)
    
    # Distraction penalty (each distraction -3 points)
    distraction_penalty = distractions * 3
    
    # Calculate final score
    productivity_score = max(0, hours_score + meeting_score + deep_work_score - distraction_penalty)
    
    # Generate productivity level
    if productivity_score >= 80:
        level = "Highly Productive"
        emoji = "🚀"
    elif productivity_score >= 65:
        level = "Productive"
        emoji = "✅"
    elif productivity_score >= 50:
        level = "Moderately Productive"
        emoji = "⚠️"
    else:
        level = "Low Productivity"
        emoji = "📉"
    
    # Generate suggestions
    suggestions = []
    if work_hours < 6:
        suggestions.append("Consider extending work hours for better output")
    elif work_hours > 10:
        suggestions.append("Reduce work hours to avoid burnout and maintain quality")
    
    if meetings > 5:
        suggestions.append("Try to consolidate or decline non-essential meetings")
    elif meetings == 0:
        suggestions.append("Consider scheduling team check-ins for collaboration")
    
    if deep_work_blocks == 0:
        suggestions.append("Block calendar time for 2+ hour focused work sessions")
    elif deep_work_blocks >= 3:
        suggestions.append("Excellent deep work! Maintain this focused approach")
    
    if distractions > 5:
        suggestions.append("Minimize distractions: notifications off, dedicated workspace")
    
    return {
        'productivity_score': productivity_score,
        'level': level,
        'emoji': emoji,
        'work_hours': work_hours,
        'meetings': meetings,
        'deep_work_blocks': deep_work_blocks,
        'distractions': distractions,
        'breakdown': {
            'hours_score': hours_score,
            'meeting_score': meeting_score,
            'deep_work_score': deep_work_score,
            'distraction_penalty': -distraction_penalty
        },
        'suggestions': suggestions
    }


def main():
    """
    Demonstrate all toolkit functions with realistic examples
    """
    print("🛠️  Eric 'Hunter' Petross's Personal Python Toolkit Demo")
    print("Applied AI Solutions Engineer | @StrayDogSyn")
    print("=" * 60)
    
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
    
    # NEW: Sleep vs Energy Calculator
    print("\n😴 Sleep vs Energy Calculator:")
    sleep_data = sleep_vs_energy_calculator(hours_slept=6.5, sleep_quality=6, stress_level=7)
    print(f"Hours slept: {sleep_data['sleep_hours']}")
    print(f"Sleep quality: {sleep_data['quality_rating']}/10")
    print(f"Stress level: {sleep_data['stress_rating']}/10")
    print(f"Energy level: {sleep_data['energy_level']}% ({sleep_data['status']})")
    print(f"Recommendations: {', '.join(sleep_data['recommendations'][:2])}")
    
    # NEW: AI Project Time Estimator
    print("\n🤖 AI Project Time Estimator:")
    project_data = ai_project_time_estimator('complex', 3, 'senior')
    print(f"Project complexity: {project_data['complexity']}")
    print(f"Team size: {project_data['team_size']} ({project_data['experience']} level)")
    print(f"Estimated time: {project_data['estimated_weeks']} weeks ({project_data['total_hours']} hours)")
    print(f"Daily hours needed: {project_data['daily_hours_needed']} hours/day")
    
    # NEW: Cryptocurrency Portfolio Tracker
    print("\n₿ Crypto Portfolio Tracker:")
    investments = {
        'BTC': {'amount': 0.1, 'buy_price': 45000},
        'ETH': {'amount': 2.0, 'buy_price': 3000}
    }
    current_prices = {'BTC': 43000, 'ETH': 3200}
    crypto_data = cryptocurrency_portfolio_tracker(investments, current_prices)
    print(f"Total invested: ${crypto_data['total_invested']}")
    print(f"Current value: ${crypto_data['current_value']}")
    print(f"Total gain/loss: ${crypto_data['total_gain_loss']} ({crypto_data['total_gain_loss_percent']}%)")
    
    # NEW: Remote Work Productivity Score
    print("\n🏠 Remote Work Productivity Score:")
    productivity_data = remote_work_productivity_score(
        work_hours=7.5, meetings=3, deep_work_blocks=2, distractions=4
    )
    print(f"Productivity Score: {productivity_data['productivity_score']}/100 {productivity_data['emoji']}")
    print(f"Level: {productivity_data['level']}")
    print(f"Work Hours: {productivity_data['work_hours']}, Meetings: {productivity_data['meetings']}")
    print(f"Deep Work Blocks: {productivity_data['deep_work_blocks']}, Distractions: {productivity_data['distractions']}")
    print(f"Top suggestion: {productivity_data['suggestions'][0] if productivity_data['suggestions'] else 'Keep up the great work!'}")
    
    print("\n" + "=" * 60)
    print("✅ Enhanced AI Solutions Toolkit demo complete! All functions optimized for professional use.")


if __name__ == "__main__":
    main()