from django.urls import path
from EAD_app import views

app_name='EAD_app'

urlpatterns = [
    path('register/',views.user_info_view,name='register'),
    path('user_login/',views.user_login,name="user_login"),
    path('booking_secy/',views.venue_book_secy,name="booking_secy"),
    path('booking_student/',views.venue_book_student,name="booking_student"),
    path('oi_nss/',views.oi_nss,name="oi_nss"),
    path('oi_css/',views.oi_css,name="oi_css"),
    path('oi_ieee/',views.oi_ieee,name="oi_ieee"),
    path('oi_saasc/',views.oi_saasc,name="oi_saasc"),
    path('oi_robotics/',views.oi_robotics,name="oi_robotics"),
    path('oi_voyagers/',views.oi_voyagers,name="oi_voyagers"),
    path('oi_music_club/',views.oi_music_club,name="oi_music_club"),
    path('da_app/',views.da_app,name="da_app"),
    path('dsa_app/',views.dsa_app,name="dsa_app"),
    path("no_entry/",views.no_entry,name="no_entry"),
    path("approved_secy/",views.approved_secy,name="approved_secy"),
    path("cdgc_app/",views.cdgc_app,name="cdgc_app"),
    path("ois_app/",views.ois_app,name="ois_app"),
    path("labt_rw/",views.labt_rw,name="labt_rw"),
    path("hod_rw/",views.hod_rw,name="hod_rw"),
    path("approved_student/",views.approved_student,name="approved_student")

]
