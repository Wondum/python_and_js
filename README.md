# Capstone Publishing
### Table of Contents
1. [Introduction](#introduction)
2. [Techonology and Justification](#techonology-and-justification)
3. [Web Application pages](#web-application-pages)
4. [Source Code](#source-code)
    * [Javascript](#javascript)
    * [CSS](#css)
    * [HTML](#html)
    * [Python with Django framework](#python-with-django-framework)

## Introduction

*Capstone Publishing* is a final project for CS50’s Web Programming with Python and JavaScript. The application helps authors to maintain their articles. The project also has admin pages to set magazine's title and the minimum "number of reads" each article needs for a 5-star grading.

## Techonology and Justification

*Capstone Publishing* is a Django based python project that uses HTML, CSS, Javascript, Python, Bootstrap and Django Web framework. The project is unique in the way it uses a dynamic star-rating system and column based article display. It uses a common javascript code to dynamically return one or all articles and also have a maintainance page that lets you choose existing articles and change their content. It also lets the user add list of tags and magazine title. The filtering approach helps to categorise articles bases on their rating or tag name.

The project covers all the topics in the course by using *javasript* to view articles and the whole magazine preview. The Javascript component uses *fetch* to get data from database.

*HTML* and *CSS* is used to maintain and manage the articles. Python together with *Django* framework is used to create Models, implement business logic and unit test the applciation.

The models are related by Foreign key constraints and also use Unique constraint. The *Unit Test* covers the all models by creating sample data and asserting the expected and actual data.

# Web Application pages

## Index page

*Index Page* lists article's title, tag, author, 5 star review, number of reads and synopsis from all authors.

## Author's Articles

*Author's Article* (*Wondu's Articles* for example) only lists the current user's articles.

## Maintain Article

*Maintain Article* page is used to add new Articles or update/delete existing ones. You can add/update Title, Tags, Synopsis, Article Content, Headline picture location URL and Article Column Size. The "Existing Articles" drop down box at the top of the page lets you switch between articles. This page only displayes the current user's articles.

## Manage Resources

Manage Resources is a page to setup

* *Magazine Settings*: the magazine's title and the minimum number of reads needed to get 5 star review. If the minimum read you expect for a 5-star is 15, then 3 reads will be needed for each star. If the minimum read you expect for a 5-star is 100, then 20 reads will be needed for each star. Read counts between starts is represented by a half-star. For example in the 15 read setup, an article read 7 times gets 2 and half start.

* *Tag*: To add and delete tags that is going to be used to group articles.

## Preview Magazine

*Preview Magazine* show a publish ready list of articles based on the "Magazine Title" in *Manage Resources* and "Article Column Size" set for each article.

## Filter

The application uses tags, 5-star review, and author's page to filter search results.

1. An article can have one or more tags and clicking on a tag will let you filter index page to list articles matching the tag.
2. 5-star review lets you display the results matching the 5-star review based on the number of reads. For example Clicking on a 2-star will display all 2-star artciles and clicking on a 3 and half star will display all ratings between 3-star and 4-star.
3. The Author's page lets you see articles authored by the current user while the index page shows articles by all authors.

## Log Out

*Log Out* lets the user log out of current session.

# Source Code

## Javascript
[publish.js](https://github.com/Wondum/python_and_js/blob/capstone/capstone/static/capstone/publish.js): Javascript code to dynamically create HTML page for displaying individual articles and entire magazine according to the column setting in *Maintain Article* page.

## CSS
[styles.css](https://github.com/Wondum/python_and_js/blob/capstone/capstone/static/capstone/styles.css): CSS code to set the look and feel of web pages.

## HTML

HTML code includes bootstrap framework to display user friendly error/success messages and various HTML elements

1. [index.html](https://github.com/Wondum/python_and_js/blob/capstone/capstone/templates/capstone/index.html): HTML code to list the articles with their title, star rating, number of reads, author name and synopsis.
2. [layput.html](https://github.com/Wondum/python_and_js/blob/capstone/capstone/templates/capstone/layout.html): HTML code to display the menu to navigate between web pages.
3. [login.html](https://github.com/Wondum/python_and_js/blob/capstone/capstone/templates/capstone/login.html): HTML code for login page.
4. [maintain_article.html](https://github.com/Wondum/python_and_js/blob/capstone/capstone/templates/capstone/maintain_article.html): HTML code to add, update, and delete article details.
5. [manage_resource.html](https://github.com/Wondum/python_and_js/blob/capstone/capstone/templates/capstone/manage_resource.html): HTML code to set magazine details and maintain tags.
6. [preview_article.html](https://github.com/Wondum/python_and_js/blob/capstone/capstone/templates/capstone/preview_article.html): HTML code to display individual articles or whole magazine using *publish.js* javascript code.
7. *register.html*: HTML code to register new authors.

## Python with Django framework

### [models.py](https://github.com/Wondum/python_and_js/blob/capstone/capstone/models.py) : Django models for the application
* *User*: a model inheriting from Django AbstractUser class.
* *Tag*: a model for all the tags in the application.
* *Article*: a model to store article data. It has a foreigk key reference to * *User* model.
* *Articletotag*: a models that stores tags associated with each article.

### [tests.py](https://github.com/Wondum/python_and_js/blob/capstone/capstone/tests.py): unit test python code using Django TestCase involving all models in the application.

### [views.py](https://github.com/Wondum/python_and_js/blob/capstone/capstone/views.py): main python code that has all the functions for the application logic
* to register, login , logout authors
* to star-rate, tag, maintain article and manage resource
* to fetch articles and return JSON data suitable for javascript processing
* to render request to display article, magazine and any error or success messages


