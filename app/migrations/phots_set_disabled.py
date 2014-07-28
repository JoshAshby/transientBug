"""
Makes sure all the phots have a disabled attribute on them.
"""

def migration(document):
    if not "disabled" in document:
        document.disabled = False
