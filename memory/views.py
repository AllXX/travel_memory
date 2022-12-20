from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, View, UpdateView, DetailView
from .forms import AccountForm, AddAccountForm, PostForm, GeoForm,MemoryImageForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from .models import Memory, Geo, Account, User, MemoryImage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
import json
from decimal import Decimal
from django.db.models import Count
from django.contrib import messages
from django.core import serializers
from django.db.models import Max


# Create your views here.


# 新規登録
class AccountRegistration(TemplateView):

    def __init__(self):
        self.params = {
            "AccountCreate": False,
            "account_form": AccountForm(),
            "add_account_form": AddAccountForm(),
        }

    # Get処理
    def get(self, request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm(data=request.POST)
        self.params["AccountCreate"] = False
        return render(request, 'memory/signup.html', context=self.params)

    def post(self, request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)

        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()

            # 下記操作のため、コミットなし
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1　紐づけ
            add_account.user = account

            # 画像アップロード有無検証
            if 'image' in request.FILES:
                add_account.image = request.FILES['image']

            # モデル保存
            add_account.save()

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効ではない場合
            messages.warning(request, 'すでにユーザー名が使われています。')
            print(self.params["account_form"].errors)


        return render(request, "memory/signup.html", context=self.params)

# ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        Username = request.POST.get('username')
        Pass = request.POST.get('password')

        # djangoの認証機能
        user = authenticate(username=Username, password=Pass)

        # ユーザー認証
        if user:
            # ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request, user)
                # 　ホームページ遷移
                return HttpResponseRedirect(reverse('memory:home'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証機能失敗
        else:
            messages.warning(request, 'パスワードが正しくありません。')
            return render(request, "memory/login.html")

    # GET
    else:
        return render(request, 'memory/login.html')


# ログアウト
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('memory:home'))


# ホーム
@login_required(login_url='memory:how-to-use')
def home(request):
    geos = Geo.objects.filter(memory__account = request.user)

    geos = list(geos.values())
    # geos = list(geos.annotate(Count('memory_id')))
    account = Account.objects.get(user = request.user)
    memory = Memory.objects.filter(account = request.user)
    data = serializers.serialize('json',memory)

    def decimal_default_proc(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError

    context = {"Username": request.user,'memory':data,'geos':json.dumps(geos,default=decimal_default_proc),'account':account}
    return render(request, "memory/index.html", context)


# 思い出記録
# class MemoryHome(LoginRequiredMixin, TemplateView):
#     template_name = 'memory/memory.html'
#     login_url = reverse_lazy('memory:login')

@login_required(login_url='memory:how-to-use') 
def memory(request):
    
    if 'old' in request.GET:
        memorys = Memory.objects.filter(
        account=request.user).order_by('date')
        account = Account.objects.get(user = request.user)
        paginator = Paginator(memorys, 9)
        page = request.GET.get('page', 1)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(1)

        context = {
            'pages':pages,
            'memorys': memorys,
            'Username': request.user,
            'account':account,}
        return render(request, "memory/memory.html", context)

    else:
        memorys = Memory.objects.filter(
        account=request.user).order_by('-date')
        account = Account.objects.get(user = request.user)
        paginator = Paginator(memorys, 9)
        page = request.GET.get('page', 1)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(1)

        context = {
            'pages':pages,
            'memorys': memorys,
            'Username': request.user,
            'account':account,}
        return render(request, "memory/memory.html", context)


# 思い出投稿機能
class MemoryCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    form_class2 = GeoForm
    model = Memory

    template_name = "memory/memory_form.html"
    login_url = reverse_lazy('memory:login')
    success_url = reverse_lazy('memory:memory')

    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        account = Account.objects.get(user = self.request.user)
        form2 = self.form_class2(self.request.GET or None)
        context.update({'form2': form2, 'Username': self.request.user,'account':account})
        return context

    def form_valid(self, form):
        form2 = self.form_class2(self.request.POST or None)
    
        form_instance = form.save(commit=False)
        form_instance.account = self.request.user
    
        form_instance.save()

        #複数画像の保存
        images = self.request.FILES.getlist("image")

        for image in images:
            upload_image_file = {"image":image}
            upload_image_name = {"memory":form_instance.id,"image":str(image)}

            form3 = MemoryImageForm(upload_image_name,upload_image_file)

            if form3.is_valid():
                form3.save()
            else:
                print(form3.errors)
        
        form_instance2 = form2.save(commit=False)
        pk = Memory.objects.get(pk=form_instance.pk)
        form_instance2.memory = pk
        form_instance2.save()

        return super().form_valid(form)

#思い出削除機能
class MemoryDelete(View):

    def post(self, request, pk, *args, **kwargs):

        memory =  Memory.objects.filter(id=pk)
        if memory:
            print('削除')
            memory.delete()
        else:
            print('対象のデータは見つかりませんでした。')
            
        return redirect('memory:memory')

delete = MemoryDelete.as_view()

#思い出編集機能
class MemoryEdit(LoginRequiredMixin, UpdateView):
    
    model = Memory
    form_class = PostForm
    form_class2 = GeoForm
    template_name = 'memory/edit.html'
    login_url = reverse_lazy('memory:login')


    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        account = Account.objects.get(user = self.request.user)
        pk = self.kwargs.get('pk')
        memory = Memory.objects.get(pk = pk)
        obj = Geo.objects.filter(memory = memory.pk).last()
        values = {'ken':obj.ken, 'lat':obj.lat,'lng':obj.lng}
        form2 = self.form_class2(self.request.GET or values)
        context.update({'form2': form2, 'Username': self.request.user,'account':account,})
        return context

    def form_valid(self, form):
        form_instance = form.save(commit=False)
        form_instance.account = self.request.user
        form_instance.save()

        # geoテーブルの既存レコードの編集
        form2 = self.form_class2(self.request.POST)
        pk = self.kwargs.get('pk')
        memory = Memory.objects.get(pk = pk)
        obj = Geo.objects.filter(memory = memory.pk).last()
        id = obj.id

        form_instance2 = form2.save(commit=False)
        form_instance2.memory = memory
        form_instance2.id = id
        form_instance2.save()

        return super().form_valid(form)


#思い出詳細機能
class MemoryDetail(generic.DetailView):
    template_name = 'memory/detail.html'
    model = Memory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = Account.objects.get(user = self.request.user)
        pk = self.kwargs.get('pk')
        memory = Memory.objects.get(pk = pk)
        geo = Geo.objects.filter(memory = memory.pk).last()
        geo_list = [geo.lat,geo.lng]
        def decimal_default_proc(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            raise TypeError
        images = MemoryImage.objects.filter(memory = memory.pk)


        context.update({'account':account,'Username': self.request.user,'geo':json.dumps(geo_list,default=decimal_default_proc),'images':images,})
        return context


#プロフィール機能
def profile(request):
    account = Account.objects.get(user=request.user)
    geo  = Geo.objects.filter(memory__account = request.user).values('ken').annotate(total= Count('ken')).order_by('-total').first()
    memory_num = Memory.objects.filter(account=request.user).count()
    context = {"account":account,'Username':request.user,'memory_num':memory_num,'geo':geo,}
    return render(request, 'memory/account.html',context)

def mymap(request):
    pass


def howtouse(request):
    return render(request,'memory/howtouse.html')

def rule(request):
    return render(request,'memory/rule.html')

def policy(request):
    return render(request,'memory/policy.html')