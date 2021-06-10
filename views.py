from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Parkslots, Freeslots, Workers
from datetime import datetime
from django.contrib import messages
import os


# Create your views here.

def index(request):
    return render(request, "Parking/index.html")


def register(request):
    if request.method == "POST":
        available = Freeslots.objects.filter(status = 0).first()
        if(available):
            carid = request.POST['carid']
            phnnum = request.POST['mobile']
            rownum = available.rowval
            colnum = available.colval
            t = datetime.now()
            if(len(carid)>6 and len(carid)<=10 and len(phnnum)):
                if Parkslots.objects.filter(carid=carid).exists():
                    messages.info(request, 'This carid has already booked slot')
                    return render(request, "Parking/register.html")
                else:
                    bookslot = Parkslots(carid=carid, phnnum=phnnum, rownum=rownum, colnum=colnum, status=1, checkin=t)
                    bookslot.save()
                    change = Freeslots.objects.get(rowval=rownum, colval=colnum)
                    change.status = 1
                    change.save()
                    messages.info(request, f'Slot is booked at Block: {rownum} and Slot: {colnum}')
                    return render(request, "Parking/register.html")
            else:
                messages.info(request, 'Enter valid details')
                return render(request, "Parking/register.html")
        else:
            messages.info(request, 'Sorry, no slots available at this time')
            return render(request, "Parking/register.html")
    else:
        return render(request, "Parking/register.html")


def checkslot(request):
    if request.method == "POST": 
        carid = request.POST['carid']
        if(len(carid)>6 and len(carid)<=10):
            if Parkslots.objects.filter(carid=carid).exists():
                slot = Parkslots.objects.get(carid=carid)
                rownum = slot.rownum
                colnum = slot.colnum
                messages.info(request, f"Park at Block: {rownum} and Slot: {colnum}")
                return render(request, "Parking/checkslot.html")
            else:
                messages.info(request, 'You did not book a slot on this carid')
                return render(request, "Parking/checkslot.html")
        else:
            messages.info(request, 'Enter valid details')
            return render(request, "Parking/checkslot.html")
    else:
        return render(request, "Parking/checkslot.html")


def cancelslot(request):
    if request.method == "POST":
        carid = request.POST['carid']
        rownum = request.POST['rownum']
        colnum = request.POST['colnum']
        rowval = rownum
        colval = colnum
        if Parkslots.objects.filter(carid=carid, rownum=rownum, colnum=colnum).exists():
            Freeslots.objects.filter(rowval=rowval, colval=colval).update(status=0)
            slot = Parkslots.objects.filter(carid=carid, rownum=rownum, colnum=colnum).delete()
            messages.info(request, "Your slot has been cancelled!")
            return render(request, "Parking/cancelslot.html")
        else:
            messages.info(request, "This car did not book a slot. Check details you have entered.")
            return render(request, "Parking/cancelslot.html")
    else:
        return render(request, "Parking/cancelslot.html")


def administrator(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if Workers.objects.filter(username=username, password=password).exists():
            return render(request, "Parking/operator.html")
        else:
            messages.info(request, 'Enter valid details')
            return render(request, "Parking/administrator.html")
    else:
        return render(request, "Parking/administrator.html")


def checkout(request):
    if request.method == "POST":
        carid = request.POST['carid']
        rate = request.POST['charge']
        parked = Parkslots.objects.filter(carid=carid).first()
        if parked:
            arrived = str(parked.checkin)
            out = str(datetime.now().time())
            FMT = '%H:%M:%S.%f'
            timediff = datetime.strptime(out, FMT) - datetime.strptime(arrived, FMT)
            minutes = (timediff.total_seconds())/60
            amount = minutes*float(rate)
            messages.info(request, f"We charge Rs. {rate} per minute")
            messages.info(request, "Your vehicle is parked for {:.2f} minutes".format(minutes))
            messages.info(request, "Charge for parking is: {:.2f}".format(amount))
            return render(request, "Parking/paid.html", {
                'carid': carid
            })
        else:
            messages.info(request, 'Enter valid details')
            return render(request, "Parking/checkout.html")
    else:
        return render(request, "Parking/checkout.html")


def blockslots(request):
    if request.method == "POST":
        rowval = request.POST['rownum']
        colval = request.POST['colnum']
        if Freeslots.objects.filter(rowval=rowval).exists():
            for i in range(int(rowval),int(rowval)+1):
                if(len(colval)>0):
                    for j in range(int(colval),int(colval)+1):
                        block = Freeslots.objects.get(rowval=rowval,colval=colval)
                        block.status = 1
                        block.save()
                    messages.info(request, f"Parking at Block: {rowval} and Slot: {colval} is blocked")
                    return render(request, "Parking/blockslots.html")
                else:
                    for colval in range(1,101):
                        Freeslots.objects.filter(rowval=rowval,colval=colval).update(status=1)
                        messages.info(request, f"Parking at Block: {rowval} is blocked")
                        return render(request, "Parking/blockslots.html")
        else:
            messages.info(request, "Enter valid details")
            return render(request, "Parking/blockslots.html")
    else:
        return render(request, "Parking/blockslots.html")


def newslots(request):
    if request.method == "POST":
        rownum = request.POST['rownum']
        colnum = request.POST['colnum']
        for rowval in range(1,int(rownum)+1):
            for colval in range(int(colnum),int(colnum)+1):
                slotpresent = Freeslots.objects.filter(rowval=rowval, colval=colval)
                if slotpresent:
                    if Parkslots.objects.filter(rownum=rowval, colnum=colval).exists():
                        continue
                    else:
                        Freeslots.objects.filter(rowval=rowval, colval=colval).update(status=0)
                else:
                    slot = Freeslots(rowval=rowval, colval=colval, status=0)
        messages.info(request, 'Slots are created')
        return render(request, "Parking/newslots.html")
    else:
        return render(request, "Parking/newslots.html")


def operator(request):
    return render(request, "Parking/operator.html")


def paid(request, carid):
    if request.method == "GET":
        slot = Parkslots.objects.get(carid=carid)
        rowval=slot.rownum
        colval=slot.colnum
        empty = Freeslots.objects.get(rowval=rowval, colval=colval)
        empty.status = 0
        empty.save()
        slot.delete()
        return render(request, "Parking/operator.html")
    else:
        return render(request, "Parking/paid.html", {
            'carid': carid
        })
