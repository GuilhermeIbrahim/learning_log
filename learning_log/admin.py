from django.contrib import admin
from learning_log.models import Topic, Entry, Category

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Category)