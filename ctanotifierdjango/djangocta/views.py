from django.shortcuts import render
# this isn't working. Need to investigate why
#import keyHold
import requests

# Create your views here.
def index(request):
    # this isn't the URL i need to use; check docs
    # base url: http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx
    url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={}&stpid=30126"
    #key = keyHold.TT_API_K
    key = "keyGoesHere"
    response = requests.get(url.format(key))
    print(response.text)

    return render(request, 'djangocta/djangocta.html')