import os
import requests
import json
from dotenv import load_dotenv
import openai
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chat_models import ChatOpenAI
import streamlit as st


def load_configurations():
    load_dotenv()
    config = {
        "serp_api_key": os.getenv("SERP_API_KEY"),
        "openai_api_key": os.getenv("OPENAI_API_KEY")
    }
    openai.api_key = config["openai_api_key"]
    return config


def search(query, api_key):
    url = "https://google.serper.dev/search"
    payload = json.dumps({'q': query})
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()


def get_best_articles(res_json, query):
    res_str = json.dumps(res_json)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.4)
    template = """
    You are a professional researcher and tech expert. 
    Given the topic "{res_str}", the following are the search results for the query "{query}". 
    Please sift through these and choose the best 3 articles that are most relevant and informative on the topic. 
    Only include the links to these articles and return them as an array. 
    It's crucial that you return ONLY the links in the array and nothing else.
    """
    prompt = PromptTemplate(input_variables=["res_str", "query"], template=template)
    top_article_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    urls = top_article_chain.predict(res_str=res_str, query=query)
    url_list = json.loads(urls)
    return url_list


def extract_content_from_urls(url_list):
    loader = UnstructuredURLLoader(urls=url_list)
    data = loader.load()

    return data


def summarise(data, query):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=3000, chunk_overlap=200, length_function=len)
    text = text_splitter.split_documents(data)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.4)
    template = """
        {text}

        You are a tech expert with the challenge of succinctly summarising the above content. 
        Your goal is to distill its main points into a brief summary that will form the foundation of an engaging 
        Instagram post about {query}. The summary should be concise, to the point, 
        and capture the essence of the content. 

        Summary:
        """
    prompt = PromptTemplate(input_variables=["text", "query"], template=template)
    summariser_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    summaries = []

    for text_chunk in enumerate(text):
        summary = summariser_chain.predict(text=text_chunk, query=query)
        summaries.append(summary)

    print(summaries)
    return summaries


def generate_instagram_post(summaries, query):
    summaries_str = str(summaries)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    template = """
        {text}
        You are an esteemed tech journalist, 
        and you're tasked with summarising the content above to create a compelling Instagram post about {query}. 
        To make this post impactful and draw the attention of coding enthusiasts worldwide, 
        please adhere to these guidelines:
        1) Ensure the content is captivating and packed with valuable insights.
        2) Limit the summary to fit a single Instagram post, making sure it's concise yet informative.
        3) Tailor the content to address the {query} topic profoundly.
        4) Craft the post in a manner that resonates with coding aficionados globally, 
        aiming to garner significant engagement.
        5) Make sure the text is lucid, easily digestible, and free from jargons.
        6) Offer readers actionable advice and unique insights related to the topic.
        7) End the post with 5 relevant hashtags optimised for Instagram's algorithm and SEO to maximise visibility.

        Note: Ensure the hashtags align with the global coding community's interests 
        and are popular among Instagram's tech circles.

        Instagram Post:
        """

    prompt = PromptTemplate(input_variables=["text", "query"], template=template)
    instagram_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    instagram_post = instagram_chain.predict(text=summaries_str, query=query)

    return instagram_post


def main():
    st.title("Tech Article Summariser")

    query = st.text_input("Enter your query:", "Tesla full self-driving 2023")

    if st.button("Generate Summary"):
        st.write("Searching for articles...")

        config = load_configurations()
        search_results = search(query, config["serp_api_key"])
        articles_url = get_best_articles(search_results, query)
        articles_text = extract_content_from_urls(articles_url)
        summaries = summarise(articles_text, query)

        st.write("Generating Instagram post...")
        instagram_post = generate_instagram_post(summaries, query)
        st.write(instagram_post)


st.sidebar.title("About")
st.sidebar.info("This is a Streamlit app that uses OpenAI to summarise tech articles and generate an Instagram post.")


if __name__ == "__main__":
    main()
