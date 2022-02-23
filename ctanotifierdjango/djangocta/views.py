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

    # red line stop id's
    # this probably isn't where these are stored, but for now it's where they are going
    red_line_ids = {
        'howard': 40900,
        'jarvis': 41190,
        'morse': 40100,
        'loyola': 41300,
        'granville': 40760,
        'thorndale': 40880,
        'bryn mawr': 41380,
        'berwyn': 40340,
        'argyle': 41200,
        'lawrence': 40770,
        'wilson': 40540,
        'sheridan': 40080,
        'addison': 41420,
        'belmont': 41320,
        'fullerton': 41220,
        'north/clybourn': 40650,
        'clark/division': 40630,
        'chicago': 41450,
        'grand': 40330,
        'lake': 41660,
        'monroe': 41090,
        'jackson': 40560,
        'harrison': 41490,
        'roosevelt': 41400,
        'cermak-chinatown': 41000,
        'sox-35th': 40190,
        '47th': 41230,
        'garfield': 41170,
        '63rd': 40910,
        '69th': 40990,
        '79th': 40240,
        '87th': 41430,
        '95th/dan ryan': 40450
    }

    # brown line stop ids: direction is super critical here
    brown_line_ids = {
        'ravenswood': 0,
        'kedzie': 0,
        'francisco': 0,
        'rockwell': 0,
        'western': 0,
        'damen': 0,
        'montrose': 0,
        'irving park': 0,
        'addison': 0,
        'paulina': 0,
        'southport': 0,
        'belmont': 0,
        'wellington': 0,
        'diversey': 0,
        'fullerton': 0,
        'armitage': 0,
        'sedgwick': 0,
        'chicago': 0,
        'merchandise mart': 0,
        'clark/lake': 0,
        'state/lake': 0,
        'randolph/wabash': 0,
        'madison/wabash': 0,
        'adams/wabash': 0,
        'harold washington library': 0,
        'lasalle/van buren': 0,
        'quincy': 0,
        'washington/wells': 0
    }

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
    arrivalMin = base[14:16]
    
    arrival = int(arrivalMin) - int(requestTime)
    #arrival = 0

    if abs(arrival) > 40:
        arrival = 60 - int(requestTime) + int(arrivalMin)
    print(arrival)

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