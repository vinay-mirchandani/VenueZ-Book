from django import forms
from fly.models import *
from parsley.decorators import parsleyfy


@parsleyfy
class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["area_name","pincode"]

@parsleyfy
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["user_name", "email", "password", "contact", "area_id"]

@parsleyfy
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name"]


class HallForm(forms.ModelForm):
    h_path = forms.FileField()
    class Meta:
        model = Hall
        fields = ["hall_name", "contact", "address", "hall_desc","h_path","category_id", "area_id"]


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["user_name", "email", "password","contact", "area_id"]

@parsleyfy
class ARegisterForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ["admin_name", "email", "password", "contact"]


class GalleryForm(forms.ModelForm):
    g_path = forms.FileField()
    class Meta:
        model = Gallery
        fields = ['g_path','hall_id']

@parsleyfy
class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ["owner_name", "owner_email", "owner_password", "owner_contact", "area_id"]

@parsleyfy
class PackageForm(forms.ModelForm):
    class Meta:
        model = Packages
        fields = ["package_name","package_type","package_desc","package_price","hall_id","service_id"]


class UpdateOwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ["owner_name", "owner_email", "owner_contact"]