from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, BlogPost, Comment,Category

class SignUpForm(UserCreationForm):
    # require an emal on signup
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
        # exclude the M2M widget, handle categories manually
        fields = ('title', 'content', 'categories_input')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing an existing post, prefill categories_input with current names
        if self.instance.pk:
            existing = ', '.join(cat.name for cat in self.instance.categories.all())
            self.fields['categories_input'].initial = existing

    def save(self, commit=True):
        # Save the core fields
        instance = super().save(commit=False)
        if commit:
            # Persist the BlogPost instance to get a pk
            instance.save()
            # Split, strip, and filter out any blank names
            raw_names = self.cleaned_data['categories_input']
            cat_names = [name.strip() for name in raw_names.split(',') if name.strip()]
            # For each name, get existing or create a new Category
            cats = []
            for name in cat_names:
                cat, created = Category.objects.get_or_create(name=name)
                cats.append(cat)
            # Replace any existing categories with the new set
            instance.categories.set(cats)
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)