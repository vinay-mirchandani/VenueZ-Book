from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt

from Revision import settings
from fly.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
import sys
from django.contrib import messages
from django.core.mail import send_mail
from fly.forms import *
import random
from fly.functions import handle_uploaded_file
import hashlib



def dashboard(request):
    c = User.objects.all().count()
    b = Booking.objects.filter(order_status=0)
    h = Hall.objects.all().count()
    print("00000000000000000000",c)
    return render(request,"dashboard.html",{"Booking":b,"user":c,"hall":h})


def del_booking(request, id):
    b = Booking.objects.get(booking_id=id)
    b.delete()
    return redirect("/dashboard")


def order_accepted(request,id):
    b = Booking.objects.get(booking_id=id)
    b.order_status=1
    b.save()
    return redirect("/dashboard")


def order_rejected(request,id):
    b = Booking.objects.get(booking_id=id)
    b.order_status=2
    b.save()
    return redirect("/dashboard")


def view(request):
    u = User.objects.all()
    return render(request, 'user.html', {"User": u})


def register(request):
    if request.method == "POST":
        forms = ARegisterForm(request.POST)
        print("<!---------------------------->", forms.errors)

        if forms.is_valid():
            try:
                print("--before---------")
                newform = forms.save(commit=False)
                newform.password = hashlib.md5(newform.password.encode('utf')).hexdigest()
                newform.save()

                forms.save()
                return redirect("/user/")
            except:
                pass
        else:
            pass
    else:
        forms = ARegisterForm()
        return render(request,"register.html",{"forms":forms})


def admin_login(request):

    if request.method == "POST":

        u = request.POST["email"]
        p = request.POST["password"]

        val = Admin.objects.filter(email=u, password=p).count()
        print("|||||||||||||||||||||||||||",val)
        if val == 1:

            data = Admin.objects.filter(email=u, password=p)

            for items in data:
                request.session["username"] = items.admin_name
                request.session["id"] = items.admin_id
            if request.POST.get("remember"):
                response = redirect("/dashboard/")
                response.set_cookie('admin_email', request.POST["email"])
                response.set_cookie('admin_password', request.POST["password"])
                return response

            return redirect("/dashboard/")
        else:
            messages.error(request, "Invalid Email or Password")
            return render(request, "login.html")

    else:
        if request.COOKIES.get("admin_email"):
            return render(request, "login.html",
                          {'admin_email_cookie': request.COOKIES['admin_email'],
                           'admin_password_cookie': request.COOKIES['admin_password']})
        else:
         return render(request, "login.html")


def logout(request):
    try:
        del request.session['id']
        del request.session['username']
        return redirect('/login/')

    except:
        pass
    return redirect('/login/')


def forgot(request):
    return render(request, "forgot-password.html")


def send_otp(request):
    otp1 = random.randint(10000,  99999)
    e = request.POST['email']
    print('-------------------', e)
    request.session['temail'] = e
    obj = Admin.objects.filter(email=e).count()

    if obj == 1:
        val = Admin.objects.filter(email=e).update(otp=otp1, otp_used=0)
        subject = 'OTP verfication'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'reset-password.html')


    else:
        messages.error(request, 'Invalid Email ID')
        return render(request, 'forgot-password.html')






def set_password(request):
    totp = request.POST['otp']
    npassword = request.POST['npass']
    cpassword = request.POST['cpass']

    if npassword == cpassword:
        e = request.session['temail']
        val = Admin.objects.filter(email=e, otp=totp, otp_used=0 ).count()

        if val == 1 :
            val = Admin.objects.filter(email=e).update(otp_used=1, password=npassword)
            return redirect('/login/')
        else:
            messages.error(request, "Invalid OTP")
            return render(request, "reset-password.html")


    else:
        messages.error(request,"Password does not match")
        return render(request,"reset-password.html")




def edit_area(request,area_id):
    a = Area.objects.filter(area_id=area_id)
    return render(request,"update_are.html",{"a":a})


def delete_area(request,id):
    a = Area.objects.get(area_id=id)
    a.delete()
    return redirect("/Area")


def update_area(request,area_id):
    a = Area.objects.get(area_id=area_id)
    forms = AreaForm(request.POST,instance=a)
    print("---------------------------", forms.errors)

    if forms.is_valid():
        try:
            forms.save()
            return redirect("/Area/")
        except:
            print("------------------------",sys.exc_info())
    return render(request,"update_are.html",{"a":a})


def show_area(request):
    a = Area.objects.all()
    return render(request,"sarea.html",{"Area": a})



def admin_edit(request):
    aid = request.session['id']
    area = Area.objects.all()
    u = Admin.objects.filter(admin_id=aid)
    print("----------------", Admin.objects.filter(admin_id=aid).count())
    return render(request, "profile.html", {'user': u, "area": area})



def admin_update(request):

    aid = request.session['id']
    # area= Area.objects.all()
    #
    # u = Area.objects.filter(admin_id=aid)
    # print(u)

    if request.method == "POST":
        u1= Admin.objects.get(admin_id=aid)
        form = ARegisterForm(request.POST, instance=u1)
        print(" ------- ", form.errors)
        if form.is_valid():
            try:
               form.save()
               return redirect("/user")
            except:
                print("---------------", sys.exc_info())

    else:
        pass
    return render(request, "profile.html")



def show_category(request):
    c = Category.objects.all()
    return render(request,"scategory.html",{"Category":c})























#Insert



def insert_are(request):
    if request.method == "POST":
        forms = AreaForm(request.POST)
        print("==========", forms.errors)

        if forms.is_valid():
            forms.save()
            return redirect("/Area/")
        else:
            pass
    else:
        forms = AreaForm()
    return render(request,"insert_are.html", {"forms": forms})


def category(request):
    if request.method == "POST":
        forms = CategoryForm(request.POST)
        print("=======", forms.errors)

        if forms.is_valid():
            forms.save()
            return redirect("/user/")
        else:
            pass
    else:
        forms = CategoryForm()
    return render(request,"insert_category.html",{"forms": forms})





def hall(request):
    c = Category.objects.all()
    a = Area.objects.all()

    if request.method == "POST":
        forms = HallForm(request.POST, request.FILES)
        print("====", forms.errors)

        if forms.is_valid():
            handle_uploaded_file(request.FILES['h_path'])
            forms.save()
            return redirect("/user/")
        else:
            pass
    else:
        forms = HallForm()
    return render(request,"insert_hall.html",{"forms": forms, "Category": c, "Area":a})




class HomeView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"doctorChart.html")



class ClientChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        cursor=connection.cursor()
        cursor.execute('''SELECT (select category_name from category where category_id  = h.category_id_id)as name , count(*) as total FROM hall h JOIN category c where h.category_id_id = c.category_id GROUP by h.category_id_id''')
        qs=cursor.fetchall()
        print("+++++++++++=")
        labels=[]
        default_items=[]
        for item in qs:
            labels.append(item[0])
            default_items.append(item[1])

        data = {
            "labels":labels,
            "default":default_items,
        }
        return Response(data)



def gallery_insert(request):

    h = Hall.objects.all()
    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES)
        print("++++++++++", form.errors)
        if form.is_valid():
            handle_uploaded_file(request.FILES['g_path'])
            form.save()
            return redirect('/gallery_view/')
    else:
        form = GalleryForm()
        return render(request, 'gallery_insert.html',{"Hall":h})
    return render(request, 'gallery_insert.html', {"Hall": h})








def gallery_view(request):
    g = Gallery.objects.all()
    return render(request,"gallery-table.html",{"Gallery": g})



def show_package(request):
    p = Packages.objects.all()
    return render(request,"spackages.html",{"Packages":p})




def insert_package(request):
    h = Hall.objects.all()
    s = Services.objects.all()
    if request.method == "POST":
        forms = PackageForm(request.POST)
        print("==========", forms.errors)

        if forms.is_valid():
            forms.save()
            return redirect("/show_packages/")
        else:
            pass
    else:
        forms = PackageForm()
    return render(request,"insert_packages.html", {"forms": forms,"Hall":h,"Service":s})

@csrf_exempt
def report1(request):
    b = Booking.objects.all()
    h = Owner.objects.all()

    if request.method == "POST":

        key = request.POST.get("owner_name")
        print("--- KEyword --------", key)

        sql = "SELECT * FROM `booking` b where b.owner_id_id = %s"
        b = Booking.objects.raw(sql,[key])
        return render(request, "test.html", {"Booking":b})

    return render(request,"booking_report1.html",{"Booking" :b,"Owner":h})

def report2(request):
    b = Booking.objects.all()

    if request.method == "POST":

        start = request.POST["sd"]
        end = request.POST["ed"]

        start = parse_date(start)
        end = parse_date(end)
        print("----",start,"---------",end)

        if start < end :
            b = Booking.objects.filter(booking_date__range=[start,end])
            return render(request, "booking_report2.html", {"Booking": b})
        else:
            msg=messages.error("start date must b smaller")
            return render(request, "booking_report2.html", {"Booking": b,"msg":msg})

    return render(request, "booking_report2.html", {"Booking": b})


def report3(request):
    sql ="SELECT (select user_name from user where user_id = b.user_id_id) as name, sum(total) as booking_id FROM `booking` b join user u WHERE b.user_id_id = u.user_id group by b.user_id_id"
    b=Booking.objects.raw(sql)
    return render(request,"booking_report3.html", {"Booking": b})

def booking(request):
    b = Booking.objects.all()
    return render(request,"booking.html",{"Booking":b})


def show_hall(request):
    h = Hall.objects.all()
    return render(request,"show_hall.html",{"hall":h})