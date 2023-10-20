from dependencies import *

def OP_Forecasting():


    if st.checkbox("Show Forecasting"):
        df=pd.read_csv("./OilProduction/data/oil_gas_data.csv")

        list_of_companies = df["treatment company"].unique()

        selected_option=st.selectbox("Select TreatmentPlant",list_of_companies)

        df_new=df[df["treatment company"]==selected_option]

        final_df=df_new.loc[:,["date on production","production"]]

        final_df['dates'] = pd.to_datetime(final_df['date on production'])

        df_sorted = final_df.sort_values(by='dates')

        df_sorted['date'] = pd.to_datetime(df_sorted['dates'])

        result = df_sorted.groupby('date')['production'].sum().reset_index()

        N = 7 # Example: using a 7-day moving average

        result['Moving_Avg'] = result['production'].rolling(window=N).mean()

        forecast = result['Moving_Avg'].iloc[-N:].mean()

        fig = px.line(result, x=result.index, y=['production', 'Moving_Avg'],

                labels={'production': 'Historical Production', 'Moving_Avg': "forecasted production"},

                markers=True, line_shape='linear', title='Production Forecast')

    

        fig.update_xaxes(title_text='Day')

        fig.update_yaxes(title_text='Production')

    

        st.plotly_chart(fig)

    