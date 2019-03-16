#coding:UTF-8
from django import forms

class UploadImageForm(forms.Form):
    """upload imgs"""
    #text = forms.CharField(max_length=100)
    image = forms.ImageField(
        label='选择文件',
    )