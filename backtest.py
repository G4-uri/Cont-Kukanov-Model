import pandas as pd
import numpy as np
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
import matplotlib.pyplot as plt
import time

# Setup logging
logging.basicConfig(filename='backtest.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to load snapshots efficiently in chunks
def load_snapshots_chunked(csv_path, chunk_size=10000):
    chunks = pd.read_csv(csv_path, chunksize=chunk_size)
    snapshot_list = []
    
    for df in chunks:
        df['ts_event'] = pd.to_datetime(df['ts_event']).astype(np.int64)
        df.sort_values(['ts_event', 'publisher_id'], inplace=True)
        df = df.drop_duplicates(subset=['ts_event', 'publisher_id'], keep='first')
        snapshots = df.groupby('ts_event')
        snapshot_list.extend(list(snapshots))
    
    return snapshot_list

# Helper function to log execution details
def log_execution_details(lambda_over, lambda_under, theta_queue, cost, total_cost):
    logging.info(f"Backtest with λ_over={lambda_over}, λ_under={lambda_under}, θ_queue={theta_queue}")
    logging.info(f"Total cost: {cost:.2f}, Cumulative cost so far: {total_cost:.2f}")

# Backtest function for a single combination of parameters
def run_backtest(snapshots, lambda_over, lambda_under, theta_queue):
    total_cost = 0
    total_filled = 0
    venue_performance = defaultdict(lambda: {'total_filled': 0, 'total_cost': 0})
    
    # Simulate the execution process
    for ts, snap in snapshots:
        # Assuming `snap` contains the order book data
        for index, row in snap.iterrows():
            # Example of cost calculation (customize as needed)
            cost = row['price'] * row['quantity'] * lambda_over + lambda_under
            filled = row['quantity'] * theta_queue
            total_cost += cost
            total_filled += filled
            venue_performance[row['publisher_id']]['total_filled'] += filled
            venue_performance[row['publisher_id']]['total_cost'] += cost

            # Log execution details periodically (e.g., every 100 iterations)
            if total_filled % 100 == 0:
                log_execution_details(lambda_over, lambda_under, theta_queue, total_cost, total_filled)

    # Calculate the final performance metrics
    avg_price = total_cost / total_filled if total_filled > 0 else 0
    return total_cost, avg_price, total_filled, venue_performance

# Parallel execution of backtests for grid search
def run_backtest_parallel(grid, snapshots):
    best_result = {'cost': float('inf')}
    
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(run_backtest, snapshots, lo, lu, tq): (lo, lu, tq) for lo, lu, tq in grid}
        
        for future in as_completed(futures):
            lo, lu, tq = futures[future]
            try:
                cost, avg, total_filled, venue_performance = future.result()
                if cost < best_result['cost']:
                    best_result = {
                        'params': {'lambda_over': lo, 'lambda_under': lu, 'theta_queue': tq},
                        'cost': cost,
                        'avg_price': avg,
                        'total_filled': total_filled,
                        'venue_performance': venue_performance
                    }
            except Exception as exc:
                logging.error(f"Error during backtest for params ({lo}, {lu}, {tq}): {exc}")
    
    return best_result

# Sensitivity analysis plot function
def plot_cost_sensitivity(lambda_over_values, lambda_under_values, results):
    fig, ax = plt.subplots(figsize=(10, 6))
    cost_matrix = np.array([[result['cost'] for result in row] for row in results])
    c = ax.pcolormesh(lambda_over_values, lambda_under_values, cost_matrix, shading='auto')
    fig.colorbar(c, ax=ax)
    ax.set_title('Cost Sensitivity')
    ax.set_xlabel('lambda_over')
    ax.set_ylabel('lambda_under')
    plt.tight_layout()
    plt.show()

# Example usage
# Example usage
if __name__ == '__main__':
    # Load snapshots
    snapshots = load_snapshots_chunked('l1_day.csv')
    
    # Define parameter grid for the backtest
    lambda_over_values = [0.1, 0.2, 0.3]
    lambda_under_values = [0.1, 0.2, 0.3]
    theta_queue_values = [0.5, 0.6, 0.7]
    
    # Generate the grid of all parameter combinations
    grid = [(lo, lu, tq) for lo in lambda_over_values for lu in lambda_under_values for tq in theta_queue_values]
    
    # Run the backtest in parallel
    start_time = time.time()
    best_result = run_backtest_parallel(grid, snapshots)
    end_time = time.time()
    
    # Log and print the best result
    logging.info(f"Best result: {best_result}")
    print(f"Best result: {best_result}")
    
    # Corrected: Run backtests over the grid and collect results
    results = [run_backtest(snapshots, lo, lu, tq) for lo, lu, tq in grid]
    
    # Plot cost sensitivity (if required)
    plot_cost_sensitivity(lambda_over_values, lambda_under_values, results)
    
    # Log the total runtime
    logging.info(f"Backtest completed in {end_time - start_time:.2f} seconds")
    print(f"Backtest completed in {end_time - start_time:.2f} seconds")


