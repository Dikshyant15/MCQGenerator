import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging  

#loading json file
with open(r"D:\GenerativeAI\MCQGenerator\response.json", 'r') as json_file:
    RESPONSE_JSON = json_file.read()

print("Streamlit version:", st.__version__)
#creating the title 
st.title("MCQ generator app with langchain")

#Create an input form using st.form 
with st.form("user_inputs"):
   # file input
   uploaded_file = st.file_uploader("Upload a PDF or text file:")
   
   #input fields 
   mcq_count = st.number_input("Number of MCQs",min_value=3, max_value=50)

   #Subject 
   subject = st.text_input("Insert subject", max_chars=50)

   #Quiz Tone 
   quiz_tone = st.text_input("Complexity level of the question", max_chars=20, placeholder="Simple")

   #Add button
   button = st.form_submit_button("Create a MCQs")


   #check the button is clicked and if the field have input
   if button and uploaded_file is not None and  mcq_count and subject and quiz_tone :
       with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                            'text':text,
                            'number': mcq_count,    
                            'subject': subject,
                            'tone':quiz_tone,
                            'response_json': json.dumps(RESPONSE_JSON) ##json
                        })
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error reading the file")

            else:
                    print(f"Total Tokens:{cb.total_tokens}")
                    print(f"Prompt Tokens:{cb.prompt_tokens}")
                    print(f"Completion Tokens:{cb.completion_tokens}")
                    print(f"Total Cost:{cb.total_cost}")

                    if isinstance(response,dict):
                        quiz = response.get("quiz",None)
                        #converting the quiz into a list
                        if quiz is not None:
                            quiz_list = get_table_data(quiz)
                            if quiz_list is not None:
                            #creating a data frame table 
                                table  = pd.DataFrame(quiz_list)
                                table.index = table.index+1
                                st.table(table)
                                st.text_area(label="Review",value = response["review"])
                            else:
                                st.write(response)


                


