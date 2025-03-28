# FAQ System 🚀

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green)
![LangChain](https://img.shields.io/badge/LangChain-0.0.201+-orange)

A contextual FAQ system using Retrieval-Augmented Generation (RAG). It utilizes DeepSeek model as the LLM

## Features ✨
- **Documents processing** 
- **Semantic search** with MPNet embeddings
- **Answer generation**
- **RESTful API** with FastAPI
- Automatic documentation (Swagger/Redoc)
- Supports multiple documents
- Scalability with FAISS (Vectorial storage)

## Requirements 📋
- Python 3.10+
- [DeepSeek](https://deepseek.com/)'s API Key 

## Set Up ⚙️

```bash
# 1. Clone repository
git clone https://github.com/tu-usuario/qa-rag-system.git
cd qa-rag-system

# 2. Create a virtual environment (Conda or Venv)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
```

# Document set up 📂

This system is designed to work with plain text (`TXT`) documents. Below is a detailed guide on how to configure
and organize the documents for optimal results. 

## Directory structure

```
documents/
    └── ia/
        ├── etica_ia.txt
        ├── historia_ia.txt
        └── redes_neuronales.txt
```

## Documents requirements
1. **Format**: Plain text files (`.txt`)
2. **Encoding**: UTF-8
3. **Recomended size**: Between 500 and 5000 words per document.
4. **Structure**: Continuous text or clearly separated paragraphs

### Example
`documents/ia/etica_ia.txt`

```
Los principales desafíos éticos en IA incluyen:

    Sesgos algorítmicos: Los modelos pueden perpetuar prejuicios presentes en los datos de entrenamiento.

    Privacidad: La recolección y uso de datos personales plantea riesgos significativos.

    Desplazamiento laboral: La automatización podría afectar ciertos empleos.

La UE propuso en 2023 regulaciones específicas para sistemas de IA de alto riesgo.
```


## How to add new documents
1. Create a new plain text `.txt` and save it to `documents/`
2. Use subdirectories to organize in topics (opcional)
3. Ensure the content is properly formated.

## Automatic Process
The system:
- Automaticly detect new files
- Splits content in optimal chunks
- Generate embeddings for each segment
- Index the documents for quick searchs

## Good practices
- **Clear titles**: Use self-descriptive names for each document
- **Reliable source**: Use verified sources
- **Regular update**: Keep documents updated
- **Metadata**: Include dates and references in documents

## Use examples

In Python:
```python
from core.qa_system import QASystem

qa = QASystem()
result = qa.query("¿Qué regulación propuso la UE?")
print(result['answer'])
```

# 🚀 How to use Q&A API 

This system allows you to ask questions and receive answers based on previously processed documents.

---

## 🏁 Start the API

To start this API, use the following command:

```bash
uvicorn api.main:app --reload
```
API will be located in `http://localhost:8000`.

# 🔍 Peform a query

# 📡 Via cURL

You can ask the system using a POST request with curl:
```bash
curl -X POST "http://localhost:8000/ask" \
-H "Content-Type: application/json" \
-d '{"question": "¿Qué regulación propuso la UE?", "max_sources": 2}'
```

# 🌐 Ussing Swagger UI

You can test this API directly from the interactive docs in:
➡️ `http://localhost:8000/docs`

