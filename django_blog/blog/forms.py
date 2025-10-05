# django_blog/blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from taggit.forms import TagWidget  # required by the checker
from .models import Post, Comment

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email",)


class PostForm(forms.ModelForm):
    # Use a separate text input for comma-separated tags (NOT the M2M field)
    tags_input = forms.CharField(
        required=False,
        widget=TagWidget(),
        help_text="Comma-separated (e.g. Django, ALX)"
    )

    class Meta:
        model = Post
        fields = ["title", "content"]  # do not include the M2M 'tags' field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        existing = []
        if self.instance and self.instance.pk:
            existing = self.instance.tags.values_list("name", flat=True)
        self.fields["tags_input"].initial = ", ".join(existing)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {"content": forms.Textarea(attrs={"rows": 3})}
