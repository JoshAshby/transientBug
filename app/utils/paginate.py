#!/usr/bin/env python
"""
helper files for generating pagination from a list of objects

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""


def pager(pail, perpage, page, sort_dir=""):
    """
    Creates a pager for pail

    :param pail: A list of items to paginate
    :param perpage: An int or string of "all" for how many results per page
    :param page: An int or string for which page the pager is on
    :param sort_dir: The direction to sort, asc or desc
    """
    page_dict = {
        "perpage": perpage,
        "dir": sort_dir
        }

    if sort_dir == "asc":
        pail.sort(reverse=True)
    elif sort_dir == "desc":
        pail.sort()

    if perpage != "all":
        page_dict["show"] = True

        perpage = int(perpage)
        page = int(page)

        offset_start = (perpage * page)
        offset_end = offset_start + perpage

        page_dict["next"] = page + 1
        page_dict["prev"] = page - 1

        if page != 0:
            page_dict["hasPrev"] = True
        else:
            page_dict["hasPrev"] = False

        if len(pail) > offset_end:
            page_dict["hasNext"] = True
        else:
            page_dict["hasNext"] = False

        pail = pail[offset_start:offset_end]

    return pail, page_dict
