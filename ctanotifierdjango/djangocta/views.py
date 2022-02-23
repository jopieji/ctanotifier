from django.shortcuts import render
# this isn't working. Need to investigate why
#import keyHold
import requests

# red line stop id's
    # this probably isn't where these are stored, but for now it's where they are going
    # first is northbound, then southbound
red_line_ids = {
        'howard': [30173, 30174],
        'jarvis': [30227, 30228],
        'morse': [30020, 30021],
        'loyola': [30251, 30252],
        'granville': [30147, 30148],
        'thorndale': [30169, 30170],
        'bryn mawr': [30267, 30268],
        'berwyn': [30066, 30067],
        'argyle': [30229, 30230],
        'lawrence': [30149, 30150],
        'wilson': [30105, 30106],
        'sheridan': [30016, 30017],
        'addison': [30273, 30274],
        'belmont': [30255, 30256],
        'fullerton': [30233, 30234],
        'north/clybourn': [30125, 30126],
        'clark/division': [30121, 30122],
        'chicago': [30279, 30280],
        'grand': [30064, 30065],
        'lake': [30289, 30290],
        'monroe': [30211, 30212],
        'jackson': [30109, 30110],
        'harrison': [30285, 30286],
        'roosevelt': [30269, 30270],
        'cermak-chinatown': [30193, 30194],
        'sox-35th': [30036, 30037],
        '47th': [302387, 30238],
        'garfield': [30223, 30224],
        '63rd': [30177, 30178],
        '69th': [30191, 30192],
        '79th': [30046, 30047],
        '87th': [30276, 30275],
        '95th/dan ryan': [30088, 30089]
}

# brown line stop ids: I DID THESE WRONG; THESE ARE MAP ID
"""
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
"""

# Create your views here.
def index(request):
    # base url: http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx
    # test id: 30126 for N/C
    stop = input("What stop are you wanting data for?\n").lower()
    ns = input("Northbound or southbound? (type 'n' or 's')\n").lower()
    trig = 0
    if ns == "s":
        trig = 1
    key = ""
    desiredStop = red_line_ids.get(stop)[trig]
    print(desiredStop)
    url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={}&stpid={}&outputType=JSON"
    
    response = requests.get(url.format(key, desiredStop)).json()
    print(response)

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