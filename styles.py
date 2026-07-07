import streamlit as st

def load_css():
    st.markdown("""
    <style>

    .stApp{
        background: linear-gradient(135deg,#eef2ff,#f8fafc);
    }

    .main-title{
        font-size:45px;
        font-weight:bold;
        text-align:center;
        color:#2563eb;
        margin-bottom:0;
    }

    .subtitle{
        text-align:center;
        color:#475569;
        font-size:18px;
        margin-top:0;
        margin-bottom:30px;
    }

    .card{
        background:white;
        padding:20px;
        border-radius:15px;
        box-shadow:0 8px 20px rgba(0,0,0,.08);
        border-left:6px solid #2563eb;
        margin-bottom:15px;
    }

    .green{
        border-left:6px solid #22c55e;
    }

    .orange{
        border-left:6px solid #f59e0b;
    }

    .red{
        border-left:6px solid #ef4444;
    }

    .footer{
        text-align:center;
        color:gray;
        margin-top:40px;
        font-size:14px;
    }

    </style>
    """, unsafe_allow_html=True)