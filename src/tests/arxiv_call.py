from langchain_community.utilities import ArxivAPIWrapper
arxiv = ArxivAPIWrapper()
docs = arxiv.run("What is agentic AI?")
print(docs)