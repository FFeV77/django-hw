from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scopes, Tag


class ArticleInlineFormset(BaseInlineFormSet):

    def clean(self):
        chosen_main = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                chosen_main += 1
        if not chosen_main:
            raise ValidationError('Укажите основной раздел')
        elif chosen_main > 1:
            raise ValidationError('Основным может быть только один раздел')
        return super().clean()  # вызываем базовый код переопределяемого метода

class ArticleInline(admin.TabularInline):
    model = Scopes
    formset = ArticleInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

