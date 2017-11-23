import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from database_setup import Category, Base, Article




#Edit this section and the txt file
category_of_article = "Science and Technology"
embeded_code = 'https://www.youtube.com/embed/2Y7xjAcmQQc'
title = "Why North Korea's Nuclear Problems are Hard to Resolve"
slug = "why-north-koreas-nuclear-problems-are-hard-to-resolve"

#Text field was set to be nullable, so if no text exists, 
#just copy and paste the title in the text file.
#Store text in a file and read it
article_file = open ("new_article.txt", "r")
#String was utf-8 encoded, so decode it to store in database
text=article_file.read().decode('utf-8')

###############Code here, don't edit#################

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

# Check if category exists, if not, create one.
check_c = session.query(exists().where(Category.name == category_of_article)).scalar()
if not check_c :
    category1 = Category(name=category_of_article)
    session.add(category1)
    session.commit()

#check if article exists, if not, create one.
check_a = session.query(exists().where(Article.title == title)).scalar()
#Ad new article
if not check_a :
    category1 = session.query(Category).filter_by(name=category_of_article).first()
    article1 = Article(title=title, slug=slug,embeded_code=embeded_code, text=text, category=category1, category_id=category1.id)
    session.add(article1)
    session.commit()

