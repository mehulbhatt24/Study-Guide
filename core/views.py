from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,LikePost

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        return render(request,'index.html',{'user_profile':user_profile})
    return render(request,'index.html')



def signup(request):
    # action="" means to the same page
    # action="index" will sent data to index
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"email already exists")
                return redirect('signup')
            if User.objects.filter(username=username).exists():
                messages.info(request,"username already exists")
                return redirect('signup')
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()

            #log user in and redirect to settings page
            user_login = auth.authenticate(username = username,password = password)
            auth.login(request,user_login)
            
            #create profile object for new user
            user_model = User.objects.get(username = username)
            new_profile = Profile.objects.create(user=user_model)
            new_profile.save()
            return redirect('accounts')
        else:
            messages.info(request,"password do not match")
            return redirect('signup')
            
    else:
        return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            if not Profile.objects.filter(user = user).exists():
                prof = Profile.objects.create(user = user)
                prof.save()
            return redirect('/')
        else:
            messages.info(request,'Invalid username or password')
            return redirect('signin')

    else:
        return render(request,'signin.html')
    
@login_required(login_url='signin')
def accounts(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image')!= None:
            user_profile.image = request.FILES.get('image')
 
        user_profile.fname = request.POST['fname']
        user_profile.lname = request.POST['lname']
        user_profile.address = request.POST['address']
        user_profile.country = request.POST['country']
        user_profile.city = request.POST['city']
        user_profile.phone = request.POST['phone']
        user_profile.save()
        return redirect('accounts')

    # return render(request,'settings.html',{'user_profile':user_profile})
    return render(request,'accounts.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def post(request):
    if request.method == 'POST':
        search_topic = request.POST['search_topic']
        search_subject = request.POST['search_subject']
        sort_by_date = request.POST['sort_by_date']
        sort_by_likes = request.POST['sort_by_likes']
        if search_topic!='':
            posts = Post.objects.filter(title = search_topic)
        elif search_subject!='':
            posts = Post.objects.filter(subject = search_subject)
        else:
            posts = Post.objects.all()
        if sort_by_date=='TopToBottom':
            posts = posts.order_by('-date').values()
        elif sort_by_date=='BottomToTop':
            posts = posts.order_by('date').values()
        if sort_by_likes=='TopToBottom':
            posts = posts.order_by('-no_of_likes').values()
        elif sort_by_likes=='BottomToTop':
            posts = posts.order_by('no_of_likes').values()
        user_profile = Profile.objects.filter(user = request.user).first()
        return render(request,'post.html',{'posts':posts,'user_profile':user_profile})
        # return redirect('post',{'posts':posts,'user_profile':user_profile})
        
    posts = Post.objects.all()
    user_profile = Profile.objects.filter(user = request.user).first()
    return render(request,'post.html',{'posts':posts,'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        file1 = request.FILES.get('file')
        thumbnail = request.FILES.get('thumbnail')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        title = request.POST['title']
        course = request.POST['course']
        subject = request.POST['subject']
        text = request.POST['text']
        profile = Profile.objects.get(user = request.user)
        new_post = Post.objects.create(profile = profile,title = title,subject=subject,course=course,file1=file1,thumbnail=thumbnail,text=text)
        if image1!=None:
            new_post.image1 = image1
        if image2!=None:
            new_post.image2 = image2
        if image3!=None:
            new_post.image3 = image3
        new_post.save()
        messages.info(request,'File uploaded successfully')
        return redirect('upload')
    return render(request, 'upload.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id = post_id)
    if not LikePost.objects.filter(username = username,post_id = post_id).exists():
        new_like = LikePost.objects.create(username = username,post_id = post_id)
        post.no_of_likes+=1
        new_like.save()
        post.save()
    else:
        new_like = LikePost.objects.get(username=username,post_id=post_id)
        post.no_of_likes-=1
        new_like.delete()
        post.save()
    return redirect('post')

@login_required(login_url='signin')
def profile(request,pk):
    user = User.objects.filter(username=pk).first()
    if not user:
        return redirect('/')
    profile = Profile.objects.get(user = user)
    posts = Post.objects.filter(profile=profile)
    user_profile = Profile.objects.filter(user = request.user).first()
    return render(request,'profile.html',{'posts':posts,'user_profile':user_profile,'profile':profile})
    # return render(request,'profile.html')