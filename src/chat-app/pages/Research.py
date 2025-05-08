import streamlit as st
import requests
import json
import time

from configs import *

from PIL import Image
image = Image.open("./img/sagemaker.png")
st.image(image, width=80)
st.header("Researcher Agent")
st.caption("Perform research and analysis on customer service conversations.")

conversation = """
Investigate the impact of different training strategies on the performance of large language models in generating coherent and contextually accurate responses. Specifically, examine the effect of the following factors:
The size of the training dataset (small vs. large corpora).
The duration of training (short vs. long training periods).
The use of fine-tuning with domain-specific data (e.g., medical, legal, technical texts).
The architecture of the model (transformer-based vs. other neural architectures).
The implementation of regularization techniques (e.g., dropout, weight decay, early stopping) during training.
Evaluate and compare the models based on their performance in a series of controlled experiments, using metrics like BLEU, ROUGE, F1 score, and human evaluation.
"""

with st.spinner("Retrieving configurations..."):

    all_configs_loaded = False

    while not all_configs_loaded:
        try:
            api_endpoint = get_parameter(key_researchAgent_api_endpoint)
            print(api_endpoint)
            sm_endpoint = get_parameter(key_researchAgent_sm_endpoint)
            print(sm_endpoint)
            all_configs_loaded = True
        except:
            time.sleep(5)

    endpoint_name = st.sidebar.text_input("SageMaker Endpoint Name:",sm_endpoint)
    url = st.sidebar.text_input("API GW Url:",api_endpoint)

    context = st.text_area("Input Context:", conversation, height=300)


    queries = ("Keep the reasoning process in mind and provide a detailed explanation of the steps taken to arrive at the conclusion.",
                "Explain each of the aspects in detail",
                "Provide a summary of the findings",)

    selection = st.selectbox(
        "Select a query:", queries)

    if st.button("Generate Response", key=selection):
        if endpoint_name == "" or selection == "" or url == "":        
            st.error("Please enter a valid endpoint name, API gateway url and prompt!")
        else:
            with st.spinner(f"Wait for it...: {endpoint_name}, {url}"):
                try:
                    prompt = f"{context}\n{selection}"
                    r = requests.post(url,json={"prompt":prompt, "endpoint_name":endpoint_name},timeout=180)
                    data = r.json()
                    print(data)
                    generated_text = data["body"]["generated_text"]
                    generated_thought = data["body"]["thought"]
                    st.write("Thought: ", generated_thought)
                    st.write(generated_text)
                    
                except requests.exceptions.ConnectionError as errc:
                    st.error("Error Connecting:",errc)
                    
                except requests.exceptions.HTTPError as errh:
                    st.error("Http Error:",errh)
                    
                except requests.exceptions.Timeout as errt:
                    st.error("Timeout Error:",errt)    
                    
                except requests.exceptions.RequestException as err:
                    st.error("OOps: Something Else",err)                
                                        
            st.success("Done!")

    query = st.text_area("Input Query:", "What aspect should the client take into account when selecting a training strategy?", height=300)

    if st.button("Generate Response", key=query):
        if endpoint_name == "" or query == "" or url == "":        
            st.error("Please enter a valid endpoint name, API gateway url and query!")
        else:
            with st.spinner("Wait for it..."):
                try:
                    prompt = f"{context}\n{query}"
                    r = requests.post(url,json={"prompt":prompt, "endpoint_name":endpoint_name},timeout=180)
                    data = r.json()
                    generated_text = data["generated_text"]
                    st.write(generated_text)
                    
                except requests.exceptions.ConnectionError as errc:
                    st.error("Error Connecting:",errc)
                    
                except requests.exceptions.HTTPError as errh:
                    st.error("Http Error:",errh)
                    
                except requests.exceptions.Timeout as errt:
                    st.error("Timeout Error:",errt)    
                    
                except requests.exceptions.RequestException as err:
                    st.error("OOps: Something Else",err)                
                                
            st.success("Done!")
        
