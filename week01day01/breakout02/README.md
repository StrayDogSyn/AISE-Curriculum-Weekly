# W1D1 Breakout 2: Personal Python Toolkit

## Overview
**Time:** 20 minutes  
**Goal:** Create a personalized Python toolkit with 3+ functions that solve real problems in your daily life

## Your Mission
Transform repetitive calculations or decision-making processes from your daily routine into reusable Python functions. Think about what you calculate on paper, in your head, or wish you had a quick tool for!

## Files in this Directory
- `personal_toolkit.py` - Complete toolkit with 6 practical functions
- `README.md` - This instruction file

## Functions Included

### 1. 📚 Academic Helper
- **Function:** `calculate_grade_needed()`
- **Problem:** Determines what score you need on a final exam to achieve your target grade
- **Example:** If you have 85.5% and want 90%, with final worth 25%, you need 103.5% (impossible!)

### 2. 💰 Bill Splitter  
- **Function:** `split_bill_with_tip()`
- **Problem:** Calculates how much each person owes when dining out with friends
- **Example:** $127.50 bill + 18% tip ÷ 4 people = $36.94 each

### 3. 📖 Study Hour Calculator
- **Function:** `calculate_study_hours_needed()`
- **Problem:** Estimates how many hours per week you should study based on course credits
- **Example:** 15 credits × 2.8 difficulty = 42.0 hours/week recommended

### 4. 🏃 Workout Pace Tracker
- **Function:** `workout_pace_calculator()`
- **Problem:** Converts workout data into easy-to-understand pace format
- **Example:** 3.1 miles in 28.5 minutes = 9:11 per mile

### 5. ☕ Caffeine Intake Monitor
- **Function:** `caffeine_intake_tracker()`
- **Problem:** Tracks daily caffeine consumption to stay within healthy limits
- **Example:** 2 coffees + 1 tea + 1 energy drink = 275mg (safe level)

### 6. 🚗 Commute Cost Calculator
- **Function:** `calculate_commute_cost()`
- **Problem:** Calculates transportation costs to help with budgeting decisions
- **Example:** 32 miles/day × 5 days × $3.45/gallon ÷ 28 mpg = $19.64/week

## How to Run
```bash
python personal_toolkit.py
```

## Instructions for Customization

### Step 1: Brainstorm (3 minutes)
Think about calculations you do regularly:
- **Fitness:** BMI, protein needs, running pace, workout splits
- **Finance:** Bill splitting, investment growth, loan payments
- **Academic:** Grade needed on final exam, study hours per credit
- **Food:** Recipe scaling, meal prep portions, nutrition tracking
- **Time:** Commute optimization, meeting scheduler, timezone converter
- **Hobbies:** Gaming statistics, crafting materials, collection value

### Step 2: Build Your Functions (12 minutes)
1. Replace existing functions or add new ones with meaningful names
2. Write clear docstrings explaining:
   - What problem it solves
   - Parameters needed
   - What it returns
3. Keep functions focused - each should do ONE thing well
4. Add input validation if time permits

### Step 3: Test & Demonstrate (5 minutes)
1. Update the `main()` function to showcase each function
2. Use realistic examples
3. Format output clearly
4. Be ready to share one function with the group!

## Tips for Success
- **Start simple:** Get a basic version working first, then enhance
- **Use meaningful names:** `calculate_macros()` not `func1()`
- **Think about edge cases:** What if someone enters 0 or negative values?
- **Make it personal:** The best functions solve YOUR actual problems
- **Comments help:** Add brief comments for complex calculations

## Sharing Format
When we reconvene, be ready to share:
1. **Function name & purpose** (15 seconds)
2. **Problem it solves** (15 seconds)
3. **Quick demo** (30 seconds)

## Example Output
```
🛠️  Personal Python Toolkit Demo
==================================================

📚 Academic Helper:
Current grade: 85.5%
Target grade: 90%
Final exam weight: 25.0%
Grade needed on final: 103.5%

💰 Bill Splitter:
Bill total: $127.5
People: 4, Tip: 18%
Each person pays: $36.94
Total with tip: $147.85

📖 Study Hour Calculator:
Total credits: 15
Difficulty multiplier: 2.8
Recommended study hours/week: 42.0

🏃 Workout Pace Tracker:
Distance: 3.1 miles
Time: 28.5 minutes
Pace: 9:11 per mile

☕ Caffeine Intake Monitor:
Coffee: 190mg
Tea: 25mg
Energy drinks: 80mg
Total caffeine: 295mg
Status: Safe

🚗 Commute Cost Calculator:
Weekly miles: 160.0
Weekly cost: $19.64
Monthly cost: $85.04
Yearly cost: $1020.48

==================================================
✅ Toolkit demo complete! All functions working properly.
```