from dependencies import *


def Oil_Production_KPIs():
    data=pd.read_csv("./Analytics/data/oil_gas_data.csv")

    show_data = st.checkbox("Show Dataset")
    
    if show_data:
        st.subheader("Data")
        st.write(data)

    # List of options
    options = ["Summary Statistics", "Production Rate vs Proppant Volume",
            "Average Production by Month", "Average Well Spacing by Treatment Company", "Production Trends"]

    # Display radio buttons for selecting one option
    selected_option = st.radio("", options)

    # Display the selected option
    # st.write("You selected:", selected_option)

    if selected_option == "Summary Statistics":
        # Create a multiselect dropdown for selecting features
        default_selected_options = ['proppant volume', 'well spacing', 'proppant fluid ratio', 'production']
        selected_options = st.multiselect("", data.columns.tolist(), default=default_selected_options)
        
        if selected_options:
            st.write(data[selected_options].describe())
        else:
            st.warning("Please select at least one feature.")


    elif selected_option=="Production Rate vs Proppant Volume":
        fig = px.scatter(data, x='production', y='proppant volume', 
                    title="Production Rate vs Proppant Volume",
                    labels={'production': 'Production Rate', 'proppant volume': 'Proppant Volume in tons'})
        
        
        st.plotly_chart(fig)


    elif selected_option=="Average Production by Month":

        data['date on production'] = pd.to_datetime(data['date on production'],format='%m/%d/%Y')

        data['month'] = data['date on production'].dt.month
        # Group data by month and calculate the mean production for each month
        monthly_production = data.groupby('month')['production'].mean()
        fig = px.bar(
            x=monthly_production.index,
            y=monthly_production,
            labels={'x': 'Month', 'y': 'Average Production in barrels'},
            title="Average Production by Month",
        )

        fig.update_xaxes(tickvals=list(range(1, 13)), ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        fig.update_yaxes(title="Average Production")

        st.plotly_chart(fig)


    elif selected_option=="Average Well Spacing by Treatment Company":
        
        fig = px.bar(
            data,
            x='treatment company',
            y='well spacing',
            title="Average Well Spacing by Treatment Company",
        )

        fig.update_xaxes(title="Treatment Company", tickangle=90)
        fig.update_yaxes(title="Average Well Spacing")

        st.plotly_chart(fig)
        
    elif selected_option=="Production Trends":
        
        trend_option = st.selectbox("Select Trend Type:", ["Yearly Trend", "Monthly Trend"])
        
        data['date on production'] = pd.to_datetime(data['date on production'], format='%m/%d/%Y')
        unique_years = sorted(data['date on production'].dt.year.unique())
        data['year'] = data['date on production'].dt.year

        if trend_option == "Monthly Trend":
            # Allow the user to select a specific year
            selected_year = st.selectbox("Select Year:", unique_years)

            # Filter data for the selected year
            yearly_data = data[data['date on production'].dt.year == selected_year]

            yearly_data['month'] = yearly_data['date on production'].dt.month
        # Group data by month and calculate the mean production for each month
            monthly_production = yearly_data.groupby('month')['production'].mean()

            fig = px.line(
                x=monthly_production.index,
                y=monthly_production,
                labels={'x': 'Month', 'y': 'Production in barrels'},
                title=f"Monthly Trend for {selected_year}",
            )
            fig.update_xaxes(tickvals=list(range(1, 13)), ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
            fig.update_yaxes(title="Production in barrels")
            # fig.update_traces(mode='lines+markers')
            st.plotly_chart(fig)

        elif trend_option == "Yearly Trend":

            yearly_production = data.groupby('year')['production'].sum()
            fig = px.line(
                x=yearly_production.index,
                y=yearly_production,
                labels={'x': 'Year', 'y': 'Production in barrels'},
                title="Yearly Trend",
            )
            # fig.update_traces(mode='lines+markers')
            fig.update_xaxes(title="Year")
            fig.update_yaxes(title="Production in barrels")

            st.plotly_chart(fig)
