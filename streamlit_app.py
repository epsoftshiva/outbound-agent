import streamlit as st
from modules import listen_azure 
from modules import speak_text
from modules import getResponse

open_ai_key = st.secrets["OPENAI_API_KEY"]
speech_key = st.secrets["speech_key"]
speech_region = st.secrets["speech_region"]
language = st.secrets["language"]



# Set the page configuration
st.set_page_config(
    page_title="Insurance Sales Agent Training & Evaluation",
    page_icon="📈",
    layout="wide",
)

# Sidebar Logo and Title
st.sidebar.image("images/ep-logo.png.svg", use_column_width=True)  # Replace 'logo.png' with the path to your logo file
st.sidebar.title("ISATE")

# Sidebar Dropdowns
st.sidebar.subheader("Configuration")
call_type = st.sidebar.selectbox(
    "Choose Call Type:", ["First Call", "Second Call", "Closing Call"]
)

character_choice = st.sidebar.selectbox(
    "Choose the Character for AI:", ["Customer", "Agent"]
)

# Main Page Title
st.title("Insurance Sales Agent Training & Evaluation")

# Conditional Input Fields
if character_choice == "Customer":
    st.subheader("Customer Information")
    customer_name = st.text_input("Customer Name:")
    age = st.number_input("Age:", min_value=0, step=1)
    gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
    marital_status = st.selectbox("Marital Status:", ["Single", "Married", "Divorced", "Widowed"])
    children = st.number_input("Number of Children:", min_value=0, step=1)
    occupation = st.text_input("Occupation:")
    location = st.text_input("Location:")

    

elif character_choice == "Agent":
    st.subheader("Agent Objective")
    agent_objective = st.text_area("Enter the Agent's Objective:")
    st.subheader("Customer Information")
    customer_name = st.text_input("Customer Name:")
    age = st.number_input("Age:", min_value=0, step=1)
    gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
    marital_status = st.selectbox("Marital Status:", ["Single", "Married", "Divorced", "Widowed"])
    children = st.number_input("Number of Children:", min_value=0, step=1)
    occupation = st.text_input("Occupation:")
    location = st.text_input("Location:")

    # Display Input Summary for Agent
    

# Add Enter Button
if st.button("Enter"):
    st.success("Information submitted successfully!")


    if character_choice == "Customer" : 
        ai_prompt = f""" You are enacting as a customer named {customer_name}, aged {age}, living in {location}. 
        Your marital status is {marital_status}, and you have {children} children. You work as a {occupation}. 

        The other person is an insurance sales agent calling you to sell an insurance product. Engage in a conversation with them to improve their sales preparedness. 

        You are expected to engage and converse and finally evaluate yourself if you would like to buy the product, or take some time to think about it or if you don't want to buy. 

        You can ask all your objections of why do you need an insurance and so on. """ 

        convo_end_check = f""" You will be provided a conversation history between a propsect and an insurance sales agent. You need to wear the hat of a Prospect in this conversation. 
                                Provide a clear response indicating whether the conversation has been concluded or if the prospect is not willing to take the conversation forward. 
                                The response should be "No" if the conversation is not ended or concluded and "Yes" otherwise """
        
        if gender == "Male" : 
            voice_name = st.secrets["voice_name_male"]
        elif gender == "Female" : 
            voice_name = st.secrets["voice_name_female"]

    elif character_choice == "Agent" : 
        ai_prompt = f"""You are an insurance sales agent preparing for a roleplay scenario. Your name is Samuel from MetLife Insurance. 
        Your objective is : {agent_objective}. The customer details are as follows : 
        1. Customer Name : {customer_name} 
        2. Age : {age}
        3. Marital Status : {marital_status}
        4. Occupation : {occupation}
        5. Numbe of Children : {children}

        Be Polite and try to attain your objective and end the call on a positive note. In case if the customer is not willing, identify ways to engage 
        and have the customer in the pipeline for the next call """ 

        convo_end_check = f""" You will be provided a conversation history between a propsect and an insurance sales agent. You need to wear the hat of a Sales Agent in this conversation. 
                                Provide a clear response indicating whether the conversation has been concluded or if the prospect is not willing to take the conversation forward. 
                                The response should be "No" if the conversation is not ended or concluded and "Yes" otherwise """
        
        voice_name = st.secrets["voice_name_male"]

    
    
    #conversation_history = [{}] 
    conversation_history = [{"role" : "system", "content" : ai_prompt}]
    
    convo_end_check_message = [{"role" : "system", "content" : convo_end_check}]
    
    while True : 

        
        user_input = listen_azure(speech_key=speech_key, speech_region=speech_region, language=language) 
        conversation_history.append({"role" : "user", "content" : user_input})
        
        ai_response = getResponse(api_key=open_ai_key).get_response(message=conversation_history)
        
        speak_text(ai_response, speech_key=speech_key, speech_region=speech_region, voice_name= voice_name)
        conversation_history.append({"role" : "assistant", "content" : ai_response})

        convo_end_check_message.append({"role" : "user", "content" : ai_response})
        end_check = getResponse(api_key=open_ai_key).get_response(message=convo_end_check_message)

        if end_check.lower() == "yes" : 
            speak_text("Closing this exercise : Thank you for using our Platform", speech_key=speech_key, speech_region=speech_region)
            break

      






