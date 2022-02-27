from django.shortcuts import render
# this isn't working. Need to investigate why
#import keyHold
import requests
from .models import Stops
from .forms import StopForm

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

brn_line_ids = {
        'kimball': [30249, 30250],
        'kedzie': [30225, 30226],
        'francisco': [30167, 30168],
        'rockwell': [30195, 30196],
        'western': [30283, 30284],
        'damen': [30018, 30019],
        'montrose': [30287, 30288],
        'irving park': [30281, 30282],
        'addison': [30277, 30278],
        'paulina': [30253, 30254],
        'southport': [30070, 30071],
        'belmont': [30257, 30258],
        'wellington': [30231, 30232],
        'diversey': [30103, 30104],
        'fullerton': [30235, 30236],
        'armitage': [30127, 20128],
        'sedgwick': [30155, 30156],
        'chicago': [30137, 30138],
        'merchandise mart': [30090, 30091],
        'clark/lake': [40380, 'S'],
        'state/lake': [30051, 'S'],
        'randolph/wabash': [0, 'S'],
        'madison/wabash': [0, 'S'],
        'adams/wabash': [30131, 'S'],
        'harold washington library': [30165, 'S'],
        'lasalle/van buren': [30030, 'S'],
        'quincy': [30008, 'S'],
        'washington/wabash': [30383, 'S'],
        'washington/wells': [30142, 'S']
}


# Create your views here.
def index(request):
    # base url: http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx
    # test id: 30126 for N/C
    
    # KEY FOR API
    key = ""

    # database query to get all user stops
    stops = Stops.objects.all()

    # list to store response dictionaries
    stopList = []
    
    # logic to store user inputs from form in database
    url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={}&stpid={}&outputType=JSON"

    if request.method == "POST":
        print(request.POST)
        form = StopForm(request.POST)
        form.save()

    form = StopForm()

    # for each stop obj in stops database
    for stop in stops:
        #print("Stop: " + stop.stop)
        desiredStop = red_line_ids.get(stop.stop)[0]    

        response = requests.get(url.format(key, desiredStop)).json()


        # might need to generate dictionaries in a loop or store them in a list
        # more than one dictionary per response
        ## ctatt is the exterior
        
        # our base returned arrival time
        base = response['ctatt']['eta'][0]['arrT']

        estArrivalFormatted = base

        # de-formatting from miliary time
        firstTwo = estArrivalFormatted[11:13]
        if int(firstTwo) > 12:
            hrNum = int(firstTwo) - 12
            estArrivalFormatted = str(hrNum) + estArrivalFormatted[13:] + " PM"
        else:
            estArrivalFormatted = estArrivalFormatted[11:] + " AM"

        # request time formatting
        requestTime = response['ctatt']['tmst'][14:16]
        arrivalMin = base[14:16]
        
        # minutes to arrival calculation
        arrival = int(arrivalMin) - int(requestTime)

        # here's the fix for when the hour changes between request and arrival time
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

        stopList.append(stop_data)

    print(stopList)

    # passing info to template
    context = {'stopList' : stopList, 'form': form}

    return render(request, 'djangocta/djangocta.html', context)