from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import BlogPost, Category, Comment
from .forms import BlogPostForm, SignUpForm, ProfileForm, CommentForm

class HomeView(ListView):
    model = BlogPost
    template_name = "home.html"
    paginate_by = 5

    def get_queryset(self):
        qs = BlogPost.objects.select_related("author").prefetch_related("categories")
        q = self.request.GET.get("q")
        cat = self.request.GET.get("cat")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        if cat:
            qs = qs.filter(categories__id=cat)
        return qs.distinct()

    def render_to_response(self, context, **response_kwargs):
        is_htmx = self.request.headers.get("HX-Request") == "true"
        template = "_partials/post_list_partial.html" if is_htmx else self.template_name
        return render(self.request, template, context, **response_kwargs)

class PostDetailView(DetailView):
    model = BlogPost
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    success_url = reverse_lazy("home")
    template_name = "blogpost_form.html"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    success_url = reverse_lazy("home")
    template_name = "blogpost_form.html"
    def test_func(self):
        return self.get_object().author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = "blogpost_confirm_delete.html"
    success_url = reverse_lazy("home")
    def test_func(self):
        return self.get_object().author == self.request.user

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProfileForm(instance=self.request.user)
        return context
    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect("profile")

class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(BlogPost, pk=kwargs["pk"])
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(post=post, user=request.user, body=form.cleaned_data["body"])
        return redirect(post.get_absolute_url())
