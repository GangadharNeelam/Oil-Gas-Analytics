from dependencies import *

def EF_KPIs():

    st.subheader('Threshold Crossings by Sensors')

    df=pd.read_csv("./EquipmentFailures/data/new_data.csv")

    f_df = df[df['target'].isin([0, 1])]
    threshold={}
    variable_names =f_df.columns[:-1] 
    for i in variable_names:
    
        x=f_df[i].mean()
        y=sum(f_df[i]>x)
        threshold[i]=[x,y]

    sensors = list(threshold.keys())
    thresholds_crossed = [data[1] for data in threshold.values()]
    fig = px.bar(x=sensors, y=thresholds_crossed, color=thresholds_crossed,
            labels={'x': 'Sensors', 'y': 'Thresholds Crossed'})
            # title='Number of Times Threshold Crossed by Sensors')

    # Customize the layout if needed
    fig.update_layout(xaxis=dict(tickangle=-45),
                    yaxis=dict(title='Thresholds Crossed'),
                    coloraxis=dict(colorscale='Reds'),
                    autosize=False, width=800, height=500)
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        """
        <style>
        .stPlotlyChart {
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
