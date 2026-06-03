import streamlit as st
import pandas as pd
import zipfile
import tempfile
import os
import glob

from stroop_utils import (
    process_single_file,
    process_multiple_files
)

# PAGE CONFIG

st.set_page_config(
    page_title="Stroop Score Calculator",
    page_icon="",
    layout="wide"
)

# CUSTOM CSS

st.markdown("""
<style>

.main-title {
    font-size:40px;
    font-weight:bold;
    color:#1E88E5;
}

.subtitle {
    color:gray;
    margin-bottom:20px;
}

.metric-box {
    padding:15px;
    border-radius:10px;
    background:#f5f5f5;
}

</style>
""", unsafe_allow_html=True)

# HEADER

st.markdown(
    '<div class="main-title"> Stroop Score Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Calculate Interference and Facilitation Scores Automatically</div>',
    unsafe_allow_html=True
)

st.divider()

# MODE SELECTION

mode = st.radio(
    "Select Analysis Type",
    [
        "Single Participant",
        "Batch Analysis"
    ],
    horizontal=True
)

# ---
# TRIAL SELECTION

analysis_type = st.radio(
    "Trial Selection",
    [
        "Correct Trials Only",
        "All Trials"
    ],
    horizontal=True
)

correct_only = (
    analysis_type ==
    "Correct Trials Only"
)

# SINGLE PARTICIPANT

if mode == "Single Participant":

    st.subheader("📄 Single Participant Analysis")

    uploaded_file = st.file_uploader(
        "Upload Participant CSV File",
        type=["csv"]
    )

    if uploaded_file:

        try:

            result = process_single_file(
                uploaded_file, correct_only
            )

            df = pd.DataFrame([result])

            st.success("Analysis Completed Successfully")

            st.subheader("Participant Scores")

            st.dataframe(
                df,
                use_container_width=True
            )

            csv = df.to_csv(
                index=False
            )

            st.download_button(
                label="⬇ Download Participant Output",
                data=csv,
                file_name="participant_scores.csv",
                mime="text/csv"
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )

# BATCH ANALYSIS

else:

    st.subheader("📁 Batch Analysis")

    st.info(
        """
        Upload a ZIP file containing the complete Stroop_Pre folder.

        Example:

        Stroop_Pre.zip
        ├── Answara_Stroop
        ├── GANAVI_Stroop_PRE_007
        ├── Hemanth_Stroop
        ├── Stroop_Gorakh_Pre
        └── ...
        """
    )

    uploaded_zip = st.file_uploader(
        "Upload Stroop_Pre.zip",
        type=["zip"]
    )

    if uploaded_zip:

        try:

            with st.spinner("Processing all participants..."):

                with tempfile.TemporaryDirectory() as temp_dir:

                    zip_path = os.path.join(
                        temp_dir,
                        uploaded_zip.name
                    )

                    with open(zip_path, "wb") as f:
                        f.write(
                            uploaded_zip.getbuffer()
                        )

                    with zipfile.ZipFile(
                        zip_path,
                        "r"
                    ) as zip_ref:

                        zip_ref.extractall(
                            temp_dir
                        )

                    csv_files = glob.glob(
                        os.path.join(
                            temp_dir,
                            "**",
                            "*.csv"
                        ),
                        recursive=True
                    )

                    if len(csv_files) == 0:

                        st.error(
                            "No CSV files found in ZIP."
                        )

                    else:

                        final_df = process_multiple_files(
                            csv_files, correct_only
                        )

                        st.success(
                            f"Successfully Processed {len(final_df)} Participants"
                        )

                        # METRICS

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric(
                                "Participants",
                                len(final_df)
                            )

                        with col2:

                            if "High_Block_IF" in final_df.columns:

                                st.metric(
                                    "Mean High IF",
                                    round(
                                        final_df["High_Block_IF"]
                                        .dropna()
                                        .mean(),
                                        3
                                    )
                                )

                        with col3:

                            if "Low_Block_IF" in final_df.columns:

                                st.metric(
                                    "Mean Low IF",
                                    round(
                                        final_df["Low_Block_IF"]
                                        .dropna()
                                        .mean(),
                                        3
                                    )
                                )

                        st.subheader(
                            "Results Preview"
                        )

                        st.dataframe(
                            final_df,
                            use_container_width=True
                        )

                        csv = final_df.to_csv(
                            index=False
                        )

                        st.download_button(
                            label="⬇ Download Final Output",
                            data=csv,
                            file_name="Final_Stroop_Output.csv",
                            mime="text/csv"
                        )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )

# FOOTER

st.divider()

st.caption(
    "Developed for Stroop Task Research Data Analysis"
)