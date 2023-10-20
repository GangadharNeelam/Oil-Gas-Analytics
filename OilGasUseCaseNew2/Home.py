from dependencies import *

from OilProduction.pages.OP_KPI import OP_KPI
from OilProduction.pages.OP_PredictiveAnalytics import OP_PredictiveAnalytics
from OilProduction.pages.OP_Simulation import OP_simulation
from OilProduction.pages.OP_forecasting import OP_Forecasting

from EquipmentFailures.pages.EF_PredictiveAnalytics import EF_Predictive_Analytics
from EquipmentFailures.pages.EF_Simulation import EF_simulation
from EquipmentFailures.pages.EF_KPIs import EF_KPIs

from AccidentAnalysis.pages.AA_KPIs import AA_KPIs
from AccidentAnalysis.pages.AA_predictive_analytics import AA_PredictiveAnalytics
from AccidentAnalysis.pages.AA_Simulation import AA_Simulation


from SeismicDataAnalysis.pages.SA_KPIs import SA_KPIs
from SeismicDataAnalysis.pages.SA_PredictiveAnalytics import SA_Predictive_Analytics
from SeismicDataAnalysis.pages.SA_Simulation import SA_Simulation


def analytics_page():
    
    with st.sidebar:
        selected_use_case = st.radio("", ["Oil Production Prediction", "Accident Analysis", "Equipment Failures", "Seismic Data Analysis"],)

    if selected_use_case == "Oil Production Prediction":
        st.markdown("<h1 style='text-align: center;'>Oil Production Prediction</h1>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        selected_option = option_menu(
            options=["KPIs", "Predictive Analytics", "Simulation"],
            orientation="horizontal",
            icons=["📊", "📈", "📉"],
            menu_title=None)

        if selected_option == "KPIs":
            OP_KPI()
        elif selected_option == "Predictive Analytics":
            
            OP_PredictiveAnalytics()
            OP_Forecasting()
        elif selected_option == "Simulation":
            OP_simulation()
            
    elif selected_use_case == "Accident Analysis":
        st.markdown("<h1 style='text-align: center;'>Accident Analysis</h1>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

        selected_option = option_menu(
            options=["KPIs", "Predictive Analytics", "Simulation"],
            orientation="horizontal",
            icons=["📊", "📈", "📉"],
            menu_title=None)

        if selected_option == "KPIs":
            AA_KPIs()
        elif selected_option == "Predictive Analytics":
            AA_PredictiveAnalytics()
        elif selected_option == "Simulation":
            AA_Simulation()

        
    elif selected_use_case == "Equipment Failures":
        st.markdown("<h1 style='text-align: center;'>Equipment Failures</h1>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        selected_option = option_menu(
            options=["KPIs", "Predictive Analytics", "Simulation"],
            orientation="horizontal",
            icons=["📊", "📈", "📉"],
            menu_title=None)
        
        if selected_option == "KPIs":
            EF_KPIs()
        elif selected_option == "Predictive Analytics":
            EF_Predictive_Analytics()
        elif selected_option == "Simulation":
            EF_simulation()

    elif selected_use_case == "Seismic Data Analysis":
        st.markdown("<h1 style='text-align: center;'>Seismic Data Analysis</h1>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        selected_option = option_menu(
            options=["KPIs", "Predictive Analytics", "Simulation"],
            orientation="horizontal",
            icons=["📊", "📈", "📉"],
            menu_title=None)
        
        if selected_option == "KPIs":  
            SA_KPIs()
        elif selected_option == "Predictive Analytics":

            SA_Predictive_Analytics()
        elif selected_option == "Simulation":
            SA_Simulation()
        

if __name__ == "__main__":

    st.set_page_config(page_title="Oil&GasAnalytics", layout="wide")

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

        image = Image.open('./OilProduction/data/oil.jpg')
        st.image(image, caption='Oil & Gas Analytics Platform',use_column_width=True)

    elif selected_page == "Analytics":
        analytics_page()
