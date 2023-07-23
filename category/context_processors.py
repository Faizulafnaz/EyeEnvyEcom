from .models import Category
from store.models import Brand

def menu_links(request):
    links = Category.objects.all()
    brands = Brand.objects.all()
    return dict(links = links, brands=brands)