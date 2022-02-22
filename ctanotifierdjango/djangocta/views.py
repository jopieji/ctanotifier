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
    key = "keyHere"
    response = requests.get(url.format(key)).json()
    #print(response.text)

    # might need to generate dictionaries in a loop or store them in a list
    # more than one dictionary per response
    ## ctatt is the exterior
    
    base = response['ctatt']['eta'][0]['arrT']

    estArrivalFormatted = base

    firstTwo = estArrivalFormatted[11:13]
    if int(firstTwo) > 12:
        hrNum = int(firstTwo) - 12
        estArrivalFormatted = str(hrNum) + estArrivalFormatted[13:] + " PM"
    else:
        estArrivalFormatted = estArrivalFormatted[11:] + " AM"

    requestTime = response['ctatt']['tmst'][14:16]
    minToArrival = base[14:16]
    print(requestTime)
    print(minToArrival)
    arrival = int(minToArrival) - int(requestTime)
    #arrival = 0

    stop_data = {
        # stopID will be inserted with variable once its working; just like key is in URL above; just use that variable
        'requestTime' : response['ctatt']['tmst'],
        'stopId' : response['ctatt']['eta'][0]['stpId'],
        'stationName' : response['ctatt']['eta'][0]['staNm'],
        'destinationName' : response['ctatt']['eta'][0]['destNm'],
        'predictionTime' : response['ctatt']['eta'][0]['prdt'],
        'arrivalTime' : estArrivalFormatted,
        'approachingBool' : response['ctatt']['eta'][0]['isApp'],
        'delayedBool' : response['ctatt']['eta'][0]['isDly'],
        'arrival' : arrival,
    }

    # passing info to template
    context = {'stop_data' : stop_data}

    return render(request, 'djangocta/djangocta.html', context)