from django import forms
from models import Product
from django.utils.text import slugify


PUBLISH_CHOICES = (
    ("publish", "PUBLISH"),
    ("draft", "DRAFT"),
)

class ProductAddForm(forms.Form):
    title = forms.CharField(label="The product title", widget=forms.TextInput(
        attrs={
            "placeholder": "Title"
        }
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "my-custom-class",
            "placeholder": "Description"
        }
    ))
    price = forms.DecimalField()
    publish = forms.ChoiceField(choices=PUBLISH_CHOICES, widget=forms.RadioSelect,
                                required=False)

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 1.00:
            print ("price value is : {0}".format(price))
            raise forms.ValidationError("The price must be greater than $1.00")
        elif price >= 99.99:
            print ("The price cannot be more than 100")
        else:
            return price

    def clean_title(self):
        title = self.cleaned_data.get("title")
        print ("title value is {0}".format(title))
        if len(title) > 3:
            return title
        else:
            raise forms.ValidationError("The title must be at less 3 characters long")


class ProductModelForm(forms.ModelForm):
    publish = forms.ChoiceField(choices=PUBLISH_CHOICES, widget=forms.RadioSelect,
                                required=False)

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "price",
        ]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "my_custom_class",
                    "placeholder": "New description here",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "placeholder": "here the title"
                }
            )
        }

    def clean(self, *args, **kwargs):
        cleaned_data = super(ProductModelForm, self).clean(*args, **kwargs)
        print(cleaned_data)
        title = cleaned_data.get("title")
        slug = slugify(title)
        qs = Product.objects.filter(slug=slug).exists()
        # if qs:
        #     raise forms.ValidationError("Title is taken, new title is needed. Please try again")

        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 1.00:
            print ("price value is {0}".format(price))
            raise forms.ValidationError("The price must be greater than $1.00")
        elif price >= 99.99:
            raise forms.ValidationError("The price must be less than $100")
        else:
            return price

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 3:
            raise forms.ValidationError("the title must be at less 3 characters long")
        else:
            return title

