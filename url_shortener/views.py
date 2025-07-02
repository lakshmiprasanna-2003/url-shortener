
from django.shortcuts import render, redirect
from django.http import HttpResponse
from url_shortener.models import longtoshort



# Create your views here.
def hello_world(request):
    return HttpResponse("Hello how are you")

def task(request):
    context={"year":"2023","attendees":["lakshmi","prasanna","pragathi","saranya"]}
    return render(request,"task.html",context)

def home_page(request):
    context={
        "submitted":False,
        "error":False
             
    }
    print(request.META)

    if request.method=="POST":
        #print(request.POST)
        data=request.POST
        longurl=data['longurl']
        customname=data['custom_name']

        try:

            context["long_url"]=longurl
            context["custom_name"]=request.build_absolute_uri() + customname
            customname=request.build_absolute_uri() + customname
            obj =longtoshort(long_url=longurl,custom_name=customname)
            obj.save()
            context["submitted"]=True
            context["date"]=obj.create_date
            context["clicks"]=obj.vist_count
            
        except:
            context["error"]=True    
    
        #print(longurl,customname)       

    else:
        print("User didn't submit yet")
    return render(request,"index.html",context)

def redirect_url(request,customname):
    row=longtoshort.objects.filter(custom_name=customname)
    if len(row)==0:
        return HttpResponse("this endpoint doesn't exist error!!")
    obj=row[0]
    long_url=obj.long_url
    obj.vist_count += 1
    obj.save()
    return redirect(long_url)

def analytics(request):
    rows=longtoshort.objects.all()
    context={
        "rows":rows
    }
    return render(request,"analytics.html",context)