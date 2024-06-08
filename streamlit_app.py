import streamlit as st
import pandas as pd
import joblib
from streamlit_chat import message as st_message
import os

# Define disease information
disease_info = {
    "Benign Paroxysmal Positional Vertigo": {
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
    "Fungal Infection": {
        "precautions": "Keep affected areas clean and dry. Avoid sharing personal items like towels and razors. Wear breathable, loose-fitting clothing.",
        "actions": "Use antifungal creams or medications as prescribed. Maintain good hygiene practices. Consult a doctor if the infection persists or worsens."
    },
    "Gastroenteritis": {
        "precautions": "Practice good hand hygiene to prevent the spread of infection. Avoid consuming contaminated food or water. Ensure proper food handling and preparation.",
        "actions": "Stay hydrated by drinking plenty of fluids. Rest and avoid solid foods until symptoms improve. Consult a doctor if symptoms are severe or prolonged."
    },
    "GERD": {
        "precautions": "Avoid foods and beverages that trigger symptoms. Eat smaller, more frequent meals. Avoid lying down immediately after eating.",
        "actions": "Take antacids or other medications as prescribed. Elevate the head of your bed to reduce nighttime symptoms. Consult a gastroenterologist for further evaluation and treatment."
    },
    "Heart Attack": {
        "precautions": "Maintain a healthy diet and exercise regularly. Avoid smoking and limit alcohol consumption. Monitor and manage blood pressure and cholesterol levels.",
        "actions": "Seek emergency medical help immediately if experiencing symptoms. Take prescribed medications and follow the treatment plan. Participate in cardiac rehabilitation programs."
    },
    "Hepatitis A": {
        "precautions": "Get vaccinated against hepatitis A. Practice good hand hygiene, especially before eating. Avoid consuming contaminated food or water.",
        "actions": "Rest and avoid alcohol to reduce liver strain. Follow a healthy diet and stay hydrated. Consult a doctor for further evaluation and treatment."
    },
    "Hepatitis B": {
        "precautions": "Get vaccinated against hepatitis B. Practice safe sex and avoid sharing needles. Ensure proper sterilization of medical equipment.",
        "actions": "Take antiviral medications as prescribed. Monitor liver function regularly. Consult a hepatologist for ongoing management."
    },
    "Hepatitis C": {
        "precautions": "Avoid sharing needles and personal items. Practice safe sex. Ensure proper sterilization of medical equipment.",
        "actions": "Take antiviral medications as prescribed. Monitor liver function regularly. Consult a hepatologist for ongoing management."
    },
    "Hepatitis D": {
        "precautions": "Get vaccinated against hepatitis B to prevent co-infection. Avoid sharing needles and personal items. Practice safe sex.",
        "actions": "Take antiviral medications as prescribed. Monitor liver function regularly. Consult a hepatologist for ongoing management."
    },
    "Hepatitis E": {
        "precautions": "Ensure proper sanitation and hygiene practices. Avoid consuming contaminated food or water. Practice good hand hygiene.",
        "actions": "Rest and avoid alcohol to reduce liver strain. Follow a healthy diet and stay hydrated. Consult a doctor for further evaluation and treatment."
    },
    "Hypertension": {
        "precautions": "Maintain a healthy diet low in salt and saturated fats. Exercise regularly and maintain a healthy weight. Monitor blood pressure regularly.",
        "actions": "Take antihypertensive medications as prescribed. Reduce stress through relaxation techniques. Consult a doctor for regular check-ups and management."
    },
    "Hyperthyroidism": {
        "precautions": "Avoid iodine-rich foods if advised by your doctor. Monitor thyroid hormone levels regularly. Manage stress through relaxation techniques.",
        "actions": "Take antithyroid medications as prescribed. Consider radioactive iodine therapy or surgery if recommended. Consult an endocrinologist for ongoing management."
    },
    "Hypoglycemia": {
        "precautions": "Monitor blood glucose levels regularly. Eat regular meals and snacks to maintain stable blood sugar levels. Avoid excessive alcohol consumption.",
        "actions": "Consume fast-acting carbohydrates like glucose tablets or juice if experiencing symptoms. Seek medical help if symptoms persist or worsen. Consult a doctor for proper management."
    },
    "Hypothyroidism": {
        "precautions": "Take thyroid hormone replacement medication as prescribed. Monitor thyroid hormone levels regularly. Maintain a balanced diet and exercise regularly.",
        "actions": "Follow the prescribed treatment plan. Consult an endocrinologist for regular check-ups. Manage symptoms through a healthy lifestyle."
    },
    "Impetigo": {
        "precautions": "Maintain good personal hygiene. Avoid close contact with infected individuals. Keep wounds clean and covered.",
        "actions": "Use prescribed antibiotics to treat the infection. Keep affected areas clean and dry. Consult a doctor if the infection spreads or worsens."
    },
    "Jaundice": {
        "precautions": "Avoid alcohol and hepatotoxic drugs. Maintain a healthy diet to support liver function. Monitor liver function regularly.",
        "actions": "Seek medical evaluation to determine the underlying cause. Follow the prescribed treatment plan. Stay hydrated and rest."
    },
    "Malaria": {
        "precautions": "Avoid mosquito bites by using repellents and wearing protective clothing. Use mosquito nets and screens in living areas. Take antimalarial medications if traveling to high-risk areas.",
        "actions": "Seek medical help immediately if experiencing symptoms. Take prescribed antimalarial medications. Follow the treatment plan and complete the full course of medication."
    },
    "Migraine": {
        "precautions": "Identify and avoid known triggers. Maintain a regular sleep schedule and stay hydrated. Manage stress through relaxation techniques.",
        "actions": "Take prescribed medications to alleviate symptoms. Rest in a dark, quiet room during an attack. Consult a doctor for ongoing management and preventive treatments."
    },
    "Osteoarthritis": {
        "precautions": "Maintain a healthy weight to reduce joint stress. Stay active with low-impact exercises. Avoid repetitive joint strain.",
        "actions": "Take pain relievers and anti-inflammatory medications as prescribed. Engage in physical therapy to improve joint function. Apply hot or cold compresses to affected joints."
    },
    "Paralysis (Brain Hemorrhage)": {
        "precautions": "Manage risk factors such as hypertension and diabetes. Avoid smoking and excessive alcohol consumption. Follow a healthy lifestyle to reduce stroke risk.",
        "actions": "Seek immediate medical help if experiencing symptoms. Follow a rehabilitation program to regain function. Consult a neurologist for ongoing management."
    },
    "Peptic Ulcer Disease": {
        "precautions": "Avoid NSAIDs and aspirin. Limit alcohol consumption and avoid smoking. Eat a balanced diet and avoid spicy foods.",
        "actions": "Take prescribed medications to reduce stomach acid. Follow a healthy diet and avoid trigger foods. Consult a gastroenterologist for ongoing management."
    },
    "Pneumonia": {
        "precautions": "Practice good hand hygiene to prevent infection. Get vaccinated against pneumococcal pneumonia and flu. Avoid close contact with sick individuals.",
        "actions": "Take prescribed antibiotics to treat bacterial pneumonia. Rest and stay hydrated. Follow the treatment plan and seek medical help if symptoms worsen."
    },
    "Psoriasis": {
        "precautions": "Keep skin moisturized and avoid triggers. Use gentle skin care products. Avoid excessive sun exposure.",
        "actions": "Use prescribed topical treatments to manage symptoms. Consider phototherapy or systemic medications if needed. Consult a dermatologist for ongoing management."
    },
    "Tuberculosis": {
        "precautions": "Avoid close contact with individuals with active TB. Practice good respiratory hygiene. Ensure proper ventilation in living areas.",
        "actions": "Take prescribed medications for the full course of treatment. Follow the treatment plan and attend regular check-ups. Consult a doctor for ongoing management."
    },
    "Typhoid": {
        "precautions": "Practice good hand hygiene and avoid contaminated food and water. Get vaccinated if traveling to high-risk areas. Ensure proper sanitation and hygiene practices.",
        "actions": "Take prescribed antibiotics to treat the infection. Stay hydrated and rest. Follow the treatment plan and seek medical help if symptoms worsen."
    },
    "Urinary Tract Infection": {
        "precautions": "Maintain good personal hygiene. Stay hydrated and urinate regularly. Avoid irritants like harsh soaps and douches.",
        "actions": "Take prescribed antibiotics to treat the infection. Drink plenty of fluids to flush out bacteria. Consult a doctor if symptoms persist or worsen."
    },
    "Varicose Veins": {
        "precautions": "Avoid prolonged standing or sitting. Maintain a healthy weight and exercise regularly. Elevate legs to reduce pressure.",
        "actions": "Wear compression stockings to improve circulation. Follow a healthy lifestyle to manage symptoms. Consult a doctor for advanced treatments if needed."
    }
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

    st.text_area("User Input", key="user_input")
    if st.button("Send", key="send_button"):
        user_input = st.session_state.user_input
        response = generate_response(user_input)
        st_message("user", user_input, key="user_message")
        st_message("bot", response, key="bot_response")

if __name__ == "__main__":
    dataframe1 = pd.read_csv("training_data.csv")
    symptoms_list = list(dataframe1.columns)[:-2]
    disease_about = (
        pd.read_excel("dis_info.xlsx").set_index("disease").to_dict()["about"]
    )
    model = joblib.load("decision_tree.joblib")
    main()
