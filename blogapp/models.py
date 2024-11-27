from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)  # タイトル
    content = models.TextField()  # 内容
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 投稿者

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return f'Comment by {self.content} on {self.author}'