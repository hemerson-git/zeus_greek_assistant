import wikipedia

def searchOnWiki(query):
    wikipedia.set_lang('pt')
    try:
        page = wikipedia.page(query)
        return page.title, page.summary
    except:
        return None, None