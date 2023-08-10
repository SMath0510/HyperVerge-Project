import streamlit as st
import openai

# OpenAI Reference to the API : https://platform.openai.com/docs/api-reference/images/createVariation?lang=python
# Link to my assignment : https://hyperverge.notion.site/AI-Engineer-Assignment-5aacf787c41f4e7ea96524e53520f7c2

# Setting my my API key here
# openai.api_key = "YOUR_API_KEY" # Need a valid API Key

#When the user wants us to generate the question for him 
def generate_question(language, concept, blooms_level, user_level):
    initialize_prompt = "You are an expert programming teacher."
    prompt = initialize_prompt + f"Give me a question on the topic : {concept} in the language : {language}. My current level is : {user_level} and my goal is to : {blooms_level}."

    response = openai.ChatCompletion.create(
        model="text-davinci-003",
        messages=[
            {"role": "user", "content": prompt}
        ]   
    )
    
    question = response.choices[0].message  
    return question 


#Generating the AI Response to our answer.
def generate_ai_response(chat_history):
    prompt_to_summarize = "Give me a feedback on my recent responses using one of the three words\n 1. Not Accepted \n 2. Satisfactory \n 3. Proficient"
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use other engines as well
        prompt=chat_history + prompt_to_summarize,
        max_tokens=50
    )
    return response.choices[0].text.strip()

def main():
    st.title("Programming Learning Assistant")

    #Getting to know the requirements
    language = st.selectbox("Select Language", ["JavaScript", "Python", "C++"])
    concept = st.selectbox("Select Concept", ["Basics", "Variables", "Loops", "If-Else", "Functions"])
    blooms_level = st.selectbox("Select Bloom's Level", ["Create", "Evaluate", "Analyze", "Apply", "Understand", "Remember"])
    user_level = st.selectbox("Select Your Current Level in the topic", ["Beginner", "Moderate", "Well-Experienced"])
    
    #Initializing the boxes
    chat_history = st.text_area("Chat History", value="", height=150)
    print(chat_history)
    latest_student_response = st.text_input("Your Latest Response", "")
    
    #Buttom triggers
    if st.button("Generate Question"):
        question = generate_question(language, concept, blooms_level, user_level)
        updated_chat_history = chat_history + f"\nSystem: {question}"
        chat_history = updated_chat_history
        st.write("Generated Question:", question)
        

    if st.button("Generate AI Response"):
        updated_chat_history = chat_history + f"\nStudent: {latest_student_response}"
        ai_response = generate_ai_response(updated_chat_history)
        chat_history = updated_chat_history
        updated_chat_history = chat_history + f"\nSystem: {ai_response}"
        chat_history = updated_chat_history
        st.write("AI Response:", ai_response)

    

if __name__ == "__main__":
    main()
