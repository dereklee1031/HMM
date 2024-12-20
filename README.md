

```markdown
# HMM Regime Detection for S&P 500

## Overview
This project uses a Hidden Markov Model (HMM) to identify different "regimes" in the S&P 500 over time. A regime can be thought of as a persistent market environment—such as stable growth periods (bullish) and turbulent, declining periods (bearish).

**Key steps in this project:**
1. **Data Acquisition:**  
   Download historical S&P 500 data from Yahoo Finance.
2. **Preprocessing:**  
   Convert daily data to weekly frequency and compute weekly log returns.
3. **HMM Fitting:**  
   Fit a Gaussian HMM to the returns time series to uncover hidden states (regimes).
4. **Visualization:**  
   Plot the S&P 500 price with shaded regions indicating the identified regimes, and a separate subplot showing the probability of each state over time.

## Project Structure
```
HMM/
├─ data/
│  └─ sp500_data.csv          # Automatically downloaded historical S&P 500 data
├─ scripts/
│  ├─ run_analysis.py         # Main script to run data fetching, modeling, and plotting
│  └─ requirements.txt        # Dependencies (yfinance, pandas, numpy, matplotlib, hmmlearn, scipy)
└─ results/
   └─ regimes_plot.png        # The final visualization of regimes
```

## Setup Instructions
1. **Clone the Repository and Navigate:**
   ```bash
   cd HMM/scripts
   ```

2. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Analysis:**
   ```bash
   python3 run_analysis.py
   ```
   - If data does not exist, it will be downloaded automatically.
   - The script will then preprocess the data, fit the HMM, produce the regime plot, and save it in the `results` folder.

## Interpreting the Results
After running the script, open `HMM/results/regimes_plot.png`. You’ll see:

- **Price Line (Top Subplot):**  
  The black line represents the historical S&P 500 prices over the chosen period.
- **Colored Shading (Top Subplot):**  
  Background colors indicate which HMM state is active. Each state corresponds to a particular statistical regime. For example:
  - **State 0:** Could represent a stable or growth-oriented period.
  - **State 1:** Could represent a more volatile or declining period.
  
  (The actual interpretation depends on the extracted state statistics.)

- **State Probabilities (Bottom Subplot):**  
  The lower panel shows the model’s probability estimates for each state over time. This helps you understand the model’s confidence and see how quickly or slowly the market transitions between regimes.

## Adjustments and Experimentation
If you find the regimes switch too often or don’t make intuitive sense, you can try:

- **Changing the number of states (N_STATES)** in `run_analysis.py`.
- **Adjusting the data frequency** (e.g., monthly instead of weekly).
- **Adding more features** (like volatility measures or volume changes).
- **Increasing smoothing or applying a different smoothing strategy** to reduce noise.

## Future Directions
- Incorporate multiple features into the HMM (returns + volatility).
- Compare different models (e.g., a 3-state HMM vs. a 2-state HMM).
- Test trading or risk management strategies based on identified regimes.

