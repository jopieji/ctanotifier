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
    brn_line_ids = {
        'kimball': 41290,
        'kedzie': 41180,
        'francisco': 40870,
        'rockwell': 41010,
        'western': 41480,
        'damen': 40090,
        'montrose': 41500,
        'irving park': 41460,
        'addison': 41440,
        'paulina': 41310,
        'southport': 40360,
        'belmont': 41320,
        'wellington': 41210,
        'diversey': 40530,
        'fullerton': 41220,
        'armitage': 40660,
        'sedgwick': 40800,
        'chicago': 40710,
        'merchandise mart': 40460,
        'clark/lake': 40380,
        'state/lake': 40260,
        'randolph/wabash': 0,
        'madison/wabash': 0,
        'adams/wabash': 40680,
        'harold washington library': 40850,
        'lasalle/van buren': 40160,
        'quincy': 40040,
        'washington/wabash': 41700,
        'washington/wells': 40730
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