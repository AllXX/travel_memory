from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Blog,Like,Comment, Account
from .form import BlogForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView,View,UpdateView,DetailView,TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy



# Create your views here.

#ブログトップページ
def blog(request):
    
    if 'old' in request.GET:
        blogs = Blog.objects.order_by('registerd_at')
        
        paginator = Paginator(blogs, 9)
        page = request.GET.get('page', 1)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(1)

        context = {
            'pages':pages,
            'blogs': blogs,
            'Username': request.user,
            }
        if request.user.is_authenticated:
            account = Account.objects.get(user = request.user)
            add1 = {'account':account,}
            context.update(add1)
            
        return render(request, "blog/blog.html", context)

    else:
        blogs = Blog.objects.order_by('-registerd_at')
        paginator = Paginator(blogs, 9)
        page = request.GET.get('page', 1)
        
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(1)

        context = {
            'pages':pages,
            'blogs': blogs,
            'Username': request.user,
            }
        if request.user.is_authenticated:
            account = Account.objects.get(user = request.user)
            add1 = {'account':account,}
            context.update(add1)
        return render(request, "blog/blog.html", context)

    
#ブログ投稿機能
class BlogCreate(CreateView):
    form_class = BlogForm
    model = Blog

    template_name = "blog/blog_form.html"
    success_url = reverse_lazy('blog:blog')

    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        context.update({'Username':self.request.user})
        if self.request.user.is_authenticated:
            account = Account.objects.get(user = self.request.user)
            add1 = {'account':account,}
            context.update(add1)
        return context
    
    def form_valid(self, form):
        form_instance = form.save(commit=False)
        form_instance.user = self.request.user
        form_instance.save()

        return super().form_valid(form)


#ブログ詳細機能
class BlogDetail(DetailView):
    template_name = 'blog/blog_detail.html'
    model = Blog
    
    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        like_count = self.object.like_set.count()
        blog_pk = self.kwargs.get('pk')
        comment = Comment.objects.filter(blog=blog_pk)
        context.update({'Username':self.request.user,'comment_form':CommentForm,'comment':comment,
        'like_count':like_count})
        if self.request.user.is_authenticated:
            account = Account.objects.get(user = self.request.user)
            add1 = {'account':account,}
            context.update(add1)
        if  self.request.user.is_authenticated:
            #ログイン中のユーザーがいいねしているかどうか
            if self.object.like_set.filter(user=self.request.user).exists():
                context['is_user_liked_for_post'] = True
            else:
                context['is_user_liked_for_post'] = False
            return context
        else:
            return context


#ブログ編集機能
class BlogEdit(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_edit.html'
    success_url = reverse_lazy('blog:blog')

    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        account = Account.objects.get(user = self.request.user)
        context.update({'account':account, 'Username':self.request.user})
        return context

    def form_valid(self, form):
        form_instance = form.save(commit=False)
        form_instance.user = self.request.user
        form_instance.save()

        return super().form_valid(form)


#ブログ削除機能
class BlogDelete(View):

    def post(self, request, pk, *args, **kwargs):

        blog =  Blog.objects.get(id=pk)
        if blog:
            print('削除')
            blog.delete()
        else:
            print('対象のデータは見つかりませんでした。')
            
        return redirect('blog:blog')


class CommentCreate(CreateView):
    """
    記事へのコメント作成ビュー
    ページは表示されないが、コメントを作成するために使用
    """
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        blog_pk = self.kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=blog_pk)
        username = self.request.user

        comment = form.save(commit=False)
        comment.user = username
        comment.blog = blog
        comment.save()

        return redirect('blog:detail', pk=blog_pk)

#どうして405エラーになるのか不明
# class CommentDelete(View):

#     def post(self, request, pk, *args, **kwargs):

#         comment =  Comment.objects.get(id=pk)
#         if comment:
#             print('削除')
#             comment.delete()
#         else:
#             print('対象のデータは見つかりませんでした。')
            
#         return redirect('blog:blog')

def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    blog_pk = comment.blog.pk
    comment.delete()
    return redirect('blog:detail',pk=blog_pk)

#いいね機能
def like(request):
    post_pk = request.POST.get('post_pk')
    post = get_object_or_404(Blog,pk=post_pk)
    context = {}
    like = Like.objects.filter(blog= post, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(blog=post, user=request.user)
        context['method'] = 'create'

    context['like_count'] = post.like_set.count()

    return JsonResponse(context)