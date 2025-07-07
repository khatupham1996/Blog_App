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
    # Model to list
    model = BlogPost
    # Template for initial full-page render
    template_name = "home.html"
    # NUmber of posts per page
    paginate_by = 5

    def get_queryset(self):
        # Optimaize DB queries
        qs = BlogPost.objects.select_related("author").prefetch_related("categories")
        # Search term
        q = self.request.GET.get("q")
        # Category filter
        cat = self.request.GET.get("cat")
        if q:
            # Filter title or content containing search term
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        if cat:
            # Filter posts belonging to selected category ID
            qs = qs.filter(categories__id=cat)
        return qs.distinct()

    def render_to_response(self, context, **response_kwargs):
        # Check for HTMX request header
        is_htmx = self.request.headers.get("HX-Request") == "true"
        # Choose a smaller partial template for HTMX, otherwise use full page
        template = "_partials/post_list_partial.html" if is_htmx else self.template_name
        return render(self.request, template, context, **response_kwargs)

class PostDetailView(DetailView):
    # Model to fetch
    model = BlogPost
    # Template for post detail
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        # Base context includes 'object'
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    # Model to create
    model = BlogPost
    # Use our custom form
    form_class = BlogPostForm
    # Redirect to home on success
    success_url = reverse_lazy("home")
    # Template for form
    template_name = "blogpost_form.html"
    def form_valid(self, form):
        # Set the current user as author
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # Model to update
    model = BlogPost
    # Use custom form
    form_class = BlogPostForm
    # Redirect after update
    success_url = reverse_lazy("home")
    # Template for form
    template_name = "blogpost_form.html"
    def test_func(self):
        # return True if current user authored the post
        return self.get_object().author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # Model to delete
    model = BlogPost
    # Confirmation template
    template_name = "blogpost_confirm_delete.html"
    # Redirect after deletion
    success_url = reverse_lazy("home")
    def test_func(self):
        # True if current user authored the pos
        return self.get_object().author == self.request.user

class SignUpView(CreateView):
    # Use signup form
    form_class = SignUpForm
    # Template for signup page
    template_name = "registration/signup.html"
    # Redirect to login on success
    success_url = reverse_lazy("login")

class ProfileView(LoginRequiredMixin, TemplateView):
    # Template for profile page
    template_name = "profile.html"
    def get_context_data(self, **kwargs):
        # Base context
        context = super().get_context_data(**kwargs)
        # Prefill form with current user
        context["form"] = ProfileForm(instance=self.request.user)
        return context
    def post(self, request, *args, **kwargs):
        # Bind form to posted data and files
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Save changes to user profile
            form.save()
        # Redirect back to profile page
        return redirect("profile")

class AddCommentView(LoginRequiredMixin, CreateView):
    # Model to create
    model = Comment
    # Use comment form
    form_class = CommentForm
    def post(self, request, *args, **kwargs):
        # Fetch target post or 404
        post = get_object_or_404(BlogPost, pk=kwargs["pk"])
        # Bind form to POST data
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create comment linked to post and current user
            Comment.objects.create(post=post, user=request.user, body=form.cleaned_data["body"])
        return redirect(post.get_absolute_url())
