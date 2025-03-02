from django import forms
from .models import BlogArticle
from django.core.exceptions import ValidationError
from django.conf import settings


class BlogArticleForm(forms.ModelForm):
    class Meta:
        model = BlogArticle
        fields = ['title', 'content', 'published', 'preview', ]

    def clean_title(self):
        title = self.cleaned_data.get('title')
        cleaned_article_pk = self.instance.pk

        for forbidden_word in settings.FORBIDDEN_WORDS:
            if forbidden_word.lower() in title.lower():
                raise ValidationError('Вы использовали какие-то слова из списка запрещенных слов. '
                                      'Ознакомьтесь с данным списком и введите название статьи, не использую слова из '
                                      'него.')
        if BlogArticle.objects.filter(title=title).exclude(id=cleaned_article_pk).exists():
            raise ValidationError('Статья с таким названием уже существует.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')

        for forbidden_word in settings.FORBIDDEN_WORDS:
            if forbidden_word.lower() in content.lower():
                raise ValidationError('Вы использовали какие-то слова из списка запрещенных слов. '
                                      'Ознакомьтесь с данным списком и введите описание статьи, не использую слова из '
                                      'него.')
        return content

    def __init__(self, *args, **kwargs):
        super(BlogArticleForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите название статьи'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'id': "exampleFormControlTextarea1",
                                                    'rows': "4", 'placeholder': 'Введите описание статьи'})
        self.fields['published'].widget.attrs.update({'class': 'form-check-input', 'type': 'checkbox'})
        self.fields['preview'].widget.attrs.update({'class': 'form-control', 'type': 'file', 'id': 'formFile'})
