import os
from tavily import TavilyClient

def search_web_tavily(query):
    api_key=os.environ.get("TAVILY_API_KEY")
    tavily = TavilyClient(api_key=api_key)
    search_resolve = tavily.search(query=query)
    
    
    results = f""" This is the information about the query topic. Show the user the name, write a summary and a list of url as reference:
    
    {search_resolve}
    """
    return results


#Es el tipo de datos que lleva el parametro
def search_web_tavily_call():
    return "Use it when you need to search the web for information about a topic."

def search_web_tavily_name():
    return "search_web_advance"

# Example usage:
if __name__ == "__main__":
    query = "current Nvidia share price"
    results = search_web_tavily(query)
    print(results)

