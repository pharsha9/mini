import streamlit as st
import pandas as pd
import joblib
from streamlit_chat import message as st_message

def predict_disease(l):
    d = {}
    for i in diseases:
        d[i] = 0
    for i in l:
        d[i] = 1
    symptoms = list(d.values())
    new_data_point = pd.DataFrame([symptoms], columns=diseases)
    probabilities = model.predict_proba(new_data_point)[0]
    top3_indices = probabilities.argsort()[-3:][::-1]
    top3_diseases = [model.classes_[i] for i in top3_indices]
    top3_probabilities = [probabilities[i] for i in top3_indices]
    return list(zip(top3_diseases, top3_probabilities))

def generate_response(user_input):
    # Simple example response logic, can be replaced with a more sophisticated chatbot logic
    if "predict" in user_input.lower():
        return "Please select your symptoms from the 'Predict' page."
    else:
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
        selected_symptoms = st.multiselect("Symptoms", diseases)
        if len(selected_symptoms) < 3:
            st.warning("Please select at least three symptoms to predict.")
        else:
            predictions = predict_disease(selected_symptoms)
            for disease, probability in predictions:
                image = f"static/{disease}.jpg".replace(" ", "")
                st.image(image, caption=f"{disease} ({probability*100:.2f}% probability)", use_column_width=True)
                st.subheader(disease)
                st.write(disease_about.get(disease, "Information not available"))

    # Chatbot icon and chat interface
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

    if st.button("💬", key="chat_button", help="Chat with the assistant", use_container_width=True):
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
    diseases = list(dataframe1.columns)[:-2]
    disease_about = (
        pd.read_excel("dis_info.xlsx").set_index("disease").to_dict()["about"]
    )
    model = joblib.load("decision_tree.joblib")
    main()
