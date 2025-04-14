

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots




st.set_page_config(page_title="dashboard")





if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login to access the dashboard ")
    st.stop()



st.sidebar.markdown("---")
st.sidebar.write(f" Logged in as: `{st.session_state.username}`")

if st.sidebar.button(" Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = "user"
    st.success("You have been logged out.")
    st.experimental_rerun()





uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, header=None)
    df.columns = ["Time", "Breath Trend", "SpO2 Info 1", "SpO2 Info 2", "Body Position", "Pulse Info", "Dummy1", "Dummy2", "Dummy3", "Dummy4"]

    
    fig = make_subplots(
        rows=5, cols=1,
        shared_xaxes=True,
        subplot_titles=("Breath Trend", "SpO2 Info 1", "SpO2 Info 2", "Body Position", "Pulse Info")
    )

    fig.add_trace(go.Scatter(x=df['Time'], y=df['Breath Trend']), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Time'], y=df['SpO2 Info 1']), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['Time'], y=df['SpO2 Info 2']), row=3, col=1)
    fig.add_trace(go.Scatter(x=df['Time'], y=df['Body Position']), row=4, col=1)
    fig.add_trace(go.Scatter(x=df['Time'], y=df['Pulse Info']), row=5, col=1)

    fig.update_layout(height=1200, width=800, title_text="Health Report: Combined Graph", showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

    
    img_bytes = fig.to_image(format="png", engine="kaleido")
    st.download_button(" Download Graph Report", data=img_bytes, file_name="health_report.png", mime="image/png")
