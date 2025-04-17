

# import streamlit as st
# import pandas as pd
# import plotly.graph_objs as go
# from plotly.subplots import make_subplots




# st.set_page_config(page_title="dashboard")





# if "logged_in" not in st.session_state or not st.session_state.logged_in:
#     st.error("Please login to access the dashboard ")
#     st.stop()



# st.sidebar.markdown("---")
# st.sidebar.write(f" Logged in as: `{st.session_state.username}`")

# if st.sidebar.button(" Logout"):
#     st.session_state.logged_in = False
#     st.session_state.username = ""
#     st.session_state.role = "user"
#     st.success("You have been logged out.")
#     st.experimental_rerun()




# data_source = st.radio("Choose Data Source:", ["SD Card", "Upload CSV"])

# df = None

# if data_source == "SD Card":
#     sd_card_path = "E:/data.csv"  # change path as per actual SD card file

#     if os.path.exists(sd_card_path):
#         df = pd.read_csv(sd_card_path, header=None)
#         st.success("✅ Data loaded from SD card!")
#     else:
#         st.error("❌ SD card or file not found!")

# elif data_source == "Upload CSV":






# uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file, header=None)
#     df.columns = ["Time", "Breath Trend", "SpO2 Info 1", "SpO2 Info 2", "Body Position", "Pulse Info", "Dummy1", "Dummy2", "Dummy3", "Dummy4"]

    
#     fig = make_subplots(
#         rows=5, cols=1,
#         shared_xaxes=True,
#         subplot_titles=("Breath Trend", "SpO2 Info 1", "SpO2 Info 2", "Body Position", "Pulse Info")
#     )

#     fig.add_trace(go.Scatter(x=df['Time'], y=df['Breath Trend']), row=1, col=1)
#     fig.add_trace(go.Scatter(x=df['Time'], y=df['SpO2 Info 1']), row=2, col=1)
#     fig.add_trace(go.Scatter(x=df['Time'], y=df['SpO2 Info 2']), row=3, col=1)
#     fig.add_trace(go.Scatter(x=df['Time'], y=df['Body Position']), row=4, col=1)
#     fig.add_trace(go.Scatter(x=df['Time'], y=df['Pulse Info']), row=5, col=1)

#     fig.update_layout(height=1200, width=800, title_text="Health Report: Combined Graph", showlegend=False)

#     st.plotly_chart(fig, use_container_width=True)





#     img_bytes = fig.to_image(format="png", engine="kaleido")
#     st.download_button(" Download Graph Report", data=img_bytes, file_name="health_report.png", mime="image/png")























import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import requests
import psutil
from io import StringIO

# ---------- Helper Function ----------
def find_sd_card_drive():
    partitions = psutil.disk_partitions()
    for p in partitions:
        if 'removable' in p.opts:
            return p.device
    return None


# ---------- Page Setup ----------
st.set_page_config(page_title="Dashboard")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login to access the dashboard.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.write(f"Logged in as: `{st.session_state.username}`")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = "user"
    st.success("You have been logged out.")
    st.experimental_rerun()

# ---------- Step 1: Import Button ----------
st.subheader("Import Health Report Data")

if "import_clicked" not in st.session_state:
    st.session_state.import_clicked = False

if not st.session_state.import_clicked:
    if st.button("Import"):
        st.session_state.import_clicked = True
    st.stop()

# ---------- Step 2: Choose Source ----------
data_source = st.radio("Choose Data Source:", ["Fetch data from server", "Fetch data from SD Card"])
df = None



# ---------- Upload CSV ----------
if data_source == "Fetch data from server":
    
    st.title("Fetch CSV from Remote API")

    api_url = "http://f595kzbv4gnter-md8lqmsh.streamlit.app"

    if st.button("Fetch CSV"):
        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                csv_content = StringIO(response.text)
                df = pd.read_csv(csv_content)

                st.success("CSV fetched successfully!")
                st.dataframe(df)

            else:
                st.error(f"Failed to fetch CSV. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")


# ---------- SD Card Upload ----------
elif data_source == "Fetch data from SD Card":
    sd_drive = find_sd_card_drive()
    
    if sd_drive:
        st.success(f" SD card detected: {sd_drive}")
        sd_file = st.file_uploader(" Browse CSV file from SD Card", type=["csv"], key="sd_card_upload")
        if sd_file is not None:
            df = pd.read_csv(sd_file, header=None)
            st.success(" SD card CSV uploaded successfully!")
    else:
        st.warning(" No SD card detected. Please insert an SD card.")

# ---------- Step 3: Plot Graphs ----------
if df is not None:
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






