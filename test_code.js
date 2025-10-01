/**
 * @param {number} numBottles
 * @param {number} numExchange
 * @return {number}
 */
var numWaterBottles = function(numBottles, numExchange) {
    let totalDrunk = numBottles;
    let emptyBottles = numBottles;
    
    while (emptyBottles >= numExchange) {
        const newBottles = Math.floor(emptyBottles / numExchange);
        totalDrunk += newBottles;
        emptyBottles = emptyBottles % numExchange + newBottles;
    }
    
    return totalDrunk;
};

// Test cases
console.log(numWaterBottles(9, 3));   // Expected: 13
console.log(numWaterBottles(15, 4));  // Expected: 19
console.log(numWaterBottles(5, 5));   // Expected: 6
console.log(numWaterBottles(2, 3));   // Expected: 2 (can't exchange)
