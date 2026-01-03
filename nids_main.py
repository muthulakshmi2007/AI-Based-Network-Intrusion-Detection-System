import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Title
st.title("AI-Based Network Intrusion Detection System")

st.write("This system detects whether network traffic is Normal or an Intrusion using Machine Learning.")

# Generate simulated dataset
def load_data():
    data = {
        "packet_size": np.random.randint(100, 1500, 200),
        "protocol_type": np.random.randint(0, 3, 200),
        "src_bytes": np.random.randint(0, 10000, 200),
        "dst_bytes": np.random.randint(0, 10000, 200),
        "label": np.random.randint(0, 2, 200)  # 0 = Normal, 1 = Attack
    }
    return pd.DataFrame(data)

df = load_data()

X = df.drop("label", axis=1)
y = df["label"]

# Train model
if st.button("Train Model"):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    st.success("Model trained successfully!")

    # Store model
    st.session_state["model"] = model

# Live Traffic Simulation
st.subheader("Live Traffic Simulation")

packet_size = st.number_input("Packet Size", 100, 1500)
protocol_type = st.number_input("Protocol Type (0-TCP,1-UDP,2-ICMP)", 0, 2)
src_bytes = st.number_input("Source Bytes", 0, 10000)
dst_bytes = st.number_input("Destination Bytes", 0, 10000)

if st.button("Detect Intrusion"):
    if "model" in st.session_state:
        model = st.session_state["model"]
        input_data = np.array([[packet_size, protocol_type, src_bytes, dst_bytes]])
        prediction = model.predict(input_data)

        if prediction[0] == 0:
            st.success("✅ Normal Traffic")
        else:
            st.error("🚨 Intrusion Detected")
    else:
        st.warning("Please train the model first.")
