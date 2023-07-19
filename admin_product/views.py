from django.shortcuts import redirect, render
from store.models import Product, ProductImage
from category.models import *
from django.contrib import messages
from category.models import Category

# Create your views here.

#product section-------------------------------

def products(request):
    products = Product.objects.all().filter(is_available = True)
    context = {
        'products' : products,
        
    }
    return render(request, 'adminpanel/page-products-grid-2.html', context)

def add_product(request):

    if request.method == 'POST':
        image = ''
        try:
            image = request.FILES['image']
        except:
            if image == '':
                messages.info(request,"Image field can't be empty")
                return redirect(add_product)
        
        name = request.POST['name']
        slug = request.POST['slug']
        brand = request.POST['brand']
        category = request.POST['category']
        description = request.POST['desc']
        price = request.POST['price']
        stock = request.POST['stock']
        images = request.FILES.getlist('images')

        try:
            Product.objects.get(product_name = name)
        except:
                check = [name,slug,description,price,stock]
                for values in check:
                    if values == '':
                        messages.info(request,'some fields are empty')
                        return redirect(add_product)
                    else:
                        pass    
                brand_instance = Brand.objects.get(id=brand)
                category_instance = Category.objects.get(id=category)

                Product.objects.create(
                    product_name=name,
                    brand=brand_instance,
                    category=category_instance,
                    description=description,
                    price=price,
                    stock=stock,
                    images=image,
                    slug=slug
                ).save()
                product = Product.objects.get(product_name = name)
                for image in images:
                    ProductImage.objects.create(product=product, pr_images=image)
                                
                messages.info(request,f'Product {name} created succefully')
                return redirect(add_product)
        else:
            messages.error(request,f'Product "{name}" already exist')
            return redirect(add_product)


    brands = Brand.objects.all()
    categories = Category.objects.all()

    context = {
        'categories' : categories,
        'brands' : brands,
    }
    return render(request, 'adminpanel/page-form-product-1.html', context)

def edit_product(request, id):

    if request.method == "POST":

        image = ''
        try:
            image = request.FILES['image']
            print(image)
            product = Product.objects.filter(id=id).first()
            product.images = image
            product.save()

        except:
            print('Hi')

        name = request.POST['name']
        slug = request.POST['slug']
        brand = request.POST['brand']
        category = request.POST['category']
        price = request.POST['price']
        stock = request.POST['stock']

        if name == '':
            messages.error(request,"Product name can't be null")
            return redirect(edit_product)

        
        brand_instance = Brand.objects.get(id=brand)
        category_instance = Category.objects.get(id=category)

        product = Product.objects.filter(id=id).update(

            product_name=name,
            brand=brand_instance,
            category=category_instance,
            slug=slug,
            stock=stock,
            price=price,
            
            
        )



        messages.success(request,f'{name} updated successfully')
        return redirect(products)
    
    product = Product.objects.get(id=id)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    context = {

        "product": product,
        'categories' : categories,
        'brands' : brands,
    }

    return render(request, "adminpanel/product-update.html", context)


def delete_product(request, id):

    product = Product.objects.get(id=id)
    name = product.product_name
    product.is_available = False
    product.save()    
    messages.success(request,f'Product "{name}" deleted')
    return redirect(products)


# Category section-------------

def add_category(request):

    if request.method == 'POST':        
        image = ''
        try:
            image = request.FILES['image']
        except:
            if image == '':
                messages.info(request,"Image field can't be empty")
                return redirect(add_category)
            
        name = request.POST['name']
        slug = request.POST['slug']
        description = request.POST['desc']
        check = [name,slug]
        is_available = request.POST.get('is_available', False)        
        if is_available:
            is_available = True
        else:
            is_available = False 
        for values in check:
            if values == '':
                messages.info(request,'some fields are empty')
                return redirect(add_category)
            else:
                pass
        try:
            Category.objects.get(category_name = name)
        except:
            Category.objects.create(category_name=name,cat_image=image,category_decs=description,slug=slug).save()
            messages.success(request,f'Category "{name}" succesfully added')
        else:
            messages.error(request,f'Category "{name}" already exist')
            return redirect(add_category)
    if not request.user.is_authenticated and not request.user.is_superuser:
        return redirect('admin_dashboard')
        
    categories = Category.objects.all()
    context = {

        'categories': categories,
    }

    return render(request, 'adminpanel/page-categories.html', context)


def edit_category(request, id):
    if request.method == "POST":
        name = request.POST['name']
        slug = request.POST['slug']
        description = request.POST['desc']

        category = Category.objects.filter(id=id).update(
            category_name=name,
            slug=slug,
            category_decs=description,
        )
        messages.success(request,f'{name} updated successfully')
        return redirect(add_category)

    category = Category.objects.get(id=id)
    context = {
        'category' : category,
    }
    return render(request, "adminpanel/update-category.html", context)


def delete_category(request, id):
    category = Category.objects.get(id=id)
    name = category.category_name
    category.is_available = False
    category.save()
    messages.success(request,f'Category "{name}" deleted')
    return redirect(add_category)



# brand section-------------------
def add_brand(request):
    if request.method == "POST":
        name = request.POST['name']
        desc = request.POST['desc']

        brand = Brand.objects.create(
            brand_name = name,
            brand_desc = desc,
        )
        brand.save()
        messages.success(request,f'Brand "{name}" created')
        return redirect(add_brand)
    brand = Brand.objects.all()
    context = {
        'brands' : brand,
    }
    return render(request,"adminpanel/brand.html", context)


def edit_brand(request, id):
    brand = Brand.objects.get(id=id)
    if request.method == "POST":
        name = request.POST['name']
        desc = request.POST['desc']
        Brand.objects.filter(id=id).update(
            brand_name = name,
            brand_desc = desc,
        )
        messages.success(request,f'{name} updated successfully')
        return redirect(add_brand)
    return render(request, 'adminpanel/editbrand.html', {'brand':brand,})