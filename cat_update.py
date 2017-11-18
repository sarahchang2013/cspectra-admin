import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Article

#give old category name for search
old_cat_name = "Travel"
#edit new category name here
new_cat_name = "Society"




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

#Search the table for category with the old name
editedCat = session.query(Category).filter_by(name=old_cat_name).one()
editedCat.name = new_cat_name

session.commit()