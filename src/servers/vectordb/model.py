from pydantic import BaseModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_nomic.embeddings import NomicEmbeddings
from langchain.schema import Document
from typing import List

class VectorSearchInput(BaseModel):
    input: str  # summary from loan_parser

class VectorSearchOutput(BaseModel):
    output: str #List[Document]


class VectorSearch:
    def __init__(self, cnx='Webbase'):
        if cnx=='Webbase':
            self.docs =[]
            self.docs_list=[]
            self.retriever=None        
        elif cnx=='VectorDB':
            raise NotImplementedError('VectorDB not implemented')
        
        else:
            raise NotImplementedError('Other methods not implemented')

    def load_urls(self,urls):
        # Load documents
        self.docs = [WebBaseLoader(url).load() for url in urls]
        self.docs_list = [item for sublist in self.docs for item in sublist]

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=200
        )
        doc_splits = text_splitter.split_documents(self.docs_list)

        # Add to vectorDB
        vectorstore = SKLearnVectorStore.from_documents(
            documents=doc_splits,
            embedding=NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local"),
        )

        # Create retriever
        self.retriever = vectorstore.as_retriever(k=3)
    
    def add_docs(self,new_docs):
        for sublist in new_docs:
            self.docs.append(sublist)
        self.docs_list = [item for sublist in self.docs for item in sublist]
            
