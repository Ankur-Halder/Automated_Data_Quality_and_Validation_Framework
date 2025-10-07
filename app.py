import streamlit as st
import pandas as pd
import logging
import os
from datetime import datetime
from io import BytesIO

# ===== Logging Setup =====
LOG_FILE = "data_quality.log"

# Always start fresh
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("")  # Clear contents

logging.basicConfig(
    filename=LOG_FILE,
    filemode='w',  # Overwrite each run
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ===== Import from utils folder =====
from utils import check_missing_values
from utils import check_duplicates
from utils import check_outliers
from utils import prep_data

# ===== Streamlit UI Config =====
st.set_page_config(page_title="Data Quality Checker", page_icon="📊", layout="wide")
st.title("📊 Data Quality Pipeline")
st.markdown("Upload your dataset to check for **missing values, duplicates, and outliers**.")

# ===== File Upload =====
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read dataset
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        logging.info("=== New Run Started ===")
        logging.info(f"Dataset Shape: {df.shape}")

        # ===== Run Checks =====
        flag = check_missing_values(df)  # Returns True if > 5% missing
        if flag:
            df_processed = prep_data(df)
            logging.info("Missing value threshold exceeded → Data preprocessed.")
        else:
            df_processed = df.copy()
            logging.info("Missing value threshold not exceeded → No preprocessing.")

        check_duplicates(df_processed)
        check_outliers(df_processed)

        logging.info("Pipeline completed successfully.")
        st.success("Data Quality Check Completed ✅")

        # ===== Show Logs =====
        st.subheader("📜 Processing Log")
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as log:
                log_content = log.read()
            st.text_area("Log Output", log_content, height=300)

            # Clear file contents after printing
            with open(LOG_FILE, "w") as log:
                log.write("")
        else:
            st.info("No log file found yet.")

        # ===== Download Processed Dataset =====
        if flag:
            buffer = BytesIO()
            df_processed.to_csv(buffer, index=False)
            buffer.seek(0)
            st.subheader("⬇ Download Processed Dataset")
            st.download_button(
                label="Download CSV",
                data=buffer,
                file_name=f"processed_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("ℹ Missing value threshold not exceeded → No processed file generated.")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("📂 Please upload a CSV file to start.")

# ===== Footer =====
st.markdown("---")
st.caption("🚀 Data Quality Checker — Built with Streamlit")
