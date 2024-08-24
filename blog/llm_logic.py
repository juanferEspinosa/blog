from django.shortcuts import render
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
import requests
import os
from urllib.parse import urlparse
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from typing import Union, Optional, Any


CHROMA_DB_DIRECTORY = "chroma_db"
SCRAPER_LINK_LIMIT = 100


def docs_builder():
    root_url = 'https://getbootstrap.com/docs/5.3/getting-started/contents/'
    root_response = requests.get(root_url)
    root_html = root_response.content.decode("utf-8")
    soup = BeautifulSoup(root_html, 'html.parser')
    root_url_parts = urlparse(root_url)
    root_links = soup.find_all(
        "a", attrs={"class": "bd-links-link d-inline-block rounded"})
    result = set()
    counter = 0
    for root_link in root_links:
        if counter >= SCRAPER_LINK_LIMIT:
            break
        path = root_link.get('href')
        path = str(Path(path).resolve())
        path = urlparse(path).path
        url = f"{root_url_parts.scheme}://{root_url_parts.netloc}{path}"
        if not url.endswidth("/"):
            url = url + "/"
        result.add(url)
    return list(result)


class CustomWebBaseLoader(WebBaseLoader):
    def _scrape(self, url: str, parser: Union[str, None] = None, bs_kwargs: Optional[dict] = None) -> Any:
        # Fetching the HTML content using the parent class method
        html_content = super()._scrape(url, parser)

        main_tag = html_content.find('div')  
        # return the text in the div tag, parsed by bs4
        return BeautifulSoup(main_tag.text, "html.parser", **(bs_kwargs or {})) # Here we’re overriding the basic scraper to take only the content we want.
    
# Check if the database already exists
def database_exists():
    return os.path.exists(CHROMA_DB_DIRECTORY)

def build_database():
    urls = docs_builder()
    loader = CustomWebBaseLoader(urls)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=2)
    splits = splitter.split_documents(documents)
    # Initialize openAI embeddings
    embeddings = OpenAIEmbeddings()
    # Build Chroma database with the documents embedded.
    db = Chroma.from_documents(
        splits,
        embeddings,
        collection_name="doc_builder",
        persist_directoty=CHROMA_DB_DIRECTORY,

    )
    # DB persist save the data into the database making it available for future use.
    db.persist()
    print(f"Saved {len(splits)} chunks to {CHROMA_DB_DIRECTORY}.")


def answer_query(query):
    # Get vector representation of user question
    embeddings = OpenAIEmbeddings()
    # Get own embedding to apply similarity
    db = Chroma(
        collection_name="doc_builder",
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_DIRECTORY
    )

    chat = ChatOpenAI(temmperature=0)
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        # type of GPT version -- gtp3.5
        llm=chat,
        chain_type="stuff",
        #Checking chroma DB to see results
        retriever=db.as_retriever(),
        chain_type_kwargs={"verbose": True}  # Log

    )
    result = chain({"question":query}, return_only_outputs=True)
    return result