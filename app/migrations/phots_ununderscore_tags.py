"""
Makes all the tags on models un-underscored
"""

def migration(document):
    if "tags" in document:
        tags = document.tags

        un_tags = [ tag.replace("_", " ") for tag in tags ]

        document.tags = un_tags
