from django.shortcuts import render
from EAD_app.models import User_info,venue
from django.contrib.auth.models import User
from EAD_app.forms import NewuserForm,userform,booking_form_secy,booking_form_student
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login,logout
# Create your views here.
def index(request):
    return render(request,'EAD_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_info_view(request):
        registered=False
        if request.method == 'POST':
            def_form=userform(data=request.POST)
            form = NewuserForm(request.POST)

            if form.is_valid() and def_form.is_valid():

                user=def_form.save()
                user.set_password(user.password)
                user.save()

                user_extra= form.save(commit=False)
                user_extra.role="student"
                user_extra.user=user
                user_extra.save()


                registered=True
            else:
                print(form.errors)

        else:
            form=NewuserForm()
            def_form=userform()
            registered=False

        return render(request,'EAD_app/register.html',{'def_form':def_form,
        'form':form,'registered':registered
    })


def user_login(request):

    if request.method=='POST':
        username= request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                id=User_info.objects.filter(user=request.user)
                for i in id:
                    if i.role=="secretary":
                        return HttpResponseRedirect("/EAD_app/booking_secy/")
                    elif i.role=="o/i" and i.description=="NSS":
                        return HttpResponseRedirect("/EAD_app/oi_nss/")
                    elif i.role=="o/i" and i.description=="CSS":
                        return HttpResponseRedirect("/EAD_app/oi_css/")
                    elif i.role=="o/i" and i.description=="IEEE":
                        return HttpResponseRedirect("/EAD_app/oi_ieee/")
                    elif i.role=="o/i" and i.description=="saasc":
                        return HttpResponseRedirect("/EAD_app/oi_saasc/")
                    elif i.role=="o/i" and i.description=="robotics":
                        return HttpResponseRedirect("/EAD_app/oi_robotics/")
                    elif i.role=="o/i" and i.description=="voyagers":
                        return HttpResponseRedirect("/EAD_app/oi_voyagers/")
                    elif i.role=="o/i" and i.description=="music_club":
                        return HttpResponseRedirect("/EAD_app/oi_music_club/")
                    elif i.role=="da":
                        return HttpResponseRedirect("/EAD_app/da_app/")
                    elif i.role=="dsa":
                        return HttpResponseRedirect("/EAD_app/dsa_app/")
                    elif i.role=="cdgc":
                        return HttpResponseRedirect("/EAD_app/cdgc_app/")
                    elif i.role=="oi_security":
                        return HttpResponseRedirect("/EAD_app/ois_app/")
                    elif i.role=="lab_technician":
                        return HttpResponseRedirect("/EAD_app/labt_rw/")
                    elif i.role=="hod":
                        return HttpResponseRedirect("/EAD_app/hod_rw/")
                    elif i.role=="student":
                        return HttpResponseRedirect("/EAD_app/booking_student/")



            else: return HttpResponse("NOT Active")

        else:
            print("username: {} password: {}".format(username,password))
            logout(request)
            return HttpResponse("invalid login")

    else:
        return render(request,'EAD_app/login.html',{})

def date_check_student(venue_req,date_req):
    id=venue.objects.filter(requested_venue_student__exact=venue_req)
    dates_all=[i.date for i in id]
    if date_req in dates_all:
        return False
    else:
        return True



@login_required
def venue_book_student(request):
    if request.method == 'POST':
        venue_form=booking_form_student(data=request.POST)

        if venue_form.is_valid():
            ven=venue_form.cleaned_data.get("requested_venue_student")
            date_req=venue_form.cleaned_data.get("date")
            if date_check_student(ven,date_req):
                saving = venue_form.save()
                saving.user=request.user
                saving.save()
                logout(request)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("oops!! There is already a booking on this date. Go back and change the date.")
        else:
            print(venue_form.errors)

    else:
        venue_form=booking_form_student(data=request.POST)
    return render(request,"EAD_app/booking_student.html",{"venue_form":venue_form})

def date_check_secy(venue_req,date_req):
    id=venue.objects.filter(requested_venue_secy__exact=venue_req)
    dates_all=[i.date for i in id]
    if date_req in dates_all:
        return False
    else:
        return True

@login_required
def venue_book_secy(request):
    if request.method == 'POST':
        venue_form=booking_form_secy(data=request.POST)

        if venue_form.is_valid():
            ven=venue_form.cleaned_data.get("requested_venue_secy")
            date_req=venue_form.cleaned_data.get("date")
            if date_check_secy(ven,date_req):
                saving = venue_form.save()
                saving.user=request.user
                saving.save()
                logout(request)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("oops!! There is already a booking on this date. Go back and change the date.")
        else:
            print(venue_form.errors)

    else:
        venue_form=booking_form_secy(data=request.POST)
    return render(request,"EAD_app/booking_secy.html",{"venue_form":venue_form})



@login_required
def oi_nss(request):
    list_work=venue.objects.filter(associated_club__exact="nss")
    for work in list_work:
        if work.rew_by_oi==False and work.considered==False:
            da_dict={"secretary":work.user,"date":work.date,
                "venue_name":work.requested_venue_secy,
                "club":work.associated_club,
                "event":work.event_name}
            break
    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.rew_by_oi=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_nss")
        elif value=="no":
            work.rew_by_oi=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_nss")

    try:
        return render(request,"EAD_app/oi_nss.html",da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")


@login_required
def oi_css(request):
    list_work=venue.objects.filter(associated_club__exact="CSS")
    for work in list_work:
        if work.rew_by_oi==False and work.considered==False:
            da_dict={"secretary":work.user,"date":work.date,
                "venue_name":work.requested_venue_secy,
                "club":work.associated_club,
                "event":work.event_name}
            break
    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.rew_by_oi=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_css")
        elif value=="no":
            work.rew_by_oi=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_css")


    try:
        return render(request,"EAD_app/oi_css.html",da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")



@login_required
def oi_ieee(request):
    list_work=venue.objects.filter(associated_club__exact="IEEE")
    for work in list_work:
        if work.rew_by_oi==False and work.considered==False:
            da_dict={"secretary":work.user,"date":work.date,
                "venue_name":work.requested_venue_secy,
                "club":work.associated_club,
                "event":work.event_name}
            break
    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.rew_by_oi=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_ieee")
        elif value=="no":
            work.rew_by_oi=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_ieee")


    try:
        return render(request,"EAD_app/oi_ieee.html",da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")



@login_required
def oi_saasc(request):
    list_work=venue.objects.filter(associated_club__exact="saasc")
    for work in list_work:
        if work.rew_by_oi==False and work.considered==False:
            da_dict={"secretary":work.user,"date":work.date,
                "venue_name":work.requested_venue_secy,
                "club":work.associated_club,
                "event":work.event_name}
            break
    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.rew_by_oi=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_saasc")
        elif value=="no":
            work.rew_by_oi=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_saasc")


    try:
        return render(request,"EAD_app/oi_saasc.html",da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")



@login_required
def oi_robotics(request):
    list_work=venue.objects.filter(associated_club__exact="robotics")
    for work in list_work:
        if work.rew_by_oi==False and work.considered==False:
            da_dict={"secretary":work.user,"date":work.date,
                "venue_name":work.requested_venue_secy,
                "club":work.associated_club,
                "event":work.event_name}
            break
    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.rew_by_oi=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_robotics")
        elif value=="no":
            work.rew_by_oi=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_robotics")


    try:
        return render(request,"EAD_app/oi_robotics.html",da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")


@login_required
def oi_voyagers(request):
    list_work=venue.objects.filter(associated_club__exact="voyagers")
    for work in list_work:
        if work.rew_by_oi==False and work.considered==False:
            da_dict={"secretary":work.user,"date":work.date,
                "venue_name":work.requested_venue_secy,
                "club":work.associated_club,
                "event":work.event_name}
            break
    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.rew_by_oi=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_voyagers")
        elif value=="no":
            work.rew_by_oi=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_voyagers")


    try:
        return render(request,"EAD_app/oi_voyagers.html",da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")



@login_required
def oi_music_club(request):
    list_work=venue.objects.filter(associated_club__exact="music_club")
    for work in list_work:
        if work.rew_by_oi==False and work.considered==False:
            da_dict={"secretary":work.user,"date":work.date,
                "venue_name":work.requested_venue_secy,
                "club":work.associated_club,
                "event":work.event_name}
            break
    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.rew_by_oi=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_music_club")
        elif value=="no":
            work.rew_by_oi=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/oi_music_club")


    try:
        return render(request,"EAD_app/oi_music_club.html",da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")

@login_required
def da_app(request):
    list_work=venue.objects.filter(rew_by_oi__exact=True,requested_venue_secy__exact="Auditorium") | venue.objects.filter(app_by_cdgc__exact=True,requested_venue_secy__exact="Audi With Arena")
    for work in list_work:
        if work.app_by_da==False and work.considered==False:
            da_dict={"date":work.date,
                "venue_name":work.requested_venue_secy,
                "club":work.associated_club,
                "event":work.event_name}
            break
    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.app_by_da=True
            work.app_final=True
            work.save()
            return HttpResponseRedirect("/EAD_app/da_app")
        elif value=="no":
            work.app_by_da=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/da_app")

    try:
        return render(request,"EAD_app/da_app.html",da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")



@login_required
def dsa_app(request):
    list_work=venue.objects.filter(app_by_da=True)
    for work in list_work:
        if work.app_by_dsa==False and work.considered==False:
            dsa_dict={"date":work.date,
                "venue_name":work.requested_venue_secy,
                "club":work.associated_club,
                "event":work.event_name}
            break

    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.app_by_dsa=True
            work.app_final=True
            work.save()
            return HttpResponseRedirect("/EAD_app/dsa_app")
        elif value=="no":
            work.app_by_dsa=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/dsa_app")

    try:
        return render(request,"EAD_app/dsa_app.html",dsa_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")

@login_required
def no_entry(request):
    return render(request,"EAD_app/no_entry.html",{})

@login_required
def approved_secy(request):
    usernam=request.user.username
    approved_forms=venue.objects.filter(user__username__exact=usernam,app_final__exact=True)
    return render(request,"EAD_app/approved_secy.html",{"approved_forms":approved_forms})

def approved_student(request):
    usernam=request.user.username
    approved_forms=venue.objects.filter(user__username__exact=usernam,app_final__exact=True)
    return render(request,"EAD_app/approved_student.html",{"approved_forms":approved_forms})


@login_required
def cdgc_app(request):
    list_work= venue.objects.filter(rew_by_oi__exact=True,requested_venue_secy__exact="Audi With Arena")
    for work in list_work:
        if work.app_by_cdgc==False and work.considered==False:
            da_dict={"date":work.date,
                "venue_name":work.requested_venue_secy,
                "club":work.associated_club,
                "event":work.event_name}
            break

    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.app_by_cdgc=True
            work.save()
            return HttpResponseRedirect("/EAD_app/cdgc_app")
        elif value=="no":
            work.app_by_cdgc=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/cdgc_app")
    try:
        return render(request,"EAD_app/cdgc_app.html",da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")


@login_required
def ois_app(request):
    list_work= venue.objects.filter(rew_by_oi__exact=True,requested_venue_secy__in=["l26","l27","l28"]) | venue.objects.filter(rew_by_hod__exact=True)
    for work in list_work:
        if work.app_by_ois==False and work.considered==False:
            if work.rew_by_oi==True:
                da_dict={"date":work.date,
                    "venue_name":work.requested_venue_secy,
                    "club":work.associated_club,
                    "event":work.event_name}
                break
            elif work.rew_by_hod==True:
                da_dict={"date":work.date,
                    "venue_name":work.requested_venue_student,
                    "club":"None",
                    "event":work.event_name}
                break

    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.app_by_ois=True
            work.app_final=True
            work.save()
            return HttpResponseRedirect("/EAD_app/ois_app")
        elif value=="no":
            work.app_by_ois=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/ois_app")
    try:
        return render(request,"EAD_app/ois_app.html",da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")


@login_required
def labt_rw(request):
    list_work= venue.objects.filter(requested_venue_student__in=["Lab-303","Lab-306","Lab-307","CL-13","CL-14"])
    for work in list_work:
        if work.rew_by_labt==False and work.considered==False:
            da_dict={"event":work.event_name,
                    "date":work.date,
                    "venue_name":work.requested_venue_student
                    }
            break

    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.rew_by_labt=True
            work.save()
            return HttpResponseRedirect("/EAD_app/labt_rw")
        elif value=="no":
            work.rew_by_labt=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/labt_rw")
    try:
        return render(request,"EAD_app/labt_rw.html",da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")


@login_required
def hod_rw(request):
    list_work= venue.objects.filter(rew_by_labt__exact=True)
    for work in list_work:
        if work.rew_by_hod==False and work.considered==False:
            da_dict={"event":work.event_name,
                    "date":work.date,
                    "venue_name":work.requested_venue_student
                    }
            break

    if request.method=="POST":
        value=request.POST.get("approve")
        if value=="yes":
            work.rew_by_hod=True
            work.save()
            return HttpResponseRedirect("/EAD_app/hod_rw")
        elif value=="no":
            work.rew_by_hod=False
            work.considered=True
            work.save()
            return HttpResponseRedirect("/EAD_app/hod_rw")
    try:
        return render(request,"EAD_app/hod_rw.html",da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/EAD_app/no_entry")
