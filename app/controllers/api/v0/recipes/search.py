#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
#from seshat.route import route
#from seshat_addons.seshat.mixed_object import MixedObject
#from seshat_addons.seshat.func_mods import JSON

#from utils.paginate import Paginate

#from searchers.recipes import RecipeSearcher


#@route()
#class search(MixedObject):
    #@JSON
    #def GET(self):
        #search_term = self.request.get_param("s")
        #if search_term:
            #search_term = search_term.replace("tag:", "tags:")

            #searcher = RecipeSearcher()
            #hidden_notes = {"disable": False,
                            #"reported": False,
                            #"public": True}
            #ids = searcher.search(search_term, collection=True, pre_filter=hidden_notes)

            #if ids is not None:
                #ids.fetch()

                #page = Paginate(ids, self.request, "title", sort_direction_default="desc")
                #return page

            #return {"page": None, "pail": None}

        #return {"error": "No search (s) term provided."}
