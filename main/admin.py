from django.contrib import admin
from .models import Profile, Category, Listing, ListingImage, Favorite, Review, Chat, Message

# Дозволяє завантажувати фотографії прямо на сторінці створення оголошення
class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 3  # Скільки порожніх полів для фото показувати відразу

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'seller', 'status', 'condition', 'created_at')
    list_filter = ('status', 'condition', 'category', 'created_at')
    search_fields = ('title', 'description', 'city')
    prepopulated_fields = {'slug': ('title',)}  # Автоматично генерує slug з назви англійською
    inlines = [ListingImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city', 'created_at')
    search_fields = ('user__username', 'phone_number', 'city')

# Вкладені повідомлення всередині вікна чату
class MessageInline(admin.TabularInline):
    model = Message
    extra = 1

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('listing', 'buyer', 'created_at')
    inlines = [MessageInline]

# Реєстрація інших допоміжних моделей
admin.site.register(Favorite)
admin.site.register(Review)
