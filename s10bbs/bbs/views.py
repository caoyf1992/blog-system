from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from bbs import forms
from bbs import models
from django.db.models import Count
import json

from django.db.models import F
from   s10bbs import settings
import os


from bs4 import BeautifulSoup
# Create your views here.


def login(request):
    if request.method == 'POST':
        ret = {'status':0,'msg':''}
        username = request.POST.get('name')
        pwd = request.POST.get('password')
        valid_code = request.POST.get('valid_code')
        if valid_code and valid_code.upper() == request.session.get('valid_code','').upper():

            user = auth.authenticate(username=username,password=pwd)
            if user:
                auth.login(request,user)
                ret['msg'] = '/index/'
            else:
                ret['status'] = 1
                ret['msg'] = '用户名和密码错误'
        else:
            ret['status'] = 1
            ret['msg'] = '验证码错误'
        return JsonResponse(ret)
    return  render(request, 'login-old.html')


def ver(request):
    from PIL import Image,ImageDraw,ImageFont
    import random
    def sj():
        return  random.randint(0,255),random.randint(0,255),random.randint(0,255)
    width = 179
    height = 35
    im = Image.new('RGB',(width,height),sj())
    da_obj = ImageDraw.Draw(im)
    font1 = ImageFont.truetype('static/China.ttf',28)

    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65,90))
        l = chr(random.randint(97,122))
        n = str(random.randint(0,9))


        tmp = random.choice([u,l,n])
        tmp_list.append(tmp)
        da_obj.text((40*i,0),tmp,fill=sj(),font=font1)
    request.session["valid_code"] = "".join(tmp_list)
    # with open('su.png','wb') as f:
    #     im.save(f,'png')
    # with open('su.png','rb') as f:
    #     data = f.read()

    from io import BytesIO
    io_obj = BytesIO()
    im.save(io_obj,'png')
    data = io_obj.getvalue()
    return  HttpResponse(data)


def index(request):
    ret = models.Article.objects.all()
    return render(request,'index.html',{'article_list':ret})

def logout(request):
    auth.logout(request)
    return redirect("/index/")


def up(request):
    if request.method == 'POST':
        filename = request.FILES['up_file'].name
        with open(filename,'wb') as f:
            for i in request.FILES['up_file'].chunks():
                f.write(i)
    return render(request,'up-file.html')


def regis(request):
    if request.method == 'POST':
        ret = {'status': 0, 'msg': ''}
        from_obj = forms.Regrdist(request.POST)
        if from_obj.is_valid():
            from_obj.cleaned_data.pop('re_password')
            avatar_img = request.FILES.get('avatar')
            models.UserInfo.objects.create_user(**from_obj.cleaned_data,avatar=avatar_img)
            ret['msg'] = '/login/'
            return JsonResponse(ret)
        else:
            ret['status'] = 1
            ret['msg'] = from_obj.errors
            return JsonResponse(ret)
    from_obj = forms.Regrdist
    return render(request,'reg.html',{'form_obj':from_obj})



def home(request,username,*args):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse('404')
    blog = user.blog
    if not args:
        article_list = models.Article.objects.filter(user=user)
        ret = models.Category.objects.filter(blog=blog).annotate(c=Count('article')).values('title','c')

        ret1 = models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values('title','c')

        ret2 = models.Article.objects.filter(user=user).extra(
            select={'archive_time':"date_format(create_time,'%%Y-%%m')"}
        ).values('archive_time').annotate(archive=Count('nid')).values('archive_time','archive')


    else:
        if args[0] == 'category':
            article_list = models.Article.objects.filter(user=user).filter(category__title=args[1])
        elif args[0] == 'tag':
            article_list = models.Article.objects.filter(user=user).filter(tags__title=args[1])
        else:
            # 按照日期归档
            try:
                year, month = args[1].split("-")
                # logger.debug("分割得到参数year:{}, month:{}".format(year, month))
                # logger_s10.info("得到年和月的参数啦！！！！")
                # logger.debug("************************")
                article_list = models.Article.objects.filter(user=user).filter(
                    create_time__year=year, create_time__month=month
                )
            except Exception as e:
                # logger.warning("请求访问的日期归档格式不正确！！！")
                # logger.warning((str(e)))
                return HttpResponse("404")
    return render(request, 'home.html',
                  {
                      'username': username,
                      'blog': blog,
                      'article_list': article_list,
                  })






def article(request,username,pk):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse('404')
    blog = user.blog
    article_obj = models.Article.objects.filter(pk=pk).first()
    comm_obj = models.Comment.objects.filter(article_id=pk)
    print(comm_obj)
    return  render(request,'article.html',
               {
                'username':username,
                'article_obj':article_obj,
                'blog':blog,
                'comment_list':comm_obj
                }
               )


def up_down(request):
    print(request.POST)
    article_id=request.POST.get('article_id')
    is_up=json.loads(request.POST.get('is_up'))
    user=request.user
    response={"state":True}
    print("is_up",is_up)
    try:
        models.ArticleUpDown.objects.create(user=user,article_id=article_id,is_up=is_up)
        models.Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)

    except Exception as e:
        response["state"]=False
        response["fisrt_action"]=models.ArticleUpDown.objects.filter(user=user,article_id=article_id).first().is_up




    return JsonResponse(response)
    #return HttpResponse(json.dumps(response))


def pinglun(request):
    res = {}
    commtext = request.POST.get('comtext')
    acd_id = request.POST.get('acd_id')
    user_pk = request.user.pk
    pid = request.POST.get('pid')
    if not pid:
        comm_obj = models.Comment.objects.create(content=commtext,article_id=acd_id,user_id=user_pk)

    res['content'] = comm_obj.content
    res['create_time'] = comm_obj.create_time.strftime("%Y-%m-%d")
    res['username'] = comm_obj.user.username
    return HttpResponse(res)



def  edit(request):
    usernam = request.user

    aricle = models.Article.objects.filter(user=usernam)
    for i in aricle:
        print(i.create_time)
    return render(request,'edit.html',{
        'user':aricle
    })


def add_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        article_content = request.POST.get('article_content')
        user = request.user
        print(article_content)
        bs = BeautifulSoup(article_content,'html.parser')
        desc=bs.text[0:150]+'...'
        for tag in bs.find_all():
            if tag.name in ['script']:
                tag.decompose()

        article_obj = models.Article.objects.create(user=user,title=title,desc=desc)
        models.ArticleDetail.objects.create(content=str(bs),article=article_obj)
        return redirect('/blog/edit/')
    return render(request,'add_blog.html')



def upload(request):
    print(request.FILES)
    obj = request.FILES.get("upload_img")

    path=os.path.join(settings.MEDIA_ROOT,"add_article_img",obj.name)

    with open(path,"wb") as f:
        for line in obj:
            f.write(line)


    res={
        "error":0,
        "url":"/media/add_article_img/"+obj.name
    }


    return HttpResponse(json.dumps(res))


def dele(request):
    del_id = request.GET.get('nid')
    print(del_id)
    models.Article.objects.get(nid=del_id).delete()
    return redirect('/blog/edit/')