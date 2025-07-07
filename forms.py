from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, BlogPost, Comment,Category

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("bio", "avatar")
        widgets = {
            "avatar": forms.FileInput(attrs={"class": "border p-2 rounded"}),
        }


class BlogPostForm(forms.ModelForm):
    # Allow users to type comma-separated categories
    categories_input = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Comma-separated categories',
                'class': 'border p-2 rounded w-full'
            }
        ),
        help_text='Enter categories separated by commas; existing ones will be reused.'
    )

    class Meta:
        model = BlogPost
        # exclude the M2M widget; we'll handle categories via categories_input
        fields = ('title', 'content', 'categories_input')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate categories_input with existing names on edit
        if self.instance.pk:
            existing = ', '.join(cat.name for cat in self.instance.categories.all())
            self.fields['categories_input'].initial = existing

    def save(self, commit=True):
        # Save the core fields
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Parse and assign categories
            cat_names = [name.strip() for name in self.cleaned_data['categories_input'].split(',') if name.strip()]
            cats = []
            for name in cat_names:
                cat, _ = Category.objects.get_or_create(name=name)
                cats.append(cat)
            instance.categories.set(cats)
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)