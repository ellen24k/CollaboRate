import pyshorteners
import streamlit as st


def padding_set():
    css = """
    <style>
    .stMainBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 {
        padding-top: 24px;
        padding-right: 0px;
        padding-bottom: 4px;
        padding-left: 0px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def logo(str='', divide=True):
    padding_set()
    st.title(':rainbow[Collabo + Rate]')
    st.markdown(f'{str} _Real-time team project rating system_')
    if divide: st.divider()


def menu_hide():
    # .stAppToolbar {visibility: hidden;}
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppToolbar {visibility: hidden;}
    .stToolbarActionButton {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def shorten_url(url):
    s = pyshorteners.Shortener()
    ret_url = s.tinyurl.short(url)
    return ret_url


def url_to_qr_code(url):
    qr_code = f'https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={url}'
    return qr_code


