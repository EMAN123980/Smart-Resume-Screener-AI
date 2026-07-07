import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        /* ==========================================
           Main App
        ========================================== */

        .stApp{
            background:#f4f7fb;
        }

        /* ==========================================
           Header
        ========================================== */

        h1{
            color:#0f172a;
            text-align:center;
            font-weight:700;
        }

        h2,h3{
            color:#1e3a8a;
            font-weight:600;
        }

        /* ==========================================
           Sidebar
        ========================================== */

        section[data-testid="stSidebar"]{
            background:#0f172a;
        }

        section[data-testid="stSidebar"] *{
            color:white;
        }

        /* ==========================================
           Buttons
        ========================================== */

        .stButton>button{

            background:#2563eb;
            color:white;

            border-radius:10px;

            border:none;

            padding:10px 20px;

            font-weight:bold;

            transition:0.3s;
        }

        .stButton>button:hover{

            background:#1d4ed8;

            color:white;
        }

        /* ==========================================
           File Uploader
        ========================================== */

        div[data-testid="stFileUploader"]{

            border:2px dashed #2563eb;

            border-radius:12px;

            padding:15px;

            background:white;

        }

        /* ==========================================
           Text Area
        ========================================== */

        textarea{

            border-radius:10px !important;

        }

        /* ==========================================
           Metric Cards
        ========================================== */

        div[data-testid="metric-container"]{

            background:white;

            border-radius:15px;

            padding:15px;

            box-shadow:0 4px 12px rgba(0,0,0,0.08);

            border-left:5px solid #2563eb;

        }

        /* ==========================================
           Progress Bar
        ========================================== */

        div[data-testid="stProgressBar"] div{

            background:#22c55e;

        }

        /* ==========================================
           Expander
        ========================================== */

        .streamlit-expanderHeader{

            font-size:18px;

            font-weight:bold;

            color:#1e3a8a;

        }

        /* ==========================================
           Footer
        ========================================== */

        footer{

            visibility:hidden;

        }

        /* ==========================================
           Top Menu
        ========================================== */

        #MainMenu{

            visibility:hidden;

        }

        </style>
        """,
        unsafe_allow_html=True
    )