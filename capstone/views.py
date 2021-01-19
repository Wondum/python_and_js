from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count,F
from django.http import JsonResponse
import json, math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .models import User, Tag, Article, Articletotag, Magazine

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")

def article_decorated(articles):
    articles_final=[]
    for a in articles:
        art_tag_list=[]
        art_tags = Articletotag.objects.filter(article_obj=a)
        tag_list=[]
        for t in art_tags:
            tag_list.append(t.tag_obj.tag_name)
        art_dict = {"id": a.id, "article_by": a.article_by.username, "title": a.title, "synopsis": a.synopsis, "publish_date": a.publish_date, "content": a.content
                    , "read_count": a.read_count, "article_picture": a.article_picture, "article_column": a.article_column}
        
        art_dict["tag_list"]=tag_list

        maga = Magazine.objects.all()
        if maga:
            m = maga[0].five_star_count
        else:
            m=5
        read_count_setting = int(round((m/5),0))*5
        i=a.read_count
        j= read_count_setting/5
        
        star_list=[]
        for t in range(5):
            if a.read_count > read_count_setting:
                star_list.append(t)
            else:
                if i>0 and i<j:
                    star_list.append('y')
                    i=i-j
                elif i>0:
                    star_list.append(t)
                    i=i-j
                else:
                    star_list.append('x')
        art_dict["star_list"]=star_list
        articles_final.append(art_dict)
    
    return articles_final
    
def index(request):
    error=""
    if request.user.is_authenticated:
        
        tags = Tag.objects.all().order_by("tag_name")
        articles = Article.objects.all().order_by("publish_date").reverse()
        articles_final= article_decorated(articles)
        
        return render(request, "capstone/index.html",{
        "articles": articles_final,
        "error": error
    })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def author(request):
    error=""
    if request.user.is_authenticated:
        
        articles = Article.objects.filter(article_by=request.user).order_by("publish_date").reverse()
        articles_final= article_decorated(articles)
        
        return render(request, "capstone/index.html",{
        "articles": articles_final,
        "error": error
    })

def tag(request, tag_name):
    error=""
    if request.user.is_authenticated:
        
        articles = Article.objects.filter(article_related__tag_obj__tag_name=tag_name).order_by("publish_date").reverse()
        articles_final= article_decorated(articles)
        
        return render(request, "capstone/index.html",{
        "articles": articles_final,
        "error": error
    })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def star(request, star_name):
    error=""
    cnt_num=0
    cnt_y=0
    maga = Magazine.objects.all()
    if maga:
        m = maga[0].five_star_count
    else:
        m=5
    read_count_setting = int(round((m/5),0))*5
    j= read_count_setting/5
        
    if request.user.is_authenticated:
        for s in star_name.split(','):
            if (s != 'x' and s != 'y'):
                cnt_num=cnt_num+j
            elif (s == 'y'):
                cnt_y=cnt_y+1
        if (cnt_num+cnt_y <=0):
            articles = Article.objects.filter(read_count=0).order_by("publish_date").reverse()
        elif ((cnt_num+cnt_y) >= m):
            articles = Article.objects.filter(read_count__gte=int(cnt_num+cnt_y)).order_by("publish_date").reverse()
        elif ((cnt_num+cnt_y) %j == 0):
            articles = Article.objects.filter(read_count=(cnt_num+cnt_y)).order_by("publish_date").reverse()
        else:
            articles = Article.objects.filter(read_count__gte=int(cnt_num+cnt_y), read_count__lte=int(cnt_num+cnt_y + j -2)).order_by("publish_date").reverse()
        articles_final= article_decorated(articles)
        
        return render(request, "capstone/index.html",{
        "articles": articles_final,
        "error": error
    })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def is_number_of_columns(noc):
    try: 
        int(noc)
        return True
    except ValueError:
        return False

def maintain_article(request,art_action):
    success=""
    error=""
    update_article=None
    art_id=""
    if request.user.is_authenticated:
        if request.method == "POST":
            art_id = request.POST["article_id"]
            if art_id and art_id != "0":
                art = Article.objects.filter(id=art_id)
                update_article=article_decorated(art)
            else:
                title = request.POST.get("article-title")
                if title: # art_id is None:
                    if (art_action == "Delete"):
                        arti = Article.objects.filter(title=title)

                        #Delete Article tags
                        art2tag = Articletotag.objects.filter(article_obj=arti[0])
                        art2tag.delete()
                        
                        # Delete Article
                        arti.delete()
                        update_article=""
                    else:
                        synopsis = request.POST["article-synopsis"]
                        content = request.POST["article-text"]
                        tags = request.POST.getlist("article-tags")
                        pic = request.POST["article-picture"]
                        number_of_columns = request.POST["article-column"]
                        if number_of_columns == "":
                            number_of_columns=1
                        arti = Article.objects.filter(title=title)
                        if (is_number_of_columns(number_of_columns)):
                            arti.delete()
                            art=  Article(article_by=request.user, title=title, synopsis=synopsis, content=content, article_picture=pic, article_column=number_of_columns)
                            art_id = art.id
                            art.save()
                            art2tag = Articletotag.objects.filter(article_obj=art)
                            art2tag.delete()
                            
                            for t in tags:
                                tag = Tag.objects.get(tag_name=t)
                                art2tag = Articletotag(tag_obj=tag, article_obj=art)
                                art2tag.save()
                            art2tag = Articletotag.objects.filter(article_obj=art)
                            art = Article.objects.filter(id=art.id)
                            update_article=article_decorated(art)
                            art_id=art[0].id
                        else:
                            art = Article.objects.filter(id=arti[0].id)
                            update_article=article_decorated(art)
                            art_id=art[0].id
                            error="Article Column size entered is '" + number_of_columns + "' should be an integer!"
                else:
                    if (art_id is None or art_id == "0"):
                        error="Title is mandatory"
                
        tags = Tag.objects.all().order_by("tag_name")
        tag_list=[]
        for t in tags:
            tag_list.append(t.tag_name)
        art=  Article.objects.filter(article_by=request.user)
        articles_final= article_decorated(art)
        return render(request, "capstone/maintain_article.html",{
            "articles": articles_final,
            "article": update_article,
            "tags": tag_list,
            "art_id": art_id,
            "success": success,
            "error": error
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def delete_article(request):
    success=""
    error=""
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST.get("article-title")
            if title: # art_id is None:
                arti = Article.objects.filter(title=title)

                #Delete Article tags
                art2tag = Articletotag.objects.filter(article_obj=arti[0])
                art2tag.delete()
                
                # Delete Article
                arti.delete()
            else:
                error="Title not found!"
        tag_list=[]
        art=  Article.objects.all()
        articles_final= article_decorated(art)
        tag_list=[]
        tags = Tag.objects.all().order_by("tag_name")
        for t in tags:
            tag_list.append(t.tag_name)
        return render(request, "capstone/maintain_article.html",{
            "articles": articles_final,
            "article": "",
            "tags": tag_list,
            "art_id": "",
            "success": success,
            "error": error
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def manage_resource(request, resource_name):
    success=""
    error=""
    try:
            
        if request.method == "POST":
            if (resource_name=='add'):
                new_tag = request.POST.get('tag','')
                if new_tag:
                    t = Tag(tag_name=new_tag)
                    t.save()
                    success = new_tag + " is added to tag list."
                else:
                    error="Tag is empty."
            elif (resource_name=='delete'):
                tag_ids = request.POST.getlist('tag-list','')
                tag_list=[]
                
                for t in tag_ids:
                    if tag_ids:
                        t = Tag.objects.get(id=t)
                        tag_list.append(t.tag_name)
                        t.delete()
                if tag_ids:
                    success = str(tag_list) + " deleted."
                else:
                    error="No tag selected for deletion."
            
            else:
                if request.method == "POST":
                    mag_title = request.POST["mag-title"]
                    mag_5_star_count = request.POST["mag-5-star-count"]
                    if (is_number_of_columns(mag_5_star_count) and int(mag_5_star_count) >=5):
                        if mag_title:
                            Magazine.objects.all().delete()
                            m = Magazine(title=mag_title, five_star_count= mag_5_star_count)
                            m.save()
                            success = "Magazine settings updated."
                        else:
                            error="Magazine title is empty."
                    else:
                        error="The value entered for 'Number of reads for 5 star' is '" + mag_5_star_count + "', should be an integer and more than or equal to 5!"
    except Exception as e:
        error = str(e)
    tags = Tag.objects.all().order_by("tag_name")
    mag_obj = Magazine.objects.all()
    if mag_obj:
        mag = {"title": mag_obj[0].title, "five_star_count": mag_obj[0].five_star_count}
    else:
        mag = {"title": "", "five_star_count": ""}
    return render(request, "capstone/manage_resource.html",{"tags":tags, "mag":mag, "success":success, "error":error})


def tag_articles(request, tag_name):
    success=""
    error=""
    if request.method == "POST":
        new_tag = request.POST.get('tag','')
        if new_tag:
            t = Tag(tag_name=new_tag)
            t.save()
            success = new_tag + " is added to tag list."
        else:
            error="Tag is empty."
    tags = Tag.objects.all().order_by("tag_name")
    return render(request, "capstone/manage_tag_resource.html",{"tags":tags, "success":success, "error":error})

def get_articles(request, page_type,article_id):
    mag={}
    if article_id:
        article=  Article.objects.filter(id=article_id)
    else:
        article = Article.objects.all().order_by("publish_date").reverse()
        maga= Magazine.objects.all()
        if maga:
            mag= maga[0]
            mag = {"title": mag.title, "five_star_count": mag.five_star_count}
        else:
            mag = {"title": "***[No Magazine Title setup!]***", "five_star_count": 5}

    articles_final= article_decorated(article)
    
    data = list(articles_final)
    article_paginated_set = {'data': articles_final, 'mag': mag}
    
    return JsonResponse(article_paginated_set)
    
def view_article(request,id):
    if request.user.is_authenticated:
        
        art=  Article.objects.get(id=id)
        art.read_count = art.read_count+1
        art.save()

        return render(request, "capstone/preview_article.html"
                        ,{"page_type": "article"
                        , "article_id": id
                        })
    else:
        return HttpResponseRedirect(reverse("login"))

def view_magazine(request):

    return render(request, "capstone/preview_article.html"
                    ,{"page_type": "magazine"
                    , "article_id": 0
                    })
