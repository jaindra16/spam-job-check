from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI Chat Model
def analyze_sentiments(contents):
    chat_model = ChatOpenAI(
        temperature=0, 
        model="gpt-3.5-turbo", 
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    prompt = PromptTemplate(
        input_variables=["text"],
        template="Classify the following text into Scam, Bad, Average, Good, Legit:\n\nText: {text}"
    )
    llm_chain = LLMChain(llm=chat_model, prompt=prompt)

    sentiments = []
    for content in contents:
        result = llm_chain.run({"text": content})
        sentiments.append(result.strip())
    
    return sentiments

