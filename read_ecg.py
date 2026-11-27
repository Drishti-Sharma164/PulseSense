import streamlit as st
import wfdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks

st.markdown("""
<style>

/* Main page */
.stApp {
    background-color: #EAF2F8;
    color: #183153;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #167D8D;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #071B2B;
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown(
    """
    <h1 style="color:#183153; font-size:42px;">
        PulseSense
    </h1>
    """,
    unsafe_allow_html=True
)

st.subheader("ECG Monitoring Dashboard")
st.caption("Real ECG Recording | MIT-BIH Database")

# Load ECG recording
@st.cache_data
def load_ecg():
    record = wfdb.rdrecord("ecg_dataset/100")
    return record

record = load_ecg()

# Recording information
sampling_frequency = record.fs
number_of_signals = record.n_sig
total_duration = record.sig_len / record.fs

st.divider()

# Display metrics
col1, col2, col3 = st.columns(3)

col1.metric("Sampling Frequency", f"{sampling_frequency} Hz")
col2.metric("ECG Channels", number_of_signals)
col3.metric("Recording Duration", f"{total_duration / 60:.2f} min")

st.divider()

# Sidebar settings
st.sidebar.header("ECG Settings")

channel = st.sidebar.selectbox(
    "Select ECG Channel",
    options=range(record.n_sig),
    format_func=lambda i: record.sig_name[i]
)

duration = st.sidebar.slider(
    "Display Duration (seconds)",
    min_value=1,
    max_value=30,
    value=5
)

# Extract selected ECG signal
ecg_signal = record.p_signal[:, channel]

# Select required samples
samples = int(duration * sampling_frequency)
signal_section = ecg_signal[:samples]

# Create time axis
time = np.arange(samples) / sampling_frequency

#Designing filter(butterworth filter)
b, a = butter(
    4,
    [0.5, 40],
    btype='bandpass',
    fs=sampling_frequency
)
# Apply filter
filtered_full_signal = filtfilt(b, a, ecg_signal)
filtered_signal = filtered_full_signal[:samples]

#R PEAK detection 
peaks, properties = find_peaks(
    filtered_signal,
    distance=int(0.5 * sampling_frequency),
    prominence=0.5
)


# ---------------- CALCULATE RR INTERVALS ----------------

peak_times = peaks / sampling_frequency

rr_intervals = np.diff(peak_times)


# ---------------- CALCULATE HEART RATE ----------------

if len(rr_intervals) > 0:

    heart_rate = 60 / np.mean(rr_intervals)

else:

    heart_rate = 0


# ---------------- DISPLAY HEART RATE ----------------

st.subheader("Heart Rate Analysis")

col1, col2 = st.columns(2)

col1.metric(
    "Estimated Heart Rate",
    f"{heart_rate:.1f} BPM" if heart_rate > 0 else "Not available"
)

col2.metric(
    "Detected R-Peaks",
    len(peaks)
)


st.divider()

# Plot ECG
st.subheader(f"ECG Waveform - {record.sig_name[channel]}")

fig, ax = plt.subplots(2, 1, figsize=(14, 8))

# Original ECG
ax[0].plot(time, signal_section)
ax[0].set_title("Original ECG Signal")
ax[0].set_ylabel(f"Voltage ({record.units[channel]})")
ax[0].grid(True)

# Filtered ECG
ax[1].plot(time, filtered_signal)
ax[1].set_title("Filtered ECG Signal")
ax[1].set_xlabel("Time (seconds)")
ax[1].set_ylabel(f"Voltage ({record.units[channel]})")
ax[1].grid(True)

st.pyplot(fig)

st.divider()


