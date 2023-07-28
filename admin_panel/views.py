from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from order.models import *
from store.models import *
from category.models import *
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
import calendar

# Create your views here.


def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:

        #filtering delivered item
        delivered_item = OrderItem.objects.filter(status='Delivered')

        revenue = 0
        order_count = delivered_item.count()
        product_count = Product.objects.count()
        category_count = Category.objects.count()
        user_count = User.objects.count()

        #calculating revenue
        for item in delivered_item:
            revenue += item.sub_total()

        recent_sale = OrderItem.objects.all().order_by('-id')[:5]

        # sale report by month for graph
        today = timezone.now().date()
        five_months_ago = today - timedelta(days=150)
        sales_report = (
        OrderItem.objects
        .annotate(month=TruncMonth('created_at'))
        .filter(created_at__gte=five_months_ago, status='Delivered')
        .values(month = F('month__month'))
        .annotate(total_sales=Sum('product_price'), total_number_of_orders = Sum('quantity'))
        .order_by('month')
        )

        for entry in sales_report:
            entry['month_name'] = get_month_name(entry['month'])

        print(sales_report)

        context = {
            'revenue' : revenue,
            'recent_sale' : recent_sale,
            'order_count' : order_count,
            'product_count' : product_count,
            'category_count' : category_count,
            'user_count' : user_count,
            'sales_report' : sales_report,

        }

        return render(request, 'adminpanel/index.html', context)
    return render(request, 'adminpanel/adminlogin.html')

# for getting month name --------------------------------------------



def get_month_name(month_number):
    if 1 <= month_number <= 12:
        return calendar.month_name[month_number]
    else:
        return None


# admin authentication -----------------------------------------------

def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("pass1")

        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')

        else:
            messages.error(request, "Invalid superuser credentials")
            return redirect("admin_login")

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')

    return render(request, 'adminpanel/adminlogin.html')

def signout(request):
    logout(request)
    return redirect(admin_dashboard)



# user details part ---------------------------------------------------

def user_details(request):
    if not request.user.is_authenticated and not request.user.is_superuser:
        return redirect('admin_dashboard')
    usr = User.objects.all()  
    context = {

        'users' : usr
    }
    return render(request, 'adminpanel/user.html', context)


@login_required(login_url='admin_login')
def user_action(request, id):
    usr = User.objects.get(id=id)
    if usr.is_active:
        usr.is_active = False
        usr.save()
        return redirect(user_details)
    else:
        User.objects.get(id=id)
        usr.is_active = True
        usr.save()  
        return redirect(user_details)

@login_required(login_url='admin_login')
def search_users(request):  
    search_text = request.POST['query']
    context = {
        'users': User.objects.filter(username__icontains=search_text),
        'search_text':search_text,
    }
    return render(request,'adminpanel/user.html',context)




# sales report ------------------------------------------------------------------------------------
@login_required(login_url='admin_login')
def sales_report(request):
    if not request.user.is_superuser:
        return redirect(admin_login)
    
    context = {}

    if request.method == 'POST':

        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')

        if start_date == '' or end_date == '':
            messages.error(request,'Give date first')
            return redirect(sales_report)
        
        if start_date ==  end_date :
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            order_items = OrderItem.objects.filter(order__created_at__date=date_obj.date())
            if order_items:
                context.update(sales = order_items,s_date=start_date,e_date = end_date)
                return render(request,'adminpanel/sales.html',context)
            else:
                messages.error(request,'no data found')
            return redirect(sales_report)

        order_items = OrderItem.objects.filter(order__created_at__gte=start_date, order__created_at__lte=end_date)

        if order_items:
            context.update(sales = order_items,s_date=start_date,e_date = end_date)
        else:
            messages.error(request,'no data found')

    return render(request,'adminpanel/sales.html',context)
