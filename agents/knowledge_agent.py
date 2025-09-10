import os
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Load your API key from the .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Create a variable to hold the path to your knowledge base
knowledge_base_path = "../knowledge_base/doc.text"

# This is the main function of your agent
def get_solution_proposal(requirements):
    # 1. Load the knowledge base documents
    loader = TextLoader(knowledge_base_path)
    documents = loader.load()

    # 2. Split the documents into small, searchable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # 3. Create a way to search the knowledge base
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectorstore = Chroma.from_documents(documents=texts, embedding=embeddings)

    # 4. Define the prompt for the AI model
    prompt_template = """You are a senior solutions architect. Your task is to design a technical solution based on the client requirements.
    Based on the following knowledge and the client's needs, create a detailed solution proposal.
    Format your response as a JSON object with the following keys: "proposal_text", "services", and "connections".
    The "services" key should be a list of the key cloud services, and "connections" should be a list of lists showing how they connect.
    
    Knowledge:
    {context}
    
    Client Requirements:
    {question}
    
    JSON Proposal:
    """
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    
    # 5. Connect the knowledge base to the AI model
    llm = ChatOpenAI(temperature=0, openai_api_key=api_key)
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT}
    )

    # 6. Get the AI's answer
    response = qa_chain.invoke({"query": requirements})
    
    # Try to parse the JSON output
    try:
        json_output = json.loads(response['result'])
        return json_output
    except json.JSONDecodeError:
        # Fallback if the AI doesn't return a perfect JSON
        return {"proposal_text": response['result'], "services": [], "connections": []}

# This is a test section to run the code
if __name__ == "__main__":
    test_requirements = "Design a low-cost, scalable web application for a small startup using AWS."
    print("Asking the Knowledge Agent to create a proposal...")
    proposal = get_solution_proposal(test_requirements)
    print("\n--- Generated Proposal from Knowledge Agent ---")
    print(json.dumps(proposal, indent=2))