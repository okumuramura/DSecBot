import wikipedia

wikipedia.set_lang("ru")

def set_lang(lang):
    wikipedia.set_lang(lang)

def summary(query):
    #return wikipedia.page(wikipedia.search(query)[0])
    search = wikipedia.search(query)
    if len(search) > 0:
        return (wikipedia.summary(search[0]), wikipedia.page(search[0]))
    return None