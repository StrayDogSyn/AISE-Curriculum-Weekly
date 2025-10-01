from typing import List

def kidsWithCandies(candies: List[int], extraCandies: int) -> List[bool]:
    # No 'self' - it's just a regular function
    max_candies = max(candies)
    return [candy + extraCandies >= max_candies for candy in candies]

# Now you can call it directly
print(kidsWithCandies([2,3,5,1,3], 3))  # Works!

# LeetCode expects a class with the method
class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        max_candies = max(candies)
        return [candy + extraCandies >= max_candies for candy in candies]