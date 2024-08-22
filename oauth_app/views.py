import googlemaps
import json
import geocoder
from django.utils import timezone
import requests

from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
from django.shortcuts import render,redirect
from django.conf import settings
from django.shortcuts import render
from django.conf import settings
from django.views import generic
from .mixins import Directions
from .models import User, Wildlife, Post, Comment, Like, SavedPost
from django import forms
from django.views.generic import TemplateView
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from .forms import WildlifeForm, PostForm, UserImageForm
from allauth.socialaccount.models import SocialAccount


from .models import Post
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
from django.forms.formsets import formset_factory

# class IndexView(generic.ListView):
#     template_name = "oauth_app/index.html"
#     context_object_name = "latest_question_list"

# class MapView(generic.DetailView):
#     template_name = "oauth_app/map/map.html"

current_logged_user = None

class WildlifePostForm(forms.Form):
    id = forms.IntegerField(label='id', widget=forms.HiddenInput)
    name = forms.CharField(label='name')
    address = forms.CharField(label='address')
    image = forms.ImageField(label='image', required=False)
    message = forms.SlugField(max_length=2000, required=False)

#WildlifePostFormSet = formset_factory(WildlifePostForm, extra=0)

def add_wildlife_post(request):
    try:
        is_admin = False
        logged_user = User.objects.get(email=request.user.email)
        if logged_user.is_admin:
            is_admin = True
        g = geocoder.ip('me')
        form = UserImageForm()
        if request.method == 'POST':
            if request.POST['post_title']:
                form = UserImageForm(request.POST, request.FILES)
                addr = request.POST.get('address')
                resp = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={addr}&key={settings.GOOGLE_MAPS_API_KEY}')
                resp_json = resp.json()
                lat = resp_json['results'][0]['geometry']['location'].get('lat')
                lng = resp_json['results'][0]['geometry']['location'].get('lng')
                wildlife=Wildlife(latitude=int(lat), longitude=int(lng), address=addr, name=request.POST.get('wf_name'), image=request.POST.get('image')) #Wildlife(name=request.POST['post_name'],
                if form.is_valid():
                    form.save()
                    img_object = form.instance
                    wildlife.image = img_object.image
                wildlife.save()
                current_user = User.objects.get(email=request.user.email)
                postEntry = Post(user=current_user, wildlife=wildlife, title=request.POST['post_title'], body=request.POST['body'], created_at=timezone.now())
                postEntry.save()
                context = {
                    'form': form,
                    'address':g.address,
                    'submit_success': True,
                    'is_admin':is_admin,
                }
                return render(request, 'forms/create_post.html', context)
            else:
                return render(
                    request,
                    "forms/create_post.html",
                    {
                        "error_message": "You didn't give text for the question.",
                    },
                )
        else: 
            context = {
                'form': form,
                'address':g.address,
                'submit_success': True,
                'is_admin':is_admin,
            }
            return render(request, 'forms/create_post.html', context)
    except AttributeError:
        return redirect("/")
    #WildlifePostFormSet = formset_factory(WildlifePostForm(), extra=0)
    # img_form = UserImageForm()
    # g = geocoder.ip('me')
    # if request.method == 'POST':
    #     form = WildlifePostForm(request.POST)
    # else:
    #     form = WildlifePostForm(initial={
    #         'address':g,
    #     })
    
    # context = {
    #     'form': img_form,
    #     'address':g.address,
    #     'submit_success': False,
    # }
    # return render(request, 'forms/create_post.html', context)
    #return render(request, "polls/add.html", {"choice_list": range(3)})
    

def add_entry(request):
    try:
        g = geocoder.ip('me')
        if request.method == 'POST':
            if request.POST['post_title']:
                form = UserImageForm(request.POST, request.FILES)
                addr = request.POST.get('address')
                resp = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={addr}&key={settings.GOOGLE_MAPS_API_KEY}')
                resp_json = resp.json()
                lat = resp_json['results'][0]['geometry']['location'].get('lat')
                lng = resp_json['results'][0]['geometry']['location'].get('lng')
                wildlife=Wildlife(latitude=int(lat), longitude=int(lng), address=addr, name=request.POST.get('wf_name')) #Wildlife(name=request.POST['post_name'],
                if form.is_valid():
                    form.save()
                    img_object = form.instance
                    wildlife.image = img_object.image
                wildlife.save()
                current_user = User.objects.get(email=request.user.email)
                postEntry = Post(user=current_user, wildlife=wildlife, title=request.POST['post_title'], body=request.POST['body'], created_at=timezone.now())
                postEntry.save()
                context = {
                    'fs': form,
                    'address':g.address,
                    'submit_success': True,
                    'img_obj': img_object,
                }
                return render(request, 'forms/create_post.html', context)
            else:
                return render(
                    request,
                    "forms/create_post.html",
                    {
                        "error_message": "You didn't give text for the question.",
                    },
                )   
        context = {
            'fs': form,
            'address':g.address,
            'submit_success': True,
        }
        return render(request, 'forms/create_post.html', context)
    except AttributeError:
        return redirect("/")


def add_wildlife_and_post(request):
    try:
        if request.method == 'POST':
            wildlife_form = WildlifeForm(request.POST)
            post_form = PostForm(request.POST, request.FILES)  # Include request.FILES for file uploads

            if wildlife_form.is_valid() and post_form.is_valid():
                # Save the Wildlife object
                wildlife = wildlife_form.save()

                # Save the Post object with the reference to the created Wildlife object
                post = post_form.save(commit=False)
                post.wildlife = wildlife
                post.user = request.user  # Assuming you have user authentication
                post.save()

                return redirect('map')  # Redirect to the map view or any other desired location
        else:
            wildlife_form = WildlifeForm()
            post_form = PostForm()

        return render(request, 'forms/create_post.html', {'wildlife_form': wildlife_form, 'post_form': post_form, 'latitude':g.latlng[0], 'longitude':g.latlng[1]})
    except AttributeError:
        return redirect("/")

def index(request):
    if request.user.is_authenticated and not User.objects.filter(email=request.user.email).exists():
        current_logged_user = request.user
        #extra_data = SocialAccount.objects.get(user=request.user).extra_data
        #curr_user_profile_pic_url = extra_data['picture']
        logged_user = User(name=request.user.username, email=request.user.email, google_id=request.user.id)
        logged_user.save()
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect("/")


def route(request):
    context = {"google_api_key": settings.GOOGLE_MAPS_API_KEY}
    return render(request, "map/route.html", context)

class CustomTemplateView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # try:
        google_login = OAuth2Adapter.get_provider().get_login_url(self.request, 'google')
        print(google_login)
        context['google_login'] = google_login
        # except OAuth2Error:
        #     context['google_login'] = None
        return context

def users_map(request):
    try:
        is_admin = False
        logged_user = get_object_or_404(User, email=request.user.email)
        if logged_user.is_admin:
            is_admin = True
        key = settings.GOOGLE_MAPS_API_KEY

        latest_wildlife = Post.objects.filter(user=logged_user).order_by("-created_at") #Get user's posts
        #users = latest_wildlife.values('user') #Get users
        wildlife = latest_wildlife.values('wildlife') #Get wildlife of each of user's posts
        context = {
            'latitude':38.0336,
            'longitude':-78.50798,
            'address':'Charlottesville, VA, USA',
            'name':'University of Virginia',
            'zoom': 12,
            'key':key,
            'latest_posts':latest_wildlife,
            'wildlife':wildlife,
            'post_select':False,
            'is_admin':is_admin,
        }
        return render(request, 'map/user_map.html', context)
    except AttributeError:
        return redirect("/")

def user_map_handle_post(request, post_id, wildlife_id):
    try:
        is_admin = False
        logged_user = get_object_or_404(User, email=request.user.email)
        if logged_user.is_admin:
            is_admin = True
        post = Post.objects.get(id=post_id)
        wildlife = Wildlife.objects.get(id=wildlife_id)
        latitude = wildlife.latitude
        longitude = wildlife.longitude
        address = wildlife.address
        name = wildlife.name
        latest_wildlife = Post.objects.filter(user=logged_user).order_by("-created_at") #Get latest 10 posts
        #users = latest_wildlife.values('user') #Get users of latest 10 posts
        wildlife = latest_wildlife.values('wildlife') #Get wildlife of latest 10 posts
        key = settings.GOOGLE_MAPS_API_KEY
        context = {
            'latitude':latitude,
            'longitude':longitude,
            'address':address,
            'name':name,
            'zoom': 15,
            'key':key,
            'latest_posts':latest_wildlife,
            'wildlife':wildlife,
            'post_select':True,
            'post':post,
            'is_admin':is_admin,
        }
        return render(request, 'map/user_map.html', context)
    except AttributeError:
        return redirect("/")

def saved_map(request):
    try:
        is_admin = False
        logged_user = get_object_or_404(User, email=request.user.email)
        if logged_user.is_admin:
            is_admin = True
        key = settings.GOOGLE_MAPS_API_KEY

        latest_posts = SavedPost.objects.filter(user=logged_user).order_by("saved_at")

        context = {
            'latitude': 38.0336,
            'longitude': -78.50798,
            'address': 'Charlottesville, VA, USA',
            'name': 'University of Virginia',
            'zoom': 12,
            'key': key,
            'latest_posts': latest_posts,
            'is_admin': is_admin,
        }
        return render(request, 'map/saved_map.html', context)
    except AttributeError:
        return redirect("/")

def map(request):
    try:
        is_admin = False
        logged_user = User.objects.filter(email=request.user.email)
        if request.user.is_authenticated and User.objects.filter(email=request.user.email).exists(): #If user is logged in and exists in database
            logged_user = User.objects.filter(email=request.user.email)
            if logged_user[0].is_admin: #If user is admin
                is_admin = True
        key = settings.GOOGLE_MAPS_API_KEY
        latest_wildlife = Post.objects.filter(approval_status=2).order_by("-created_at")[:10] #Get latest 10 posts
        users = latest_wildlife.values('user') #Get users of latest 10 posts
        wildlife = latest_wildlife.values('wildlife') #Get wildlife of latest 10 posts
        saved_posts = SavedPost.objects.filter(user=logged_user[0]).order_by("saved_at")
        saved_wildlife = [x.post for x in saved_posts]
        print(type(saved_posts))
        context = {
            'latitude':38.0336,
            'longitude':-78.50798,
            'address':'Charlottesville, VA, USA',
            'name':'University of Virginia',
            'zoom': 12,
            'key':key,
            'latest_posts':latest_wildlife,
            'users':users,
            'wildlife':wildlife,
            'post_select':False,
            'is_admin':is_admin,
            'saved_posts':saved_wildlife,
        }
        return render(request, 'map/map.html',context)
    except AttributeError:
        return redirect("/")

def approval_portal(request):
    if request.method == 'POST':
            decline_body = request.POST.get('decline_reason')
            post_id = request.POST.get('postid')
            declined_post = Post.objects.get(id=post_id)
            declined_post.decline_reason = decline_body
            declined_post.save()
            print("reason: ", decline_body, post_id)
            return redirect(f"/{post_id}/decline_post/")
    try:
        is_admin = False
        logged_user = User.objects.get(email=request.user.email)
        if logged_user.is_admin:
            is_admin = True
        to_be_approved_wildlife = Post.objects.filter(approval_status=1).order_by("created_at")[:10] #Get posts that are pending approval
        users = to_be_approved_wildlife.values('user') #Get users of posts that are pending approval
        wildlife = to_be_approved_wildlife.values('wildlife') #Get wildlife of posts that are pending approval
        context = {
            'posts':to_be_approved_wildlife,
            'users':users,
            'wildlife':wildlife,
            'is_admin':is_admin,
        }
        return render(request, 'approval_site/approval_portal.html',context)
    except AttributeError:
        return redirect("/")
    
def save(request, post_id):
    try:
        logged_user = User.objects.get(email=request.user.email)
        saved_post = SavedPost(user=logged_user, post=Post.objects.get(id=post_id), saved_at=timezone.now())
        saved_post.save()
        return redirect("/activity")
    except AttributeError:
        return redirect("/")
    
def unsave(request, post_id):
    try:
        logged_user = User.objects.get(email=request.user.email)
        saved_post = SavedPost.objects.filter(user=logged_user, post=Post.objects.get(id=post_id))[0]
        saved_post.delete()
        return redirect("/activity")
    except AttributeError:
        return redirect("/")

def approve_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        post.approval_status = 2  # Set to approved
        post.save()
        to_be_approved_wildlife = Post.objects.filter(approval_status=1).order_by("created_at")[:10] #Get posts that are pending approval
        users = to_be_approved_wildlife.values('user') #Get users of posts that are pending approval
        wildlife = to_be_approved_wildlife.values('wildlife') #Get wildlife of posts that are pending approval
        context = {
            'posts':to_be_approved_wildlife,
            'users':users,
            'wildlife':wildlife,
        }
        return render(request, 'approval_site/approval_portal.html',context)
    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Post not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    except AttributeError:
        return redirect("/")
    
def decline_post(request, post_id):
    try:
        comment_body = request.POST.get('decline_reason')
        print(comment_body)
        post = get_object_or_404(Post, id=post_id)
        post.approval_status = 0  # Set to declined
        post.save()
        to_be_approved_wildlife = Post.objects.filter(approval_status=1).order_by("created_at")[:10] #Get posts that are pending approval
        users = to_be_approved_wildlife.values('user') #Get users of posts that are pending approval
        wildlife = to_be_approved_wildlife.values('wildlife') #Get wildlife of posts that are pending approval
        context = {
            'posts':to_be_approved_wildlife,
            'users':users,
            'wildlife':wildlife,
        }
        return render(request, 'approval_site/approval_portal.html',context)
    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Post not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    except AttributeError:
        return redirect("/")
    
def react(request, post_id, action):
    logged_user = User.objects.get(email=request.user.email)
    post = Post.objects.get(id=post_id)
    try:
        existing_like = Like.objects.get(post=post, user=logged_user)
    except Like.DoesNotExist:
        existing_like = None
    if existing_like:
        existing_like.delete()
    like = True
    if action == 'dislike':
        like = False
    likeObj = Like(user=logged_user, post=post, like=like)
    likeObj.save()
    return redirect('post_detail', post_id=post_id, wildlife_id=post.wildlife.id)
    
def mydata(request):
    print("hello")
    result_list = list(Wildlife.objects\
                .values('id',
                        'name', 
                        'latitude',
                        'longitude',
                        'address',
                        ))
  
    return JsonResponse(result_list, safe=False)

# from https://djangocentral.com/creating-comments-system-with-django/
def post_detail(request, post_id, wildlife_id):
    try:
        is_admin = False
        logged_user = User.objects.get(email=request.user.email)
        if logged_user.is_admin:
            is_admin = True
        template_name = 'post_detail.html'
        saved = False
        post = get_object_or_404(Post, pk=post_id)
        num_likes = Like.objects.filter(post=post, like=True).count()
        num_dislikes = Like.objects.filter(post=post, like=False).count()
        key = settings.GOOGLE_MAPS_API_KEY
        longitude = float(post.wildlife.longitude)
        latitude = float(post.wildlife.latitude)
        context = {
            'post':post,
            'num_likes':num_likes,
            'num_dislikes':num_dislikes,
            'saved':saved,
            'is_admin':is_admin,
            'latitude':latitude,
            'longitude':longitude,
            'zoom':17,
            'key':key,
        }
        if request.method == 'POST':
            comment_body = request.POST.get('comment')
            posting_name = request.POST.get('posting_name')
            print(posting_name)
            #comment_form = CommentForm(data=request.POST)
            logged_user = User.objects.get(email=request.user.email)
            comment = Comment(user=logged_user, posting_name=posting_name, post=post, body=comment_body, created_at=timezone.now())
            comment.save()
            #context['comment_form'] = comment_form
        try:
            comments = Comment.objects.filter(post=post)
            count = comments.count()
            # extra_data = SocialAccount.objects.get(user=request.user).extra_data
            # curr_user_profile_pic_url = extra_data['picture']
            context['comments'] = comments
            context['count'] = count
            # context['profile_pic_url'] = curr_user_profile_pic_url
        except Comment.DoesNotExist:
            comments = []
        new_comment = None    # Comment posted
        return render(request, template_name, context)
    except AttributeError:
        return redirect("/")

def handle_post(request, post_id, wildlife_id):
    try:
        is_admin = False
        logged_user = User.objects.get(email=request.user.email)
        if logged_user.is_admin:
            is_admin = True
        post = Post.objects.get(id=post_id)
        wildlife = Wildlife.objects.get(id=wildlife_id)
        latitude = wildlife.latitude
        longitude = wildlife.longitude
        address = wildlife.address
        name = wildlife.name
        logged_user = User.objects.get(email=request.user.email)
        latest_wildlife = Post.objects.filter(approval_status=2).order_by("-created_at")[:10] #Get latest 10 posts
        users = latest_wildlife.values('user') #Get users of latest 10 posts
        saved_posts = SavedPost.objects.filter(user=logged_user).order_by("saved_at")
        saved_wildlife = [x.post for x in saved_posts]
        wildlife = latest_wildlife.values('wildlife') #Get wildlife of latest 10 posts
        key = settings.GOOGLE_MAPS_API_KEY
        context = {
            'latitude':latitude,
            'longitude':longitude,
            'address':address,
            'name':name,
            'zoom': 15,
            'key':key,
            'latest_posts':latest_wildlife,
            'users':users,
            'wildlife':wildlife,
            'post_select':True,
            'post':post,
            'saved_posts':saved_wildlife,
            'is_admin':is_admin,
        }
        return render(request, 'map/map.html', context)
    except AttributeError:
        return redirect("/")

def handle_saved_post(request, post_id, wildlife_id):
    try:
        post = Post.objects.get(id=post_id)
        wildlife = Wildlife.objects.get(id=wildlife_id)
        latitude = wildlife.latitude
        longitude = wildlife.longitude
        address = wildlife.address
        name = wildlife.name
        logged_user = get_object_or_404(User, email=request.user.email)
        latest_posts = SavedPost.objects.filter(user=logged_user).order_by("saved_at")
        posts = latest_posts.values('post')
        users = latest_posts.values('post__user')  # Get users of latest 10 posts
        wildlife = latest_posts.values('post__wildlife')  # Get wildlife of latest 10 posts
        key = settings.GOOGLE_MAPS_API_KEY
        context = {
            'latitude': latitude,
            'longitude': longitude,
            'address': address,
            'name': name,
            'zoom': 15,
            'key': key,
            'latest_posts': latest_posts,
            'users': users,
            'wildlife': wildlife,
            'post_select': True,
            'post': post,
        }
        return render(request, 'map/saved_map.html', context)
    except AttributeError:
        return redirect("/")

def all_posts(request):
    try:
        is_admin = False
        if request.user.is_authenticated and User.objects.filter(email=request.user.email).exists(): #If user is logged in and exists in database
            logged_user = User.objects.filter(email=request.user.email)
            if logged_user[0].is_admin: #If user is admin
                is_admin = True
        key = settings.GOOGLE_MAPS_API_KEY
        logged_user = User.objects.get(email=request.user.email)
        all_wildlife = Post.objects.filter(approval_status=2).order_by("-created_at") 
        users = all_wildlife.values('user')
        wildlife = all_wildlife.values('wildlife')
        saved_posts = SavedPost.objects.filter(user=logged_user).order_by("saved_at")
        saved_wildlife = [x.post for x in saved_posts]
        context = {
            'latitude':38.0336,
            'longitude':-78.50798,
            'address':'Charlottesville, VA, USA',
            'name':'University of Virginia',
            'zoom': 12,
            'key':key,
            'all_postings':all_wildlife,
            'users':users,
            'wildlife':wildlife,
            'post_select':False,
            'is_admin':is_admin,
            'saved_posts':saved_wildlife,
        }
        return render(request, 'map/all_posts.html',context)
    except AttributeError:
        return redirect("/")

def handle_all_posts(request, post_id, wildlife_id):
    try:
        post = Post.objects.get(id=post_id)
        wildlife = Wildlife.objects.get(id=wildlife_id)
        latitude = wildlife.latitude
        longitude = wildlife.longitude
        address = wildlife.address
        name = wildlife.name
        all_wildlife = Post.objects.order_by("created_at")
        users = all_wildlife.values('user')
        wildlife = all_wildlife.values('wildlife')
        key = settings.GOOGLE_MAPS_API_KEY
        context = {
            'latitude':latitude,
            'longitude':longitude,
            'address':address,
            'name':name,
            'zoom': 15,
            'key':key,
            'all_postings':all_wildlife,
            'users':users,
            'wildlife':wildlife,
            'post_select':True,
            'post':post,
        }
        return render(request, 'map/all_posts.html', context)
    except AttributeError:
        return redirect("/")

def save_post(request, post_id, wildlife_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        save = True
        logged_user = get_object_or_404(User, email=request.user.email)
        #savedPost = SavedPost.objects.filter(post=post, user=request.user)
        # Check if the post is not already saved by the user
        if not SavedPost.objects.filter(user=logged_user, post=post).exists():
            #SavedPost.objects.create(user=logged_user, post=post)
            savedPost = SavedPost(user=logged_user, post=post)
            savedPost.save()
        elif SavedPost.objects.get(user=logged_user, post=post):
            save = False
            SavedPost.objects.get(user=logged_user, post=post).delete()

        # Redirect to the post detail page after saving
        return redirect('post_detail', post_id, wildlife_id)
    except AttributeError:
        return redirect("/")