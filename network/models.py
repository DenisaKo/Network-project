from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    following = models.ManyToManyField(User, related_name="followers", symmetrical=False, blank=True)

    def serialize(self):
        return {
            "id": self.user.id,
            "user_id": self.user.id,
            "user_username": self.user.username,
            "image": self.image,
            "bio": self.bio,
            "following": [user.username for user in self.following.all()],
            "followers": [user.user.username for user in Profil.objects.filter(following=self.user.id)],
        }


class Post(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    body_text = models.CharField(max_length=500)
    likes = models.ManyToManyField(User, related_name = 'liked_posts', blank=True)

    class Meta:
        ordering = ['-timestamp']

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.id,
            "sender_name": self.sender.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "body_text": self.body_text,
            "likes": [user.id for user in self.likes.all()],
            'likes_count': self.likes.all().count(),
            'comments': [com.serialize() for com in self.post_comments.all()]
        }

    
class Comment(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    timestamp = models.DateTimeField(auto_now_add=True)
    body_text = models.CharField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")

    class Meta:
        ordering = ['-timestamp']

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.id,
            "post_id": self.post.id,
            "sender_name": self.sender.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "body_text": self.body_text,
        }
    