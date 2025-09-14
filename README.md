# RagBase - Private Chat with Your Documents

> Completely local RAG with chat UI

<a href="https://www.mlexpert.io/bootcamp" target="_blank">
  <img src="https://raw.githubusercontent.com/mnuzzose/ragbase/master/.github/ui.png">
</a>

## Demo

Check out the [RagBase on Streamlit Cloud](https://ragbase.streamlit.app/). Runs with Groq API.

## Prerequisites

Pandoc needs to be installed for EPub parsing.



## Installation

Clone the repo:

```sh
git clone git@github.com:mnuzzose/ragbase.git
cd ragbase
```

Install the dependencies (requires Poetry):

```sh
poetry install
```

Fetch your LLM (deepseek-r1:7b by default):

```sh
ollama pull deepseek-r1:7b
```

Run the Ollama server

```sh
ollama serve
```

Start RagBase:

```sh
poetry run streamlit run app.py
```

## Architecture

<a href="https://www.mlexpert.io/bootcamp" target="_blank">
  <img src="https://raw.githubusercontent.com/curiousily/ragbase/master/.github/architecture.png">
</a>

### Ingestor

Extracts text from PDF documents and creates chunks (using semantic and character splitter) that are stored in a vector databse

### Retriever

Given a query, searches for similar documents, reranks the result and applies LLM chain filter before returning the response.

### QA Chain

Combines the LLM with the retriever to answer a given user question

## Tech Stack

- [Ollama](https://ollama.com/) - run local LLM
- [Groq API](https://groq.com/) - fast inference for mutliple LLMs
- [LangChain](https://www.langchain.com/) - build LLM-powered apps
- [Qdrant](https://qdrant.tech/) - vector search/database
- [FlashRank](https://github.com/PrithivirajDamodaran/FlashRank) - fast reranking
- [FastEmbed](https://qdrant.github.io/fastembed/) - lightweight and fast embedding generation
- [Streamlit](https://streamlit.io/) - build UI for data apps
- [PDFium](https://pdfium.googlesource.com/pdfium/) - PDF processing and text extraction

## Add Groq API Key (Optional)

You can also use the Groq API to replace the local LLM, for that you'll need a `.env` file with Groq API key:

```sh
GROQ_API_KEY=YOUR API KEY
```