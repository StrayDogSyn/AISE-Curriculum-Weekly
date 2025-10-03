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
    
# intersection of two arrays
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        return list(set(nums1) & set(nums2))
        
# Iterator methods
class Solution:
    def __init__(self, nums: List[int]):
        self.nums = nums
        self.index = 0

    def hasNext(self) -> bool:
        return self.index < len(self.nums)

    def next(self) -> int:
        if not self.hasNext():
            raise StopIteration("No more elements")
        value = self.nums[self.index]
        self.index += 1
        return value

# iterator example
    
arr = [1,2,3, 12, "hello", 3.14]
arr_iterator = iter(arr)
try:
    while True:
        print(next(arr_iterator))
except StopIteration:
    print("No more elements in the iterator")

