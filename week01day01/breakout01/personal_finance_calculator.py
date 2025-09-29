#!/usr/bin/env python3
"""
Personal Finance Calculator - W1D1 Breakout Activity

A comprehensive personal finance calculator that helps users analyze their
monthly budget and calculate savings potential using Python best practices.

Author: AISE Curriculum
Date: September 29, 2025
Version: 1.0.0
"""

from decimal import Decimal, InvalidOperation
from typing import Dict, List, Optional, Tuple, Union
import logging
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ExpenseCategory(Enum):
    """Enumeration for expense categories."""
    HOUSING = "housing"
    FOOD = "food"
    TRANSPORTATION = "transportation"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    HEALTHCARE = "healthcare"
    OTHER = "other"


class IncomeSource(Enum):
    """Enumeration for income source types."""
    SALARY = "salary"
    SIDE_HUSTLE = "side_hustle"
    FREELANCE = "freelance"
    INVESTMENTS = "investments"
    OTHER_INCOME = "other_income"


class ExpenseType(Enum):
    """Enumeration for expense types (fixed vs variable)."""
    FIXED = "fixed"
    VARIABLE = "variable"


@dataclass
class FinancialData:
    """Data class to store comprehensive financial information."""
    monthly_income: Decimal
    expenses: Dict[ExpenseCategory, Decimal]
    savings_goal_percentage: Decimal = Decimal('20')  # Default 20%
    income_sources: Dict[IncomeSource, Decimal] = field(default_factory=dict)
    fixed_expenses: Dict[str, Decimal] = field(default_factory=dict)
    variable_expenses: Dict[str, Decimal] = field(default_factory=dict)
    person_name: Optional[str] = None


class PersonalFinanceCalculator:
    """
    A comprehensive personal finance calculator for budget analysis.
    
    This class provides methods to calculate monthly budgets, track expenses,
    and determine savings potential based on income and spending patterns.
    """
    
    def __init__(self) -> None:
        """Initialize the Personal Finance Calculator."""
        self.financial_data: Optional[FinancialData] = None
        logger.info("Personal Finance Calculator initialized")
    
    def validate_amount(self, amount: str) -> Decimal:
        """
        Validate and convert string input to Decimal for precise calculations.
        
        Args:
            amount: String representation of monetary amount
            
        Returns:
            Decimal: Validated monetary amount
            
        Raises:
            ValueError: If amount is invalid or negative
        """
        try:
            decimal_amount = Decimal(amount)
            if decimal_amount < 0:
                raise ValueError("Amount cannot be negative")
            return decimal_amount
        except InvalidOperation as e:
            raise ValueError(f"Invalid amount format: {amount}") from e
    
    def calculate_total_income(self, salary: Union[str, Decimal], side_hustle: Union[str, Decimal] = Decimal('0')) -> Decimal:
        """
        Calculate total monthly income from multiple sources.
        
        This function implements the starter code requirement for income calculation
        with salary and side hustle support.
        
        Args:
            salary: Primary salary income
            side_hustle: Additional income from side activities (default: 0)
            
        Returns:
            Decimal: Total monthly income
            
        Raises:
            ValueError: If income values are invalid
        """
        try:
            if isinstance(salary, str):
                salary = self.validate_amount(salary)
            if isinstance(side_hustle, str):
                side_hustle = self.validate_amount(side_hustle)
                
            total_income = salary + side_hustle
            logger.info(f"Calculated total income: ${total_income:.2f} (salary: ${salary:.2f}, side hustle: ${side_hustle:.2f})")
            return total_income
            
        except Exception as e:
            logger.error(f"Error calculating total income: {e}")
            raise ValueError(f"Invalid income values: {e}")
    
    def calculate_fixed_expenses(self, rent: Union[str, Decimal], insurance: Union[str, Decimal], 
                               phone: Union[str, Decimal], internet: Union[str, Decimal]) -> Decimal:
        """
        Add up monthly fixed costs.
        
        This function implements the starter code requirement for fixed expense calculation.
        
        Args:
            rent: Monthly rent or mortgage payment
            insurance: Monthly insurance premiums
            phone: Monthly phone bill
            internet: Monthly internet bill
            
        Returns:
            Decimal: Total fixed monthly expenses
            
        Raises:
            ValueError: If expense values are invalid
        """
        try:
            # Convert string inputs to Decimal if needed
            if isinstance(rent, str):
                rent = self.validate_amount(rent)
            if isinstance(insurance, str):
                insurance = self.validate_amount(insurance)
            if isinstance(phone, str):
                phone = self.validate_amount(phone)
            if isinstance(internet, str):
                internet = self.validate_amount(internet)
                
            total_fixed = rent + insurance + phone + internet
            
            # Store for detailed reporting
            if self.financial_data:
                self.financial_data.fixed_expenses = {
                    'rent': rent,
                    'insurance': insurance,
                    'phone': phone,
                    'internet': internet
                }
            
            logger.info(f"Calculated fixed expenses: ${total_fixed:.2f}")
            return total_fixed
            
        except Exception as e:
            logger.error(f"Error calculating fixed expenses: {e}")
            raise ValueError(f"Invalid expense values: {e}")
    
    def calculate_savings_potential(self, income: Union[str, Decimal], fixed_expenses: Union[str, Decimal], 
                                  variable_expenses: Union[str, Decimal]) -> Decimal:
        """
        Determine how much can be saved after all expenses.
        
        This function implements the starter code requirement for savings calculation.
        
        Args:
            income: Total monthly income
            fixed_expenses: Total fixed monthly expenses
            variable_expenses: Total variable monthly expenses
            
        Returns:
            Decimal: Amount available for savings (can be negative if overspending)
            
        Raises:
            ValueError: If input values are invalid
        """
        try:
            # Convert string inputs to Decimal if needed
            if isinstance(income, str):
                income = self.validate_amount(income)
            if isinstance(fixed_expenses, str):
                fixed_expenses = self.validate_amount(fixed_expenses)
            if isinstance(variable_expenses, str):
                variable_expenses = self.validate_amount(variable_expenses)
                
            savings_potential = income - fixed_expenses - variable_expenses
            
            logger.info(
                f"Calculated savings potential: ${savings_potential:.2f} "
                f"(income: ${income:.2f}, fixed: ${fixed_expenses:.2f}, variable: ${variable_expenses:.2f})"
            )
            return savings_potential
            
        except Exception as e:
            logger.error(f"Error calculating savings potential: {e}")
            raise ValueError(f"Invalid calculation values: {e}")
    
    def generate_budget_report(self, name: str, income: Decimal, expenses: Decimal, savings: Decimal) -> str:
        """
        Create a formatted budget summary report.
        
        This function implements the starter code requirement for budget reporting.
        
        Args:
            name: Person's name for the report
            income: Total monthly income
            expenses: Total monthly expenses
            savings: Available savings amount
            
        Returns:
            str: Formatted budget report
        """
        try:
            current_date = datetime.now().strftime("%B %Y")
            expense_ratio = (expenses / income * 100) if income > 0 else 0
            savings_ratio = (savings / income * 100) if income > 0 else 0
            
            # Determine financial health status
            if savings_ratio >= 20:
                status = "🟢 Excellent"
            elif savings_ratio >= 10:
                status = "🟡 Good"
            elif savings_ratio >= 0:
                status = "🟠 Fair"
            else:
                status = "🔴 Needs Attention"
            
            report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                            PERSONAL BUDGET REPORT                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Name: {name:<30} │ Report Date: {current_date:<22} ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ 💰 INCOME SUMMARY                                                           ║
║ ──────────────────────────────────────────────────────────────────────────── ║
║ Total Monthly Income:        ${income:>12,.2f}                             ║
║                                                                              ║
║ 💸 EXPENSE SUMMARY                                                          ║
║ ──────────────────────────────────────────────────────────────────────────── ║
║ Total Monthly Expenses:      ${expenses:>12,.2f}  ({expense_ratio:>5.1f}% of income)    ║
║                                                                              ║
║ 💵 SAVINGS ANALYSIS                                                         ║
║ ──────────────────────────────────────────────────────────────────────────── ║
║ Available for Savings:       ${savings:>12,.2f}  ({savings_ratio:>5.1f}% of income)    ║
║ Financial Health Status:     {status:<20}                        ║
║                                                                              ║
║ 📊 RECOMMENDATIONS                                                          ║
║ ──────────────────────────────────────────────────────────────────────────── ║"""
            
            # Add personalized recommendations
            if savings_ratio >= 20:
                report += """
║ • Excellent work! You're exceeding the 20% savings goal.                    ║
║ • Consider increasing investments or emergency fund.                         ║"""
            elif savings_ratio >= 10:
                report += """
║ • Good progress! Try to reach the 20% savings goal.                         ║
║ • Look for opportunities to reduce variable expenses.                        ║"""
            elif savings_ratio >= 0:
                report += """
║ • You're breaking even. Focus on reducing expenses.                         ║
║ • Consider additional income sources or expense cuts.                       ║"""
            else:
                report += """
║ • ⚠️  You're overspending! Immediate action needed.                         ║
║ • Review all expenses and cut non-essential items.                          ║
║ • Consider increasing income or find cheaper alternatives.                  ║"""
            
            report += """
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
            
            logger.info(f"Generated budget report for {name}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating budget report: {e}")
            return f"Error generating report: {e}"
    
    def get_user_income(self) -> Decimal:
        """
        Get monthly income from user input with validation.
        
        Returns:
            Decimal: Validated monthly income
        """
        while True:
            try:
                income_input = input("Enter your monthly income ($): $")
                return self.validate_amount(income_input)
            except ValueError as e:
                print(f"Error: {e}")
                print("Please enter a valid positive number.")
    
    def get_expense_by_category(self, category: ExpenseCategory) -> Decimal:
        """
        Get expense amount for a specific category from user input.
        
        Args:
            category: The expense category
            
        Returns:
            Decimal: Validated expense amount
        """
        while True:
            try:
                prompt = f"Enter monthly {category.value} expenses ($): $"
                expense_input = input(prompt)
                return self.validate_amount(expense_input)
            except ValueError as e:
                print(f"Error: {e}")
                print("Please enter a valid positive number.")
    
    def collect_financial_data(self) -> FinancialData:
        """
        Collect all financial data from user input.
        
        Returns:
            FinancialData: Complete financial information
        """
        print("\n=== Personal Finance Calculator ===")
        print("Let's analyze your monthly budget and savings potential!\n")
        
        # Get monthly income
        monthly_income = self.get_user_income()
        
        # Get expenses by category
        print("\nNow, let's collect your monthly expenses by category:")
        expenses = {}
        
        for category in ExpenseCategory:
            expense_amount = self.get_expense_by_category(category)
            expenses[category] = expense_amount
        
        # Get savings goal percentage (optional)
        while True:
            try:
                goal_input = input("\nWhat percentage of income would you like to save? (default 20%): ")
                if not goal_input.strip():
                    savings_goal = Decimal('20')
                    break
                savings_goal = self.validate_amount(goal_input)
                if savings_goal > 100:
                    print("Savings goal cannot exceed 100% of income.")
                    continue
                break
            except ValueError as e:
                print(f"Error: {e}")
                print("Please enter a valid percentage (0-100).")
        
        return FinancialData(
            monthly_income=monthly_income,
            expenses=expenses,
            savings_goal_percentage=savings_goal
        )
    
    def calculate_total_expenses(self, expenses: Dict[ExpenseCategory, Decimal]) -> Decimal:
        """
        Calculate total monthly expenses across all categories.
        
        Args:
            expenses: Dictionary of expenses by category
            
        Returns:
            Decimal: Total monthly expenses
        """
        return sum(expenses.values())
    
    def calculate_remaining_income(self, income: Decimal, total_expenses: Decimal) -> Decimal:
        """
        Calculate remaining income after expenses.
        
        Args:
            income: Monthly income
            total_expenses: Total monthly expenses
            
        Returns:
            Decimal: Remaining income (can be negative if overspending)
        """
        return income - total_expenses
    
    def calculate_target_savings(self, income: Decimal, savings_goal_percentage: Decimal) -> Decimal:
        """
        Calculate target savings amount based on income and goal percentage.
        
        Args:
            income: Monthly income
            savings_goal_percentage: Target savings percentage
            
        Returns:
            Decimal: Target monthly savings amount
        """
        return income * (savings_goal_percentage / Decimal('100'))
    
    def analyze_budget(self) -> Dict[str, Decimal]:
        """
        Perform comprehensive budget analysis.
        
        Returns:
            Dict: Budget analysis results
        """
        if not self.financial_data:
            raise ValueError("No financial data available. Please collect data first.")
        
        total_expenses = self.calculate_total_expenses(self.financial_data.expenses)
        remaining_income = self.calculate_remaining_income(
            self.financial_data.monthly_income, 
            total_expenses
        )
        target_savings = self.calculate_target_savings(
            self.financial_data.monthly_income,
            self.financial_data.savings_goal_percentage
        )
        
        # Calculate expense percentages
        expense_percentages = {}
        for category, amount in self.financial_data.expenses.items():
            percentage = (amount / self.financial_data.monthly_income) * Decimal('100')
            expense_percentages[category.value] = percentage
        
        return {
            'monthly_income': self.financial_data.monthly_income,
            'total_expenses': total_expenses,
            'remaining_income': remaining_income,
            'target_savings': target_savings,
            'savings_gap': remaining_income - target_savings,
            'expense_percentage': (total_expenses / self.financial_data.monthly_income) * Decimal('100'),
            'expense_breakdown': expense_percentages
        }
    
    def get_financial_recommendations(self, analysis: Dict[str, Decimal]) -> List[str]:
        """
        Generate personalized financial recommendations based on analysis.
        
        Args:
            analysis: Budget analysis results
            
        Returns:
            List: Financial recommendations
        """
        recommendations = []
        
        # Check if meeting savings goal
        if analysis['savings_gap'] >= 0:
            recommendations.append(
                f"✅ Great job! You can meet your savings goal with "
                f"${analysis['savings_gap']:.2f} extra to spare."
            )
        else:
            recommendations.append(
                f"⚠️  You're ${abs(analysis['savings_gap']):.2f} short of your savings goal. "
                f"Consider reducing expenses or increasing income."
            )
        
        # Check expense-to-income ratio
        expense_ratio = analysis['expense_percentage']
        if expense_ratio > 80:
            recommendations.append(
                f"🔴 High spending alert: You're spending {expense_ratio:.1f}% of your income. "
                f"Aim for 80% or less."
            )
        elif expense_ratio > 70:
            recommendations.append(
                f"🟡 Moderate spending: {expense_ratio:.1f}% of income. Room for improvement."
            )
        else:
            recommendations.append(
                f"🟢 Good spending habits: {expense_ratio:.1f}% of income."
            )
        
        # Category-specific recommendations
        for category, percentage in analysis['expense_breakdown'].items():
            if category == 'housing' and percentage > 30:
                recommendations.append(
                    f"🏠 Housing costs are {percentage:.1f}% of income. "
                    f"Consider reducing to 30% or less."
                )
            elif category == 'food' and percentage > 15:
                recommendations.append(
                    f"🍽️  Food expenses are {percentage:.1f}% of income. "
                    f"Consider meal planning to reduce costs."
                )
            elif category == 'transportation' and percentage > 15:
                recommendations.append(
                    f"🚗 Transportation costs are {percentage:.1f}% of income. "
                    f"Explore cost-saving alternatives."
                )
        
        return recommendations
    
    def display_results(self, analysis: Dict[str, Decimal]) -> None:
        """
        Display comprehensive budget analysis results.
        
        Args:
            analysis: Budget analysis results
        """
        print("\n" + "="*50)
        print("📊 BUDGET ANALYSIS RESULTS")
        print("="*50)
        
        print(f"\n💰 Monthly Income: ${analysis['monthly_income']:,.2f}")
        print(f"💸 Total Expenses: ${analysis['total_expenses']:,.2f}")
        print(f"💵 Remaining Income: ${analysis['remaining_income']:,.2f}")
        print(f"🎯 Savings Target: ${analysis['target_savings']:,.2f}")
        
        # Savings status
        if analysis['savings_gap'] >= 0:
            print(f"✅ Savings Status: ${analysis['savings_gap']:,.2f} above target")
        else:
            print(f"❌ Savings Status: ${abs(analysis['savings_gap']):,.2f} below target")
        
        # Expense breakdown
        print(f"\n📋 EXPENSE BREAKDOWN")
        print("-" * 30)
        for category, percentage in analysis['expense_breakdown'].items():
            amount = self.financial_data.expenses[ExpenseCategory(category)]
            print(f"{category.title():15}: ${amount:8.2f} ({percentage:5.1f}%)")
        
        # Recommendations
        recommendations = self.get_financial_recommendations(analysis)
        print(f"\n💡 RECOMMENDATIONS")
        print("-" * 30)
        for i, recommendation in enumerate(recommendations, 1):
            print(f"{i}. {recommendation}")
        
        print("\n" + "="*50)
    
    def run_calculator(self) -> None:
        """
        Main method to run the personal finance calculator.
        """
        try:
            # Collect financial data
            self.financial_data = self.collect_financial_data()
            
            # Perform analysis
            analysis = self.analyze_budget()
            
            # Display results
            self.display_results(analysis)
            
            # Log completion
            logger.info("Budget analysis completed successfully")
            
        except KeyboardInterrupt:
            print("\n\nCalculation cancelled by user.")
            logger.info("Calculator session cancelled by user")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            logger.error(f"Calculator error: {e}")


def main() -> None:
    """
    Main function to run the Personal Finance Calculator application.
    """
    calculator = PersonalFinanceCalculator()
    calculator.run_calculator()


if __name__ == "__main__":
    main()