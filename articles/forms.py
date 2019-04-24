from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 4, 'cols': 50}))

    class Meta:
        model = Article
        fields = ["title", "body"]
