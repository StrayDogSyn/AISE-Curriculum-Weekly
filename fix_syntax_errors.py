"""Fix syntax errors in w8_d2_team_microsoft.py"""

with open('week8 ML challenges/w8_d2_team_microsoft.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix line 278: self.X -> cls.X
lines[277] = "        cls.X = np.random.randn(200, 4)\n"

# Fix line 279: self.X -> cls.X  
lines[278] = "        cls.y = (cls.X[:, 0] + cls.X[:, 1] * 0.5 > 0).astype(int)\n"

# Fix line 280: Remove escaped quotes and extra parentheses
lines[279] = "        cls.config = ModelConfig(verbose=0, cv_folds=3, param_grid={'C': [1], 'solver': ['liblinear'], 'class_weight': [None]})\n"

# Write fixed content
with open('week8 ML challenges/w8_d2_team_microsoft.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Fixed all syntax errors:")
print("  • Line 278: self.X → cls.X")
print("  • Line 279: self.X → cls.X")  
print("  • Line 280: Fixed escaped quotes and removed extra parentheses")
