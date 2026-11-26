
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# 1. Create a 5-second timeline
duration = 5
time = np.linspace(0, duration, 2500)

# 2. Create an empty ECG signal
ecg_signal = np.zeros_like(time)

# 3. Set simulated heart rate
heart_rate = 75
rr_interval = 60 / heart_rate

# 4. Generate repeated PQRST waves
for start in np.arange(0, duration, rr_interval):

    # P wave
    p_wave = 0.25 * np.exp(
        -((time - (start + 0.2)) ** 2) / (2 * 0.03 ** 2)
    )

    # Q wave
    q_wave = -0.15 * np.exp(
        -((time - (start + 0.38)) ** 2) / (2 * 0.01 ** 2)
    )

    # R wave
    r_wave = 1.0 * np.exp(
        -((time - (start + 0.40)) ** 2) / (2 * 0.012 ** 2)
    )

    # S wave
    s_wave = -0.25 * np.exp(
        -((time - (start + 0.43)) ** 2) / (2 * 0.01 ** 2)
    )

    # T wave
    t_wave = 0.35 * np.exp(
        -((time - (start + 0.65)) ** 2) / (2 * 0.06 ** 2)
    )

    # Combine all waves
    ecg_signal += p_wave + q_wave + r_wave + s_wave + t_wave


# 5. Detect R peaks
r_peaks, properties = find_peaks(
    ecg_signal,
    height=0.5,
    distance=100
)

# 6. Convert peak indices into time values
r_peak_times = time[r_peaks]

# 7. Calculate R-R intervals
rr_intervals = np.diff(r_peak_times)

# 8. Calculate heart rate
bpm = 60 / rr_intervals
average_bpm = np.mean(bpm)

# 9. Print results
print("R Peak Times:", r_peak_times)
print("R-R Intervals:", rr_intervals)
print("Heart Rate:", average_bpm, "BPM")


# 10. Plot ECG waveform
plt.figure(figsize=(12, 5))

plt.plot(time, ecg_signal, label="Simulated ECG")

# Mark detected R peaks
plt.plot(
    r_peak_times,
    ecg_signal[r_peaks],
    "ro",
    label="Detected R Peaks"
)

plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.title("PulseSense - ECG and Heart Rate Detection")
plt.legend()
plt.grid()

plt.show()
