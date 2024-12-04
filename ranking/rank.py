import os
import json
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


def create_chat_groq_model():
    """
    Initializes the ChatGroq model using the ragbase configuration.
    Replace with your actual configuration setup.
    """
    return ChatGroq(
        model_name="llama-3.1-70b-versatile",
        temperature=0,
        max_tokens=1000,
        groq_api_key = "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"
    )


def generate_response_from_llm(prompt: str, chat_groq: ChatGroq) -> str:
    """
    Generates a response from the local LLM based on the user prompt and the vector store.
    """

    # prompt_with_context = f"Context:\n{context}\n\nAnswer the following question:\n{prompt}"


    # # Create the prompt template and LLM chain
    # prompt_template = PromptTemplate(input_variables=["prompt"], template=prompt_with_context)
    # llm_chain = LLMChain(llm=chat_groq, prompt=prompt_template)

    # Get the response from the LLM
    # response = llm_chain.run({"prompt": prompt})

    response = chat_groq.invoke(prompt)
    response = response.content

    return response


def save_response_to_json(response: str, filename: str):
    """
    Parse the string response, extract the JSON part, and save it to a JSON file.
    """
    try:
        start_index = response.find("{")  # Find the starting index of the JSON part
        end_index = response.find("}") + 1

        json_str = response[start_index:end_index].strip()

        # Parse the JSON string into a dictionary
        parsed_json = json.loads(json_str)

        # Save the response to a valid JSON file path
        json_file_path = f"data/rank/{filename}.json"
        with open(json_file_path, "w") as json_file:
            json.dump(parsed_json, json_file, indent=4)
            print(f"Response saved to {json_file_path}")

    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error while parsing JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def read_json_files_from_folder(folder_path):
    # Initialize an empty string to store the combined content
    profiles_context = ""
    
    # List all files in the specified folder
    for filename in os.listdir(folder_path):
        # Check if the file is a JSON file based on its extension
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            # Open and read the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    # Read the content as a JSON object and then convert it to a string
                    json_data = json.load(file)
                    json_string = json.dumps(json_data)  # Convert JSON data back to string
                    # Append the string to the main string
                    profiles_context += f"\nStudent name is {filename[:-5]} \n"
                    profiles_context += json_string + "\n"  # Adding newline for separation
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file {filename}")
    
    return profiles_context

def rank():
        # Create a local LLM instance (ChatOllama)
    chat_groq = create_chat_groq_model()

    # student profiles combined in a single text file to pass on as a context
    profiles_context = read_json_files_from_folder("data/response")

    # Get the user prompt and generate a response
    
    rank_prompt = f"""
    The string JSON of student profiles is provided below with the name of each student.
    {profiles_context}

    For each of the student profiles provided, calculate the final score.
    The formula to calculate the final score of each profile is given below.

    Final_score_formula = 0.1*GRE + 0.1*IELTS + 0.15*GPA + 0.1*YOE + 0.05*Number_of_certifications + 
                0.05*Extra_curricular_score + 0.15*Awards&Recognition + 0.05*Leadership_Score + 
                0.05*Clarity_and_coherence + 0.05*Relevance_to_Computer_Science_program + 
                0.05*Credibility_of_recommender + 0.05*Future_potential + 0.05*Character_traits

    Return the response in three parts-
    First, the json format with the student name as the key and final score as value and sort the json key value pairs in descending order of the score value.
    Second, show the individual category scores for each student.
    Third, compare and explain the ranking of each student. Explaination for each student should 
    be less than 200 words.
    
    Other things to remember:
        If some keys are missing, try to find relevant information from the data only, otherwise assign 
        0 value to such keys during calculation.

        Please do not add comments in the response as it is a JSON format response.

        For all the values, return only the final value after performing all the calculations.
    """
    
    response = generate_response_from_llm(rank_prompt, chat_groq)

    # Print the response
    print("Response from the model:\n", response)

    # Save the parsed JSON response to a file
    save_response_to_json(response, "rank")
    

def main():

    # Create a local LLM instance (ChatOllama)
    '''chat_groq = create_chat_groq_model()

    # student profiles combined in a single text file to pass on as a context
    profiles_context = read_json_files_from_folder("data/response")

    # Get the user prompt and generate a response
    
    rank_prompt = f"""
    The string JSON of student profiles is provided below with the name of each student.
    {profiles_context}

    For each of the student profiles provided, calculate the final score.
    The formula to calculate the final score of each profile is given below.

    Final_score_formula = 0.1*GRE + 0.1*IELTS + 0.15*GPA + 0.1*YOE + 0.05*Number_of_certifications + 
                0.05*Extra_curricular_score + 0.15*Awards&Recognition + 0.05*Leadership_Score + 
                0.05*Clarity_and_coherence + 0.05*Relevance_to_Computer_Science_program + 
                0.05*Credibility_of_recommender + 0.05*Future_potential + 0.05*Character_traits

    Return the response in three parts-
    First, the json format with the student name as the key and final score as value.
    Second, show the individual category scores for each student.
    Third, compare and explain the ranking of each student. Explaination for each student should 
    be less than 200 words.
    
    Other things to remember:
        If some keys are missing, try to find relevant information from the data only, otherwise assign 
        0 value to such keys during calculation.

        Please do not add comments in the response as it is a JSON format response.

        For all the values, return only the final value after performing all the calculations.
    """
    
    response = generate_response_from_llm(rank_prompt, chat_groq)

    # Print the response
    print("Response from the model:\n", response)

    # Save the parsed JSON response to a file
    save_response_to_json(response, "rank")'''


if __name__ == "__main__":
    #main()
    rank()


"""
Categories and Their Possible Weights-

Academic Profile (e.g., CGPA, degree relevance): 20%
Technical Skills: 20%
Certifications: 10%
Extra-Curricular Activities: 10%
Awards & Recognition: 15%
Achievements: 10%
Leadership Experience: 10%
Character Traits: 5%
Recommendation (Credibility, LOR match, etc.): 5%



Example Calculation for the Given Profile-

CGPA: 3.556 out of 4 (score: 8/10)
Technical Skills: 21 skills (score: 8/10)
Certifications: 8 certifications (score: 8/10)
Extra-Curricular Activities: 5 activities (score: 8/10)
Awards & Recognition: 5 awards (score: 8/10)
Achievements: 3 achievements (score: 8/10)
Leadership Experience: 3 roles (score: 8/10)
Character Traits: Positive traits (score: 9/10)
Recommendation: Strong recommendation (score: 9/10)

"""


"""

score_matrix = 0.1*GRE + 0.1*English_score + 0.15*GPA + 0.1*YOE + 0.05*Number_of_certifications + 
               0.05*Extra_curricular_score + 0.15*Awards&Recognition + 0.05*Leadership_Score + 
               0.05*Clarity_and_coherence + 0.05*Relevance_to_Computer_Science_program + 
               0.05*Credibility_of_recommender + 0.05*Future_potential + 0.05*Character_traits

"""

