import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
# from langchain.callbacks import get_openai_callback
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Use os.path.join for cross-platform compatibility
json_path = os.path.join(current_dir, 'Response.json')

# Open the file using the relative path
with open(json_path, 'r') as file:
    RESPONSE_JSON = json.load(file)

#creating a title for the app
st.title("MCQs Creator Application with LangChain 🦜⛓️")

#Create a form using st.form
with st.form("user_inputs"):
    #File Upload
    uploaded_file=st.file_uploader("Uplaod a PDF or txt file")

    #Input Fields
    mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=50)

    #Subject
    subject=st.text_input("Insert Subject",max_chars=20)

    # Quiz Tone
    tone=st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    #Add Button
    button=st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
                #Count tokens and the cost of API call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                        "text": text,
                        "number": mcq_count,
                        "subject":subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                            }
                    )
                #st.write(response)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        print("Raw quiz response:", quiz)
                        try:
                            table_data = get_table_data(quiz)
                            if table_data:
                                df = pd.DataFrame(table_data)
                                df.index = df.index + 1
                                st.table(df)
                                st.text_area(label="Review", value=response["review"])
                            else:
                                st.error("Failed to process quiz data into table format")
                                st.write("Raw response:", response)
                        except Exception as e:
                            st.error(f"Error processing quiz data: {str(e)}")
                            print("Full error:", traceback.format_exc())
                    else:
                        st.error("No quiz data found in response")
                else:
                    st.error("Unexpected response format")
                    st.write(response)