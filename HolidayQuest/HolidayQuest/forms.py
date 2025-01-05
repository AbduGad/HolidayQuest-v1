from django import forms


class HotelForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    price = forms.FloatField()
    description = forms.CharField(widget=forms.Textarea)
    rooms_available = forms.IntegerField()
    total_rooms = forms.IntegerField()
    country = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    image = forms.ImageField(required=True)
