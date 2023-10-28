from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
def survey(_):
    html='<html><body>"survey"</body></html>'
    return HttpResponse(html)

def about(request):
    return render(request, "about.html", {
        'active_menu':'about',
        })
