from dependencies import *
import plotly.graph_objects as go


def AA_KPIs():
    # Load the Iris dataset (you can replace this with your own dataset)
    data=pd.read_csv("./AccidentAnalysis/data/Database.csv")
    data.drop('Unnamed: 0', axis=1, inplace=True)

    # Streamlit app title
    # st.title("Exploratory Data Analysis (EDA)")

    # Sidebar with options
    # st.sidebar.title("Options")
    show_data = st.checkbox("Show Dataset")
    
    # selected_feature = st.sidebar.selectbox("Select a Feature for Analysis", data.columns)

    # Show the dataset if selected
    if show_data:
        st.subheader("Historical data")
        st.write(data)

    st.markdown("<br>", unsafe_allow_html=True)

    # EDA Section
    # st.subheader("Exploratory Data Analysis")

    # selected_category = st.selectbox("Select a category:", ("Descriptive Analytics", "Predictive Analytics"))

    # if selected_category == "Descriptive Analytics":
    #     # st.header("Descriptive Analytics")
    #     # Create radio buttons for options in the Descriptive Analytics category

        
    selected_option = st.radio("Select an option:", [
        "Summary Statistics",
        "Accident Locations",
        "Loss per Each State",
        "State And Liquid Wise Loss",
        "Pipeline Locations",
        "Costs by Liquid Type and Pipeline Type",
        "Trends",
        "Accident Cause",
        # "Root Causes",
        "Causes for Oil Pipeline Spills"
    ])

# List of options
# options = ["Summary Statistics", "Trends", "Accident locations", "Accident Cause", "Root Causes", "Loss per Each State", "State And Liquid wise Loss", "Pipeline Locations", "Costs by Liquid Type and Pipeline Type", "Causes for Oil Pipeline Pills"]
# Display radio buttons for selecting one option
# selected_option = st.radio("Select one option:", options)

# Display the selected option
    # st.write("You selected:", selected_option)

    if selected_option=="Summary Statistics":

        # st.write("### Summary Statistics")
        columns = [
    'Operator Name','Pipeline/Facility Name', 'Pipeline Location', 'Pipeline Type',
    'Liquid Type', 'Liquid Subtype', 'Liquid Name', 'Accident City',
    'Accident County', 'Accident State', 'Cause Category', 'Cause Subcategory',
    'Unintentional Release (Barrels)', 'Intentional Release (Barrels)',
    'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'Liquid Ignition',
    'Liquid Explosion', 'Pipeline Shutdown', 'Shutdown Date/Time',
    'Restart Date/Time', 'Public Evacuations', 'Operator Employee Injuries',
    'Operator Contractor Injuries', 'Emergency Responder Injuries',
    'Other Injuries', 'Public Injuries', 'All Injuries',
    'Operator Employee Fatalities', 'Operator Contractor Fatalities',
    'Emergency Responder Fatalities', 'Other Fatalities',
    'Public Fatalities', 'All Fatalities', 'Property Damage Costs',
    'Lost Commodity Costs', 'Public/Private Property Damage Costs',
    'Emergency Response Costs', 'Environmental Remediation Costs',
    'Other Costs', 'All Costs']
        data = data[columns]

        default_selected_options = ['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'Other Costs', 'All Costs']

        selected_options = st.multiselect("Select features:", data.columns.tolist(), default=default_selected_options)
        
        if selected_options:
            st.write(data[selected_options].describe())
        else:
            st.warning("Please select at least one feature.")

    elif selected_option == "Accident Locations":
        df_scatter = data[['Accident Date/Time','Accident City','Pipeline/Facility Name','Pipeline Type', 'Accident Latitude', 'Accident Longitude','Accident State' ]]
        fig = px.scatter_mapbox(df_scatter, lat="Accident Latitude", lon="Accident Longitude", hover_name="Pipeline/Facility Name", 
                        hover_data=["Accident Date/Time", "Accident City",'Pipeline Type'],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=500)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        # Center the output
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            """
            <style>
            .streamlit-container {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


    elif selected_option == "Loss per Each State":
        df_bystate = data
        df_scatter = data[['Accident Date/Time','Accident City','Pipeline/Facility Name','Pipeline Type', 'Accident Latitude', 'Accident Longitude','Accident State' ]]
        df_bystate = df_scatter.groupby('Accident State').agg('count')['Pipeline Type']
        df_bystate = df_bystate.reset_index()
        df_bystate = df_bystate.rename(columns={"Pipeline Type": "Number of Accidents"})
        columns = ['Net Loss (Barrels)','All Costs']

        df_bystate = data.groupby('Accident State').agg(['sum','count'])
        df_bystate = df_bystate[columns]
        df_bystate['Number of Accident'] = df_bystate['Net Loss (Barrels)']['count']
        df_bystate['Num Barrels Lost'] = df_bystate['Net Loss (Barrels)']['sum'].apply(lambda x: round(x,2))
        df_bystate['Loss (million USD)'] = (df_bystate['All Costs']['sum'] / (1000000)).apply(lambda x: round(x,2))
        df_bystate = df_bystate.drop(columns=columns, axis=1)
        df_bystate = df_bystate.reset_index()

        k = df_bystate.sort_values(by='Loss (million USD)', ascending=False)

        for col in df_bystate.columns:
            df_bystate[col] = df_bystate[col].astype(str)

        df_bystate['text'] = df_bystate['Accident State'] + '<br>' + \
                            'Number of Accident: ' + df_bystate['Number of Accident']+ '<br>' + \
                            'Num Barrels Lost: ' + df_bystate['Num Barrels Lost']

        fig = go.Figure(data=go.Choropleth(
            locations=df_bystate['Accident State'], # Spatial coordinates
            z=df_bystate['Loss (million USD)'].astype(float), # Data to be color-coded
            locationmode='USA-states', # set of locations match entries in `locations`
            colorscale='Reds',
            text=df_bystate['text'],
            colorbar_title="Net Loss (million of USD)"
        ))

        fig.update_layout(
            title_text='Overall Loss (million of USD) by State from 2010-2017',
            geo_scope='usa' # limit map scope to USA
        )

        # Center the output
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            """
            <style>
            .streamlit-container {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


    elif selected_option == "State And Liquid Wise Loss":
        # Create a new DataFrame to group data by country and oil type
        grouped_df = data.groupby(['Accident State', 'Liquid Type'])['All Costs'].sum().reset_index()

        # Create a bar chart for visualization
        fig = px.bar(grouped_df, x='Accident State', y='All Costs', color='Liquid Type',
                    title='Costs by State and Liquid Type', labels={'All Costs': 'Total Costs'})

        # Customize the layout to increase the size of the graph
        fig.update_layout(
            xaxis_title='State',
            yaxis_title='Total Loss in USD',
            legend_title='Liquid Type',
            width=1000,  # Increase the width
            height=500  # Increase the height
        )

        # Center the output
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            """
            <style>
            .streamlit-container {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


    elif selected_option == "Pipeline Locations":
        bar_colors = px.colors.qualitative.Set3

        pipeline_location_counts = data['Pipeline Location'].value_counts().reset_index()
        pipeline_location_counts.columns = ['Pipeline Location', 'Count']

        # Create a bar chart for visualization with assigned colors
        fig = px.bar(pipeline_location_counts, x='Pipeline Location', y='Count',
                    title='Distribution of Pipeline Locations', color_discrete_sequence=bar_colors)

        # Customize the layout
        fig.update_xaxes(title_text='Pipeline Location')
        fig.update_yaxes(title_text='Number of Pipelines')

        # Center the output
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            """
            <style>
            .streamlit-container {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    elif selected_option == "Costs by Liquid Type and Pipeline Type":
        filtered_df = data[data['Pipeline Type'].isin(['ABOVEGROUND', 'TANK', 'UNDERGROUND']) &
                        data['Liquid Type'].isin(['CRUDE OIL', 'HVL OR OTHER FLAMMABLE OR TOXIC FLUID, GAS', 'REFINED AND/OR PETROLEUM PRODUCT (NON-HVL), LIQUID'])]

        # Create a new DataFrame to group data by liquid type and pipeline type
        liquid_pipeline_grouped_df = filtered_df.groupby(['Liquid Type', 'Pipeline Type'])['All Costs'].sum().reset_index()

        # Create a grouped bar chart for visualization
        fig = px.bar(liquid_pipeline_grouped_df, x='Liquid Type', y='All Costs',
                    color='Pipeline Type', barmode='group',
                    title='Loss by Liquid Type and Pipeline Type',
                    labels={'All Costs': 'Total Costs'})

        # Customize the layout
        fig.update_layout(xaxis_title='Liquid Type', yaxis_title='Total Loss in USD')

        # Center the output
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            """
            <style>
            .streamlit-container {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


# elif selected_category == "Predictive Analytics":

#     selected_option = st.radio("Select an option:", [
#         "Trends",
#         "Accident Cause",
#         # "Root Causes",
#         "Causes for Oil Pipeline Spills"
#     ])


    elif selected_option == "Trends":
        trend_option = st.radio("Select Trend Type:", ["Yearly Trend", "Monthly Trend"])

        data['datetime'] = pd.to_datetime(data['datetime'], format='%Y-%m-%d %H:%M:%S')

        if trend_option == "Monthly Trend":
            # Allow the user to select a specific year
            unique_years = sorted(data['datetime'].dt.year.unique())
            selected_year = st.selectbox("Select Year:", unique_years)

            # Filter data for the selected year
            yearly_data = data[data['datetime'].dt.year == selected_year]

            yearly_data['month'] = yearly_data['datetime'].dt.month

            # Group data by month and calculate the mean production for each month
            monthly_production = yearly_data.groupby('month')['All Costs'].mean()

            fig = px.line(
                x=monthly_production.index,
                y=monthly_production,
                labels={'x': 'Month', 'y': 'Average Cost'},
                title=f"Monthly Trend for {selected_year}",
            )
            fig.update_xaxes(tickvals=list(range(1, 13)), ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
            fig.update_yaxes(title="Total Loss in USD")

        elif trend_option == "Yearly Trend":
            yearly_production = data.groupby(data['datetime'].dt.year)['All Costs'].sum()
            fig = px.line(
                x=yearly_production.index,
                y=yearly_production,
                labels={'x': 'Year', 'y': 'Overall Costs'},
                title="Yearly Trend",
            )
            fig.update_xaxes(title="Year")
            fig.update_yaxes(title="Total Loss in USD")

        # Center the output
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            """
            <style>
            .streamlit-container {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


    elif selected_option == "Accident Cause":
        custom_colors = px.colors.qualitative.Set1
        main_causes = data['Cause Category'].value_counts().reset_index()
        main_causes.columns = ['Cause Category', 'Count']

        # Sort the data in descending order by Count
        main_causes = main_causes.sort_values(by='Count', ascending=False)

        fig = px.bar(main_causes, x='Count', y='Cause Category', orientation='h',
                    labels={'Count': 'Number of Accidents'},
                    color_discrete_sequence=custom_colors, category_orders={"Cause Category": main_causes['Cause Category']})

        # Center the output
        st.plotly_chart(fig, use_container_width=True)
        # st.markdown(
        #     """
        #     <style>
        #     .streamlit-container {
        #         display: flex;
        #         justify-content: center;
        #     }
        #     </style>
        #     """,
        #     unsafe_allow_html=True,
        # )


    # elif selected_option == "Root Causes":
    #     # Cross-tabulation
    #     crosstab = pd.crosstab(data['Cause Category'], data['Cause Subcategory'], margins=True)
    #     fig = go.Figure()

    #     for subcategory in crosstab.columns:
    #         fig.add_trace(go.Bar(
    #             y=crosstab.index,
    #             x=crosstab[subcategory],
    #             name=subcategory,
    #             orientation='h',
    #         ))

    #     fig.update_layout(
    #         barmode='stack',
    #         title='Accidents by Cause Category and Subcategory',
    #         xaxis_title='Number of Accidents',
    #         yaxis_title='Cause Category',
    #     )

    #     # Display the bar chart in Streamlit
    #     st.plotly_chart(fig)

    elif selected_option == "Causes for Oil Pipeline Spills":
        Material_Weld_Equipment_Failure = data[data['Cause Category'] == 'MATERIAL/WELD/EQUIP FAILURE']
        CORROSION = data[data['Cause Category'] == 'CORROSION']
        INCORRECT_OPERATION = data[data['Cause Category'] == 'INCORRECT OPERATION']
        NATURAL_FORCE_DAMAGE = data[data['Cause Category'] == 'NATURAL FORCE DAMAGE']
        EXCAVATION_DAMAGE = data[data['Cause Category'] == 'EXCAVATION DAMAGE']
        OTHER_OUTSIDE_FORCE_DAMAGE = data[data['Cause Category'] == 'OTHER OUTSIDE FORCE DAMAGE']
        ALL_OTHER_CAUSES = data[data['Cause Category'] == 'ALL OTHER CAUSES']

        trace0 = Material_Weld_Equipment_Failure['Cause Subcategory'].value_counts()
        trace0 = go.Bar(
            y=trace0.values,
            x=trace0.index.values,
            name='Material/Weld/Equipment Failure Count',
            marker=dict(
                color=trace0.values,
                colorscale='Viridis',
                reversescale=True
            )
        )

        trace1 = CORROSION['Cause Subcategory'].value_counts()
        trace1 = go.Bar(
            y=trace1.values,
            x=trace1.index.values,
            name='Corroison Count',
            marker=dict(
                color=trace1.values,
                colorscale='Viridis',
                reversescale=True
            )
        )

        trace2 = INCORRECT_OPERATION['Cause Subcategory'].value_counts()
        trace2 = go.Bar(
            y=trace2.values,
            x=trace2.index.values,
            name='INCORRECT OPERATION COUNT',
            marker=dict(
                color=trace2.values,
                colorscale='Viridis',
                reversescale=True
            )
        )

        trace3 = NATURAL_FORCE_DAMAGE['Cause Subcategory'].value_counts()
        trace3 = go.Bar(
            y=trace3.values,
            x=trace3.index.values,
            name='NATURAL FORCE DAMAGE COUNT',
            marker=dict(
                color=trace3.values,
                colorscale='Viridis',
                reversescale=True
            )
        )

        trace4 = EXCAVATION_DAMAGE['Cause Subcategory'].value_counts()
        trace4 = go.Bar(
            y=trace4.values,
            x=trace4.index.values,
            name='EXCAVATION DAMAGE COUNT',
            marker=dict(
                color=trace4.values,
                colorscale='Viridis',
                reversescale=True
            )
        )

        trace5 = OTHER_OUTSIDE_FORCE_DAMAGE['Cause Subcategory'].value_counts()
        trace5 = go.Bar(
            y=trace5.values,
            x=trace5.index.values,
            name='OTHER OUTSIDE FORCE DAMAGE COUNT',
            marker=dict(
                color=trace5.values,
                colorscale='Viridis',
                reversescale=True
            )
        )

        trace6 = ALL_OTHER_CAUSES['Cause Subcategory'].value_counts()
        trace6 = go.Bar(
            y=trace6.values,
            x=trace6.index.values,
            name='ALL OTHER CAUSES COUNT',
            marker=dict(
                color=trace6.values,
                colorscale='Viridis',
                reversescale=True
            )
        )

        fig = tls.make_subplots(rows=3, cols=3,
                                subplot_titles=('MATERIAL/WELD/EQUIPMENT FAILURE',
                                                'CORROSION', 'INCORRECT OPERATION', 'NATURAL FORCE DAMAGE',
                                                'EXCAVATION DAMAGE', 'OTHER OUTSIDE FORCE DAMAGE', 'ALL OTHER CAUSES'),
                                )

        fig.append_trace(trace0, 1, 1)
        fig.append_trace(trace1, 1, 2)
        fig.append_trace(trace2, 1, 3)
        fig.append_trace(trace3, 2, 1)
        fig.append_trace(trace4, 2, 2)
        fig.append_trace(trace5, 2, 3)
        fig.append_trace(trace6, 3, 1)

        fig['layout']['xaxis3'].update(tickangle=90)
        fig['layout']['xaxis4'].update(tickangle=90)
        fig['layout']['xaxis5'].update(tickangle=90)

        fig['layout']['yaxis1'].update(range=[0, 400])
        fig['layout']['yaxis2'].update(range=[0, 400], showticklabels=False)
        fig['layout']['yaxis3'].update(range=[0, 400], showticklabels=False)
        fig['layout']['yaxis4'].update(range=[0, 400])
        fig['layout']['yaxis5'].update(range=[0, 400], showticklabels=False)
        fig['layout']['yaxis6'].update(range=[0, 400], showticklabels=False)
        fig['layout']['yaxis7'].update(range=[0, 400])

        fig['layout'].update(title='CAUSES FOR OIL PIPELINE SPILLS',
                            height=2600, width=900, showlegend=False,
                            )

        # Center the output
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            """
            <style>
            .streamlit-container {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
