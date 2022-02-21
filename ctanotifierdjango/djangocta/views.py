from django.shortcuts import render
# this isn't working. Need to investigate why
#import keyHold
import requests

# Create your views here.
def index(request):
    # this isn't the URL i need to use; check docs
    # base url: http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx
    url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={}&stpid=30126&outputType=JSON"
    #key = keyHold.TT_API_K
    key = "880e68d77bed4ca4b68a5681cbf7def5"
    response = requests.get(url.format(key)).json()
    #print(response.text)

    # might need to generate dictionaries in a loop or store them in a list
    # more than one dictionary per response
    ## ctatt is the exterior
    
    stop_data = {
        # stopID will be inserted with variable once its working; just like key is in URL above; just use that variable
        'requestTime' : response['ctatt']['tmst'],
        'stopId' : response['ctatt']['eta'][0]['stpId'],
        'stationName' : response['ctatt']['eta'][0]['staNm'],
        'destinationName' : response['ctatt']['eta'][0]['destNm'],
        'predictionTime' : response['ctatt']['eta'][0]['prdt'],
        'arrivalTime' : response['ctatt']['eta'][0]['arrT'],
        'approachingBool' : response['ctatt']['eta'][0]['isApp'],
        'delayedBool' : response['ctatt']['eta'][0]['isDly']
    }

    # passing info to template
    context = {'stop_data' : stop_data}

    return render(request, 'djangocta/djangocta.html', context)