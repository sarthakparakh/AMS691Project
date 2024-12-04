import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from langchain_community.document_loaders import PyPDFium2Loader

def load_document(file_path: str) -> str:
    """
    Loads a document from the given file path.
    """
    loaded_documents = PyPDFium2Loader(file_path).load()
    document_text = "\n".join([doc.page_content for doc in loaded_documents])

    return document_text

def generate_wordcloud(text: str):
    """
    This function generates a word cloud from the given text.
    """
    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    # Display the generated word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Hide axes
    plt.show()

def main():

    document_path = 'data\student_profiles\AMS_691_Kushagra_Agarwal_docs.pdf'
    document_text = load_document(document_path)
    
    # Generate and display the word cloud from the text
    generate_wordcloud(document_text)

if __name__ == "__main__":
    main()
