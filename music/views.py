from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

# Create your views here.

@login_required
def ReplyView(request, pk):
    data = Category.objects.all()
    obj = Review.objects.get(id=pk)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            add = form.save(commit=False)
            add.writer = request.user
            add.music = obj.music
            add.parent = obj
            add.save()
            messages.success(request, 'review reply success')
            return redirect(reverse('detail', args=[obj.music.pk]))
    return render(request, 'reply.html', {'form':form, 'data':data, 'obj':obj})

def DelView(request, pk):
    obj = Review.objects.get(id=pk)
    obj.delete()
    messages.success(request, 'review delete success')
    return redirect(reverse('detail', args=[obj.music.pk]))

def DetailView(request, pk):
    data = Category.objects.all()
    obj = Music.objects.get(id=pk)
    review_c = Review.objects.filter(music=obj).count()
    post = Review.objects.filter(music=obj).order_by('-date')
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and not form.is_valid():
        obj.likes += 1
        obj.save()
        messages.success(request, 'music like success')
        return redirect(reverse('detail', args=[obj.pk]))
    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid:
                add = form.save(commit=False)
                add.writer = request.user
                add.music = obj
                add.save()
                messages.success(request, 'review added successfully')
                return redirect(reverse('detail', args=[obj.pk]))
        else:
            return redirect(f'/account/login/?next=/music/detail/{obj.pk}/')
    return render(request, 'detail.html', {'data':data, 'obj':obj, 'review_c':review_c, 'post':post, 'form':form})

def RegisterView(request):
    data = Category.objects.all()
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'user created successfully. now log in')
            return redirect('login')
    return render(request, 'registration/register.html', {'form':form, 'data':data})

@login_required
def ReportView(request):
    data = Category.objects.all()
    form = ReportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Report successful. A mail will be sent to you')
            return redirect('home')
    return render(request, 'report.html', {'form':form, 'data':data})

def HotView(request):
    obj = Music.objects.order_by('-likes')[:10]
    data = Category.objects.all()
    return render(request, 'hot.html', {'obj':obj, 'data':data})

def CategoryView(request, area):
    cat = Category.objects.get(area=area)
    obj = Music.objects.filter(category__area=area).order_by('-date')
    obj_c = Music.objects.filter(category__area=area).order_by('-date').count()
    data = Category.objects.all()
    return render(request, 'category.html', {'obj':obj, 'data':data, 'obj_c':obj_c, 'cat':cat})

def UserSearchView(request, singer):
    obj = Music.objects.filter(Q(singer__icontains=singer)).order_by('-date')
    obj_c = Music.objects.filter(Q(singer__icontains=singer)).order_by('-date').count()
    data = Category.objects.all()
    return render(request, 'search.html', {'obj':obj, 'data':data, 'obj_c':obj_c})

def SearchView(request):
    q = request.POST.get('q') if request.POST.get('q') != None else ''
    obj = Music.objects.filter( Q(category__area__icontains=q) | Q(title__icontains=q) | Q(singer__icontains=q)).order_by('-date')
    obj_c = Music.objects.filter( Q(category__area__icontains=q) | Q(title__icontains=q) | Q(singer__icontains=q)).order_by('-date').count()
    data = Category.objects.all()
    return render(request, 'search.html', {'obj':obj, 'data':data, 'obj_c':obj_c})

def HomeView(request):
    obj = Music.objects.order_by('-date')[:10]
    data = Category.objects.all()
    return render(request, 'home.html', {'obj':obj, 'data':data})
