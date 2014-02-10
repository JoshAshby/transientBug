#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from searchers.notes import NoteSearcher
from searchers.phots import PhotSearcher
from rethinkORM import RethinkCollection
from models.rethink.note.noteModel import Note
from models.rethink.phot.photModel import Phot


if __name__ == "__main__":
    searcher = NoteSearcher()

    all_notes = RethinkCollection(Note).fetch()
    searcher.update_multiple(all_notes)
    searcher.save()

    searcher = PhotSearcher()

    all_phots = RethinkCollection(Phot).fetch()
    searcher.update_multiple(all_phots)
    searcher.save()
