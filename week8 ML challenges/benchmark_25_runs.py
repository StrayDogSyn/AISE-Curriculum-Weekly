"""Run test_code.py 25 times and calculate average performance."""

import time
import sys
from test_code import process_customer_data

def run_benchmark(num_runs=25):
    """Run the customer processing test multiple times and calculate averages."""
    
    print(f"Running {num_runs} benchmark iterations...")
    print("=" * 70)
    
    times_100 = []
    times_1000 = []
    
    # 100 customers benchmark
    customers_100 = [{'id': i, 'name': f'Customer{i}'} for i in range(100)]
    
    for i in range(num_runs):
        start = time.time()
        result = process_customer_data(customers_100)
        elapsed = time.time() - start
        times_100.append(elapsed)
        print(f"Run {i+1:2d}/25 (100 customers):  {elapsed:.4f}s", end='\r')
    
    print(f"\n{'='*70}")
    
    # 1000 customers benchmark
    customers_1000 = [{'id': i, 'name': f'Customer{i}'} for i in range(1000)]
    
    for i in range(num_runs):
        start = time.time()
        result = process_customer_data(customers_1000)
        elapsed = time.time() - start
        times_1000.append(elapsed)
        print(f"Run {i+1:2d}/25 (1000 customers): {elapsed:.4f}s", end='\r')
    
    print(f"\n{'='*70}\n")
    
    # Calculate statistics
    avg_100 = sum(times_100) / len(times_100)
    min_100 = min(times_100)
    max_100 = max(times_100)
    
    avg_1000 = sum(times_1000) / len(times_1000)
    min_1000 = min(times_1000)
    max_1000 = max(times_1000)
    
    # Display results
    print("📊 BENCHMARK RESULTS (25 runs)")
    print("=" * 70)
    print(f"\n{'Test Case':<25} {'Average':<12} {'Min':<12} {'Max':<12}")
    print("-" * 70)
    print(f"{'100 Customers':<25} {avg_100:.4f}s{'':<4} {min_100:.4f}s{'':<4} {max_100:.4f}s")
    print(f"{'1000 Customers':<25} {avg_1000:.4f}s{'':<4} {min_1000:.4f}s{'':<4} {max_1000:.4f}s")
    print("-" * 70)
    
    # Performance metrics
    starter_time = 1.05
    speedup_100 = starter_time / avg_100
    speedup_1000 = (starter_time * 10) / avg_1000
    
    print(f"\n⚡ Average Speedup (100 customers):  {speedup_100:.1f}x faster")
    print(f"⚡ Average Speedup (1000 customers): {speedup_1000:.1f}x faster")
    print(f"\n📈 Consistency (100 customers):  {min_100:.4f}s - {max_100:.4f}s")
    print(f"📈 Consistency (1000 customers): {min_1000:.4f}s - {max_1000:.4f}s")
    
    # Check if consistently under target
    target = 0.019
    under_target_100 = sum(1 for t in times_100 if t < target)
    under_target_1000 = sum(1 for t in times_1000 if t < target)
    
    print(f"\n🎯 Runs under {target}s target:")
    print(f"   100 customers:  {under_target_100}/25 ({under_target_100/25*100:.0f}%)")
    print(f"   1000 customers: {under_target_1000}/25 ({under_target_1000/25*100:.0f}%)")
    print("=" * 70)
    
    if avg_100 < target:
        print(f"✅ SUCCESS! Average time ({avg_100:.4f}s) is below {target}s target!")
    else:
        print(f"⚠️  Average time ({avg_100:.4f}s) exceeds {target}s target")

if __name__ == '__main__':
    run_benchmark(25)
