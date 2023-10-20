from dependencies import *

def EF_Predictive_Analytics():
    # Load your pre-trained models
    model1_filename = './EquipmentFailures/models/random_forest_classifier.joblib'
    model1 = joblib.load(model1_filename)

    model2_filename = './EquipmentFailures/models/adaboost_classifier.joblib'
    model2 = joblib.load(model2_filename)

    # Load your dataset (replace with your dataset file)
    df = pd.read_csv('./EquipmentFailures/data/new_data.csv')

    st.subheader("Actual vs Predicted Production")
    selected_model = st.selectbox("Select a model:", ["Random Forest Classifier (75% accuracy)", "ADA Boost (70% accuracy)"])

    number_of_records = st.number_input("Select number of records", value=20, step=10)
    df = df.head(number_of_records)

    target = df['target']
    # st.write(target)
    df.drop('target', axis=1, inplace=True)

    # Define a function to make predictions and return a DataFrame
    def predict_and_get_df(selected_model):
        if selected_model == "Random Forest Classifier (75% accuracy)":
            model = model1
        elif selected_model == "ADA Boost (70% accuracy)":
            model = model2
        else:
            st.warning("Please select a model.")
            return None

        predictions = model.predict(df)

        return predictions
    
    pred = predict_and_get_df(selected_model)

    class_labels = {0: 'Not Failure', 1: 'Failure'}

    if st.button("Predictions"):
        # Replace values with class labels
        target_labels = target.map(class_labels)
        pred_labels = pd.Series(pred).map(class_labels)

        # Create a DataFrame with renamed values
        data = {'Actual': target_labels, 'Predicted': pred_labels}
        final_df = pd.DataFrame(data)

        # Display the DataFrame using Streamlit
        st.write(final_df)

    class_labels = ['Not Failure', 'Failure']

    if st.button("Model Performance"):
        def plot_predictions(actual, predicted):
            # Calculate confusion matrix
            conf_matrix = confusion_matrix(actual, predicted)

            # Extract TP, FP, TN, FN
            tp = conf_matrix[1, 1]
            fp = conf_matrix[0, 1]
            tn = conf_matrix[0, 0]
            fn = conf_matrix[1, 0]

            fig = go.Figure()

            # Add separate bars for each category
            fig.add_trace(go.Bar(
                x=['Failure'],
                y=[tp],
                name='True Positive (Failure))',
                marker=dict(color='green')
            ))

            fig.add_trace(go.Bar(
                x=['Failure'],
                y=[fp],
                name='False Positive (Not Failure)',
                marker=dict(color='red')
            ))

            fig.add_trace(go.Bar(
                x=['Not Failure'],
                y=[tn],
                name='True Negative (Not Failure)',
                marker=dict(color='green')
            ))

            fig.add_trace(go.Bar(
                x=['Not Failure'],
                y=[fn],
                name='False Negative (Failure)',
                marker=dict(color='red')
            ))

            fig.update_layout(
                barmode='group',
                xaxis=dict(title='Predictions'),
                yaxis=dict(title='Number of Parameters'),
                title='True and False Predictions'
            )

            # Display the plot using Streamlit
            st.plotly_chart(fig, use_container_width=True)

        actual_values = target
        predicted_values = pred
        plot_predictions(actual_values, predicted_values)
