#!/usr/bin/env python3
"""
Test file for Personal Finance Calculator
W1D1 Breakout Activity

Simple tests to verify the calculator functionality.
"""

import sys
import os
from decimal import Decimal

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from personal_finance_calculator import PersonalFinanceCalculator, ExpenseCategory, FinancialData
from starter_code_implementation import (
    calculate_total_income, 
    calculate_fixed_expenses, 
    calculate_savings_potential, 
    generate_budget_report
)


def test_calculator_validation():
    """Test input validation functionality."""
    calculator = PersonalFinanceCalculator()
    
    # Test valid amount
    try:
        result = calculator.validate_amount("1000.50")
        assert result == Decimal("1000.50")
        print("✅ Valid amount test passed")
    except Exception as e:
        print(f"❌ Valid amount test failed: {e}")
    
    # Test invalid amount
    try:
        calculator.validate_amount("invalid")
        print("❌ Invalid amount test failed - should have raised ValueError")
    except ValueError:
        print("✅ Invalid amount test passed")
    except Exception as e:
        print(f"❌ Invalid amount test failed with unexpected error: {e}")
    
    # Test negative amount
    try:
        calculator.validate_amount("-100")
        print("❌ Negative amount test failed - should have raised ValueError")
    except ValueError:
        print("✅ Negative amount test passed")
    except Exception as e:
        print(f"❌ Negative amount test failed with unexpected error: {e}")


def test_calculator_calculations():
    """Test calculation functionality."""
    calculator = PersonalFinanceCalculator()
    
    # Create sample financial data
    expenses = {
        ExpenseCategory.HOUSING: Decimal("1500"),
        ExpenseCategory.FOOD: Decimal("600"),
        ExpenseCategory.TRANSPORTATION: Decimal("400"),
        ExpenseCategory.UTILITIES: Decimal("200"),
        ExpenseCategory.ENTERTAINMENT: Decimal("300"),
        ExpenseCategory.HEALTHCARE: Decimal("150"),
        ExpenseCategory.OTHER: Decimal("100")
    }
    
    calculator.financial_data = FinancialData(
        monthly_income=Decimal("5000"),
        expenses=expenses,
        savings_goal_percentage=Decimal("20")
    )
    
    # Test total expenses calculation
    total_expenses = calculator.calculate_total_expenses(expenses)
    expected_total = Decimal("3250")
    if total_expenses == expected_total:
        print("✅ Total expenses calculation test passed")
    else:
        print(f"❌ Total expenses test failed: expected {expected_total}, got {total_expenses}")
    
    # Test remaining income calculation
    remaining = calculator.calculate_remaining_income(Decimal("5000"), total_expenses)
    expected_remaining = Decimal("1750")
    if remaining == expected_remaining:
        print("✅ Remaining income calculation test passed")
    else:
        print(f"❌ Remaining income test failed: expected {expected_remaining}, got {remaining}")
    
    # Test savings potential calculation
    savings = calculator.calculate_target_savings(Decimal("5000"), Decimal("20"))
    expected_savings = Decimal("1000")
    if savings == expected_savings:
        print("✅ Savings potential calculation test passed")
    else:
        print(f"❌ Savings potential test failed: expected {expected_savings}, got {savings}")


def test_budget_analysis():
    """Test comprehensive budget analysis."""
    calculator = PersonalFinanceCalculator()
    
    # Create sample financial data
    expenses = {
        ExpenseCategory.HOUSING: Decimal("1500"),
        ExpenseCategory.FOOD: Decimal("600"),
        ExpenseCategory.TRANSPORTATION: Decimal("400"),
        ExpenseCategory.UTILITIES: Decimal("200"),
        ExpenseCategory.ENTERTAINMENT: Decimal("300"),
        ExpenseCategory.HEALTHCARE: Decimal("150"),
        ExpenseCategory.OTHER: Decimal("100")
    }
    
    calculator.financial_data = FinancialData(
        monthly_income=Decimal("5000"),
        expenses=expenses,
        savings_goal_percentage=Decimal("20")
    )
    
    try:
        analysis = calculator.analyze_budget()
        
        # Verify analysis components
        expected_keys = [
            'monthly_income', 'total_expenses', 'remaining_income',
            'target_savings', 'savings_gap', 'expense_percentage',
            'expense_breakdown'
        ]
        
        for key in expected_keys:
            if key not in analysis:
                print(f"❌ Budget analysis missing key: {key}")
                return
        
        print("✅ Budget analysis test passed")
        
        # Test recommendations generation
        recommendations = calculator.get_financial_recommendations(analysis)
        if len(recommendations) > 0:
            print("✅ Recommendations generation test passed")
        else:
            print("❌ Recommendations generation test failed")
            
    except Exception as e:
        print(f"❌ Budget analysis test failed: {e}")


def test_starter_code_functions():
    """Test the original starter code functions."""
    print("🧪 Testing Starter Code Functions")
    print("-" * 35)
    
    # Test calculate_total_income
    try:
        income = calculate_total_income(3000, 500)
        expected = Decimal('3500')
        if income == expected:
            print("✅ calculate_total_income test passed")
        else:
            print(f"❌ calculate_total_income test failed: expected {expected}, got {income}")
    except Exception as e:
        print(f"❌ calculate_total_income test failed: {e}")
    
    # Test calculate_fixed_expenses
    try:
        fixed = calculate_fixed_expenses(1200, 250, 80, 60)
        expected = Decimal('1590')
        if fixed == expected:
            print("✅ calculate_fixed_expenses test passed")
        else:
            print(f"❌ calculate_fixed_expenses test failed: expected {expected}, got {fixed}")
    except Exception as e:
        print(f"❌ calculate_fixed_expenses test failed: {e}")
    
    # Test calculate_savings_potential  
    try:
        savings = calculate_savings_potential(3500, 1590, 800)
        expected = Decimal('1110')
        if savings == expected:
            print("✅ calculate_savings_potential test passed")
        else:
            print(f"❌ calculate_savings_potential test failed: expected {expected}, got {savings}")
    except Exception as e:
        print(f"❌ calculate_savings_potential test failed: {e}")
    
    # Test generate_budget_report
    try:
        report = generate_budget_report("Test User", 3500, 2390, 1110)
        if "Test User" in report and "3,500.00" in report:
            print("✅ generate_budget_report test passed")
        else:
            print("❌ generate_budget_report test failed")
    except Exception as e:
        print(f"❌ generate_budget_report test failed: {e}")


def test_enhanced_calculator_functions():
    """Test the enhanced calculator functions that use starter code."""
    calculator = PersonalFinanceCalculator()
    
    print("🔧 Testing Enhanced Calculator Functions")
    print("-" * 40)
    
    # Test enhanced calculate_total_income method
    try:
        income = calculator.calculate_total_income(Decimal('3000'), Decimal('500'))
        expected = Decimal('3500')
        if income == expected:
            print("✅ Enhanced calculate_total_income test passed")
        else:
            print(f"❌ Enhanced calculate_total_income test failed: expected {expected}, got {income}")
    except Exception as e:
        print(f"❌ Enhanced calculate_total_income test failed: {e}")
    
    # Test enhanced calculate_fixed_expenses method
    try:
        fixed = calculator.calculate_fixed_expenses(
            Decimal('1200'), Decimal('250'), Decimal('80'), Decimal('60')
        )
        expected = Decimal('1590')
        if fixed == expected:
            print("✅ Enhanced calculate_fixed_expenses test passed")
        else:
            print(f"❌ Enhanced calculate_fixed_expenses test failed: expected {expected}, got {fixed}")
    except Exception as e:
        print(f"❌ Enhanced calculate_fixed_expenses test failed: {e}")
    
    # Test enhanced calculate_savings_potential method
    try:
        savings = calculator.calculate_savings_potential(
            Decimal('3500'), Decimal('1590'), Decimal('800')
        )
        expected = Decimal('1110')
        if savings == expected:
            print("✅ Enhanced calculate_savings_potential test passed")
        else:
            print(f"❌ Enhanced calculate_savings_potential test failed: expected {expected}, got {savings}")
    except Exception as e:
        print(f"❌ Enhanced calculate_savings_potential test failed: {e}")
    
    # Test enhanced generate_budget_report method
    try:
        report = calculator.generate_budget_report("Enhanced User", Decimal('3500'), Decimal('2390'), Decimal('1110'))
        if "Enhanced User" in report and "3,500.00" in report:
            print("✅ Enhanced generate_budget_report test passed")
        else:
            print("❌ Enhanced generate_budget_report test failed")
    except Exception as e:
        print(f"❌ Enhanced generate_budget_report test failed: {e}")
def main():
    """Run all tests."""
    print("🧪 Running Personal Finance Calculator Tests")
    print("=" * 50)
    
    test_calculator_validation()
    print()
    
    test_calculator_calculations()
    print()
    
    test_budget_analysis()
    print()
    
    test_starter_code_functions()
    print()
    
    test_enhanced_calculator_functions()
    print()
    
    print("=" * 50)
    print("🎉 Test suite completed!")


if __name__ == "__main__":
    main()