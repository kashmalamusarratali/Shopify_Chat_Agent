import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai.llms import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma

# =========================
# ENV SETUP
# =========================
load_dotenv(override=True)

api_key = os.getenv("Gemini_key")
os.environ["GOOGLE_API_KEY"] = api_key

# =========================
# CONFIG
# =========================
VECTOR_DB_PATH = "data/store"
DATA_PATH = "data"

embedding = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    api_key=api_key
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# =========================
# BUILD VECTOR STORE
# =========================
def build_vector_store():
    loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.txt",
        loader_cls=TextLoader
    )

    docs = loader.load()

    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=VECTOR_DB_PATH
    )

    db.persist()
    print("✅ Vector store built and saved.")


# =========================
# LOAD VECTOR STORE
# =========================
def load_vector_store():
    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embedding
    )


# =========================
# RAG ANSWER FUNCTION
# =========================
def rag_answer(query: str):
    db = load_vector_store()

    docs = db.similarity_search(query, k=3)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
    Answer ONLY using the provided context.
    If answer is not in context, say "I'm sorry, but I could not find that information Please drop your query at abc@abc.com".

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)

    return response.content


