from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView


# Create your views here.
from digitalmarket.mixins import MultiSligMixin, SubmitBtnMixin

from .forms import ProductAddForm, ProductModelForm
from .models import Product


class ProductCreateView(SubmitBtnMixin, CreateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    success_url = "/products/"
    submit_btn = "Add product"

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(ProductCreateView, self).form_valid(form)
        form.instance.managers.add(user)

        return valid_data


class ProductUpdateView(SubmitBtnMixin, MultiSligMixin, UpdateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    success_url = "/products/"
    submit_btn = "Update product"

    def get_object(self, *args, **kwargs):
        user = self.request.user
        obj = super(ProductUpdateView, self).get_object(*args, **kwargs)
        if obj.user == user or user in obj.managers.all():
            return obj
        else:
            raise Http404


class ProductDetailView(MultiSligMixin, DetailView):
    model = Product


class ProductListView(ListView):
    model = Product

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(**kwargs)
        # qs = qs.filter(title__icontains="Product")
        return qs


def create_view(request):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data.get("publish"))
        instantce = form.save(commit=False)
        instantce.sale_price = instantce.price
        instantce.save()
    template = "form.html"
    context = {
        "form": form,
        "submit_btn": "Create product"
    }

    return render(request, template, context)


def update_view(request, object_id=None):
    product = get_object_or_404(Product, id=object_id)
    form = ProductModelForm(request.POST or None, instance=product)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    template="form.html"
    context = {
        "form": form,
        "submit_btn": "Update product"
    }
    return render(request, template, context)


def detail_slug_view(request, slug=None):
    """
    this method will display the detail of a picture
    """
    print(request)
    try:
        product = get_object_or_404(Product, slug=slug)
    except Product.MultipleObjectsReturned:
        product = Product.objects.filter(slug=slug).order_by("title").first()
    template = "detail_view.html"
    context = {
        "title": "hello my friend",
        "product": product
    }
    return render(request, template, context)


def detail_view(request, object_id=None):
    """
    this method will display the detail of a picture
    """
    print(request)
    product = get_object_or_404(Product, id=object_id)
    template = "detail_view.html"
    context = {
        "title": "hello my friend",
        "product": product
    }
    return render(request, template, context)


def list_view(request):
    """
    this method will display the list of pictures
    """
    quereyset = Product.objects.all()

    if request.user.is_authenticated():
        print(request.user)
        template = "list_view.html"
        context = {
            "queryset": quereyset
        }
    else:
        print("not found url")
        template = "not_found.html"
        context = {}

    return render(request, template, context)
