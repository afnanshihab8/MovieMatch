from django import forms

class WordInputForm(forms.Form):
    words = forms.CharField(label="Enter three words", max_length=100, help_text="E.g. dark, thrilling, mystery")
