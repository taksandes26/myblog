from django import forms
from .models import Comment


# class CommentNormalForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     email = forms.EmailField()
#     comment = forms.CharField(widget=forms.Textarea)
#
#     def __str__(self):
#         return self.name
#
#
# f = CommentNormalForm()

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "content")


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
    query = forms.CharField()
