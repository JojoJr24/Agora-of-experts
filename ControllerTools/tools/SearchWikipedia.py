import wikipedia  

def search_wikipedia(topic):
    suggest = wikipedia.suggest(topic)
    if suggest == None:
        suggest = topic

    if(topic):
        try:
            result = wikipedia.summary(suggest, sentences=10)  # Summarizing with 2 sentences for brevity
        except wikipedia.exceptions.PageError:
            result = "No Wikipedia page found for the topic."
        except wikipedia.exceptions.DisambiguationError as e:
            result = f"Multiple pages found for the topic, please specify: {e.options}. Show all the options to the user"
        return result
    return ""

#Es el tipo de datos que lleva el parametro
def search_wikipedia_call():
    return "Use it when you need information about a topic."
