from django.contrib.auth.models import AbstractUser
from django.db import models


def profile_upload_path(instance, filename):
    return f"profiles/{instance.username}/{filename}"


class User(AbstractUser):
    bio = models.TextField(blank=True, default="")
    # You can switch to URLField if you prefer to avoid media/Pillow setup:
    # profile_picture = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=profile_upload_path, blank=True, null=True)

    # A user can follow many other users; no reciprocal implied
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
    )

    def __str__(self):
        return self.username


class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profiles/", blank=True, null=True)

    # Users this user is following
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
    )

    def follow(self, other: "User") -> bool:
        if other == self:
            return False
        self.following.add(other)
        return True

    def unfollow(self, other: "User") -> None:
        self.following.remove(other)

    def is_following(self, other: "User") -> bool:
        return self.following.filter(pk=other.pk).exists()

    @property
    def followers_count(self) -> int:
        return self.followers.count()

    @property
    def following_count(self) -> int:
        return self.following.count()
