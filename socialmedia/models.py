import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class User(AbstractUser, TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(TimeStampedModel):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(
        max_length=100, choices=GENDER_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return self.user.email


class Post(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)
    content = models.TextField()
    image = models.ImageField(upload_to="post_image/", null=True, blank=True)
    user = models.ForeignKey(
        User, related_name="post", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post, related_name="comment", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    comment = models.TextField(max_length=200)

    def __str__(self):
        return self.comment


class Like(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_likes"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_likes"
    )

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user} likes {self.post.title}"


class Follow(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user"
    )
    user_following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_following"
    )

    class Meta:
        unique_together = ("user", "user_following")

    def __str__(self):
        return f"{self.user.email} follows {self.user_following.email}"
