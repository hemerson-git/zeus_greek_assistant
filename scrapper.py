import wikipedia

def searchOnWiki(query):
    wikipedia.set_lang('pt')
    page = wikipedia.page(query)
    print(page.summary)