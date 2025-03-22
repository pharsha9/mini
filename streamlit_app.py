import streamlit as st
import pandas as pd
import joblib
from streamlit_chat import message as st_message
import os
import time
import google.generativeai as genai

# Gemini API Key (Hardcoded - FOR DEVELOPMENT PURPOSES ONLY.  NEVER DO THIS IN PRODUCTION)
GEMINI_API_KEY = "AIzaSyBb14-qC2cEIwn8UG0No6Cno8_99p7TDxA"  # Replace with your actual API key.  DANGEROUS!

# Initialize Gemini
def initialize_gemini():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        st.error(f"Error initializing Gemini: {e}.  Check your API key.")
        return None

def generate_response(gemini_model, user_input):
    if not gemini_model:
        return "Gemini is not initialized.  Please check the API key in the code."

    # PROMPT ENGINEERING:  This is the key addition.
    prompt = f"""You are a helpful and informative AI assistant specializing in health-related topics.
    You should ONLY provide information related to diseases, symptoms, prevention, and general health advice.
    If the user asks a question that is not related to health, politely decline to answer.

    When a user asks about a specific disease, provide information about:
    - Precautions they can take.
    - Preventive measures they can take.
    - General information about the disease.

    User question: {user_input}
    """

    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

def main():
    st.title("Disease Predictor and Chatbot")
    page = st.sidebar.selectbox("Select a page", ["Home", "About", "Predict"])

    gemini_model = initialize_gemini()

    if page == "Home":
        st.header("Welcome to the Disease Predictor and Chatbot")
        st.write("This app predicts diseases based on symptoms and allows you to chat with an AI assistant about health-related topics.")

    elif page == "About":
        st.header("About")
        st.write("This app combines a disease prediction model with the  AI to provide information and answer questions about health.")

    elif page == "Predict":
        st.header("Predict Disease")
        st.write("Please select the symptoms:")
        dataframe1 = pd.read_csv("training_data.csv")
        symptoms_list = list(dataframe1.columns)[:-2]
        disease_about = (
        pd.read_excel("dis_info.xlsx").set_index("disease").to_dict()["about"]
        )
        model = joblib.load("decision_tree.joblib")
        selected_symptoms = st.multiselect("Symptoms", symptoms_list)
        if len(selected_symptoms) < 3:
            st.warning("Please select at least three symptoms to predict.")
        else:
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
        st.write("Ask me anything about diseases, symptoms, or general health advice.")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Use a unique key for the text input each time
        user_input = st.text_input("You: ", key=f"chat_input_{len(st.session_state.messages)}")  # Unique key

        if st.button("Send", key=f"chat_send_{len(st.session_state.messages)}"): # unique key for the button
            if user_input:
                st.session_state.messages.append({"message": user_input, "is_user": True})
                response = generate_response(gemini_model, user_input)
                st.session_state.messages.append({"message": response, "is_user": False})

        # Display messages using a unique key for each message
        for i, msg in enumerate(st.session_state.messages):
            st_message(**msg, key=f"msg_{i}") # Unique key for each message

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
