# W1D1 Breakout Activity Instructions

## 🎯 Personal Finance Calculator - Quick Start Guide

### For Students

#### Option 1: Run the Demo (Recommended for beginners)
```bash
python demo.py
```
This will show you the calculator with sample data first, then ask if you want to try interactive mode.

#### Option 2: Run the Full Interactive Calculator
```bash
python personal_finance_calculator.py
```
Enter your own financial data and get personalized analysis.

#### Option 3: Run the Test Suite
```bash
python test_calculator.py
```
See how the code validation and testing works.

---

### For TAs and Instructors

#### Learning Objectives Checklist
- [ ] Students understand problem decomposition
- [ ] Students recognize Python best practices
- [ ] Students can trace through code logic
- [ ] Students appreciate error handling importance
- [ ] Students see real-world application

#### Key Discussion Points
1. **Problem Breakdown**: How do we turn "calculate budget" into specific functions?
2. **Data Types**: Why use Decimal instead of float for money?
3. **Error Handling**: What could go wrong with user input?
4. **Code Organization**: How does OOP help structure this problem?
5. **Testing**: How do we verify our calculations are correct?

#### Breakout Room Rotation Schedule
- **Minutes 0-5**: Group discussion on approach
- **Minutes 5-15**: Individual coding/exploration
- **Minutes 15-20**: Share discoveries and debug together

#### Extension Activities
- Modify expense categories
- Add new calculation features  
- Improve the user interface
- Add data persistence

---

### Common Student Questions & Answers

**Q: Why use Decimal instead of float?**
A: Financial calculations need precision. Float can have rounding errors like `0.1 + 0.2 = 0.30000000000000004`

**Q: What are type hints for?**
A: They help with code clarity and enable better IDE support and error checking.

**Q: Why so much error handling?**
A: Real applications must handle invalid input gracefully. Users will enter unexpected data!

**Q: What's the benefit of classes vs just functions?**
A: Classes group related data and behavior together, making code more organized and reusable.

---

### Troubleshooting

#### If students get import errors
Make sure they're running Python from the correct directory where the files are located.

#### If calculations seem wrong
Walk through the logic step by step using the demo data as an example.

#### If students are overwhelmed
Start with just running the demo, then explore one function at a time.

---

**Remember**: Focus on understanding over perfection. Every expert was once a beginner! 🌟
