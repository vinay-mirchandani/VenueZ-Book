import datetime
import random
import sys
from datetime import date

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.http import JsonResponse

from fly.models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from .cart import Cart
from fly.forms import *
import hashlib
from Revision import settings
from django.core.mail import send_mail




def home(request):

    a = Area.objects.all()
    f = Feedback.objects.all()
    h = Hall.objects.all()
    c = Category.objects.all()

    return render(request, "index.html",{"Feedback": f, "Area": a, "Hall": h, "Category": c})


def c_login(request):
    if request.method == "POST":

        u = request.POST["email"]
        password = request.POST["password"]
        p = hashlib.md5(password.encode('utf')).hexdigest()

        val = User.objects.filter(email=u, password=password).count()

        if val == 1:

            data = User.objects.filter(email=u, password=password)

            for items in data:
                request.session["cusername"] = items.user_name
                request.session["cid"] = items.user_id

            return redirect("/client/Home/")
        else:
            messages.error(request, "Invalid Email or Password")
            return render(request, "clientlogin.html")

    return render(request, "clientlogin.html")


def c_register(request):
    area = Area.objects.all()
    if request.method == "POST":
        forms = RegisterForm(request.POST)

        print("================",forms.errors)
        if forms.is_valid():
            try:
                print("------------- Before save data ------------")
                newform = forms.save(commit=False)
                newform.password = hashlib.md5(newform.password.encode('utf')).hexdigest()

                newform.save()
                print("++++++save data +++++++++++")

                # forms.save()
                return redirect("/client/Home")
            except:
                pass
        else:
            pass
    else:
        forms =RegisterForm()
        return render(request,"clientregister.html",{"forms":forms,"area":area})

    forms = RegisterForm()
    return render(request, "clientregister.html", {"forms": forms, "area": area})



def forgot_password(request):
    return render(request,"fpassword.html")


def c_destination(request,pckg_id):
    h = Hall.objects.all()
    f = Feedback.objects.all()
    p = Packages.objects.get(package_id=pckg_id)
    # gl = Gallery.objects.filter(h
    return render(request, "destination.html", { "Feedback": f,"package":p, "Hall":h})


def hall_details(request,hall_id):
    f = Feedback.objects.all()
    h = Hall.objects.filter(hall_id=hall_id)
    gl = Gallery.objects.filter(hall_id=hall_id)

    return render(request,"hall_details.html",{"Hall":h,"Feedback":f,"Gallery":gl,"Hall":h})


def c_feedback(request):
    try:
        feedback = date.today().strftime("%Y-%m-%d")
        des = request.POST["message"]
        user = request.session["cid"]
        hall = request.POST["name"]
        rate = request.POST.get("rate")
        id=request.POST["hall_id"]
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++des")
        f = Feedback(feedback_date=feedback, description=des, user_id_id=user, hall_id_id=id, rate=rate)
        f.save()
        return redirect("/client/destination/%s" %id)
    except:
        print("-----------------", sys.exc_info())
        return render(request, "error.html")



def cart(request):
    if 'cid' in request.session:
        id=request.session['cid']
        b = Booking.objects.filter(user_id_id=id)
        return render(request, "cart.html", {"Booking": b})
    else:
        return render(request, "clientlogin.html")


def client(request):
    f = Feedback.objects.all()
    h = Hall.objects.all()
    return render(request, "dashboard.html", {"Feedback": f, "Hall": h})


def booking(request,pckg_id):
    h = Packages.objects.get(package_id=pckg_id)
    id=request.session['cid']
    u=User.objects.get(user_id=id)
    return render(request,"booking.html",{"package": h,"user":u})


def venues(request,category_id):
    c = Hall.objects.filter(category_id=category_id)

    sql1 = "SELECT hall_id_id as feedback_id , FLOOR(AVG(rate)) as AVG FROM Feedback GROUP by hall_id_id"
    q = Feedback.objects.raw(sql1)
    print("----", q)
    return render(request, "venues.html", {"Hall": c,"rate": q})


def venuez(request):
    c = Hall.objects.all()

    if request.method == "POST":
        name = request.POST["hall_name"]
        c = Hall.objects.filter(hall_name=name)
    else:
        c=Hall.objects.all()
    #     page = request.GET.get('page', 1)
    #
    #
    #     print("page ----------------", page)
    #
    #     paginator = Paginator(c1, 1)
    #
    #     try:
    #         c = paginator.page(page)
    #     except PageNotAnInteger:
    #         c = paginator.page(1)
    #     except EmptyPage:
    #         c = paginator.page(paginator.num_pages)

    return render(request, "venues.html",{"Hall":c})


def FAQ(request):
    return render(request,"FAQ.html")

def contact(request):
    return render(request,"contact.html")


def load_menu(request):
    c=Category.objects.all()
    return render(request,"test2.html",{"cat":c})



def error404(request):
    return render(request,"error.html")



def about_us(request):
    return render(request,"about.html")



def autosuggest(request):

    print("---- autosuggest ----")

    if 'term' in request.GET:
        qs=Hall.objects.filter(hall_name__istartswith=request.GET.get('term'))

        name=list()

        for x in qs:
            name.append(x.hall_name)

        return JsonResponse(name,safe=False)

    return render(request,"clientheader.html")


def showhall(request):

    a=request.POST.get("area_name")
    c=request.POST.get("cat")

    print("+++++++++++",a)
    print("++++++++++",c)

    h=Hall.objects.filter(area_id=a, category_id=c)

    return render(request,"venues.html",{"Hall":h})

def select_checkout(request,pckg_id):
    if request.method=="POST":
        if request.session.has_key('cid'):
            pay=request.POST["payment"]
            req_date=request.POST["req_date"]
            # d=datetime.datetime(int(req_date)).formate("%Y-%m-%d")
            p=Packages.objects.get(package_id=pckg_id)
            uid = request.session['cid']
            date1 = date.today().strftime("%Y-%m-%d")
            o = Booking(user_id_id=uid, total=int(p.package_price), booking_date=date1, payment_status=1, order_status=0 ,package_id_id=p.package_id,owner_id_id=p.hall_id.owner_id_id , req_date=req_date)
            o.save()



    return redirect("/client/My_Bookings/")



def packages(request,package_id):
    p = Packages.objects.filter(hall_id_id=package_id)
    return render(request,"packages.html",{'Packages':p})


def c_package(request,package_id):
    p = Packages.objects.filter(package_id=package_id)
    return render(request, "singlepackage.html", {"Package": p})










def owner_login(request):
    if request.method == "POST":

        u = request.POST["owner_email"]
        p = request.POST["owner_password"]

        val = Owner.objects.filter(owner_email=u, owner_password=p).count()
        print(val)
        if val == 1:

            data = Owner.objects.filter(owner_email=u, owner_password=p)

            for items in data:
                request.session["ownername"] = items.owner_name
                request.session["ownerid"] = items.owner_id

            return redirect("/owner/owner_dashboard/")
        else:
            messages.error(request, "Invalid Email or Password")
            return render(request, "ownerlogin.html")

    return render(request, "ownerlogin.html")


def owner_register(request):
    area = Area.objects.all()
    if request.method == "POST":
        forms = OwnerForm(request.POST)

        print("================",forms.errors)
        if forms.is_valid():
            forms.save()
            return redirect("/owner/owner_log")
        else:
            pass
    else:
        forms =OwnerForm()
        return render(request,"ownerregister.html",{"forms":forms,"area":area})


#client

def send_otp(request):

    otp1 = random.randint(10000,  99999)
    e = request.POST['email']
    print('-------------------', e)
    request.session['temail'] = e
    obj = User.objects.filter(email=e).count()
    print()
    if obj == 1:
        val = User.objects.filter(email=e).update(otp=otp1, otp_used=0)
        subject = 'OTP verfication'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'resetpassword.html')


    else:
        messages.error(request, 'Invalid Email ID')
        return render(request, 'fpassword.html')






def set_password(request):
    totp = request.POST['otp']
    npassword = request.POST['npass']
    cpassword = request.POST['cpass']

    if npassword == cpassword:
        e = request.session['temail']
        val = User.objects.filter(email=e, otp=totp, otp_used=0 ).count()

        if val == 1 :
            val = User.objects.filter(email=e).update(otp_used=1, password=npassword)
            return redirect('/client/log/')
        else:
            messages.error(request, "Invalid OTP")
            return render(request, "resetpassword.html")


    else:
        messages.error(request,"Password does not match")
        return render(request,"resetpassword.html")



#owner

def resetowner(request):
    totp = request.POST.get('otp')
    npassword = request.POST.get('npass')
    cpassword = request.POST.get('cpass')
    print(totp)
    if npassword == cpassword:
        e = request.session['oemail']
        val = Owner.objects.filter(owner_email=e, otp=totp, otp_used=0).count()

        if val == 1 :
            val = Owner.objects.filter(owner_email=e).update(otp_used=1, owner_password=npassword)
            return redirect('/client/owner_log/')
        else:
            messages.error(request, "Invalid OTP")
            return render(request, "resetowner.html")

    else:
        messages.error(request,"Password does not match")
        return render(request,"resetowner.html")


def send_oOtp(request):

    otp1 = random.randint(10000,  99999)
    e = request.POST.get('owner_email')
    print('-------------------', e)
    request.session['oemail'] = e
    obj = Owner.objects.filter(owner_email=e).count()
    print()
    if obj == 1:
        val = Owner.objects.filter(owner_email=e).update(otp=otp1, otp_used=0)
        subject = 'OTP verfication'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'resetowner.html')


    else:
        messages.error(request, 'Invalid Email ID')
        return render(request, 'forgotowner.html')



def owner_forgot(request):
    return render(request,"forgotowner.html")



