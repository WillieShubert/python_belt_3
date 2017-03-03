from django.shortcuts import render, redirect, HttpResponse
from .models import User, Quote
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request, 'belt/index.html')

def quotes(request):
    if 'userid' not in request.session:
        return redirect ("/")
    context = {
        'user' : User.objects.get(id=request.session['userid']),
        'quotes' : Quote.objects.all(),
        'fav_quotes' : Quote.objects.filter(admirers__id=request.session['userid'])
    }
    return render(request, 'belt/quoteboard.html', context)

def process_quote(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        newquote= Quote.objects.quote_validate(request.POST, request.session['userid'])
        print newquote
        if newquote[0] == False:
            for each in newquote[1]:
                messages.add_message(request, messages.INFO, each)
                return redirect('/quotes')
        if newquote[0] == True:
            messages.add_message(request, messages.INFO, "Quote Added")
            return redirect('/quotes')

def like_quote(request, quote_id):
    if request.method != "GET":
        messages.error(request,"Be nice")
        return redirect('/quotes')
    new_admirer= Quote.objects.like(request.session['userid'], quote_id)
    print 80 * ('*'), new_admirer
    if new_admirer[0] == False:
        for each in new_admirer[1]:
            messages.add_message(request, messages.INFO, each)
            return redirect('/quotes')
    if new_admirer[0] == True:
            messages.add_message(request, messages.INFO, "Quote favorited")
            return redirect('/quotes')

def user_details(request, id):
    if 'userid' not in request.session:
        return redirect ("/")
    context = {
        'user' : User.objects.get(id=id),
        'quote_count': Quote.objects.filter(author=id).count(),
        'quote_details' : Quote.objects.filter(author=id),
    }
    return render(request, 'belt/user_page.html', context)

def register(request):
    if request.method == 'GET':
        return redirect ('/')
    newuser = User.objects.validate(request.POST)
    print newuser
    if newuser[0] == False:
        for each in newuser[1]:
            messages.error(request, each)
        return redirect('/')
    if newuser[0] == True:
        messages.success(request, 'Well done')
        request.session['userid'] = newuser[1].id
        return redirect('/quotes')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        user = User.objects.login(request.POST)
        print user
        if user[0] == False:
            for each in user[1]:
                messages.add_message(request, messages.INFO, each)
            return redirect('/')
        if user[0] == True:
            messages.add_message(request, messages.INFO,'Welcome, You are logged in!')
            request.session['userid'] = user[1].id
            return redirect('/quotes')

def logout(request):
    if 'userid' not in request.session:
        return redirect('/')
    print "*******"
    print request.session['userid']
    del request.session['userid']
    return redirect('/')
