import os
from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv
from langchain.memory.buffer import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pydantic import BaseModel


from prompt import qa_template
import uvicorn
from PyPDF2 import PdfReader
from fastapi.responses import RedirectResponse
from typing import List

load_dotenv()


app = FastAPI(debug=True, title="Memorizer", version="0.0.1")

embedding_function = OpenAIEmbeddings()


def pdfs_to_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(".temp_faiss_index")

def get_context(query):
    embeddings = OpenAIEmbeddings()
    new_db = FAISS.load_local(".temp_faiss_index", embeddings, allow_dangerous_deserialization=True)
    return new_db.similarity_search(query)

def get_qa_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain, memory


@app.get('/')
def root():
    return RedirectResponse(url='/docs', status_code=301)

@app.post("/upload/")
async def context(files: List[UploadFile] = File(...)):
    try:
            combined_text = ""
            # Read the file
            for file in files:
                combined_text += pdfs_to_text(file.file)
            text_chunks = get_text_chunks(combined_text)
            get_vectorstore(text_chunks)
            # qa_chain, memory = get_qa_chain(vectorstore)
            # print(qa_chain)
    except Exception as e:
        return {"ERROR": str(e)}
    



@app.post("/ask/")
async def conversation(query: dict ):
    llm = ChatOpenAI(
        temperature=0.3,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
    )
    prompt = PromptTemplate(
        input_variables=["context", "question"], template=qa_template
    )
    context = get_context(query["question"])
    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(context=context, question=query)

    return {"answer": response}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)