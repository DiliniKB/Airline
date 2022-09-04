from audioop import reverse
# from http.client import HTTPResponseRedirect
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render

from flights.models import Flight, Passenger

# Create your views here.
def index(request):
    return render(request, 'flights/index.html', {
        "flights": Flight.objects.all(),
    })

#get is used when it is exactly one result
#pk is for primary key
def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    passengers = flight.passenger.all()
    return render(request, 'flights/flight.html', {
        "flight": flight,
        "passengers": passengers,
        "non_passengers": Passenger.objects.exclude(flights=flight_id).all()
    })

def book(request, flight_id):
    if request.method == 'POST':
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk = (int(request.POST["passenger"])))
        passenger.flights.add(flight)

        # comma after the args is compulsory
        return HttpResponseRedirect(reverse("flight", args=(flight_id,)))

    flight = Flight.objects.get(id=flight_id)
