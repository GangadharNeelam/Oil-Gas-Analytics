from dependencies import *


def Simulation_AA():
    
    st.write("#### Input Parameter for Failure Prediction")

    default_values = {
        'Accident Year' : 2010.0,
        'Pipeline Location' : 1.0,
        'Pipeline Type' : 0.0,
        'Liquid Type'	: 3.0,
        'Liquid Subtype'	: 4.0,
        'Unintentional Release (Barrels)'	: 21.0,
        'Intentional Release (Barrels)' : 0.1,
        'Liquid Recovery (Barrels)' : 0.0,
        'Net Loss (Barrels)': 21.0,
        'Pipeline Shutdown' :	0.0,
        'Public Evacuations' : 0.0,
        'All Injuries' : 1.0,
        'All Fatalities' : 1.0,
        'Property Damage Costs' : 110.0,
        'Lost Commodity Costs' : 1517.0,
        'Public/Private Property Damage Costs' : 0.0,
        'Emergency Response Costs' : 0.0,
        'Environmental Remediation Costs'	: 0.0,
        'Other Costs'	: 0.0,
        'All Costs' : 1627.0,
        }

    # st.write(default_values)
    col1, col2, col3, col4 = st.columns(4)
    columns = [col1, col2, col3, col4]

    # Create input widgets for each parameter
    user_input = {}
    for i, (param, default_value) in enumerate(default_values.items()):
        with columns[i % 4]:
            user_input[param] = st.number_input(param, value=default_value, step=0.01, format="%.2f")

    confirmed = st.checkbox("Confirm Input")

    # Display the user-inputted values after confirmation
    if confirmed:
        
        st.write(user_input)

    test_input= np.array(list(user_input.values()),ndmin=2)

    st.write(test_input)

    # Load your pre-trained models
    model1_path = "./AccidentAnalysis/models/Bagging_SVC_model.pkl"
    model1 = joblib.load(model1_path)

    model2_path = './AccidentAnalysis/models/SVC_model.pkl'
    model2 = joblib.load(model2_path)


    selected_model = st.selectbox("Select a model:", ["Bagging SVC_model (75% accuracy)", "SVC model (70% accuracy)"])

    if selected_model == "Bagging SVC_model (75% accuracy)":
            model = model1

    elif selected_model == "SVC model (70% accuracy)":
            model = model2
    
    if st.button("Predict"):
        model = model
        prediction = model.predict(test_input)
        # st.write(prediction)

        with open('./AccidentAnalysis/models/encoder_cause_category.pkl', 'rb') as file:
            loaded_model = pickle.load(file)

        pred = loaded_model.inverse_transform(prediction)
        st.write("The Accident Caused due to ", pred[0])