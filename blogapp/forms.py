from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='本名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'お名前を書いてね'})
    )
    email = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'メールアドレスを書いてね'})
    )
    title = forms.CharField(
        max_length=100,
        label='タイトル',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'タイトルを書いてね'})
    )
    message = forms.CharField(
        label='メッセージ',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'メッセージを書いてね', 'rows': 5})
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # 対応するモデル
        fields = ['title', 'content']  # フォームに表示するフィールド
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': 'タイトルを入力してください',
        #     }),
        #     'content': forms.Textarea(attrs={
        #         'class': 'form-control',
        #         'rows': 5,
        #         'placeholder': '内容を入力してください',
        #     }),
        # }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']