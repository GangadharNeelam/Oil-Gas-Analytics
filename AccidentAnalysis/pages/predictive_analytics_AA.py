from dependencies import *

def PredictiveAnalyticsAA():
    # Load your pre-trained models
    model1_path = "./AccidentAnalysis/models/Bagging_SVC_model.pkl"
    model1 = joblib.load(model1_path)

    model2_path = './AccidentAnalysis/models/SVC_model.pkl'
    model2 = joblib.load(model2_path)

    # Load your dataset (replace with your dataset file)
    df = pd.read_csv("./AccidentAnalysis/data/test_data_cls.csv")
    st.write(df)
    # df.drop('target', axis=1, inplace=True)
    # st.write(df.shape)
    # Create a Streamlit title and selection box for models
    st.subheader("Actual vs Predicted Production")
    selected_model = st.selectbox("Select a model:", ["Bagging_SVC_model (75% accuracy)", "SVC_model(70% accuracy)"])

    number_of_records = st.number_input("Select number of records", value=20)
    df = df.head(number_of_records)

    target = df['Cause Category']
    # st.write(target)
    df.drop('Cause Category', axis=1, inplace=True)

    # Define a function to make predictions and return a DataF
    # rame
    def predict_and_get_df(selected_model):
        if selected_model == "Bagging_SVC_model (75% accuracy)":
            model = model1
        elif selected_model == "SVC_model(70% accuracy)":
            model = model2
        else:
            st.warning("Please select a model.")
            return None

        predictions = model.predict(df)

        return predictions
    
    pred = predict_and_get_df(selected_model)
    # st.write(pred)

        # Replace "model.pkl" with the path to your pickle file
    with open('./AccidentAnalysis/models/encoder_cause_category.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
    # st.write(type(pred))
    pred = loaded_model.inverse_transform(pred)
    st.write(pred)
    # class_labels = {0: 'Not Failure', 1: 'Failure'}

    # if st.button("Predictions"):
    #     # Replace values with class labels
    #     target_labels = target.map(class_labels)
    #     pred_labels = pd.Series(pred).map(class_labels)

    #     # Create a DataFrame with renamed values
    #     data = {'Actual': target_labels, 'Predicted': pred_labels}
    #     final_df = pd.DataFrame(data)

    #     # Display the DataFrame using Streamlit
    #     st.write(final_df)

    # class_labels = ['Not Failure', 'Failure']

    # if st.button("Model Performance"):
    #     def plot_predictions(actual, predicted):
    #         # Calculate confusion matrix
    #         conf_matrix = confusion_matrix(actual, predicted)

    #         # Extract TP, FP, TN, FN
    #         tp = conf_matrix[1, 1]
    #         fp = conf_matrix[0, 1]
    #         tn = conf_matrix[0, 0]
    #         fn = conf_matrix[1, 0]

    #         # Group positive (both true and false) and negative (both true and false) predictions
    #         positive_predictions = tp + fp
    #         negative_predictions = tn + fn

    #         fig = go.Figure()

    #         # Add stacked bar chart
    #         fig.add_trace(go.Bar(
    #             x=['Failure', 'Not Failure'],
    #             y=[tp, tn],
    #             name='True Prediction',
    #             marker=dict(color='green')
    #         ))

    #         fig.add_trace(go.Bar(
    #             x=['Failure', 'Not Failure'],
    #             y=[fp, fn],
    #             name='False Prediction',
    #             marker=dict(color='red')
    #         ))

    #         fig.update_layout(
    #             barmode='stack',
    #             # xaxis=dict(title='Predictions'),
    #             yaxis=dict(title='Number of Parameters'),
    #             title='True and False Predictions'
    #         )

    #         # Display the plot using Streamlit
    #         st.plotly_chart(fig)

    #     actual_values = target
    #     predicted_values = pred
    #     plot_predictions(actual_values, predicted_values)
