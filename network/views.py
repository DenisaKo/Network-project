
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import Profil, User, Post, Comment

def index(request):
    posts = Post.objects.all()
    all_posts = [item.serialize() for item in posts]
    
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        if request.method == "GET" :
            user = request.user
            user_profil = Profil.objects.get(pk=user)
        return render(request, "network/index.html", {
        'page_obj': page_obj,
        'img': user_profil.image
        })

    else:
        if request.method == "GET" :
            return render(request, "network/index.html", {
            'page_obj': page_obj,
            })


@csrf_exempt
def following_page(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        # 
        # receiving data from db
        if request.method == 'GET':
            # get user
            user = request.user
            # get his profil
            my_profil = Profil.objects.get(pk=user)
            # get his following users - type user
            following_users = my_profil.following.all()
            # get all their posts - nested list
            posts = [Post.objects.filter(sender=following_user.id) for following_user in following_users]
            posts_not_nested = [obj for post in posts for obj in post]
            posts_not_nested.sort(key=lambda x: x.timestamp, reverse=True)
            all_posts = [item.serialize() for item in posts_not_nested]

            # create a paginator, and counter pages
            paginator = Paginator(all_posts, 10)
            # counter = int(request.GET.get('page') or 1)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            return render(request, "network/following_page.html", {
                'page_obj': page_obj,
                "img": my_profil.image
            })
            
        else:
            return HttpResponseNotFound("Sorry only GET method is supported")


    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def post_detail(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
    # check if post_id is valid
        try:
            user = request.user 
            post_item = Post.objects.get(pk=post_id)
        except ObjectDoesNotExist:
            return JsonResponse({"Status": f"There is no post with id {post_id}"}, status=404)

        if request.method == "POST":
            data = json.loads(request.body)
            if data.get('add_like') is not None:
                print('like button goes')
                if post_item.likes.all().contains(user):
                        post_item.likes.remove(user)
                else:
                    post_item.likes.add(user)

                all_likes = post_item.likes.all().count()
                return JsonResponse({
                    "all_likes": all_likes
                })
        
            elif data.get('body_text') is not None:
                print('post editing goes')
                edited_post_body = data.get('body_text')
                post_item.__dict__.update(data)
                post_item.save()
                return JsonResponse({
                    "edited_post_body": edited_post_body
                })
            
            else:
                JsonResponse({
                    "error": 'Something went wrong'
                })

        elif request.method == 'GET':
            post = post_item.serialize()
            return JsonResponse({
                "post_item": post
            })

        else:
            return HttpResponseNotFound("Sorry only POST and GET method are supported")


@csrf_exempt
def add_post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    else:
        # write data into db
        if request.method == "POST":
            user = request.user
            body_text = request.POST['body_text']
            # creat an object of Post + save
            new_post = Post(sender=user, body_text=body_text)
            new_post.save()
            # added_post = new_post.serialize()
            return HttpResponseRedirect(reverse("index"))
        
        # other method are not allowed
        return HttpResponseNotFound("Sorry only POST method is supported")


@csrf_exempt
def user_detail_profil(request, user_id):
    
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        if request.method == "GET":
            # login user - the one who is looking the profil
            login_user = request.user
            profil_login_user = Profil.objects.get(pk=login_user)

            user = User.objects.get(pk=user_id) 
            profil = Profil.objects.get(pk = user)
            user_profil = profil.serialize()
            followers_count = user.followers.all().count()
            following_count = profil.following.all().count()

            if profil_login_user.following.all().contains(user):
                status = 'unfollow'
            else:
                status = 'follow'

            posts = Post.objects.filter(sender = user)
            all_posts = [item.serialize() for item in posts]

            # create a paginator, and counter pages
            paginator = Paginator(all_posts, 10)
            # counter = int(request.GET.get('page') or 1)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

  
            return render(request, "network/profil.html", {
                "user_id": user_id,
                'user_username': user.username,
                "profil": user_profil,
                "followers_count": followers_count,
                "following_count": following_count,
                'page_obj': page_obj,
                'status': status.upper()
            })
        else:
            return HttpResponseNotFound("Sorry only POST method is supported")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def user_detail(request, user_id):
    # check if user_id is valid
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        try:
            # whose profile to follow/unfollow
            user = User.objects.get(pk=user_id) 
            profil = Profil.objects.get(pk=user) 
        except ObjectDoesNotExist:
            return JsonResponse({"Status": f"There is no user with id {user_id}"}, status=404)

        if request.method == "POST":
            # receive data
            data = json.loads(request.body)

            if data.get('status') is not None:
                status = data.get('status').lower()
                # log in user clicking follow button
                login_user = request.user
                profil_login_user = Profil.objects.get(pk=login_user)

                if status == 'follow':
                    profil_login_user.following.add(user)
                    return JsonResponse({
                        "followers": user.followers.all().count(),
                        'status': 'unfollow'
                    })

                elif status == "unfollow":
                    profil_login_user.following.remove(user)
                    return JsonResponse({
                        "followers": user.followers.all().count(),
                        'status': 'follow'
                    })
                else:
                    return JsonResponse({"Status": "Only follow/unfollow status allowed."}, status=404)

            else:
                image = data.get('image')
                bio = data.get('bio')
                profil.__dict__.update(data)
                profil.save()
                return JsonResponse({
                    'image': image,
                    "bio": bio
                })
                # return JsonResponse({"message": f"Log in user {user_id} successfully updated profile."}, status=201)    
        
        if request.method == "GET":
            return JsonResponse(profil.serialize())
        
        else:
            return HttpResponseNotFound("Sorry only POST method is supported")


@csrf_exempt
def comments_list(request, post_id):
    # check if user_id is valid
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = request.user 
        # check if post_id is valid
        try:
            post_item = Post.objects.get(pk=post_id)
        except ObjectDoesNotExist:
            return JsonResponse({"Status": f"There is no post with id {post_id}"}, status=404)

        if request.method == "GET":
            comments = Comment.objects.filter(post = post_item)
            comments_view = [comment.serialize() for comment in comments]

            return JsonResponse({
                "comments_view": comments_view
            })
        
        elif request.method == "POST":
            data = json.loads(request.body)
            comment_body = data.get('comment_body')
            print(comment_body)
            comment = Comment(
                sender = user,
                body_text = comment_body,
                post = post_item
            )
            comment.save()
            
            return JsonResponse({
                "comment": comment.serialize() 
            })

        else:
            return HttpResponseNotFound("Sorry only POST method is supported")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profil = Profil.objects.create(pk=user.id)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


