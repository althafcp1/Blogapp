from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Follow
from django.shortcuts import render



from .models import Profile


def signup(request):
      if request.method=='POST':
            fullname=request.POST['fullname']
            email=request.POST['email']
            username=request.POST['username']
            password=request.POST['password']
            user = User.objects.create_user(
                  username=username,
                  password=password,
                  first_name=fullname,
                  email=email

            )
            user.save()
            return redirect('signin')

      else:
            return render(request,'signup.html')
      
def signin(request):
      if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']
            user = authenticate(
                  request,username=username,password=password
            )
            if user is not None:
                  login(request,user)
                  return redirect('home')
            else:
                  err ='username and password doesnt match'
                  return render(request,'signin.html',{'err':err})

      else:
            return render(request,'signin.html')
      
def check_username(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip().lower()
        is_available = not User.objects.filter(username=username).exists()
        return JsonResponse({'available': is_available})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def home(request):
      return render(request,'home.html')


def signout(request):
      logout(request)
      return redirect('signin')


@login_required
def createProfile(request):
      if request.method== 'POST':
            dob = request.POST['dob']
            gender = request.POST['gender']
            about= request.POST['about']
            photo = request.FILES.get('photo')
            profile = Profile(
                  user = request.user,
                  dob=dob,
                  gender=gender,
                  about=about,
                  photo = photo        
            )
            profile.save()
            return redirect('profile_redirect')
      else:
            return render(request,'createProfile.html')
      

@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('createProfile')
    posts = Post.objects.filter(user=request.user)
    return render(request, 'profile.html', {'profile': profile, 'posts': posts})

      

@login_required
def profile_redirect(request):
    profile_exists = Profile.objects.filter(user=request.user).exists()
    return redirect('profile') if profile_exists else redirect('createProfile')

      


def create_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        description = request.POST.get('description')

        user = request.user 
        post = Post(
              user=user, 
              image=image, 
              caption=caption, 
              description=description
            )
        post.save()
        return redirect('profile')
    else:
        return render(request, 'create_post.html')
    

@login_required
def search_user(request):
    query = request.GET.get('query') 
    users = User.objects.filter(username__icontains=query) if query else []
    return render(request, 'search_results.html', {'users': users})

          
@login_required
def profile_view(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    # Get profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=user_profile)
    posts = Post.objects.filter(user=user_profile)
    return render(request, 'profile.html', {'profile_user': user_profile, 'profile': profile, 'posts': posts})



    
    





