from django.shortcuts import render, redirect
from django.urls import reverse
from httpx import post
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from apps.models import *


def home(request):
    users = User.objects.first()
    skills = Skills.objects.all()
    services = Service.objects.all()
    priz = Priz.objects.all()
    portfolio = Portfolio.objects.all()
    blogs = Blog.objects.all()
    blogSingle = BlogSingle.objects.all()
    blog = Blog.objects.first()
    users = User.objects.first()
    opinions = Opinion.objects.all()
    return render(
        request,
        "index.html",
        {
            "user": users,
            "skills": skills,
            "services": services,
            "prizs": priz,
            "portfolios": portfolio,
            "blogs": blogs,
            "blogSingle": blogSingle,
            "blog": blog,
            "users": users,
            "opinions": opinions
        },
    )


def PortfolioDetailsView(request, id):
    portfolios = Portfolio.objects.all()
    portfolio = Portfolio.objects.filter(id=id).first()
    
    return render(
        request,
        "portfolio-details.html",
        {"portfolio": portfolio, "portfolios": portfolios},
    )


def BlogSingleView(request,id):
    blog_single = BlogSingle.objects.all()
    blog_single = BlogSingle.objects.filter(id=id).first()
    
    return render(
        request,
        "blog-single.html",
        {"blog_single": blog_single, "blog_single": blog_single},
    )
    

def commentfunc(request, pk):
    blog = Blog.objects.filter(id=pk).first()
    personal_info = User.objects.first()
    if not blog:
        return redirect("error_page")

    if request.POST:
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        post_id = pk
        text = request.POST.get("text")
        if fullname and post_id and text and email:
            Comment.objects.create(
                fullname=fullname, email=email, post_id_id=post_id, text=text
            )
            return redirect(reverse("post", args=(pk,)))

    searchs = ""
    if request.GET:
        key = request.GET.get("s")
        searchs = BlogSingle.objects.filter(title__contains=key)

    comments = Comment.objects.filter(post_id=pk).order_by("created_at")
    return render(
        request,
        "blog-single.html",
        {
            "comments": comments,
            "searchs": searchs,
            "blog": blog,
            "personal_info": personal_info,
        },
    )