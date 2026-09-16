"""
Key Features:
Document Processing: Supports PDFs, text files, directories, and web pages
Chunking: Smart text splitting with overlap
Embeddings: Uses HuggingFace sentence transformers
Vector Store: FAISS for efficient similarity search
LLM Integration: Works with your local Ollama setup
Conversation Memory: Maintains chat history
Source Attribution: Shows which documents were used
"""
from dataclasses import dataclass
from typing import List, Dict

from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    DirectoryLoader,
    WebBaseLoader
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


@dataclass
class RAGConfig:
    """Configuration for RAG pipeline"""
    # Document processing
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Embeddings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_device: str = "cpu"  # or "cuda" for GPU

    # Vector store
    vector_store_path: str = "./vector_store"

    # LLM (using Ollama since you have it locally)
    llm_model: str = "llama3.1"  # or mistral, llama2, etc.
    ollama_base_url: str = "http://localhost:11434"

    # Retrieval
    top_k: int = 4

    # Prompt template
    system_prompt: str = """You are a helpful AI assistant. Use the following context to answer the question.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.

Context: {context}

Question: {question}

Answer:"""


class DocumentProcessor:
    """Handles document loading and chunking"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def load_documents(self, source: str, source_type: str = "directory") -> List:
        """
        Load documents from various sources.

        Args:
            source: Path to file/directory or URL
            source_type: 'file', 'directory', 'pdf', 'web'

        Returns:
            List of documents
        """
        documents = []

        if source_type == "directory":
            loader = DirectoryLoader(source)
            documents = loader.load()

        elif source_type == "file":
            if source.endswith('.pdf'):
                loader = PyPDFLoader(source)
            else:
                loader = TextLoader(source)
            documents = loader.load()

        elif source_type == "pdf":
            loader = PyPDFLoader(source)
            documents = loader.load()

        elif source_type == "web":
            loader = WebBaseLoader(source)
            documents = loader.load()

        print(f"Loaded {len(documents)} documents from {source}")
        return documents

    def split_documents(self, documents: List) -> List:
        """Split documents into chunks"""
        chunks = self.text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        return chunks


class EmbeddingEngine:
    """Handles document embedding creation"""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': device}
        )

    def create_embeddings(self, chunks: List) -> FAISS:
        """Create vector store from document chunks"""
        print("Creating embeddings...")
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        print("Embeddings created successfully")
        return vector_store

    def save_vector_store(self, vector_store: FAISS, path: str):
        """Save vector store to disk"""
        vector_store.save_local(path)
        print(f"Vector store saved to {path}")

    def load_vector_store(self, path: str) -> FAISS:
        """Load vector store from disk"""
        vector_store = FAISS.load_local(
            path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print(f"Vector store loaded from {path}")
        return vector_store


class RAGPipeline:
    """Main RAG pipeline orchestrator"""

    def __init__(self, config: RAGConfig = None):
        self.config = config or RAGConfig()
        self.document_processor = DocumentProcessor(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap
        )
        self.embedding_engine = EmbeddingEngine(
            model_name=self.config.embedding_model,
            device=self.config.embedding_device
        )
        self.vector_store = None
        self.qa_chain = None

        # Initialize Ollama LLM
        self._init_llm()

    def _init_llm(self):
        """Initialize LLM using Ollama"""
        try:
            from langchain_community.llms import Ollama

            self.llm = Ollama(
                model=self.config.llm_model,
                base_url=self.config.ollama_base_url,
                temperature=0.7
            )
            print(f"LLM initialized: {self.config.llm_model}")
        except ImportError:
            raise ImportError("Please install langchain-community: pip install langchain-community")

    def ingest_documents(self, source: str, source_type: str = "directory"):
        """
        Ingest documents into the vector store.

        Args:
            source: Path to documents
            source_type: Type of source
        """
        print("\n=== Starting Document Ingestion ===")

        # Load documents
        documents = self.document_processor.load_documents(source, source_type)

        # Split into chunks
        chunks = self.document_processor.split_documents(documents)

        # Create embeddings and vector store
        self.vector_store = self.embedding_engine.create_embeddings(chunks)

        # Save vector store
        self.embedding_engine.save_vector_store(
            self.vector_store,
            self.config.vector_store_path
        )

        # Create QA chain
        self._create_qa_chain()

        print("=== Document Ingestion Complete ===\n")

    def load_existing_index(self):
        """Load existing vector store from disk"""
        print("\n=== Loading Existing Index ===")
        self.vector_store = self.embedding_engine.load_vector_store(
            self.config.vector_store_path
        )
        self._create_qa_chain()
        print("=== Index Loaded ===\n")

    def _create_qa_chain(self):
        """Create retrieval QA chain"""
        # Custom prompt template
        prompt_template = PromptTemplate(
            template=self.config.system_prompt,
            input_variables=["context", "question"]
        )

        # Create conversation memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": self.config.top_k}
            ),
            chain_type_kwargs={
                "prompt": prompt_template,
                "memory": memory
            }
        )

        print("QA chain created successfully")

    def query(self, question: str) -> Dict:
        """
        Query the RAG pipeline.

        Args:
            question: User's question

        Returns:
            Dictionary with answer and source documents
        """
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Call ingest_documents() or load_existing_index() first.")

        print(f"\nQuery: {question}")

        # Get answer
        result = self.qa_chain({"query": question})

        # Extract relevant documents for source attribution
        docs = self.vector_store.similarity_search(question, k=self.config.top_k)

        response = {
            "question": question,
            "answer": result['result'],
            "sources": [
                {
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                }
                for doc in docs
            ]
        }

        return response

    def batch_query(self, questions: List[str]) -> List[Dict]:
        """Process multiple queries"""
        results = []
        for question in questions:
            result = self.query(question)
            results.append(result)
        return results


def main():
    """Example usage of RAG pipeline"""

    # Configuration
    config = RAGConfig(
        chunk_size=1000,
        chunk_overlap=200,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        embedding_device="cuda",  # Change to "cuda" if you have GPU
        vector_store_path="./vector_store",
        llm_model="llama3.1",  # Make sure this model is pulled in Ollama
        top_k=4
    )

    # Initialize pipeline
    rag = RAGPipeline(config)

    # Option 1: Ingest new documents
    # rag.ingest_documents("./documents", source_type="directory")

    # Option 2: Load existing index
    try:
        rag.load_existing_index()
    except FileNotFoundError:
        print("No existing index found. Please ingest documents first.")
        return

    # Interactive query loop
    print("\n=== RAG Query System ===")
    print("Type 'quit' to exit\n")

    while True:
        question = input("Your question: ").strip()

        if question.lower() in ['quit', 'exit', 'q']:
            break

        if not question:
            continue

        try:
            result = rag.query(question)

            print("\n" + "=" * 60)
            print("ANSWER:")
            print("=" * 60)
            print(result['answer'])

            print("\n" + "-" * 60)
            print("SOURCES:")
            print("-" * 60)
            for i, source in enumerate(result['sources'], 1):
                print(f"\n{i}. {source['metadata'].get('source', 'Unknown')}")
                print(f"   {source['content']}")

            print("\n" + "=" * 60)

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
