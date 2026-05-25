from django import forms
from .models import Category, Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text', 'categories']
        labels = {'text': '', 'categories': 'Categorias'}
        widgets = {'text': forms.Textarea(attrs={'cols':80}), 'categories': forms.CheckboxSelectMultiple()}
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.filter(owner=user)
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Nome da Categoria'}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user