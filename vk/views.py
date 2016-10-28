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


def news(request):
    posts = getposts(request.session['id'])
    return render_to_response('vk/news.html', {'posts': posts})


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
            if request.session['id'] > int(p_id):
                rel = get_string_relationship(int(p_id), request.session['id'])
            else:
                rel = get_string_relationship(request.session['id'], int(p_id))
            return render(request, 'vk/other_profile.html',
                          {'user_id': request.session['id'], 'profile_info': info,
                           'posts': posts, 'relationship': rel})
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


def query_add_to_friends(request, other_p_id):
    weight = 0
    if request.session['id'] > other_p_id:
        weight = 2
        record = get_or_create_relationship(other_p_id,request.session['id'])
    else:
        weight = 1
        record = get_or_create_relationship(request.session['id'], other_p_id)
    r = record.relationship
    if r == 0:
       record.relationship = weight
    elif r == 3 - weight:
        record.relationship = 3
    return redirect(request.META['HTTP_REFERER'])


def query_delete_from_friends(request, other_p_id):
    weight = 0
    if request.session['id'] > other_p_id:
        weight = 2
        record = get_relationship(other_p_id,request.session['id'])
    else:
        weight = 1
        record = get_relationship(request.session['id'], other_p_id)
    r = record.relationship
    if r == weight:
       record.delete()
    elif r == 3:
        record.relationship = 3 - weight
    return redirect(request.META['HTTP_REFERER'])


def insertpost(request, w_id):
    a = getprofileinfo(request.session['id'])
    p = Post(
        wall_id=w_id,
        author=a,
        body=request.POST['textbox'])

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
            if person.avatar:
                person.avatar.delete(save=False)
            person.avatar = form.cleaned_data["avatar"]
            person.save()
        else:
            return render_to_response('vk/notification.html', {'hdr': request.POST, 'message': request.FILES})
    return redirect(request.META['HTTP_REFERER'])


def get_or_create_relationship(first, second):
    array = Friends.objects.filter(user1_id = first, user2_id = second)
    if array:
        return array[0]
    else:
        r = Friends(user1_id=first,user2_id=second, relationship=0)
        r.save()
        return r


def get_relationship(first, second):
    array = Friends.objects.filter(user1_id=first, user2_id=second)
    if array:
        return array[0]
    else:
        return None


def get_string_relationship(first, second):
    rel = get_relationship(first,second)
    if rel:
        if rel.relationship == 1:
            return "follower"
        elif rel.relationship ==2:
            return "master"
        elif rel.relationship ==3:
            return "friends"
    else:
        return "none"


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
