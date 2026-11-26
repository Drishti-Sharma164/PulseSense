
import streamlit as st
import wfdb
import numpy as np
import matplotlib.pyplot as plt

st.markdown("""
<style>

/* Main page */
.stApp {
    background-color: #EAF2F8;
    color: #183153;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #183153;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: rgb(13, 170, 136);
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown(
    """
    <h1 style="color:#183153; font-size:42px;">
        <span style="font-family:'Segoe UI"></span>
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

# Plot ECG
st.subheader(f"ECG Waveform - {record.sig_name[channel]}")

fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(time, signal_section)

ax.set_xlabel("Time (seconds)")
ax.set_ylabel(f"Voltage ({record.units[channel]})")
ax.set_title("Real ECG Signal")
ax.grid(True)

st.pyplot(fig)

st.divider()

# Footer
st.markdown(
    "### About PulseSense\n"
    "PulseSense is an educational ECG visualisation project "
    "built using Python, Streamlit and the WFDB library. "
    "It uses recorded ECG data from the MIT-BIH database."
)

st.caption(
    "Educational demonstration only — not intended for medical diagnosis."
)
