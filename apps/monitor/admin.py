from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models
from django.forms import TextInput
from .models import Comment, UserForm, LeadStatus, LeadSupport, Portfolio
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Portfolio)


class CommentInline(GenericTabularInline):
    model = Comment
    extra = 1
    fields = ('content',)
    can_delete = True
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10'})},
    }
    classes = ['collapse']

    def has_delete_permission(self, request, obj=None):
        return True


class AdminChangeHistoryMixin:
    def view_change_history(self, obj):
        history_url = reverse(
            'admin:%s_%s_history' % (obj._meta.app_label, obj._meta.model_name),
            args=(obj.pk,)
        )
        return format_html('<a href="{}">Просмотр истории</a>', history_url)
    view_change_history.short_description = 'История изменений'


class LeadStatusInline(admin.TabularInline):
    model = LeadStatus
    extra = 1
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10'})},
    }
    classes = ['collapse']


class LeadSupportInline(admin.TabularInline):
    model = LeadSupport
    extra = 1
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10'})},
    }
    classes = ['collapse']


@admin.register(UserForm)
class UserFormAdmin(AdminChangeHistoryMixin, admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'status')
    list_filter = ('status', 'updated_at', 'created_at')
    search_fields = ('name', 'phone', 'email')
    ordering = ('-created_at',)
    inlines = [LeadStatusInline, LeadSupportInline, CommentInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, (Comment, LeadStatus, LeadSupport)) and request.user.is_authenticated:
                if not instance.pk:
                    instance.author = request.user
                instance.save()
        formset.save_m2m()
        for obj in formset.deleted_objects:
            if isinstance(obj, (Comment, LeadStatus, LeadSupport)):
                obj.delete()


@admin.register(LeadStatus)
class LeadStatusAdmin(AdminChangeHistoryMixin, admin.ModelAdmin):
    list_display = ('lead', 'contract', 'design', 'back', 'front', 'testing', 'mvp')
    list_filter = ('mvp',)
    search_fields = ('lead__name', 'contract', 'design', 'back', 'front', 'testing')
    ordering = ('lead',)
    inlines = [CommentInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Comment) and not instance.pk and request.user.is_authenticated:
                instance.author = request.user
                instance.save()
        formset.save_m2m()
        for obj in formset.deleted_objects:
            if isinstance(obj, Comment):
                obj.delete()


@admin.register(LeadSupport)
class LeadSupportAdmin(AdminChangeHistoryMixin, admin.ModelAdmin):
    list_display = ('lead', 'testing', 'updating')
    search_fields = ('lead__name',)
    ordering = ('-updating',)
    inlines = [CommentInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Comment) and not instance.pk and request.user.is_authenticated:
                instance.author = request.user
                instance.save()
        formset.save_m2m()
        for obj in formset.deleted_objects:
            if isinstance(obj, Comment):
                obj.delete()
                Comment.objects.filter(object_id=obj.pk, content_type__model=obj._meta.model_name.lower()).delete()
                obj.delete()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    inlines = [CommentInline]

    def delete_model(self, request, obj):
        Comment.objects.filter(object_id=obj.pk, content_type__model=obj._meta.model_name.lower()).delete()
        obj.delete()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, (Comment, LeadStatus, LeadSupport)) and request.user.is_authenticated:
                if not instance.pk:
                    instance.author = request.user
                instance.save()
        formset.save_m2m()
        for obj in formset.deleted_objects:
            if isinstance(obj, (Comment, LeadStatus, LeadSupport)):
                obj.delete()


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)
    inlines = [CommentInline]


@admin.register(Group)
class CustomGroupAdmin(BaseGroupAdmin):
    list_display = ('name', 'permissions_count')
    list_filter = ('name', 'permissions')
    search_fields = ('name',)

    def permissions_count(self, obj):
        return obj.permissions.count()
    permissions_count.short_description = 'Количество разрешений'
