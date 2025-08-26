from django.shortcuts import render, redirect
from django.http import HttpResponse
from url_shortener.models import longtoshort


# Create your views here.
def hello_world(request):
    return HttpResponse("Hello how are you")


def task(request):
    context = {
        "year": "2023",
        "attendees": ["lakshmi", "prasanna", "pragathi", "saranya"]
    }
    return render(request, "task.html", context)


def home_page(request):
    context = {
        "submitted": False,
        "error": False
    }

    if request.method == "POST":
        data = request.POST
        longurl = data['longurl']
        customname = data['custom_name']

        try:
            # save only the slug (customname) in DB
            obj = longtoshort(long_url=longurl, custom_name=customname)
            obj.save()

            # display shortened full URL to user
            short_url = request.build_absolute_uri(customname)

            context["long_url"] = longurl
            context["custom_name"] = short_url
            context["submitted"] = True
            context["date"] = obj.create_date
            context["clicks"] = obj.vist_count

        except Exception as e:
            print("Error:", e)
            context["error"] = True

    return render(request, "index.html", context)


def redirect_url(request, customname):
    row = longtoshort.objects.filter(custom_name=customname)
    if not row.exists():
        return HttpResponse("This endpoint doesn't exist error!!")
    obj = row.first()
    long_url = obj.long_url
    obj.vist_count += 1
    obj.save()
    return redirect(long_url)


def analytics(request):
    rows = longtoshort.objects.all()
    context = {
        "rows": rows
    }
    return render(request, "analytics.html", context)
