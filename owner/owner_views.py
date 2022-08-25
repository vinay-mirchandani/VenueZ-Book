import sys

from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt

from fly.models import *
from fly.forms import *

def owner_dashboard(request):
    id=request.session["ownerid"]
    b = Booking.objects.filter(owner_id_id=id,order_status=0)
    return render(request,"owner_dashboard.html",{"Booking":b})

def show_hall(request):
    id=request.session["ownerid"]
    h=Hall.objects.filter(owner_id_id=id)
    return render(request,"all_hall.html",{"hall":h})

def del_booking(request,id):
    b = Booking.objects.get(booking_id=id)
    b.delete()
    return redirect("/owner_dashboard")

def order_accepted(request,id):
    b = Booking.objects.get(booking_id=id)
    b.order_status=1
    b.save()
    return redirect("/owner_dashboard")

def order_rejected(request,id):
    b = Booking.objects.get(booking_id=id)
    b.order_status=2
    b.save()
    return redirect("/owner_dashboard")

def owner_area(request):
    a = Area.objects.all()
    return render(request,"owner_area.html",{"Area": a})



def owner_edit(request):
    pid = request.session['ownerid']
    o = Owner.objects.get(owner_id=pid)
    a = Area.objects.all()
    return render(request, "owner_profile.html", {'owner': o,'area': a})



def owner_update(request):
    pid = request.session['ownerid']
    o = Owner.objects.get(owner_id=pid)
    a = Area.objects.all()
    form = UpdateOwnerForm(request.POST, instance=o)
    print("---------------", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/owner/owner_dashboard")
        except:
            print("------------", sys.exc_info())
    else:
        pass

    return render(request, 'owner_profile.html', {'owner': o, 'area': a})



def owner_area(request):
    a = Area.objects.all()
    return render(request,"show_area.html",{"Area": a})


def owner_package(request):
    p = Packages.objects.all()
    return render(request,"show_packages.html",{"Packages":p})



@csrf_exempt
def report1(request):
    id = request.session["ownerid"]
    b = Booking.objects.filter(owner_id_id = id)
    h = Hall.objects.filter(owner_id_id=id)


    if request.method == "POST":

        key = request.POST.get("hall_name")
        print("--- KEyword --------", key)

        sql = " SELECT * FROM `booking` b join hall h join packages p where b.package_id_id = p.package_id and p.hall_id_id = h.hall_id and h.hall_id = %s "
        b=Booking.objects.raw(sql,[key])
        print("||||||||||||||||||||||||||||||||")
        return render(request, "test1.html", {"Booking": b, "Hall": h})

    return render(request,"owner_report1.html",{"Booking":b,"Hall":h})

def report2(request):
    id = request.session["ownerid"]
    b = Booking.objects.filter(owner_id_id=id)
    if request.method == "POST":

        start = request.POST["sd"]
        end = request.POST["ed"]

        start = parse_date(start)
        end = parse_date(end)
        print("----",start,"---------",end)

        if start < end :
            b = Booking.objects.filter(booking_date__range=[start,end])
            return render(request, "owner_report2.html", {"Booking": b})
        else:
            msg=messages.error("start date must b smaller")
            return render(request, "owner_report2.html", {"Booking": b,"msg":msg})

    return render(request, "owner_report2.html", {"Booking": b})



def gallery_view(request):
    g = Gallery.objects.all()
    return render(request,"gallery-table.html",{"Gallery": g})

