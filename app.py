import streamlit as st
import spacy
import speech_recognition as sr

# Load spaCy model 
nlp = spacy.load("en_core_web_sm")

# Configure Streamlit page
st.set_page_config(page_title="spaCy Chatbot", layout="centered")
st.title("Simple Chatbot with spaCy")
st.markdown("Ask anything and get a response based on basic NLP analysis.")

# Initialize chat history 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#. Speech recognition function 
r = sr.Recognizer()

def transcribe_speech():
    #Listen to microphone and return transcribed text.
    with sr.Microphone() as source:
        st.info("Speak now...")
        audio_data = r.listen(source)
        st.info("Transcribing...")
    try:
        text = r.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand you."
    except sr.RequestError:
        return "Speech recognition service is unavailable."

# Chatbot response function 
def generate_response(user_input):
    doc = nlp(user_input)

    # Location entities
    locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
    if locations:
        return f"I see you're talking about {', '.join(locations)}. What's happening there?"

    # Money entities
    if any(ent.label_ == "MONEY" for ent in doc.ents):
        return "Sounds like you're talking about money. Want to discuss finance?"

    # Default fallback
    return "I'm just a simple bot, but I'm listening!"

# . Input choice: Voice or Text
input_method = st.radio("Choose input method:", ("Type", "Speak"))

if input_method == "Type":
    user_input = st.text_input("You:", key="text_input")
    if st.button("Send", key="send_text"):
        if user_input.strip():
            response = generate_response(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", response))

elif input_method == "Speak":
    if st.button("Start Talking"):
        user_input = transcribe_speech()
        st.session_state.chat_history.append(("You", user_input))
        response = generate_response(user_input)
        st.session_state.chat_history.append(("Bot", response))

# Display chat history 
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")