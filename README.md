# 📊 Smart Order Routing Backtest Engine

This project simulates a cost-aware **smart order routing** (SOR) strategy over historical limit order book snapshots, performing grid search over key hyperparameters and providing both logging and visualization for analysis.

---

## 🧠 Features

* ✅ Efficient loading of large L1 order book snapshots in chunks
* ✅ Parameterized backtest engine simulating cost-based routing
* ✅ Parallel grid search with `ProcessPoolExecutor`
* ✅ Real-time logging and monitoring
* ✅ Best configuration selection based on total cost
* ✅ Cost sensitivity heatmap visualization

---

## 🛠️ Installation

1. **Clone the repository** (or place your code in a working directory):

   ```bash
   git clone https://github.com/yourname/sor-backtest.git
   cd sor-backtest
   ```

2. **Install Python dependencies**:

   ```bash
   pip install pandas numpy matplotlib
   ```

---

## 📁 File Structure

```
sor-backtest/
│
├── backtest.py              # Main backtest script
├── l1_day.csv               # Example input CSV with L1 order book snapshots (from 2024)
├── backtest.log             # Log file created during backtesting
└── README.md                # You're reading it now
```

---

## 📄 Input Format (`l1_day.csv` from 2024)

| ts\_event        | publisher\_id | price  | quantity |
| ---------------- | ------------- | ------ | -------- |
| 2024-01-01 10:00 | VENUE\_1      | 100.50 | 200      |
| 2024-01-01 10:00 | VENUE\_2      | 101.00 | 150      |

* `ts_event`: Timestamp of the order book event
* `publisher_id`: Venue or exchange ID
* `price`: Ask or bid price
* `quantity`: Available quantity at that price

---

## ⚙️ Parameters

* **λ\_over (`lambda_over`)**: Penalty for over-filling
* **λ\_under (`lambda_under`)**: Penalty for under-filling
* **θ\_queue (`theta_queue`)**: Queue position or fill factor (0–1)

These are scanned using a grid search:

```python
lambda_over_values = [0.1, 0.2, 0.3]
lambda_under_values = [0.1, 0.2, 0.3]
theta_queue_values = [0.5, 0.6, 0.7]
```

---

## 🚀 Running the Backtest

Simply run:

```bash
python backtest.py
```

Output:

* The **best parameter configuration** will be printed and logged
* A **cost sensitivity heatmap** will be plotted
* Runtime and intermediate details are logged to `backtest.log`

---

## 📈 Output Example

```text
Best result: {
    'params': {'lambda_over': 0.2, 'lambda_under': 0.1, 'theta_queue': 0.6},
    'cost': 10345.2,
    'avg_price': 100.2,
    'total_filled': 4000,
    'venue_performance': { ... }
}
Backtest completed in 12.45 seconds
```

---

## 📊 Visualization

The `plot_cost_sensitivity` function generates a 2D heatmap of total cost vs. λ\_over and λ\_under to help analyze sensitivity and optimal regions.

---

## 💡 Realism Improvement Suggestion

One idea to improve **fill realism** is to include:

* **Queue Position Modeling**: Use order book depth and estimate probability of execution based on queue priority. A lower `theta_queue` for deeper levels or longer queues.
* **Slippage Penalty**: Add extra cost for executing beyond top-of-book or in volatile time windows.

This would more closely approximate real execution dynamics in live markets.

---

## 🧑‍💼 Author

* **Gauri Nair** 

---

## 📜 License

MIT License – feel free to use, modify, and distribute with attribution.

