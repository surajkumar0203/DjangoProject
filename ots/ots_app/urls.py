from ots_app.views import OTS_APP
from django.urls import path
from django.urls import re_path as url  
from django.views.static import serve 
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404,handler500


# create object of ots app
oa=OTS_APP()



urlpatterns = [
   url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),# use in productinon media file
   url(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),# use in productinon static file
   path('',oa.Welcome,name='welcomepage'),
   path('ragistrationForm',oa.CandidateRegistrationFrom,name='ragistration-form'),
   path('verifyotp',oa.send_otp,name='verifyotp'),
   path('storeCandidate',oa.CandidateRegistration,name='store-candidate'),
   path('home',oa.CandidateHome,name='home'),
   path('about',oa.about,name='about'),
   path('contact',oa.contact,name='contact'),
   path('login',oa.LoginView,name='login'),
   path('forgotpin',oa.forgot_pin,name='forgot-pin'),
   path('resetpassword',oa.reset_password,name='reset_password'),
   path('updatepassword',oa.update_password,name='update_password'), # update forget password logic
   path('testhistory',oa.TestResultHistory,name='test-history'),
   path('calculateresult',oa.CalculateTestResult,name='calculate_result'),
   path('testpaper/<str:titles>/',oa.TestPaper,name='test_paper'),
   path('result',oa.ShowTestResult,name='result'),
   path('resulthistory/<int:id1>/',oa.ShowResultHistory,name='result-history'),
   path('instruction/<str:titles>/',oa.instruction,name='instruction'),#login
   path('instructions/<str:titles>/',oa.ins,name='ins'),#logout
   path('sendusermessage',oa.send_user_message,name='send_user_message'),
   path('logout',oa.LogOut,name='logout'),

] #+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# page not found
handler404 = oa.error_404

# server error
handler500 = oa.error_500

if settings.DEBUG:
   urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)