from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Article
import os

app = Flask(__name__)

engine = create_engine(os.environ.get('CSPECTRA_DATABASE_URL'))
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def homePage():
	#Print index.html with URLs to add new, update or delete articles
	return render_template('index.html')


@app.route('/articles/JSON')
def articlesJSON():
	articles = session.query(Article).all()
	return jsonify(Articles=[i.serialize for i in articles])

@app.route('/add-new-article', methods=['GET','POST'])
def newArticle():
	if request.method == 'POST':
		#Retrieve form data
		title = request.form['title']
		slug = request.form['slug']
		embeded_code = request.form['embeded_code']
		text = request.form['text']
		category_of_article = request.form['category_name']
		#Check if article exists, if not, create one.
		check_a = session.query(exists().where(Article.title == title)).scalar()
		#Add new article if title not found.
		if not check_a :
			# Check if category exists, if not, create one.
			check_c = session.query(exists().where(Category.name == category_of_article)).scalar()
			if not check_c :
				category1 = Category(name=category_of_article)
				session.add(category1)
				session.commit()
		#Add new article to database
		category1 = session.query(Category).filter_by(name=category_of_article).first()
		article1 = Article(title=title, slug=slug,embeded_code=embeded_code, text=text, category=category1, category_id=category1.id)
		session.add(article1)
		session.commit()
		return render_template('index.html')
	else:
		return render_template('newArticle.html')


@app.route('/update-article', methods=['GET', 'POST'])
def updateArticle():
	if request.method == 'POST':
		#Retrieve form data
		article_id = request.form['article_id']
		title = request.form['title']
		slug = request.form['slug']
		embeded_code = request.form['embeded_code']
		category_id = request.form['category_id']
		text = request.form['text']
		#Query article with article_id
		editedArticle = session.query(Article).filter_by(id=article_id).one()
		if title:
			editedArticle.title = title
		if slug:
			editedArticle.slug = slug
		if embeded_code:
			editedArticle.embeded_code = embeded_code
		if text:
			editedArticle.text = text
		if category_id:
			editedArticle.category_id = category_id
		#Must commit the transaction, otherwise the previous operations are not applied.
		session.commit()
		return render_template('index.html')
	else:
		return render_template("updateArticle.html")


@app.route('/update-category', methods=['GET', 'POST'])
def updateCategory():
	if request.method == 'POST':
		#Retrieve form data
		old_cat_name = request.form['old_cat_name']
		new_cat_name = request.form['new_cat_name']
		#Search the table for category with the old name
		editedCat = session.query(Category).filter_by(name=old_cat_name).one()
		editedCat.name = new_cat_name
		session.commit()
		return render_template('index.html')
	else:
		return render_template('updateCategory.html')


@app.route('/delete-article', methods=['GET', 'POST'])
def deleteArticle():
	if request.method == 'POST':
		#Retrieve form data:
		article_id = request.form['article_id']
		articleToDelete = session.query(Article).filter_by(id=article_id).one()
		session.delete(articleToDelete)
		session.commit()
		return render_template('index.html')
	else:
		return render_template('deleteArticle.html')

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)