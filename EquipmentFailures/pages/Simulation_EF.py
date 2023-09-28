from dependencies import *


def Simulation_EF():
    
    st.write("#### Input Parameter for Failure Prediction")
    default_values = {
        'sensor35_measure': 799478.0, 
        'sensor468': 4148518.0, 
        'sensor59_measure': 5245752.0, 
        'sensor61_measure': 916567.68, 
        'sensor45_measure': 76698.08, 
        'sensor17_measure': 1132040.0, 
        'sensor7_histogram_bin2': 0.0, 
        'sensor1_measure': 76698.0, 
        'sensor89_measure': 62282.0, 
        'sensor14_measure': 4933296.0, 
        'sensor278': 4148518.0, 
        'sensor13_measure': 0.0, 
        'sensor64_histogram_bin0': 0.0, 
        'sensor53_measure': 6167850.0, 
        'sensor1427': -1766918.0, 
        'sensor4615': 3045048.0, 
        'sensor16_measure': 1766008.0, 
        'sensor67_measure': 6700214.0, 
        'sensor105_histogram_bin0': 965866.0, 
        'sensor7_histogram_bin1': 0.0, 
        }

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

    model1_filename = './EquipmentFailures/models/random_forest_classifier.joblib'
    model1 = joblib.load(model1_filename)

    model2_filename = './EquipmentFailures/models/adaboost_classifier.joblib'
    model2 = joblib.load(model2_filename)

    selected_model = st.selectbox("Select a model:", ["Random Forest Classifier (75% accuracy)", "ADA Boost (70% accuracy)"])

    if selected_model == "Random Forest Classifier (75% accuracy)":
            model = model1

    elif selected_model == "ADA Boost (70% accuracy)":
            model = model2
    
    if st.button("Predict"):
        model = model
        prediction = model.predict(test_input)
        if prediction == 0:
            st.write("Not Failure")
        else:
            st.write("Failure")

    
