from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from ots_app.models import Candidate,Question,Result
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import EmailMultiAlternatives
import random
from datetime import datetime
from django.core.paginator import Paginator


class OTS_APP:
    def __init__(self):
        self.instructions=None
    
    # generate otp
    def generate_otp(self):
        randomNumber = random.randint(1000,9999)
        self.generated_otp=randomNumber
        return self.generated_otp
    
    # when page not found
    def error_404(self,request,exception):
        
        return render(request,'404.html',status=404)
    
    # when error found from server
    def error_500(self,request):
        
        return render(request,'500.html',status=500)

    # email send
    def email_send(self,request,user_email):
        try:
            self.OTP=self.generate_otp()
            context={'OTP':self.OTP}
            
            subject, from_email, to = 'OTP Verification', 'djangoaayansh@gmail.com', user_email
            t=loader.get_template('email_send.html')
            html_template=t.render(context)
            msg = EmailMultiAlternatives(subject,  html_template,from_email, [to])
            msg.attach_alternative(html_template, "text/html")
            msg.send()
            return 1
        except:
           return 0
    
    # landing page / welcome page
    def Welcome(self,request):
        if 'name' not in request.session.keys():
            template=loader.get_template('welcome.html')
            res=template.render({'title':'welcome'},request)
            return HttpResponse(res)
        else:
            return HttpResponseRedirect('home',request)

    # register page
    def CandidateRegistrationFrom(self,request):
        if 'name' not in request.session.keys():
            template=loader.get_template('register.html')
            res=template.render({'title':'register'},request)
            return HttpResponse(res)
        else:
            return HttpResponseRedirect('home',request)

    # otp accept
    def send_otp(self,request):
        if request.method == 'POST':
            postData=request.POST
            self.userName=postData.get('user_name')
            self.password=postData.get('password')
            self.name=postData.get('name')
            self.email=postData.get('email')
            
            # check if user already exists
            if len(Candidate.objects.filter(username=self.userName))==0 and len(Candidate.objects.filter(email=self.email))==0:
                # send otp in gmail
                isconnect=self.email_send(request,self.email)
                
                if isconnect:
                    messages.success(request,'Check Your Email')
                    self.redirect='register.html'
                    # self.titles='register'
                    self.counter=3
                else:
                    messages.error(request,'Please Connect To The Internet.')
                    return HttpResponseRedirect('ragistrationForm',request)
                
                self.context={
                    'user_name':self.userName,
                    'password':self.password,
                    'name':self.name,
                    'email':self.email,
                }
                return render(request,'register.html',{'title':'verify otp','otp_validate':isconnect,'context':self.context})
            else:
                messages.error(request,"Already Exists.")
                return HttpResponseRedirect('ragistrationForm',request)
        
        # when user input invalid otp and get access to get method
        try:
            # to identify which fuction call
            if self.isRunStoreCandidate == 1:  # CandidateRegistration method
                self.isRunStoreCandidate=0
                return render(request,'register.html',{'title':'verify otp','otp_validate':1,'context':self.context})
            elif self.isRunStoreCandidate == 2: # forgot pin method
                self.isRunStoreCandidate=0
                return render(request,'forgotPin.html',{'title':'verify otp','otp_validate':1,'email_name':self.email_user})
        except:
            pass


    # email check user otp enter invalid 
    def email_checker(self,request):
        if self.counter==0:
            self.counter=3
            isconnect=self.email_send(request,self.email)
            if isconnect:
                messages.success(request,'Check Your Email Again') 
                return isconnect
            else:
                messages.error(request,'Please Connect To The Internet.')
                return 0
        messages.error(request,f"Invalid OTP, You have a chance {self.counter}.")
        self.counter-=1
        return 1
    
    # register success
    def CandidateRegistration(self,request):
        if request.method=='POST':
            postData=request.POST
            otp=postData.get('otp')
            
            if not otp==str(self.OTP):
                check=self.email_checker(request)
                if check==1:
                    self.isRunStoreCandidate=1
                    return HttpResponseRedirect('verifyotp',request)
                else:
                    return HttpResponseRedirect('ragistrationForm',request)    
            # store data in data base
            candidate=Candidate() # object create
            candidate.username=self.userName
            self.password=make_password(self.password)  # hash password
            candidate.password=self.password
            candidate.name=self.name
            candidate.email=self.email
            candidate.save()
            return HttpResponseRedirect('login',request)
            
    # leave user message
    def send_user_message(self,request):
        if request.method=='POST':
            postData=request.POST
            Name=None
            Email=None
            if 'username' in request.session.keys():
                candidate=Candidate.objects.get(username=request.session['username'])
                Name=candidate.name
                Email=candidate.email
            else:   
                Name=postData.get('name')
                Email=postData.get('email')
            
            if Email==None:
                return HttpResponseRedirect('/',request)
            
            topic=postData.get('options')
            user_message=postData.get('user_message')
            context={
                'Name':Name,
                'Email':Email,
                'topic':topic,
                'user_message':user_message
            }
            # send message
            subject, from_email, to = topic, 'djangoaayansh@gmail.com','djangoaayansh@gmail.com'
            t=loader.get_template('user_message.html')
            html_template=t.render(context)
            msg = EmailMultiAlternatives(subject,  html_template,from_email, [to])
            msg.attach_alternative(html_template, "text/html")
           
            msg.send()
            
            messages.success(request,'we will contact you shortly')
            return HttpResponseRedirect('contact',request)

    
    # home page
    def CandidateHome(self,request):
        
        if 'name' not in request.session.keys():
            return HttpResponseRedirect('/',request)
        # fetch from data base
        titles_imgs=list(Question.objects.values_list('title','img'))
        
        
        
        # remove duplicate title/subject
        temp=[]
        inc=0
        for title_img in titles_imgs:
            if titles_imgs.index(title_img)==inc and title_img[1]!='':
                temp.append(title_img)
            inc+=1
        
        titles_imgs=temp
        
        temp=[]
        
        # conver list to dict
        l=['title','img']
        for title_img in titles_imgs:
            dict={}
            inc=0
            for ti in title_img:
                dict[l[inc]]=ti
                inc+=1
            temp.append(dict)
        titles_imgs=temp
        
        paginator = Paginator(titles_imgs, 6)
        page_number=request.GET.get('page')
        finalData=paginator.get_page(page_number)
        totalpage=finalData.paginator.num_pages
        
        res=render(request,'home.html',{'title':'homepage','titles_imgs':finalData,'totalpagelist':[n+1 for n in range(totalpage)],'lastpage':totalpage})
        return res

    # about
    def about(self,request):
        return render(request,'about.html',{'title':'about'})
    # contact
    def contact(self,request):
        return render(request,'contact.html',{'title':'contact'})
    
    # login page
    def LoginView(self,request):
        if 'forgot_pin' in request.session.keys():
            del request.session['forgot_pin']
            del request.session['username']
            request.session.flush()
        
        if 'name' not in request.session.keys():
            if request.method=='POST':
                postData=request.POST
                # get data
                self.login_username=postData.get('user_name')
                self.login_password=postData.get('password')
                
                candidate=Candidate.objects.filter(username=self.login_username)
                
                if len(candidate) and check_password(self.login_password,Candidate.objects.get(username=self.login_username).password):
                    # create session. you can store any thing in session. you can use any where request.session
                    
                    request.session['username']=candidate[0].username 
                    request.session['name']=candidate[0].name
                    res=HttpResponseRedirect('home',request)
                    return res
                
                messages.error(request,"Invalid username or password.")
            
            res=render(request,'login.html',{'title':'login'})
            return res
        else:
            return HttpResponseRedirect('home',request)
        
    # forgot pin
    def forgot_pin(self,request):
        # when user login-in and want to access forgot-pin by url user will redirect to home page
        if 'name' in request.session.keys():
            return HttpResponseRedirect('home',request)
        
        isconnect=0
        
        if request.method=='POST':
            
            self.email_user=request.POST['email_name']
            candidates=Candidate.objects.all().values()
            
            for candidate in candidates:
                if candidate['username']==self.email_user or candidate['email']==self.email_user:
                    self.userName=candidate['username']
                    self.email=candidate['email']
                    
                    self.counter=3
                    isconnect=self.email_send(request,self.email)
                    if isconnect:
                        request.session['username']=self.userName
                        request.session['forgot_pin']='forgot_pin'# to identify which session is running
                        request.session.set_expiry(60)
                        request.session.modified=True # when any activity session expiry auto increment
                        # request.session.
                        messages.success(request,'Check Your Email')
                        
                        self.isRunStoreCandidate=2 
                        return HttpResponseRedirect('verifyotp',request)
                        
                    else:
                        messages.error(request,"Please Connect to the internet.")
                        return render(request,'forgotPin.html',{'title':'forgotPin','email_name':self.email_user})
                    
            else:
                messages.error(request,'Invalid UserName or Email id.')
            
        return render(request,'forgotPin.html',{'title':'forgotPin'})
        
       
        

       
    
    # logic to update password/forgot password
    def update_password(self,request):
        try:
            if 'username' not in request.session.keys() and self.email!=None:
                messages.error(request,"Session expired.")
                return HttpResponseRedirect('/',request)
        except:
            pass
        
        if request.method=='POST':
            new_password=request.POST.get('password')
            UserName=request.session['username']
            candidate=Candidate.objects.get(username=UserName)
            # covert plain text to cypher text
            new_password=make_password(new_password)
            
            temp=Candidate()
            temp.username=candidate.username
            temp.password=new_password
            temp.email=candidate.email
            temp.name=candidate.name
            temp.test_attempt=candidate.test_attempt
            temp.point=candidate.point
            temp.save()
            
            del request.session['username']
            del request.session['forgot_pin']
            request.session.flush()
            messages.success(request,'Password Updated successfully')
            return HttpResponseRedirect('login',request)

        return HttpResponseRedirect('/',request)
    
    # reset password 
    def reset_password(self,request):
        if 'name' in request.session.keys():
            return HttpResponseRedirect('home',request)
        

        if request.method=='POST':
            postData=request.POST
            otp=postData.get('otp')
            # when session expired
            if 'username' not in request.session.keys():
                messages.error(request,"Session expired.")
                return HttpResponseRedirect('/',request)
            
            if not otp==str(self.OTP):
                check=self.email_checker(request)
                if check==1:
                    self.isRunStoreCandidate=2
                    return HttpResponseRedirect('verify otp',request)
                else:
                    return HttpResponseRedirect('ragistration-form',request)
            
            return render(request,'reset_password.html')

        
       
        return HttpResponseRedirect('forgot-pin',request)
        
    
    
    
    # TestResultHistory
    def TestResultHistory(self,request):
        if 'name' not in request.session.keys():
            return HttpResponseRedirect('login',request)
        
        candidate=Result.objects.filter(username=request.session['username'])
      
        results=[]
        for i in candidate:
            temp={}
        
           
            temp['title']=i.title
            temp['date']=i.date
            temp['time']=i.time
            temp['right']=i.right
            temp['wrong']=i.wrong
            temp['points']=round((i.points),1)
            temp['user_answer_id']=i.resultid
            results.append(temp)
        
        
        return render(request,'history_test_list.html',{'title':'test-history','results':results,'name':request.session['name']})
        
    def ShowResultHistory(self,request,id1):
        if 'name' not in request.session.keys():
            return HttpResponseRedirect('login',request)
       
        res=Result.objects.get(resultid=id1)
        
        
        if request.session['username']==res.username.username:
            
            # fetch user answer and Question id from Result table
            user_answer_option=res.user_answer_option
            
            user_answer_option=user_answer_option.strip('[]')
            # conver string into list
            user_answer_option=user_answer_option.split(',')
            temp=[]
            for i in user_answer_option:
                i=i.strip(" ").strip("'")
                temp.append(i)
                
            user_answer_option=temp
            
            Questions=[]
            # fetch time duration from Result table
            time_durations=res.time_durations
            for t in user_answer_option:
                
                t=t.split("-")
                t[0]=t[0]
                t[1]=int(t[1])
                temp_dict={}
                temp_dict['border_color_a']='info'
                temp_dict['background_color_a']='bg-transparent'
                temp_dict['border_color_b']='info'
                temp_dict['background_color_b']='bg-transparent'
                temp_dict['border_color_c']='info'
                temp_dict['background_color_c']='bg-transparent'
                temp_dict['border_color_d']='info'
                temp_dict['background_color_d']='bg-transparent'
                
                q_obj=Question.objects.get(Qid=t[1])
                
                temp_dict['Question']=q_obj.Question
                answer=q_obj.answer
                temp_dict['option_a']=q_obj.option_a
                temp_dict['option_b']=q_obj.option_b
                temp_dict['option_c']=q_obj.option_c
                temp_dict['option_d']=q_obj.option_d
                
                if t[0]=='a':
                    temp_dict['border_color_a']='danger-subtle'
                    temp_dict['background_color_a']='bg-danger'
                elif t[0]=='b':
                    temp_dict['border_color_b']='danger-subtle'
                    temp_dict['background_color_b']='bg-danger'
                elif t[0]=='c':
                    temp_dict['border_color_c']='danger-subtle'
                    temp_dict['background_color_c']='bg-danger'
                else:
                    temp_dict['border_color_d']='danger-subtle'
                    temp_dict['background_color_d']='bg-danger'

                if answer==q_obj.option_a:
                    temp_dict['border_color_a']='success-subtle'
                    temp_dict['background_color_a']='bg-success'
                elif answer==q_obj.option_b:
                    temp_dict['border_color_b']='success-subtle'
                    temp_dict['background_color_b']='bg-success'
                elif answer==q_obj.option_c:
                    temp_dict['border_color_c']='success-subtle'
                    temp_dict['background_color_c']='bg-success'
                elif answer==q_obj.option_d:
                    temp_dict['border_color_d']='success-subtle'
                    temp_dict['background_color_d']='bg-success'
                temp_dict['explanation']=q_obj.explanation
                
                Questions.append(temp_dict)
            
            return render(request,'result_history.html',{'title':'result_history','Questions':Questions,'time_durations':time_durations})      
        else:
            return HttpResponseRedirect('home',request)
    
    # CalculateTestResult
    def CalculateTestResult(self,request):
        if 'name' not in request.session.keys():
            return HttpResponseRedirect('/',request)

        if 'test_paper' not in request.session.keys():
            return HttpResponseRedirect('/',request)
        
        
        total_right=0
        total_wrong=0
        # fetch Question id from client side
        list_question_id=[]
        for k in request.POST:
            if k.startswith('question_'):
                list_question_id.append(int(request.POST[k]))
        # fetch question from database table
            
        titles=''
        user_answers=[]
        for fetch in list_question_id:
            # return object
            question_list=Question.objects.get(Qid=fetch)
            titles=question_list.title
            
            user_select_option=request.POST[f'option_{fetch}']
            if user_select_option[0:-1]==question_list.answer:
                total_right+=1
            else:
                total_wrong+=1
            t=str()
            
            t=f"{user_select_option[-1]}-{fetch}"
            
            user_answers.append(t)
            
        
        
        total_points=round((total_right-total_wrong)/len(list_question_id)*10,1)
        
        # store result in result table
        result=Result() # create result object
        
        result.username=Candidate.objects.get(username=request.session['username'])
        
        result.title=titles
        result.right=total_right
        result.wrong=total_wrong
        result.points=total_points
        result.user_answer_option=user_answers
        self.end_time=datetime.now()
        
        # end time calculate and store in data base
        result.time_durations=str(self.end_time-self.start_time).split('.')[0]
        result.save()
        # update candidate table
        candidate=Candidate.objects.get(username=request.session['username'])
        candidate.test_attempt=+1
        candidate.point+=total_points
        candidate.save()
        
   
    # test paper
    def TestPaper(self,request,titles):
        # fetch question from database
        que=list(Question.objects.filter(title=titles).values())
        
        # restrict to access test paper using url
        try:
            if len(que)!=0 and self.instructions==titles:
                random.shuffle(que)
                self.instructions=None
            else:
                
                self.instructions=None
                return HttpResponseRedirect('/',request)
        except:
            self.instructions=None
            return HttpResponseRedirect('/',request)
            
        
        # when not log-in
        if 'name' not in request.session.keys():
            que=que[:10]
            context={
                'que':que,
            }
        else:
            # when login
            que=que[:25]
            context={
                'que':que,
                'subject':que[0]['title'],
                'name':request.session['name'],
            }
        self.start_time=datetime.now()
        # create session
        request.session['test_paper']='test_paper'
        return render(request,'test_paper.html',{'Questions':context,'title':'test'})
        
        
        

# result
    def ShowTestResult(self,request):

        if 'test_paper' not in request.session.keys():
            return HttpResponseRedirect('/',request)
        
        if 'name' not in request.session.keys():
            
            # calculate when time 
            self.end_time=datetime.now()
            time_durations=str(self.end_time-self.start_time).split('.')[0]
            
            # when user log out
            total_right=0
            total_wrong=0
            # fetch Question id from client side
            list_question_id=[]
            for k in request.POST:
                if k.startswith('question_'):
                    list_question_id.append(int(request.POST[k]))
            
            titles=''
            for fetch in list_question_id:
            # return object
                question_list=Question.objects.get(Qid=fetch)
                titles=question_list.title
            
                if request.POST[f'option_{fetch}'][0:-1]==question_list.answer:
                    total_right+=1
                else:
                    total_wrong+=1
            
            total_points=round((total_right-total_wrong)/len(list_question_id)*10,1)
            res={
                'title':'result',
                'subject':titles,
                'right':total_right,
                'wrong':total_wrong,
                'point':total_points,
                'time_duration':time_durations
            }
            del request.session['test_paper']
            request.session.flush()
            return render(request,'result.html',{'res':res,'not_login':1})
            
        
        
        # when user log in
        self.CalculateTestResult(request)
        result=Result.objects.get(resultid=Result.objects.latest('resultid').resultid)
        
        res={
            'title':'result',
            'subject':result.title,
            'right':result.right,
            'wrong':result.wrong,
            'point':result.points,
            'time_duration':result.time_durations
        }
        
        del request.session['test_paper']
        
        return render(request,'result.html',{'res':res,'name':request.session['name']})
    

    
    
    # Instructions about test login
    def instruction(self,request,titles):
        if 'name' not in request.session.keys():
            return HttpResponseRedirect('/',request)
        self.instructions=titles

        return render(request,'instruction.html',{'title':'OTS | instruction','titles':titles,'number_of_question':'25'})

    # instractions about test logout
    def ins(self,request,titles):
        if 'name' in request.session.keys():
            return HttpResponseRedirect('/',request)
        self.instructions=titles#
        return render(request,'instruction.html',{'title':'OTS | instruction','titles':titles,'number_of_question':'10'})
    
    # log out
    def LogOut(self,request):
        # session destory
        if 'test_paper' in request.session.keys():
            del request.session['test_paper']
        
        if 'username' in request.session.keys(): 
            del request.session['username']
            del request.session['name']
            request.session.flush()
        return HttpResponseRedirect('/',request)