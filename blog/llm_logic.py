"""from django.shortcuts import render
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


CHROMA_DB_DIRECTORY = "chroma_db/docs_builder"
SCRAPER_LINK_LIMIT = 100


def docs_builder():
    root_url = 'https://www.analyticsmania.com/post/google-analytics-4-best-practices/'
    root_response = requests.get(root_url)
    root_html = root_response.content.decode("utf-8")
    soup = BeautifulSoup(root_html, 'html.parser')
    root_url_parts = urlparse(root_url)
    root_links = soup.find_all("a", attrs={"id":"content"})
    result = set()
    for root_link in root_links:
        path = root_link.get('href')
        path = str(Path(path).resolve())
        url = f"{root_url_parts.scheme}://{root_url_parts.netloc}{path}"
        if not url.endswidth("/"):
            url = url + "/"
        result.add(url)
    return list(result)


class CustomWebBaseLoader(WebBaseLoader):
    def _scrape(self, url: str, parser: Union[str, None] = None, bs_kwargs: Optional[dict] = None) -> Any:
        # Fetching the HTML content using the parent class method
        html_content = super()._scrape(url, parser)

        main_tag = html_content.find('div')  # Find the <main> tag
        # return the text in the div tag, parsed by bs4
        return BeautifulSoup(main_tag.text, "html.parser", **(bs_kwargs or {})) # Here we’re overriding the basic scraper to take only the contents from the main tag, with a couple of lines we’re avoiding already a lot of noise that we would otherwise get in the scrape.
    
# Check if the database already exists
def database_exists():
    return os.path.exists(CHROMA_DB_DIRECTORY)

def build_database():
    urls = docs_builder()
    loader = CustomWebBaseLoader(urls)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=0)
    splits = splitter.split_documents(documents)
    # Initialize openAI embeddings
    embeddings = OpenAIEmbeddings()
    # Build Chroma database with the documents already split and embedded.
    db = Chroma.from_documents(
        splits,
        embeddings,
        collection_name="doc_builder",
        persist_directoty=CHROMA_DB_DIRECTORY,

    )
    # DB persist save the data into the database making it available for future use without having to rebuild.
    db.persist()

# Need a function to answer the query after a lookup in the chunk of documents
def answer_query(query):
    # Get vector representationof the user question
    embeddings = OpenAIEmbeddings()
    # Fetch the vector collection to compare against the question
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
        retriever=db.as_retriever(), # Use the chroma DB to check for results
        chain_type_kwargs={"verbose": True}  # Log everything

    )
    result = chain({"question":query}, return_only_outputs=True)
    return result"""