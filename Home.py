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

    # selected_use_case = option_menu(
    #     options=["Oil Production Prediction", "Accident Analysis", "Equipment Failures", "Seismic Data Analysis"],
    #     orientation="horizontal",
    #     menu_title=None)
    
    selected_use_case = st.sidebar.selectbox("Select a use case", ["Oil Production Prediction", "Accident Analysis", "Equipment Failures", "Seismic Data Analysis"])

    # Display content based on the selected use case
    if selected_use_case == "Oil Production Prediction":
        # selected_option = st.selectbox("Select a page", ["KPIs", "Dashboard", "Simulation"])
        selected_option = option_menu(
            options=["KPIs", "Dashboard", "Simulation"],
            orientation="horizontal",
            menu_title=None)

        if selected_option == "Dashboard":
            Dashboard()
        elif selected_option == "KPIs":
            Oil_Production_KPIs()
        elif selected_option == "Simulation":
            Simulation()
        # Oil_Production_KPIs()

    elif selected_use_case == "Accident Analysis":
        EF_KPIs()
    elif selected_use_case == "Equipment Failures":
        
        selected_option = option_menu(
            options=["Dashboard", "Simulation"],
            orientation="horizontal",
            menu_title=None)
        
        if selected_option == "Dashboard":
            Dashboard_EF()
        elif selected_option == "Simulation":
            Simulation_EF()

    elif selected_use_case == "Seismic Data Analysis":
        seismic_analysis_page()

if __name__ == "__main__":
    # selected_page = st.sidebar.selectbox("Select a page", ["Home", "Analytics"])
    with st.sidebar:
        selected_page = option_menu(
            options=["Home", "Analytics"],
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
        st.markdown("<h1 style='text-align: center;'>Analytics Overview</h1>", unsafe_allow_html=True)
        analytics_page()
