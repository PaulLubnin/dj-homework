from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Article, Scope, ScopeSetter


class ScopeSetterInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_count = 0
        for form in self.forms:
            if main_count > 1:
                raise ValidationError('Можно только одну основную категорию')
            if form.cleaned_data and form.cleaned_data['is_main']:
                main_count += 1
        if main_count == 0:
            raise ValidationError('Добавьте основную категорию')
        return super().clean()


class ScopeSetterInline(admin.TabularInline):
    model = ScopeSetter
    extra = 1
    formset = ScopeSetterInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        ScopeSetterInline,
    ]
    exclude = ('scopes',)


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass
