from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
import joblib
from main.models import Profile

def home(request):
    return render(request,"home.html")

# def logins(request):
#     return render(request,"login.html")

# def handlogout(request):
#     logout(request)
#     return redirect('home')

def handlogin(request):
    if request.method=='POST':
        logusername=request.POST['logusername']
        logpass=request.POST['logpass']
        user=authenticate(username=logusername,password=logpass)  
        # if user is not None:
        login(request,user)
        messages.success(request,'successfully login')
        return redirect('prediction')
        # else:
            # messages.error(request,'invalid user')
            # return redirect('home')

# def log(request):
#     if request.method=='POST':
#         username=request.POST['username']
#         email=request.POST['email']
#         password1=request.POST['password1']
#         password2=request.POST['password2']
#         dob=request.POST['dob']
#         #sex=request.POST['sex']
#         if (password1!=password2):
#             messages.error(request,'password incorrect')
#             return redirect('login')
#         myuser=User.objects.create_user(username,email,password1)
        
#         myuser.save()
#         messages.success(request,"your account has been created")

#         info=Profile(username=myuser,dob=dob,email=email)
#         info.save()
#         return redirect('home')
#     else:
#         return HttpResponse('Error')

def prediction(request):
    return render(request,"prediction.html")



def suggestions(request):
    
    return render(request,"suggestions.html")

def prevent(lis, z):
    suggest = ""
    ans = []
    if z == 0 :
        if lis[ 0] > 50 :
            suggest += "Paitent is highly vulnerable to Heart Disease "
        else:
            suggest+=" Paitent must strictly follow the suggestions "
        ans.append(suggest)
        suggest = ""
        suggest += """* High Fiber Food  like Whole grain, beans , apple , corn , dried fruits 
        * Avoid High Transfat Food like Fast food , packed food 
        * Avoid oily Food 
        """
        ans.append(suggest)
        suggest = ""
        
        if lis[0] > 40 and lis[0] <= 50 :
            suggest += "* Daily walk 2 km "
        elif lis[0] <= 40 :
            suggest += "Daily walk 5 km  * Yoga  * Breathing Exercise " 
        suggest += "Avoid alcohol , tobacco product , smoking "
        if lis[0 ] > 40 :
            suggest += "Body Mass Index must be less than 25 "
        suggest += "Maintain Sleep and Stress  maitain salt and sugar intake "
        ans.append(suggest)
        suggest = ""
        suggest +="""
        * Nitrates
        * BiDil """
        if lis[3] > 140 :
            suggest += " * Calcium Channel Blocker "
        suggest += "  Contact your Doctor "
        if lis[5]  == 1 :
            suggest += " May need to do PCI "
        ans.append(suggest)
    if z == 4 :
        suggest="Patient should follow preventionly measurese to prevent heart disease "
        ans.append(suggest)
        suggest = ""
        suggest += """
        * Consume more vegetable and Fruits , fish,poutary, 
        * Use vegetable Oil
        * Low Transfat
        * Avoid refined carbohydrate
        * Avoid Processed Sugar
        * Dash Diet """
        ans.append(suggest)
        suggest = ""


        suggest = """
        * Avoid   alcohol , tobacco product , smoking 
        * Try to do daily exercise 
        * Maintain good BMI 
        * Do total check up once a year

        """
        ans.append(suggest)
        ans.append("NO MEDICINE NEEDED")
    else:
        suggest="Patient should focuse more on their health "
        ans.append(suggest)
        suggest = ""
        suggest+= """
        * Low Transfat
        * Avoid refined carbohydrate
        * Dash Diet
        * High Fiber Food  like Whole grain, beans , apple , corn , dried fruits
        """
        ans.append(suggest)
        suggest = ""
        
        if lis[0] > 40 and lis[0] <= 50 :
            suggest += "* Daily walk 2 km "
        elif lis[0] <= 40 :
            suggest += "Daily walk 5 km  * Yoga  * Breathing Exercise " 
        suggest += "Avoid alcohol , tobacco product , smoking  "
        suggest += "Maintain Sleep and Stress  maitain salt and sugar intake "
        ans.append(suggest)
        suggest=""
        if lis[2] == 0 or lis[0] == 1 :
            suggest += "Antiaginal drug like Nitrate "
            if lis[3] > 140:
                suggest += "beta blocker , Calcium Channel Blocker"
        if lis[5] == 1:
             suggest += "antidibetics drug / insulin"
        if lis[3] > 140 :
            suggest += "anti hypertension drug like ACEI / ARB "
        if lis[4] > 250 :
            suggest += "Antihyperlipidemie drug like Statins"
        ans.append(suggest)
        suggest = ""




    
    return ans



def result(request):
    cls=joblib.load('final_mod.sav')
    abc=joblib.load('final_kmeansmodel.sav')
    lis=[]
    lis.append(int(request.GET['age']))
    lis.append(int(request.GET['sex']))
    lis.append(int(request.GET['cp']))
    lis.append(int(request.GET['trestbps']))
    lis.append(int(request.GET['chol']))
    lis.append(int(request.GET['fbs']))
    lis.append(int(request.GET['restecg']))
    lis.append(int(request.GET['thalach']))
    lis.append(int(request.GET['exang']))
    

    print(lis)

    ans=cls.predict([lis])
    
    y=ans[0]
    lis.append(y)

    an=abc.predict([lis])
    z=an[0]
    print(z)
    
    t=""
    d={2:"moderate",1:"moderately severe",0:"severe ",4:"low",3:"mild"}
    if(y==1):
        
        x="You have "+d[z]+" risk of heart disease," +"stage is "+str(z)  
        ans = prevent(lis, z )
         
        
        return render(request,"result.html",{'x':x,'t':ans[0], 'u' : ans[1], 'v': ans[2], 'w':ans[3]})
    else:
        x="You are Safe,stage 5"
        t="NA"
        u="NA"
        v="NA"
        w="NA"
        return render(request,"result.html",{'x':x,'t':t,'u':u,'v':v,'w':w})