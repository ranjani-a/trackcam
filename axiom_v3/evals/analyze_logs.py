import glob
import os

import pandas as pd


def newest_log():

    logs = glob.glob("logs/*.csv")

    if len(logs) == 0:
        raise FileNotFoundError("No log files found.")

    return max(logs, key=os.path.getctime)


log = newest_log()

print(f"\nAnalyzing:\n{log}\n")

df = pd.read_csv(log)

frames = len(df)

avg_conf = df["confidence"].mean()

raw_jitter = (
    (df["center_x"].diff() ** 2 +
     df["center_y"].diff() ** 2) ** 0.5
).mean()

smooth_jitter = (
    (df["smooth_x"].diff() ** 2 +
     df["smooth_y"].diff() ** 2) ** 0.5
).mean()

print("========== AXIOM REPORT ==========")
print(f"Frames Logged        : {frames}")
print(f"Average Confidence  : {avg_conf:.3f}")
print(f"Raw Jitter          : {raw_jitter:.2f} px")
print(f"EMA Jitter          : {smooth_jitter:.2f} px")

if raw_jitter > 0:

    reduction = (1 - smooth_jitter / raw_jitter) * 100

    print(f"Jitter Reduction    : {reduction:.1f}%")

print("==================================")

