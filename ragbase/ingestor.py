from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFium2Loader, UnstructuredEPubLoader
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.vectorstores import VectorStore
from langchain_experimental.text_splitter import SemanticChunker
from langchain_qdrant import Qdrant
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ragbase.config import Config


class Ingestor:
    def __init__(self):
        self.embeddings = FastEmbedEmbeddings(model_name=Config.Model.EMBEDDINGS)
        self.semantic_splitter = SemanticChunker(
            self.embeddings, breakpoint_threshold_type="interquartile"
        )
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2048,
            chunk_overlap=128,
            add_start_index=True,
        )

    def ingest(self, doc_paths: List[Path]) -> VectorStore:
        documents = []
        
        for doc_path in doc_paths:
            loaded_documents = self.GetDocumentLoader(doc_path).load()
            document_text = "\n".join([doc.page_content for doc in loaded_documents])
            documents.extend(
                self.recursive_splitter.split_documents(
                    self.semantic_splitter.create_documents([document_text])
                )
            )
        
        return Qdrant.from_documents(
            documents=documents,
            embedding=self.embeddings,
            path=Config.Path.DATABASE_DIR,
            collection_name=Config.Database.DOCUMENTS_COLLECTION,
            force_recreate=True,
        )
    
    def GetDocumentLoader(self, doc_path: Path) -> BaseLoader:
        match doc_path.suffix:
            case ".pdf":
                return PyPDFium2Loader(doc_path)
            case ".epub":
                return UnstructuredEPubLoader(doc_path)
            case _:
                raise ValueError(f'File {doc_path.name} with type {doc_path.suffix} cannot be loaded.')
