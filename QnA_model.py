from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
# Load your documents (For simplicity, loading a text file here)

def get_answer(question,conversation_history,context):
#     with open("clean_transcript.txt", "r") as file:
#         document_content = file.read()


    # Create a document object with the content
    # document = Document(page_content=document_content)

    # Create a chat model (You can choose a different LLM model)
    llm = ChatOpenAI(model="gpt-4o")
    n_words = len(context.split())
    # st.write(f"length of words : {n_words}")
    if n_words > 100000:
        error_message= f"Context Length greater than 100k Words"
        raise RuntimeError(error_message) 
    # Define a simple prompt template that includes the document as context
    prompt_template = """You are a helpful assistant. Based on the provided conversation transcript, answer the user's questions.
    REMEMBER: REMEMBER : Do not make up or guess ANY extra information. Make your analysis based only on the context provided.
    '''
    Context: {context}
    Conversation History: {conversation_history}
    Question: {question}
    '''
    """

    # Initialize the prompt with the document content and conversation history
    prompt = PromptTemplate(input_variables=["context", "conversation_history", "question"], template=prompt_template)

    # Create a ConversationChain (this will use the whole document as context)
    # qa_chain = ConversationChain.from_llm(llm, prompt)
    qa_chain= prompt | llm | StrOutputParser()

    answer = qa_chain.invoke({"context": context, "conversation_history": conversation_history, "question": question})

        
    return answer