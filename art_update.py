import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Article

#Edit this section to decide which fields to update
editTitle = False
editSlug = False
editEmbeded = False
editText = False
editCategory = True
#Edit this section and the txt file to update the article
#Enter url inside the embeded code
embeded_code = ''
title = ""
slug = ""
article_id = 9
category_id = 12



engine = create_engine(os.environ.get('CSPECTRA_DATABASE_URL'))

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Update the article

editedArticle = session.query(Article).filter_by(id=article_id).one()
if editTitle:
    editedArticle.title = title
if editSlug:
    editedArticle.slug = slug
if editEmbeded:
    editedArticle.embeded_code = embeded_code
if editText:
    #Store new text in a file with the new slug and read it
    article_file = open (slug+".txt", "r")
    #String was utf-8 encoded, so decode it to store in database
    text=article_file.read().decode('utf-8')
    editedArticle.text = text
if editCategory:
    editedArticle.category_id = category_id

#Must commit the transaction, otherwise the previous operations are not applied.
session.commit()

