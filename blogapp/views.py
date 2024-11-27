from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
# django.views.generic.baseからTemplateViewをインポート
from django.views.generic.base import TemplateView
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm
from django.views.generic import CreateView,ListView,FormView
from django.urls import reverse_lazy


class IndexView(TemplateView):
    '''トップページのビュー

    テンプレートのレンダリングに特化したTemplateViewを継承

    Attributes:s
        template_name: レンダリングするテンプレート
    '''
    # index.htmlをレンダリングする
    template_name = 'index.html'


class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()  # ContactFormをテンプレートに渡す
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            # フォームのデータを取得
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            title = form.cleaned_data['title']
            message = form.cleaned_data['message']

            # メール送信の設定
            subject = f"{title} - お問い合わせ from {name}"
            full_message = f"名前: {name}\nメール: {email}\n\nメッセージ:\n{message}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]

            # メール送信
            send_mail(subject, full_message, from_email, recipient_list)

            # 成功時にリダイレクト
            return redirect('blogapp:contact_success')

        # フォームにエラーがある場合は再表示
        return render(request, self.template_name, {'form': form})


class ContactSuccessView(TemplateView):
    template_name = 'contact_success.html'

class Post_List(ListView):
    template_name = 'post_list.html'
    model = Post  # 表示するモデルを指定
    context_object_name = 'posts'  # テンプレートで使用する変数名（任意）
    # def post_list(request, pk=None):
    #     posts = Post.objects.all().order_by('-created_at')
    #     return render(request, 'blogapp/templates/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

# class Post_Form(CreateView):
#     template_name = 'post_form.html'
#     @login_required
#     def post_create(request):
#         if request.method == "POST":
#             form = PostForm(request.POST)
#             if form.is_valid():
#                 post = form.save(commit=False)  # モデルのインスタンスを作成（まだ保存しない）
#                 post.author = request.user  # 投稿者を現在のユーザーに設定
#                 post.save()  # データベースに保存
#                 return redirect('post_list')  # 投稿一覧ページにリダイレクト
#         else:
#             form = PostForm()

#         return render(request, 'blogapp/templates/post_form.html', {'form': form})
class Post_Form(CreateView):
    model = Post  # 対応するモデルを指定
    form_class = PostForm  # 使用するフォームクラス
    template_name = 'post_form.html'  # 使用するテンプレート
    success_url = reverse_lazy('blogapp:post_list')  # 成功後のリダイレクト先
    def form_valid(self, form):
        form.instance.author = self.request.user  # ログイン中のユーザーを設定
        return super().form_valid(form)

# class Add_Comment(FormView):
#     model = Comment  # 対応するモデルを指定
#     form_class = CommentForm  # 使用するフォームクラス
#     template_name = 'comment_form.html'  # 使用するテンプレート
#     success_url = reverse_lazy('blogapp:post_list')  # 成功後のリダイレクト先
#     def form_valid(self, form):
#         form.instance.author = self.request.user  # ログイン中のユーザーを設定
#         return super().form_valid(form)

class ResumeView(TemplateView):
    template_name = 'resume.html'
    def register(request):
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'アカウントが作成されました: {username}')
                return redirect('login')  # ログインページにリダイレクト
        else:
            form = UserRegisterForm()
        return render(request, 'blogapp/templates/logout.html', {'form': form})

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class SignupView(TemplateView):
    template_name = 'signup.html'
    def signup(request):
        if request.method == "POST":
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()  # ユーザーを保存
                login(request, user)  # 登録後に自動的にログイン
                messages.success(request, 'アカウントが作成されました！')
                return redirect('post_list')  # 任意のリダイレクト先
        else:
            form = UserRegisterForm()

        return render(request, 'templates/signup.html', {'form': form})

class PostDetail(ListView):
    template_name = 'post_detail.html'
    model = Comment

class Add_Comment(FormView):
    template_name = 'comment_form.html'
    form_class = CommentForm

    def form_valid(self, form):
        # 投稿を取得
        post = get_object_or_404(Post, pk=self.kwargs['pk'])

        # コメントオブジェクトを作成
        form.instance.post = post
        form.instance.author = self.request.user  # ログインユーザーを設定
        form.save()  # コメントを保存

        # 投稿詳細ページにリダイレクト
        return redirect('blogapp:post_list')