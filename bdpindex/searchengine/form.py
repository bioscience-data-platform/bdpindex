from django import forms


class SearchForm(forms.Form):
    query_field = forms.CharField(max_length=1024, required=True, label='')