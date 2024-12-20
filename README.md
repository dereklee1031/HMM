HMM Regime Detection for S&P 500
Overview
This project uses a Hidden Markov Model (HMM) to identify different "regimes" in the S&P 500 over time. Each regime represents a market environment characterized by distinct statistical properties of returns. For example, one regime might be stable and growing (often considered "bullish"), while another might be volatile or declining ("bearish").

Key Steps:

Download historical S&P 500 data from Yahoo Finance.
Resample daily data to weekly frequency to reduce noise.
Compute weekly log returns.
Fit a Gaussian HMM to uncover hidden states (regimes).
Visualize the results: a price chart with shaded regions for regimes and a separate plot showing state probabilities over time.
Project Structure
bash
Copy code
HMM/
├─ data/
│  └─ sp500_data.csv        # Automatically downloaded data
├─ scripts/
│  ├─ run_analysis.py       # Main script: fetch data, model, and plot
│  └─ requirements.txt      # Dependencies (yfinance, pandas, numpy, matplotlib, hmmlearn, scipy)
└─ results/
   └─ regimes_plot.png      # Final visualization of identified regimes
Setup Instructions
Install Dependencies: From the scripts directory:

Copy code
pip install -r requirements.txt
Run the Analysis:

Copy code
python3 run_analysis.py
If sp500_data.csv does not exist, it will be downloaded. Then the script preprocesses the data, fits the HMM, and saves the resulting plot to results/regimes_plot.png.

Interpreting the Results
Open results/regimes_plot.png to see the output.

Top Plot:
Black line: S&P 500 adjusted close price.
Shaded regions: Indicate which state (regime) the HMM believes the market is in. Each color represents a different regime.
Bottom Plot:
State probability lines: Show the model’s confidence in each regime over time. A probability near 1 means the model is certain the market is in that state.
Use these results to understand how the market transitions between different states. Do the regimes align with known bull/bear phases or major economic events?

Adjustments and Experimentation
Change N_STATES in run_analysis.py to see if fewer or more states produce clearer regimes.
Experiment with monthly data instead of weekly for different levels of smoothing.
Add additional features (e.g., volatility measures) to help the HMM distinguish regimes more clearly.
Apply smoothing techniques or filters to the states if they switch too frequently.
Future Directions
Incorporate multiple features (e.g., returns and volatility) for richer regime definitions.
Explore different HMM variants (e.g., Gaussian Mixture emissions).
Use identified regimes to develop trading or risk management strategies and test their performance.
License
This project is for educational and illustrative purposes. Consult the repository owner for licensing details, if any.
