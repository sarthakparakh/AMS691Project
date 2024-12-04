import os
import json
from langchain_community.document_loaders import PyPDFium2Loader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel

def load_document(file_path: str) -> str:
    """
    Loads a document from the given file path.
    """
    loaded_documents = PyPDFium2Loader(file_path).load()
    document_text = "\n".join([doc.page_content for doc in loaded_documents])

    return document_text

def create_chat_groq_model():
    """
    Initializes the ChatGroq model using the ragbase configuration.
    Replace with your actual configuration setup.
    """
    return ChatGroq(
        model_name="llama-3.1-70b-versatile",  # Specify the model name (e.g., "gpt-3.5-turbo" or similar)
        temperature=0,  # Adjust temperature if needed
        max_tokens=700,  # Adjust max tokens for your use case
        groq_api_key = "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"
    )

def create_local_llm() -> BaseLanguageModel:
    """
    Initializes and returns the local LLM (ChatOllama) instance.
    """
    return ChatOllama(
        model="gemma2:9b",
        temperature=0.0,
        keep_alive="1h",
        max_tokens=8000,
    )

def create_embeddings() -> FastEmbedEmbeddings:
    """
    Initializes and returns the FastEmbedEmbeddings instance.
    """
    return FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")

def create_vector_db(documents: list, student_profile: str) -> Qdrant:
    """
    Creates a vector store (Qdrant) and returns the vector database.
    """
    embeddings = create_embeddings()
    vector_db = Qdrant.from_documents(
        documents=documents,
        embedding=embeddings,
        path='data/embeddings',
        collection_name=f"document_collection_{student_profile}"
    )
    return vector_db

def generate_response_from_llm(prompt: str, document_text: str, chat_groq: ChatGroq) -> str:
    """
    Generates a response from the local LLM based on the user prompt and the vector store.
    """
    context = document_text

    # Perform similarity search on the vector database
    # search_results = vector_db.similarity_search([prompt], k=8)  # Get top 3 similar results
    # print(search_results)

    # Format the retrieved documents to create a prompt
    # context = "\n".join([result.page_content for result in search_results])
    prompt_with_context = f"Context:\n{context}\n\nAnswer the following question:\n{prompt}"

    # Create the prompt template and LLM chain
    prompt_template = PromptTemplate(input_variables=["prompt"], template=prompt_with_context)
    llm_chain = LLMChain(llm=chat_groq, prompt=prompt_template)

    # Get the response from the LLM
    response = llm_chain.run({"prompt": prompt})
    return response


def save_response_to_json(response: str, student_profile_name: str):
    """
    Parse the string response, extract the JSON part, and save it to a JSON file.
    """
    try:
        # Extract the JSON part from the response (inside the triple backticks)
        # start_index = response.find("```")  # Find the starting index of the JSON part
        # end_index = response.rfind("```")  # Find the ending index of the JSON part
        
        # # Get the raw JSON string
        # json_str = response[start_index:end_index].strip()

        # Parse the JSON string into a dictionary
        parsed_json = json.loads(response)

        # Save the response to a valid JSON file path
        json_file_path = f"data/response/{student_profile_name}.json"
        with open(json_file_path, "w") as json_file:
            json.dump(parsed_json, json_file, indent=4)
            print(f"Response saved to {json_file_path}")

    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error while parsing JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def read_pdf_files_from_folder(folder_path):
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


def process_student_profiles(filename: str):

    #for filename in os.listdir(folder_path):
    #document_path = os.path.join(folder_path, filename)
    document_path = filename
    print(f"Processing document: {document_path}")

    # Load the document text
    document_text = load_document(document_path)
    student_profile_name = document_path[30:-9]

    # Create the LLM instances (Local LLM and ChatGroq)
    local_llm = create_local_llm()
    chat_groq = create_chat_groq_model()

    # Get the user prompt for generating a response
    user_prompt = """
        Answer the following questions in JSON format from the student's profile:

        1. CGPA (decimal)
        2. Education degree experience - (bachelor's, master's, PhD)
        3. Previous degree major - (Computer Science?, Computer Engineering?)
        4. Total number of years of IT Industry experience - (Decimal)
        5. Total Number of certifications present - (Decimal)
        6. Technical skills - (list of skills)
        7. Extra-curricular activities - (list of activities)
        8. Awards and recognition - (list and count)
        9. Achievements - (count the number of achievements based on its impact. E.g., increased sales by 10%)
        10. Count the number of times a person has led teams or projects.
        11. Which degree does the person's profile fit in? (Computer Science, Computer Engineering, Data Science, etc.)
        12. Clarity and coherence - according to the Clarity of Purpose, Logical Flow, etc. (Decimal Score out of 10)
        13. Relevance to Computer Science program (Decimal Score out of 10)
        14. Personal motivation?
        15. Clear Short-term and Long-term goals?
        16. Conclusion and final impressions?
        17. Leadership skills - (List of skills)
        18. Achievement while working with the professor? (list)
        19. Character traits - (List)
        20. Credibility of the recommender - (Eg. Dean vs Professor vs Associate professor)
        21. Does LOR match with SOP and Resume? (Yes or No)
        22. Future potential - Discussed or not?
        23. Length of relationship with the recommender?

        Other things to remember:
        Please do not add comments in the response as it is a JSON format response.
        For all the values, return only the final value after performing all the calculations.
    """
    print(user_prompt)
    response = generate_response_from_llm(user_prompt, document_text, chat_groq)

    # Print and save the response
    print(f"Response from the model for {student_profile_name}:\n", response)
    save_response_to_json(response, student_profile_name)

def main():
    # Load the document from the provided path

    '''folder_path='data/student_profiles/'
    for filename in os.listdir(folder_path):

        
        document_path = os.path.join(folder_path, filename)
        print(document_path)
        document_text = load_document(document_path)

        student_profile_name = document_path[30:-9]

        # Create a local LLM instance (ChatOllama)
        local_llm = create_local_llm()
        chat_groq = create_chat_groq_model()

        # # Embed the document
        # recursive_splitter = RecursiveCharacterTextSplitter(
        #         chunk_size=2048,
        #         chunk_overlap=128,
        #         add_start_index=True,
        #     )

        # recursive_chunks = recursive_splitter.split_text(document_text)
        # splits = [Document(page_content=chunk) for chunk in recursive_chunks]
        
        # # Store documents in the vector database (Qdrant)
        # vector_db = create_vector_db(splits, student_profile_name)
        # print("Vector db created!")

        # Get the user prompt and generate a response
        user_prompt = """
            Answer the following questions in JSON format from the student's profile:

            1. CGPA (decimal)
            2. Education degree experience - (bachelor's, master's, PhD)
            3. Previous degree major - (Computer Science?, Computer Engineering?)
            4. Total number of years of IT Industry experience - (Decimal)
            5. Total Number of certifications present - (Decimal)
            6. Technical skills - (list of skills)
            7. Extra-curricular activities - (list of activities)
            8. Awards and recognition - (list and count)
            9. Achievements - (count the number of achievements based on its impact. E.g., increased sales by 10%)
            10. Count the number of times a person has led teams or projects.
            11. Which degree does the person's profile fit in? (Computer Science, Computer Engineering, Data Science, etc.)
            12. Clarity and coherence -  according to the Clarity of Purpose, Logical Flow, etc. (Decimal Score out of 10)
            13. Relevance to Computer Science program (Decimal Score out of 10)
            14. Personal motivation ?
            15. Clear Short-term and Long-term goals ?
            16. Conclusion and final impressions ?
            17. Leadership skills - (List of skills)
            18. Achievement while working with the professor? (list)
            19. Character traits - (List)
            20. Credibility of the recommender - (Eg. Dean vs Professor vs Associate professor)
            21. Does LOR match with SOP and Resume? (Yes or No)
            22. Future potential - Discussed or not?
            23. Length of relationship with the recommender?

            Other things to remember:
            Please do not add comments in the response as it is a JSON format response.
            For all the values, return only the final value after performing all the calculations.
            """
        print(user_prompt)
        response = generate_response_from_llm(user_prompt, document_text, chat_groq)

        # Print the response
        print("Response from the model:\n", response)

        # Save the parsed JSON response to a file
        save_response_to_json(response, f"{student_profile_name}")'''

if __name__ == "__main__":
    folder_path = 'data/student_profiles/'  # Path to the folder containing student profiles
    process_student_profiles(folder_path)

   #main()
