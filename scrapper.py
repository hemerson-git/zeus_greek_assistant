import wikipedia

def searchOnWiki(query, section, searchType = 'page'):
    wikipedia.set_lang('pt')
    try:
        page = wikipedia.page(query, None, True)

        if searchType == 'page':
            return page.title, page.summary
        
        if searchType == 'section':
            page = wikipedia.page(query, None, True)
            return page.title, page.section(section)
    except:
        return None, None