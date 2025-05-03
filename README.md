# Cont-Kukanov-Model

📊 Smart Order Routing Backtest Engine

This project simulates a cost-aware smart order routing (SOR) strategy over historical limit order book snapshots, performing grid search over key hyperparameters and providing both logging and visualization for analysis.

🧠 Features

✅ Efficient loading of large L1 order book snapshots in chunks
✅ Parameterized backtest engine simulating cost-based routing
✅ Parallel grid search with ProcessPoolExecutor
✅ Real-time logging and monitoring
✅ Best configuration selection based on total cost
✅ Cost sensitivity heatmap visualization
🛠️ Installation

Clone the repository (or place your code in a working directory):
git clone https://github.com/yourname/sor-backtest.git
cd sor-backtest
Install Python dependencies:
pip install pandas numpy matplotlib
📁 File Structure

sor-backtest/
│
├── backtest.py              # Main backtest script
├── l1_day.csv               # Example input CSV with L1 order book snapshots
├── backtest.log             # Log file created during backtesting
└── README.md                # You're reading it now
📄 Input Format (l1_day.csv)

ts_event	publisher_id	price	quantity
2023-01-01 10:00	VENUE_1	100.50	200
2023-01-01 10:00	VENUE_2	101.00	150
ts_event: Timestamp of the order book event
publisher_id: Venue or exchange ID
price: Ask or bid price
quantity: Available quantity at that price
⚙️ Parameters

λ_over (lambda_over): Penalty for over-filling
λ_under (lambda_under): Penalty for under-filling
θ_queue (theta_queue): Queue position or fill factor (0–1)
These are scanned using a grid search.

🚀 Running the Backtest

Simply run:

python backtest.py
Output:

The best parameter configuration will be printed and logged
A cost sensitivity heatmap will be plotted
Runtime and intermediate details are logged to backtest.log
📈 Output Example

Best result: {
    'params': {'lambda_over': 0.2, 'lambda_under': 0.1, 'theta_queue': 0.6},
    'cost': 10345.2,
    'avg_price': 100.2,
    'total_filled': 4000,
    'venue_performance': { ... }
}
Backtest completed in 12.45 seconds
📊 Visualization

The plot_cost_sensitivity function generates a 2D heatmap of total cost vs. λ_over and λ_under to help analyze sensitivity and optimal regions.

🧪 Future Improvements

Add support for TWAP, VWAP, and Best Ask benchmarks
Integrate with Optuna or Ray Tune for smarter hyperparameter search
Extend to L2 order books or real-time feeds
🧑‍💻 Author

Your Name – LinkedIn | GitHub
📜 License

MIT License – feel free to use, modify, and distribute with attribution.
