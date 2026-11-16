from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.views.generic import TemplateView, ListView

class TestTemplateView(TemplateView):
    template_name = "main/test.html"

# def index(request):
#     category = request.GET.get('category', 'all')
#     products = Product.objects.filter(available=True)
#     categories = Category.objects.all()

#     if category != "all":
#         # ct = get_object_or_404(Category, slug=category)
#         products = products.filter(category__slug=category)

#     context = {
#         "products": products,
#         "categories": categories,
#         "category_select": category,
#     }
#     return render(request, 'main/index.html', context)


class ProductListView(ListView):
    model = Product
    template_name = "main/index.html"
    context_object_name = "products"
    extra_context = {"title": "Главная страница"}

    def get_queryset(self):
        self.category = self.request.GET.get("category", "all")
        products = Product.objects.filter(available=True)
        if (self.category != "all"):
            products = products.filter(category__slug=self.category)
        
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        context["categories"] = Category.objects.all()
        context["category_select"] = self.category
        return context


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'main/product_detail.html', {'product': product})


def about(request):
    return render(request, 'main/about.html')


def contacts(request):
    return render(request, 'main/contacts.html')
        
