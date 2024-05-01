from duckduckgo_search import DDGS

def search_web(query):
    results = f""" This is a list of sites with information about the topic. Show the user the name, the href and a description:
    
    {DDGS().text(query, max_results=10)}
    """
    return results


#Es el tipo de datos que lleva el parametro
def search_web_call():
    return "Use it when you need to search the web for information about a topic."

def search_web_name():
    return "search_web"

# Example usage:
if __name__ == "__main__":
    query = "current Nvidia share price"
    results = search_web(query)
    print(results)
