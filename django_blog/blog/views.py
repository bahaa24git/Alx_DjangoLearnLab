from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Post, Comment, Tag
from .forms import RegisterForm, ProfileForm, PostForm, CommentForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('blog:post_list')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can log in now.")
            return redirect('blog:login')
    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {"form": form})

@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Email updated successfully.")
            return redirect('blog:profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'blog/profile.html', {"form": form})
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        resp = super().form_valid(form)     # self.object now exists
        self._save_tags(form)               # attach tags
        return resp

    def _save_tags(self, form):
        raw = form.cleaned_data.get("tags_input", "")
        names = [n.strip() for n in raw.split(",") if n.strip()]
        tag_objs = [Tag.objects.get_or_create(name=name)[0] for name in names]
        self.object.tags.set(tag_objs)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        resp = super().form_valid(form)
        self._save_tags(form)
        return resp

    def _save_tags(self, form):
        raw = form.cleaned_data.get("tags_input", "")
        names = [n.strip() for n in raw.split(",") if n.strip()]
        tag_objs = [Tag.objects.get_or_create(name=name)[0] for name in names]
        self.object.tags.set(tag_objs)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")

    def test_func(self):
        return self.get_object().author == self.request.user
    

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comments"] = self.object.comments.select_related("author").all()
        ctx["comment_form"] = CommentForm()
        return ctx

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"  # fallback if someone hits GET or invalid POST

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, "Comment added.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.post.pk})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Comment deleted.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.post.pk})


# --- NEW: filter posts by tag ---
class TagPostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag_name = self.kwargs["tag_name"]
        return (
            Post.objects.filter(tags__name__iexact=tag_name)
            .select_related("author")
            .order_by("-published_date")
            .distinct()
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_tag"] = self.kwargs["tag_name"]
        return ctx

# --- NEW: search posts by title/content/tags ---
class PostSearchView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        q = (self.request.GET.get("q") or "").strip()
        qs = Post.objects.all()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(tags__name__icontains=q)
            ).distinct()
        return qs.order_by("-published_date")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["query"] = (self.request.GET.get("q") or "").strip()
        return ctx