from django.forms import ModelForm
from .models import SQLMODEL

class SqlModelForm(ModelForm):
    class Meta:
        model = SQLMODEL
        fields = '__all__'