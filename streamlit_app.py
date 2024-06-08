import streamlit as st
import pandas as pd
import joblib
from streamlit_chat import message as st_message
import os

# Define disease information
disease_info = {
    "Vertigo": {
        "precautions": "Avoid sudden head movements. Sleep with your head slightly elevated. Be careful when lying down or getting up.",
        "actions": "Perform Epley maneuvers to reposition ear crystals. Consult a doctor for medication if symptoms persist. Stay hydrated and avoid caffeine and alcohol."
    },
    "Acne": {
        "precautions": "Keep your skin clean and oil-free. Avoid heavy makeup and use non-comedogenic products. Do not pick or squeeze pimples.",
        "actions": "Use over-the-counter topical treatments containing benzoyl peroxide or salicylic acid. Consult a dermatologist for prescription medications if necessary. Maintain a balanced diet and stay hydrated."
    },
    "AIDS": {
        "precautions": "Practice safe sex by using condoms. Do not share needles or syringes. Regularly get tested for HIV if at risk.",
        "actions": "Take antiretroviral therapy (ART) as prescribed by your doctor. Maintain a healthy lifestyle to boost your immune system. Seek support from counseling and support groups."
    },
    "Alcoholic Hepatitis": {
        "precautions": "Avoid alcohol consumption entirely. Eat a balanced diet rich in vitamins and nutrients. Monitor liver health regularly.",
        "actions": "Seek medical treatment and follow the prescribed medication regimen. Join a support group for alcohol dependence. Follow a liver-friendly diet and avoid toxins."
    },
    "Allergy": {
        "precautions": "Identify and avoid known allergens. Keep your living environment clean and free from dust mites and pet dander. Use hypoallergenic products.",
        "actions": "Take antihistamines to relieve symptoms. Consult an allergist for allergy testing and treatment options. Carry an epinephrine injector if you have severe allergies."
    },
    "Arthritis": {
        "precautions": "Maintain a healthy weight to reduce joint stress. Stay active with low-impact exercises. Avoid repetitive joint strain.",
        "actions": "Take anti-inflammatory medications as prescribed. Engage in physical therapy to improve joint function. Apply hot or cold compresses to affected joints."
    },
    "Bronchial Asthma": {
        "precautions": "Avoid known triggers such as pollen, smoke, and dust. Monitor your breathing with a peak flow meter. Keep rescue inhalers accessible.",
        "actions": "Use inhaled corticosteroids and bronchodilators as prescribed. Follow an asthma action plan created with your doctor. Seek emergency medical help if experiencing severe asthma attacks."
    },
    "Cervical Spondylosis": {
        "precautions": "Maintain good posture, especially while sitting and working. Avoid heavy lifting and neck strain. Perform neck exercises to maintain flexibility.",
        "actions": "Use pain relievers and anti-inflammatory medications as needed. Apply heat or cold packs to the neck area. Consult a physical therapist for tailored exercises."
    },
    "Chickenpox": {
        "precautions": "Avoid contact with infected individuals. Vaccinate children against varicella. Maintain good personal hygiene.",
        "actions": "Use calamine lotion and antihistamines to relieve itching. Keep fingernails short to prevent skin infections from scratching. Rest and stay hydrated."
    },
    "Chronic Cholestasis": {
        "precautions": "Avoid alcohol and hepatotoxic drugs. Follow a low-fat diet to reduce liver workload. Monitor liver function regularly.",
        "actions": "Take prescribed medications to manage bile flow. Seek regular medical follow-ups. Consult a hepatologist for advanced care."
    },
    "Common Cold": {
        "precautions": "Wash hands frequently and avoid close contact with sick individuals. Avoid touching your face with unwashed hands. Maintain good overall health with a balanced diet and exercise.",
        "actions": "Rest and drink plenty of fluids. Use over-the-counter cold medications to alleviate symptoms. Use a humidifier to ease nasal congestion."
    },
    "Dengue": {
        "precautions": "Avoid mosquito bites by using repellents and wearing protective clothing. Eliminate standing water to reduce mosquito breeding sites. Use mosquito nets and screens in living areas.",
        "actions": "Rest and stay hydrated. Take acetaminophen for pain relief (avoid NSAIDs like ibuprofen). Seek medical attention for severe symptoms like bleeding or abdominal pain."
    },
    "Diabetes": {
        "precautions": "Monitor blood glucose levels regularly. Maintain a healthy diet low in sugars and refined carbohydrates. Exercise regularly to manage blood sugar levels.",
        "actions": "Take insulin or oral hypoglycemic agents as prescribed. Consult an endocrinologist for regular diabetes management. Educate yourself about managing diabetes complications."
    },
    "Dimorphic Hemorrhoids (Piles)": {
        "precautions": "Avoid straining during bowel movements. Eat a high-fiber diet to prevent constipation. Stay hydrated and exercise regularly.",
        "actions": "Use over-the-counter creams or suppositories to relieve symptoms. Take sitz baths to reduce pain and swelling. Consult a doctor for advanced treatments if needed."
    },
    "Drug Reaction": {
        "precautions": "Inform healthcare providers of any known drug allergies. Read medication labels carefully. Monitor for any signs of adverse reactions.",
        "actions": "Discontinue the drug and seek medical attention immediately. Follow the treatment plan provided by your healthcare provider. Consider alternative medications if necessary."
    },
    # Add more diseases as needed
}

def predict_disease(l):
    d = {symptom: 0 for symptom in symptoms_list}
    for symptom in l:
        d[symptom] = 1
    new_data_point = pd.DataFrame([d])
    probabilities = model.predict_proba(new_data_point)[0]
    top3_indices = probabilities.argsort()[-3:][::-1]
    top3_diseases = [model.classes_[i] for i in top3_indices]
    top3_probabilities = [probabilities[i] for i in top3_indices]
    return list(zip(top3_diseases, top3_probabilities))

def generate_response(user_input):
    user_input = user_input.lower()
    for disease in disease_info:
        if disease.lower() in user_input:
            info = disease_info[disease]
            return f"**{disease}**\n\n**Precautions:**\n{info['precautions']}\n\n**Actions to Take:**\n{info['actions']}"
    return "I'm here to help with your disease prediction queries. How can I assist you?"

def main():
    st.title("Disease Predictor")
    page = st.sidebar.selectbox("Select a page", ["Home", "About", "Predict"])

    if page == "Home":
        st.header("Welcome to the Disease Predictor")
        st.write("This app predicts diseases based on symptoms.")

    elif page == "About":
        st.header("About")
        st.write("This app provides information about various diseases.")

    elif page == "Predict":
        st.header("Predict Disease")
        st.write("Please select the symptoms:")
        selected_symptoms = st.multiselect("Symptoms", symptoms_list)
        if len(selected_symptoms) < 3:
            st.warning("Please select at least three symptoms to predict.")
        else:
            predictions = predict_disease(selected_symptoms)
            for disease, probability in predictions:
                image_path = f"static/{disease}.jpg".replace(" ", "")
                if os.path.exists(image_path):
                    st.image(image_path, caption=f"{disease} ({probability*100:.2f}% probability)", use_column_width=True)
                st.subheader(disease)
                st.write(disease_about.get(disease, "Information not available"))

    st.markdown(
        """
        <style>
        .chat-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 24px;
            text-align: center;
            cursor: pointer;
            z-index: 1000;
        }
        .chat-window {
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 300px;
            height: 400px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            padding: 10px;
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if "chat_visible" not in st.session_state:
        st.session_state.chat_visible = False

    if st.button("💬", key="chat_button", help="Chat with the assistant"):
        st.session_state.chat_visible = not st.session_state.chat_visible

    if st.session_state.chat_visible:
        st.markdown(
            """
            <script>
            document.querySelector('.chat-window').style.display = 'block';
            </script>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <script>
            document.querySelector('.chat-window').style.display = 'none';
            </script>
            """,
            unsafe_allow_html=True
        )

    if st.session_state.chat_visible:
        st.markdown('<div class="chat-window">', unsafe_allow_html=True)
        st.header("Chatbot")
        st.write("Chat with our assistant to get help with disease predictions.")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        user_input = st.text_input("You: ", key="chat_input")
        if st.button("Send", key="chat_send"):
            if user_input:
                st.session_state.messages.append({"message": user_input, "is_user": True})
                response = generate_response(user_input)
                st.session_state.messages.append({"message": response, "is_user": False})

        for msg in st.session_state.messages:
            st_message(**msg)

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    dataframe1 = pd.read_csv("training_data.csv")
    symptoms_list = list(dataframe1.columns)[:-2]
    disease_about = (
        pd.read_excel("dis_info.xlsx").set_index("disease").to_dict()["about"]
    )
    model = joblib.load("decision_tree.joblib")
    main()
