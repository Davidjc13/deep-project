"""
Módulo que usa la API de DeepSeek para el procesamiento de archivos de texto .txt.
La implementación está pensada para un sistema de preguntas y respuestas.

Instrucciones:
    - Guarda los txt en la ruta qa_project/documentos (Puedes organizar por carpeta).
    - Importa la clase QA_System
    - Crea una instancia y usa el método query() para hacer tus consultas

```
from qa_project.core.qa_system import QASystem

qa = QASystem()
result = qa.query("¿Cuál es el tema principal?")
print(result['result'])
```

"""


from typing import Any, Dict, List
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from qa_project.core.config import Config
from qa_project.core.llm import DeepSeekClient

class DocumentProcessor:
    
    def __init__(self):
        self.config = Config()
    
    def load_documents(self) -> List[Any]:
        try:
            loader = DirectoryLoader(
                self.config.DOCUMENTS_DIR,
                glob=self.config.FILE_PATTERN
            )
            return loader.load()
        except Exception as e:
            raise RuntimeError(f"Error loading documents: {str(e)}")
    
    def split_documents(self, documents: List[Any]) -> List[Any]:
        text_splitter = CharacterTextSplitter(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP
        )
        return text_splitter.split_documents(documents)
   

class VectorStoreManager:
    
    def __init__(self):
        self.config = Config()
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.config.EMBEDDING_MODEL
        )
    
    def create_vector_store(self, documents: List[Any]) -> FAISS:
        return FAISS.from_documents(documents, self.embeddings)

class QASystem:
    
    def __init__(self):
        self.config = Config()
        self.vector_store_manager = VectorStoreManager()
        self.document_processor = DocumentProcessor()
        self.llm = DeepSeekClient()
        self.initialize_qa_system()
        self.qa_chain = self._create_qa_chain()
    
    def initialize_qa_system(self):
        documents = self.document_processor.load_documents()
        split_docs = self.document_processor.split_documents(documents)
        self.vector_store = self.vector_store_manager.create_vector_store(split_docs)
        self.qa_chain = self._create_qa_chain()
    
    
    def _create_qa_chain(self) -> RetrievalQA:

        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 5}  # Retornar top 5 documentos
            ),
            return_source_documents=True
        )
    
    def query(self, question: str) -> Dict[str, Any]:
        
        result = self.qa_chain({"query": question})

        for doc in result['source_documents']:
            doc.metadata['score'] = doc.metadata.get('relevance_score', 0.0)
        return result

def main():
    try:
        qa_system = QASystem()
        
        print("Sistema de Q&A listo. Escribe 'salir' para terminar.")
        print("Q&A: Ready. Write `exit` to finish.")

        while True:
            query = input("\nQuestion: ").strip()
            if query.lower() == "exit":
                break
            
            result = qa_system.query(query)
            print(f"\nAnswer: {result['result']}")
            print("\nSources:")
            for doc in result['source_documents']:
                print(f"- {doc.metadata['source']}")
    
    except KeyboardInterrupt:
        print("Cancelled.")
                
    except Exception as e:
        print(f"\nSystem Error: {str(e)}")

if __name__ == "__main__":
    main()