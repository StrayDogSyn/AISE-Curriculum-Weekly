#!/usr/bin/env python3
"""
Demo Script for Personal Finance Calculator
W1D1 Breakout Activity

This script demonstrates the calculator with sample data for quick testing.
"""

import sys
import os
from decimal import Decimal

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from personal_finance_calculator import PersonalFinanceCalculator, ExpenseCategory, FinancialData
from starter_code_implementation import demo_starter_functions


def demo_with_sample_data():
    """Demonstrate the calculator with predefined sample data."""
    print("🎯 Personal Finance Calculator Demo")
    print("=" * 50)
    print("Using sample data for quick demonstration...")
    print()
    
    # Create calculator instance
    calculator = PersonalFinanceCalculator()
    
    # Create sample financial data
    sample_expenses = {
        ExpenseCategory.HOUSING: Decimal("1500.00"),      # 30% of income
        ExpenseCategory.FOOD: Decimal("600.00"),          # 12% of income
        ExpenseCategory.TRANSPORTATION: Decimal("400.00"), # 8% of income
        ExpenseCategory.UTILITIES: Decimal("200.00"),      # 4% of income
        ExpenseCategory.ENTERTAINMENT: Decimal("300.00"),  # 6% of income
        ExpenseCategory.HEALTHCARE: Decimal("150.00"),     # 3% of income
        ExpenseCategory.OTHER: Decimal("100.00")           # 2% of income
    }
    
    calculator.financial_data = FinancialData(
        monthly_income=Decimal("5000.00"),
        expenses=sample_expenses,
        savings_goal_percentage=Decimal("20")  # 20% savings goal
    )
    
    print("📊 Sample Financial Data:")
    print(f"Monthly Income: ${calculator.financial_data.monthly_income:,.2f}")
    print(f"Savings Goal: {calculator.financial_data.savings_goal_percentage}%")
    print()
    
    print("💸 Monthly Expenses:")
    for category, amount in sample_expenses.items():
        percentage = (amount / calculator.financial_data.monthly_income) * 100
        print(f"  {category.value.title():15}: ${amount:7.2f} ({percentage:4.1f}%)")
    print()
    
    # Perform analysis
    try:
        analysis = calculator.analyze_budget()
        calculator.display_results(analysis)
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")


def demo_interactive():
    """Run the full interactive calculator."""
    print("\n" + "=" * 50)
    print("🎮 Interactive Mode")
    print("=" * 50)
    print("Now let's try the interactive calculator!")
    print("You can enter your own financial data...")
    print()
    
    calculator = PersonalFinanceCalculator()
    calculator.run_calculator()


def main():
    """Main demo function."""
    print("🚀 W1D1 Personal Finance Calculator Demo")
    print("This demonstrates Python best practices in action!")
    print()
    
    # First show the starter code functions
    print("=" * 60)
    print("🎯 PART 1: STARTER CODE FUNCTIONS DEMO")
    print("=" * 60)
    demo_starter_functions()
    
    print("\n" + "=" * 60)
    print("🚀 PART 2: ENHANCED APPLICATION DEMO")
    print("=" * 60)
    
    # Show sample data demo
    demo_with_sample_data()
    
    # Ask if user wants to try interactive mode
    print("\n" + "=" * 50)
    print("Would you like to try the interactive calculator?")
    choice = input("Enter 'yes' to continue or any other key to exit: ").lower().strip()
    
    if choice in ['yes', 'y']:
        demo_interactive()
    else:
        print("\n🎉 Demo completed! Thank you for exploring the Personal Finance Calculator.")
        print()
        print("💡 Key Python concepts demonstrated:")
        print("  ✅ Object-Oriented Programming")
        print("  ✅ Type Hints & Documentation")
        print("  ✅ Error Handling")
        print("  ✅ Data Classes & Enums")
        print("  ✅ Decimal Precision")
        print("  ✅ Logging & Monitoring")
        print("  ✅ Input Validation")
        print("  ✅ Modular Design")
        print("  ✅ Starter Code Function Implementation")


if __name__ == "__main__":
    main()