#for helper function
import os
import PyPDF2
import json
import traceback

# reading the input file format 

#for PDF files 
def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)

            num_pages = pdf_reader.pages
            text = ''
            for page in num_pages:
                # Extract text from the page
                page_text = page.extractText()
                
                # Append the extracted text to the overall text
                text += page_text
        except:
            raise Exception ("Error reading the file")
    elif file.name.endswith(".txt"):
        return file.read().decode('utf-8')
    else:
         raise Exception ("Only pdf and text supported")
    

#converting the generated quiz to a list of dictionary 
def get_table_data(quiz):
    try:
        #json -> dictionary
        quiz_data = []
        #converting json to dictionary 
        quiz_dict = json.load(quiz)
        
        for key,value in quiz_dict.items():
            questions = value["mcq"]

            options = "|".join
            (
                [f"{option_key}: {option_value}"
                for option_key,option_value in value["options"].items()   
                ]
            )
            correct = value["correct"]
            quiz_data.append({"mcq":questions,"options":options,"correct":correct})
        return quiz_data
    except:
        raise Exception("Failed to create a table")