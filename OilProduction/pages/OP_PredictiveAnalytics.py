from dependencies import *

def OP_PredictiveAnalytics():
    # Load your pre-trained models
    model1 = joblib.load("./OilProduction/model/XGboost_Model.pkl")
    model2 = joblib.load("./OilProduction/model/LGB_Model.pkl")
    model3 = joblib.load("./OilProduction/model/ran_for_reg_Model.pkl")
    model4 = joblib.load("./OilProduction/model/grad_bos_reg_Model.pkl")

    df = pd.read_csv('./OilProduction/data/testing.csv')
    # if st.checkbox("Show Dataset"):
    #     number_of_records = st.number_input("Number of records to view", value=20)
    #     df = df.head(number_of_records)
    #     st.write(df)
    # st.write(df.shape)
    st.subheader("Actual vs Predicted Production")
    selected_model = st.selectbox("Select a model:", ["XgBOOST (96.06% accuracy)","LightGBM (96.39% accuracy)","Random Forest Regresssor (92.27% accuracy)","Gradient Boosting (accuracy 96.03%)"])

    number_of_records = st.number_input("Select number of records", value=20)
    df = df.head(number_of_records)

    def predict_and_get_df(selected_model):
        if selected_model == "XgBOOST (96.06% accuracy)":
            model = model1
        elif selected_model == "LightGBM (96.39% accuracy)":
            model = model2
        elif selected_model == "Random Forest Regresssor (92.27% accuracy)":
            model = model3
        elif selected_model == "Gradient Boosting (accuracy 96.03%)":
            model = model4
        else:
            st.warning("Please select a model.")
            return None
        
        X = df.drop('production', axis=1)
        y = df['production']
        predictions = model.predict(X)
        data = {'Actual': y, 'Predicted': predictions}
        return pd.DataFrame(data)

    # Create buttons for DataFrame and Graph
    show_df = st.checkbox("Predictions")
    show_graph = st.checkbox("Model Performance")

    if show_df:
        # st.write(f"## Model: {selected_model})")
        df_to_show = predict_and_get_df(selected_model)
        if df_to_show is not None:
            st.write(df_to_show)


    if show_graph:
        df_for_graph = predict_and_get_df(selected_model)
        if df_for_graph is not None:
            fig = px.line(df_for_graph, x=df_for_graph.index, y=['Actual', 'Predicted'],
                        labels={'index': 'Number of Records', 'value': 'Production in barrels'}, title=f'Actual vs Predicted Production')
            
            # Customize the line colors
            fig.update_traces(line=dict(color='blue'), selector=dict(name='Actual'))
            fig.update_traces(line=dict(color='red'), selector=dict(name='Predicted'))
            
            st.plotly_chart(fig)
