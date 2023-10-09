from dependencies import *

def AA_PredictiveAnalytics():

    model1_path = "./AccidentAnalysis/models/Bagging_SVC_model.pkl"
    with open(model1_path, 'rb') as file:
        model1 = pickle.load(file)

    model2_path = './AccidentAnalysis/models/SVC_model.pkl'
    with open(model2_path, 'rb') as file:
        model2 = pickle.load(file)


    # Load your dataset (replace with your dataset file)
    df = pd.read_csv("./AccidentAnalysis/data/test_data_cls.csv")
    df2 = pd.read_csv("./AccidentAnalysis/data/accident_data.csv")

    if st.checkbox("Show Dataset"):
        st.write(df2.head())

    select_prediction = st.radio("Select a prediction:", ["Accident Cause Prediction", "Total loss Prediction"])
    
    if select_prediction == "Accident Cause Prediction":
        st.subheader("Accident Prediction")
        selected_model = st.selectbox("Select a model:", ["SVC_model(65% accuracy)", "Bagging_SVC_model (61% accuracy)"])

        number_of_records = st.number_input("Select number of records", value=20)
        df = df.head(number_of_records)

        target = df['Cause Category']
        # st.write(target)
        df.drop('Cause Category', axis=1, inplace=True)

        # Define a function to make predictions and return a DataF
        # rame
        def predict_and_get_df(selected_model):
            if selected_model == "SVC_model(65% accuracy)":
                model = model2
            elif selected_model == "Bagging_SVC_model (61% accuracy)":
                model = model1
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
        actual = loaded_model.inverse_transform(target)
        st.write(pred)

    elif select_prediction == "Total loss Prediction":
        # Load your pre-trained models
        reg_model1_path = "./AccidentAnalysis/models/reg_lgb_model.pkl"
        with open(reg_model1_path, 'rb') as file:
            reg_model1 = pickle.load(file)

        reg_model2_path = './AccidentAnalysis/models/rf_reg_model.pkl'
        with open(reg_model2_path, 'rb') as file:
            reg_model2 = pickle.load(file)

        st.subheader("Total loss prediction")
        selected_model = st.selectbox("Select a model:", ["Random Forest Regressor", "Light GBM Regressor"])

        number_of_records = st.number_input("Select number of records", value=20)
        df = df.head(number_of_records)

        target = df['All Costs']
        # st.write(target)
        df.drop('All Costs', axis=1, inplace=True)

        # Define a function to make predictions and return a DataF
        # rame
        def predict_and_get_df(selected_model):
            if selected_model == "Random Forest Regressor":
                model = model1
            elif selected_model == "Light GBM Regressor":
                model = model2
            else:
                st.warning("Please select a model.")
                return None

            predictions = model.predict(df)

            return predictions
        
        predictions = predict_and_get_df(selected_model)

        st.write(predictions)