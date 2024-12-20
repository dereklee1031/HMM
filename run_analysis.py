import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM
import yfinance as yf
from scipy.stats import mode
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

DATA_PATH = os.path.join("..", "data", "sp500_data.csv")
RESULT_PATH = os.path.join("..", "results", "regimes_plot.png")
TICKER = "^GSPC"
START_DATE = "2014-01-01"
END_DATE = "2024-01-01"
N_STATES = 2
SMOOTH_WINDOW = 4

if not os.path.exists(DATA_PATH):
    df = yf.download(TICKER, start=START_DATE, end=END_DATE)
    df.reset_index(inplace=True)
    df.to_csv(DATA_PATH, index=False)

df = pd.read_csv(DATA_PATH, parse_dates=["Date"], index_col="Date")
numeric_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

weekly_df = df.resample('W').last()
weekly_df["Return"] = np.log(weekly_df["Adj Close"] / weekly_df["Adj Close"].shift(1))
weekly_df.dropna(inplace=True)

X = weekly_df["Return"].values.reshape(-1, 1)
model = GaussianHMM(n_components=N_STATES, covariance_type='full', n_iter=1000, random_state=42)
model.fit(X)
states = model.predict(X)

def rolling_mode(arr, window):
    rolled = pd.Series(arr).rolling(window=window, center=True, min_periods=1).apply(lambda x: mode(x, keepdims=True)[0][0])
    return rolled.fillna(method='bfill').fillna(method='ffill').astype(int).values

smoothed_states = rolling_mode(states, SMOOTH_WINDOW)
weekly_df["State"] = smoothed_states

logprob, posteriors = model.score_samples(X)

print("State Statistics:")
for i in range(N_STATES):
    mean = model.means_[i][0]
    var = model.covars_[i][0][0]
    print(f"State {i}: mean return = {mean:.6f}, variance = {var:.6f}")

state_colors = ["#1f77b4", "#ff7f0e"]
segments = []
current_state = smoothed_states[0]
start_idx = 0
for i in range(1, len(smoothed_states)):
    if smoothed_states[i] != current_state:
        segments.append((start_idx, i-1, current_state))
        current_state = smoothed_states[i]
        start_idx = i
segments.append((start_idx, len(smoothed_states)-1, current_state))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,8), sharex=True)

# Plot price line with label
price_line, = ax1.plot(weekly_df.index, weekly_df["Adj Close"], color="black", linewidth=1.5, label='Price')
ax1.set_title("S&P 500 Regime Switching (2 States) via HMM (Weekly Data & Smoothed)")
ax1.set_ylabel("Adjusted Close Price")

# Add shaded regions for states
for (start, end, st) in segments:
    ax1.axvspan(weekly_df.index[start], weekly_df.index[end], color=state_colors[st], alpha=0.2)

# Create patch handles for states
state_patches = [
    mpatches.Patch(color=state_colors[i], alpha=0.2, label=f"State {i}")
    for i in range(N_STATES)
]

# Combine line (price) and state patches in the legend
ax1.legend(handles=[price_line] + state_patches, loc="upper left")

# Plot state probabilities
for i in range(N_STATES):
    ax2.plot(weekly_df.index, posteriors[:, i], label=f"State {i} Probability", color=state_colors[i])
ax2.set_ylabel("State Probability")
ax2.set_xlabel("Date")
ax2.legend(loc="upper left")

plt.tight_layout()
plt.savefig(RESULT_PATH)
plt.close()
print(f"Plot saved to {RESULT_PATH}")




