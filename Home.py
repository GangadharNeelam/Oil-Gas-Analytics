import streamlit as st
from streamlit.elements import image as st_image
from PIL import Image

from streamlit_option_menu import option_menu

# Import your page functions
from Analytics.pages.Dashboard import Dashboard
from Analytics.pages.EDA import Oil_Production_KPIs
from Analytics.pages.Simulation import Simulation
from EquipmentFailures.pages.EDA_EF import EF_KPIs
from EquipmentFailures.pages.Dashboard_EF import Dashboard_EF
from EquipmentFailures.pages.Simulation_EF import Simulation_EF
from SeismicDataAnalysis.pages.seismic_analysis import seismic_analysis_page


def analytics_page():
    
    with st.sidebar:
    # selected_use_case = st.sidebar.selectbox("Select a use case", ["Oil Production Prediction", "Accident Analysis", "Equipment Failures", "Seismic Data Analysis"])
        selected_use_case = st.radio("", ["Oil Production Prediction", "Accident Analysis", "Equipment Failures", "Seismic Data Analysis"],
        )
    # Display content based on the selected use case
    
    if selected_use_case == "Oil Production Prediction":
        st.markdown("<h1 style='text-align: center;'>Oil Production Prediction</h1>", unsafe_allow_html=True)
        # Custom HTML and CSS styles for a professional and attractive header
        # header_html = f"""
        #     <style>
        #         .header {{
        #             background-color: #3498db; /* Blue color */
        #             color: white;
        #             text-align: center;
        #             padding: 20px;
        #             margin-bottom: 20px;
        #         }}
        #         .company-name {{
        #             font-weight: bold;
        #             font-size: 36px;
        #         }}
        #     </style>
        #     <div class="header">
        #         <p class="company-name">{"Oil"}</p>
        #     </div>
        # """
        # st.markdown(header_html, unsafe_allow_html=True)
        # selected_option = st.selectbox("Select a page", ["KPIs", "Dashboard", "Simulation"])
        st.markdown("<br><br>", unsafe_allow_html=True)
        selected_option = option_menu(
            options=["KPIs", "Predictive Analytics", "Simulation"],
            orientation="horizontal",
            icons=["📊", "📈", "📉"],
            menu_title=None)

        if selected_option == "Predictive Analytics":
            Dashboard()
        elif selected_option == "KPIs":
            Oil_Production_KPIs()
        elif selected_option == "Simulation":
            Simulation()
            st.write("Simulation")
    elif selected_use_case == "Accident Analysis":
        st.markdown("<h1 style='text-align: center;'>Accident Analysis</h1>", unsafe_allow_html=True)
        # EF_KPIs()
        st.markdown("<br><br>", unsafe_allow_html=True)
        selected_option = option_menu(
            options=["KPIs", "Predictive Analytics", "Simulation"],
            orientation="horizontal",
            icons=["📊", "📈", "📉"],
            menu_title=None)

        if selected_option == "Predictive Analytics":
            st.write("")
        elif selected_option == "KPIs":
            EF_KPIs()

        
    elif selected_use_case == "Equipment Failures":
        st.markdown("<h1 style='text-align: center;'>Equipment Failures</h1>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        selected_option = option_menu(
            options=["KPIs", "Predictive Analytics", "Simulation"],
            orientation="horizontal",
            icons=["📊", "📈", "📉"],
            menu_title=None)
        
        if selected_option == "Predictive Analytics":
            Dashboard_EF()
        elif selected_option == "Simulation":
            Simulation_EF()
        elif selected_option == "KPIs":
            st.write("")

    elif selected_use_case == "Seismic Data Analysis":
        st.markdown("<h1 style='text-align: center;'>Seismic Data Analysis</h1>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        selected_option = option_menu(
            options=["KPIs", "Predictive Analytics", "Simulation"],
            orientation="horizontal",
            icons=["📊", "📈", "📉"],
            menu_title=None)
        
        if selected_option == "Predictive Analytics":
            st.write("")
        elif selected_option == "Simulation":
            st.write("")
        elif selected_option == "KPIs":
            
            seismic_analysis_page()
        

if __name__ == "__main__":

    st.set_page_config(page_title="Oil&GasAnalytics", layout="wide")

    # image = Image.open('./Analytics/data/celebal_logo.png')
    # resized_image = image.resize((180, 70))
    # st.sidebar.image(resized_image)
    
    with st.sidebar:
        selected_page = option_menu(
            options=["Home", "Analytics"],
            icons=["🏠", "📊"],
            menu_title=None
        )

    if selected_page == "Home":
        st.markdown("<h1 style='text-align: center;'>Oil & Gas Analytics Platform</h1>", unsafe_allow_html=True)
        st.subheader('About')
        st.write("At Oil & Gas Analytix, our expertise lies in the art of turning raw data into actionable intelligence. With a sophisticated blend of Exploratory Data Analysis (EDA) and advanced simulation techniques, we illuminate the complex dynamics of the oil and gas industry. Our solutions don't just stop at numbers; we craft insightful graphs that offer a clear and intuitive understanding of trends and patterns.")
        st.subheader('Capabilities')
        st.write(" Our capabilities revolve around the mastery of data-driven insights. We excel in the art of Exploratory Data Analysis (EDA) and sophisticated simulation techniques, enabling us to decode the intricate complexities of the oil and gas sector.")

        image = Image.open('./Analytics/data/oil.jpg')
        st.image(image, caption='Oil & Gas Analytics Platform',use_column_width=True)
        

    elif selected_page == "Analytics":
        # st.markdown("<h1 style='text-align: center;'>Analytics Overview</h1>", unsafe_allow_html=True)
        analytics_page()
