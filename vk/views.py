from django.http import Http404
from django.shortcuts import render, render_to_response, redirect
from vk.forms import UploadPhotoForm
from vk.models import Person, Friends, Post


def allusers(request):
    users = getallusers()
    return render_to_response('vk/user_list.html',
                              {'users': users, 'mode': 'allusers', 'current_status': request.session['status']})


def delete_post(request, p_id):
    Post.objects.get(id=p_id).delete()
    return redirect(request.META['HTTP_REFERER'])


def friends(request):
    users = getfriends(request.session['id'])
    return render_to_response('vk/user_list.html',
                              {'users': users, 'mode': 'friends', 'current_status': request.session['status']})


def guest(request):
    try:
        request.session['status'] = 'guest'
        return redirect('allusers')
    except:
        hed = "Произошла ошибка"
        message = "Мне жаль =( "
    return render_to_response('vk/notification.html', {'hdr': hed, 'message': message})


def home(request):
    if "status" in request.session:
        if request.session['status'] == 'login':
            return redirect('profile_with_id', request.session['id'])
    return render(request, 'vk/home.html')


def register(request):
    return render(request, 'vk/register.html')


def post(request, p_id):
    return render(request, 'vk/post.html')


def profile(request, p_id):
    info = getprofileinfo(p_id)
    posts = getposts(p_id)
    if request.session['status'] == 'login':
        if request.session['id'] == int(p_id):
            return render(request, 'vk/home_profile.html',
                          {'user_id': request.session['id'], 'profile_info': info, 'posts': posts})
        else:
            return render(request, 'vk/other_profile.html',
                          {'user_id': request.session['id'], 'profile_info': info,
                           'posts': posts})
    else:
        if request.session['status'] == 'guest':
            return render(request, 'vk/guest_profile.html',
                          {'profile_info': info, 'posts': posts})
    raise 404


def myprofile(request):
    return redirect('profile_with_id', request.session['id'])


def notification(request, header, message):
    return render(request, 'vk/notification.html', {'header': header, 'message': message})


def query_registration(request):
    hed = "Registration completed"
    message = "Log in with your username and password"
    p = Person(first_name=request.POST['first_name'],
               last_name=request.POST['last_name'],
               email=request.POST['email'],
               password=request.POST['password'],
               birthday=request.POST['birthday'],
               )
    try:
        p.validate_unique()
    except:
        hed = "Registration Failed"
        message = "Check the data you entered is correct"
    else:
        p.save()
    return render(request, 'vk/notification.html', {'hdr': hed, 'message': message})


def insertpost(request, w_id):
    author_info = getprofileinfo(request.session['id'])
    p = Post(wall_id=w_id,
             author_id=request.session['id'],
             author_name=author_info.first_name + ' ' + author_info.last_name,
             author_foto=author_info.avatar,
             body=request.POST['textbox'],
             )
    p.save()
    return redirect(request.META['HTTP_REFERER'])


def login(request):
    try:
        p = Person.objects.get(email=request.POST['login'])
        if p.password == request.POST['password']:
            request.session['status'] = 'login'
            request.session['id'] = p.id
            return redirect('/home/')
        else:
            hed = "Неправильный пароль"
            message = "Попробуй ещё раз %)"
    except:
        hed = "Не существует пользователя с указанным логином"
        message = "Проверьте правильность ввода поля 'Login' "
    return render_to_response('vk/notification.html', {'hdr': hed, 'message': message})


def logout(request):
    try:
        del request.session['status']
        del request.session['id']
    except KeyError:
        pass
    return redirect('/home/')


def upload_photo(request):
    if request.method == "POST":
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            person = getprofileinfo(request.session['id'])
            person.avatar = form.cleaned_data["avatar"]
            person.save()
        else:
            return render_to_response('vk/notification.html', {'hdr': request.POST, 'message': request.FILES})
    return redirect(request.META['HTTP_REFERER'])


def getrelationship(first, second):
    array = Friends.objects.filter(user1_id=first, user2_id=second)
    if array:
        return -1
    array - Friends.objects.filter(user2_id=first, user1_id=second)
    if array:
        return 1
    return 0


def getstringrelationship(first, second):
    num = getrelationship(first, second)
    if num == -1:
        return "Вы находитесь в подписчиках у этого пользователя"
    elif num == 1:
        return "Этот пользователь подал вам заявку в друзья"
    elif num == 0:
        return "Этот пользователь ваш друг"
    return ""


def getprofileinfo(profile_id):
    try:
        p = Person.objects.get(id=profile_id)
    except:
        raise Http404
    return p


def getauthorsinfo(authors):
    try:
        a = Person.objects.filter(id__in=authors)
    except:
        raise Http404
    return a


def getallusers():
    try:
        p = Person.objects.all()
    except:
        raise Http404
    return p


def getfriends(user_id):
    try:
        array = Friends.objects.filter(user1_id=user_id).values('user2_id').aggregate
        (Friends.objects.filter(user2_id=user_id).values('user1_id'))
    except:
        raise Http404
    return array


def getposts(profile_id):
    try:
        p = Post.objects.filter(wall_id=profile_id).order_by('-timestamp')
    except:
        raise Http404
    return p
