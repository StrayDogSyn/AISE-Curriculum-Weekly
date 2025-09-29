#!/usr/bin/env python3
"""
W1D1 Breakout 1: Personal Finance Calculator - Starter Code Implementation

This file implements the exact functions from the starter code with complete
functionality, demonstrating how the original problem decomposition works.
"""

from decimal import Decimal
from datetime import datetime
import logging

# Configure logging for demonstration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_total_income(salary, side_hustle=0):
    """
    Calculate total monthly income.
    
    This is the exact function signature from the starter code,
    now with complete implementation following Python best practices.
    
    Args:
        salary: Primary salary income (can be int, float, or Decimal)
        side_hustle: Additional income from side activities (default: 0)
        
    Returns:
        Decimal: Total monthly income
    """
    try:
        # Convert to Decimal for precision
        salary_decimal = Decimal(str(salary))
        side_hustle_decimal = Decimal(str(side_hustle))
        
        # Validate non-negative values
        if salary_decimal < 0 or side_hustle_decimal < 0:
            raise ValueError("Income values cannot be negative")
        
        total = salary_decimal + side_hustle_decimal
        logger.info(f"Total income calculated: ${total:.2f}")
        return total
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid income values: {e}")


def calculate_fixed_expenses(rent, insurance, phone, internet):
    """
    Add up monthly fixed costs.
    
    This is the exact function signature from the starter code,
    implementing the core fixed expense calculation.
    
    Args:
        rent: Monthly rent or mortgage payment
        insurance: Monthly insurance premiums  
        phone: Monthly phone bill
        internet: Monthly internet bill
        
    Returns:
        Decimal: Total fixed monthly expenses
    """
    try:
        # Convert all inputs to Decimal for precision
        expenses = [rent, insurance, phone, internet]
        decimal_expenses = []
        
        for expense in expenses:
            decimal_val = Decimal(str(expense))
            if decimal_val < 0:
                raise ValueError("Expense values cannot be negative")
            decimal_expenses.append(decimal_val)
        
        total_fixed = sum(decimal_expenses)
        logger.info(f"Fixed expenses calculated: ${total_fixed:.2f}")
        return total_fixed
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid expense values: {e}")


def calculate_savings_potential(income, fixed_expenses, variable_expenses):
    """
    Determine how much can be saved.
    
    This is the exact function signature from the starter code,
    calculating available savings after all expenses.
    
    Args:
        income: Total monthly income
        fixed_expenses: Total fixed monthly expenses
        variable_expenses: Total variable monthly expenses
        
    Returns:
        Decimal: Amount available for savings (can be negative if overspending)
    """
    try:
        # Convert to Decimal for precision
        income_decimal = Decimal(str(income))
        fixed_decimal = Decimal(str(fixed_expenses))
        variable_decimal = Decimal(str(variable_expenses))
        
        # Validate non-negative values (except savings can be negative)
        if income_decimal < 0 or fixed_decimal < 0 or variable_decimal < 0:
            raise ValueError("Income and expense values cannot be negative")
        
        savings_potential = income_decimal - fixed_decimal - variable_decimal
        
        if savings_potential >= 0:
            logger.info(f"Savings potential: ${savings_potential:.2f} available")
        else:
            logger.warning(f"Overspending by: ${abs(savings_potential):.2f}")
            
        return savings_potential
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid calculation values: {e}")


def generate_budget_report(name, income, expenses, savings):
    """
    Create a formatted budget summary.
    
    This is the exact function signature from the starter code,
    creating a comprehensive and visually appealing budget report.
    
    Args:
        name: Person's name for the report
        income: Total monthly income
        expenses: Total monthly expenses  
        savings: Available savings amount
        
    Returns:
        str: Formatted budget report
    """
    try:
        # Convert to Decimal for consistency
        income_decimal = Decimal(str(income))
        expenses_decimal = Decimal(str(expenses))
        savings_decimal = Decimal(str(savings))
        
        # Calculate percentages
        expense_percentage = (expenses_decimal / income_decimal * 100) if income_decimal > 0 else 0
        savings_percentage = (savings_decimal / income_decimal * 100) if income_decimal > 0 else 0
        
        # Determine status
        if savings_percentage >= 20:
            status = "🟢 Excellent"
            status_msg = "Meeting or exceeding 20% savings goal!"
        elif savings_percentage >= 10:
            status = "🟡 Good"
            status_msg = "Good progress toward financial goals."
        elif savings_percentage >= 0:
            status = "🟠 Fair"
            status_msg = "Breaking even, but room for improvement."
        else:
            status = "🔴 Alert"
            status_msg = "Overspending - immediate action needed!"
        
        current_month = datetime.now().strftime("%B %Y")
        
        # Create formatted report
        report = f"""
{'='*70}
           PERSONAL BUDGET REPORT - {current_month}
{'='*70}
Name: {name}
Date Generated: {datetime.now().strftime("%m/%d/%Y at %I:%M %p")}

💰 INCOME & EXPENSES
{'-'*40}
Monthly Income:          ${income_decimal:>10,.2f}
Monthly Expenses:        ${expenses_decimal:>10,.2f}  ({expense_percentage:>5.1f}%)
Available for Savings:   ${savings_decimal:>10,.2f}  ({savings_percentage:>5.1f}%)

📊 FINANCIAL HEALTH STATUS
{'-'*40}
Overall Status: {status}
{status_msg}

💡 QUICK RECOMMENDATIONS
{'-'*40}"""

        # Add specific recommendations based on financial situation
        if savings_percentage >= 20:
            report += """
• Excellent job! Consider increasing investment contributions
• Build emergency fund if not already at 6 months expenses
• Look into tax-advantaged retirement accounts"""
        elif savings_percentage >= 10:
            report += """
• Try to increase savings rate to 20% if possible
• Review variable expenses for reduction opportunities
• Consider additional income sources"""
        elif savings_percentage >= 0:
            report += """
• Focus on reducing variable expenses first
• Create a strict monthly budget and stick to it
• Look for ways to increase income"""
        else:
            report += """
• ⚠️  URGENT: You're spending more than you earn
• Immediately cut all non-essential expenses
• Consider debt consolidation if applicable
• Seek financial counseling if needed"""

        report += f"""

📋 EXPENSE BREAKDOWN TARGET GUIDELINES
{'-'*40}
Housing (Rent/Mortgage):     ≤ 30% of income
Transportation:              ≤ 15% of income  
Food:                        ≤ 12% of income
Savings:                     ≥ 20% of income
Other Expenses:              Remaining balance

{'='*70}
Report generated by Personal Finance Calculator v1.0
{'='*70}
"""
        
        logger.info(f"Budget report generated for {name}")
        return report
        
    except (ValueError, TypeError) as e:
        error_msg = f"Error generating budget report: {e}"
        logger.error(error_msg)
        return error_msg


def demo_starter_functions():
    """
    Demonstrate all starter code functions with sample data.
    
    This shows exactly how the original starter code functions work
    with realistic financial data and proper error handling.
    """
    print("🎯 W1D1 Starter Code Functions Demo")
    print("=" * 50)
    print("Testing the exact functions from the starter code...")
    print()
    
    try:
        # Step 1: Calculate total income (as in starter code comment)
        print("Step 1: Calculate total income")
        income = calculate_total_income(3000, 500)
        print(f"Total income: ${income}")
        print(f"✅ calculate_total_income(3000, 500) = ${income:.2f}")
        print()
        
        # Step 2: Calculate fixed expenses
        print("Step 2: Calculate fixed expenses")
        fixed = calculate_fixed_expenses(1200, 250, 80, 60)
        print(f"✅ calculate_fixed_expenses(1200, 250, 80, 60) = ${fixed:.2f}")
        print("   (Rent: $1200, Insurance: $250, Phone: $80, Internet: $60)")
        print()
        
        # Step 3: Calculate variable expenses (simulated)
        print("Step 3: Calculate variable expenses")
        variable_expenses = Decimal('800')  # Food, entertainment, etc.
        print(f"Variable expenses (estimated): ${variable_expenses:.2f}")
        print()
        
        # Step 4: Calculate savings potential
        print("Step 4: Calculate savings potential")
        savings = calculate_savings_potential(income, fixed, variable_expenses)
        print(f"✅ calculate_savings_potential({income}, {fixed}, {variable_expenses}) = ${savings:.2f}")
        print()
        
        # Step 5: Generate budget report
        print("Step 5: Generate budget report")
        total_expenses = fixed + variable_expenses
        report = generate_budget_report("Demo Student", income, total_expenses, savings)
        print("✅ generate_budget_report() completed successfully!")
        print()
        print("Generated Report:")
        print(report)
        
        # Show the exact test case from starter code
        print("\n" + "🧪 STARTER CODE TEST CASE")
        print("=" * 40)
        print("# Step 3: Test your functions")
        print("# income = calculate_total_income(3000, 500)")
        print("# print(f'Total income: ${income}')")
        print()
        print("RESULT:")
        test_income = calculate_total_income(3000, 500)
        print(f"Total income: ${test_income}")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    # Run the demo when file is executed directly
    demo_starter_functions()