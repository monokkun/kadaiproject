from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLogoutView

# URLconfのURLパターンを逆引きできるようにアプリ名を登録
app_name = 'blogapp'

# URLパターンを登録するためのリスト
urlpatterns = [
    # http(s)://ホスト名/以下のパスが''(無し)の場合
    # viewsモジュールのIndexViewを実行
    # URLパターン名は'index'
    path('', views.IndexView.as_view(), name='index'),

    path('resume/', views.ResumeView.as_view(), name='resume'),

    path('contact/', views.ContactView.as_view(), name='contact'),

    path('posts/', views.Post_List.as_view(), name='post_list'),

    path('contact/success/', views.ContactSuccessView.as_view(template_name="contact_success.html"), name='contact_success'),

    path('posts/<int:pk>/', views.post_detail, name='post_detail'),

    path('posts/<int:pk>/add_comment/', views.Add_Comment.as_view(), name='add_comment'),

    path('posts/new/', views.Post_Form.as_view(), name='post_form'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

]