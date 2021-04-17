from django.shortcuts import render
from MainApp.models import *
from AuthenticationAndVerification.models import *
from datetime import datetime as dt
# Create your views here.
#for dashboard sid send karna he
#for feed page sid nhi bhejna he


def active_post(sid):
        if sid:
                pm = PostModel.objects.filter(status="active", sender_id=sid)
        else:
                pm = PostModel.objects.filter(status="active")
        posts_active = {}

        for post in pm:
                post1 = {}
                post1["id"] = post.id
                k = FoodDonorModel.objects.filter(id=post.sender_id).first()
                post1["sender"] = k.name
                post1["type"] = k.donor_type
                post1["sender_city"] = k.address.city
                post1["sender_landmark"] = k.address.landmark
                post1["content"] = post.content
                post1["packaging"] = post.packaging
                post1["dead_time"] = post.dead_time
                post1["location_url"] = post.location_url
                post1["approx_weight"] = post.food_model.approx_weight
                post1["num_people"] = post.food_model.num_people
                post1["status"] = "active"
                posts_active[post.id] = post1
        return posts_active

def active_request(ngousername):
        if ngousername:
                rs=RequestLocation.objects.filter(ngo_username=ngousername)
        else:
                rs=RequestLocation.objects.all()
        active_requests={}
        for request in rs:
                if request.expiration_date <= dt.now():
                        req={}
                        req["city"]=request.city
                        req["content"]=request.content
                        req["area"]=request.area
                        req["contact"]=request.contact
                        req["num_people"]=request.num_people
                        req["posted_by"]=request.posted_by
                        req["expiration_date"]=request.expiration_date
                        req["location_url"]=request.location_url
                        active_requests[request.id]=req
        return active_requests
#for dashboard 
def archive_request(ngousername):
        if ngousername:
                rs=RequestLocation.objects.filter(ngo_username=ngousername)
        else:
                rs=RequestLocation.objects.all()
        active_requests={}
        for request in rs:
                if request.expiration_date > dt.now():
                        req={}
                        req["city"]=request.city
                        req["content"]=request.content
                        req["area"]=request.area
                        req["contact"]=request.contact
                        req["num_people"]=request.num_people
                        req["posted_by"]=request.posted_by
                        req["expiration_date"]=request.expiration_date
                        req["location_url"]=request.location_url
                        active_requests[request.id]=req
        return active_requests
#for dashboard        
def archive_post(ngoid):
        if ngoid:
                pm=PostModel.objects.filter(status="succesfull",sender_id=ngoid)
        else:
                pm=PostModel.objects.filter(status="succesfull")
        if pm:
                posts_active={}
                for post in pm:
                        post1={}
                        post1["id"]=post.id
                        k=FoodDonorModel.objects.filter(sender_id=post.sender_id).first()
                        post1["sender"]=k.name
                        post1["type"]=k.donor_type
                        post1["sender_city"]=k.address.city
                        post1["sender_landmark"]=k.address.landmark
                        post1["content"]=post.content
                        post1["packaging"]=post.packaging
                        post1["dead_time"]=post.dead_time
                        post1["location_url"]=post.location_url
                        post1["approx_weight"]=post.food_model.approx_weight
                        post1["num_people"]=post.food_model.num_people
                        post1["status"]="succesfull"
                        post1["pick_up_time"]=post.pick_up_time
                        post1["reciver"]=post.receiver
                        post1["destination"]=post.destination
                        posts_active[post.id]=post1
                return posts_active
        else:
                return None


def index(request):
        context = {}
        return render(request, 'index.html', context)

def feed(request):
        context = {}
        if "logged_in" in request.session:
                context["logged_in"] = True
                if "ngo" in  request.session:
                        context["dashboard_url"] = "ngo_dashboard"
                elif "donor" in  request.session:
                        context["dashboard_url"] = "donor_dashboard"
                else:
                        context["dashboard_url"] = "volunteer_dashboard"
        else:
                pass
        return render(request, 'MainApp/feed.html', context)

def ngo_dashboard(request):
        context = {}
        if "logged_in" in request.session:
                if "ngo" in  request.session:
                        context["logged_in"] = True
                        ngo=NGOModel.objects.filter(id=request.session["ngo"]).first()
                        if ngo:
                                if ngo.verified:
                                        context["email"]=True
                                if ngo.address:
                                        context["completed"]=True
                                if request.method=="GET":
                                        if "ajax" in request.GET:
                                                if "profile" in request.GET:
                                                        try:
                                                                city=request.GET["city"]
                                                                state=request.GET["state"]
                                                                district=request.GET["district"]
                                                                pincode=reqest.GET["pincode"]
                                                                landmark=request.GET["landmark"]
                                                                houseno=request.GET["houseno"]
                                                                area=request.GET["area"]
                                                                street=request.GET["street"]
                                                        address=AddressModel.objects.create(city=city,
                                                        state=state,district=district,
                                                        pincode=pincode,landmark=landmark,
                                                        house_no=houseno,area=area,street=street).save()
                                                        ngo.address=address
                                                        ngo.save()
                                                elif "request" in request.GET:
                                                        city=request.GET["city"]
                                                        content=request.GET["content"]
                                                        area=request.GET["area"]
                                                        num_people=request.GET["num_people"]
                                                        expiration_date=request.GET["expiration_date"]
                                                        location_url=request.GET["location_url"]
                                                        try:
                                                                contact=request.GET["contact"]
                                                        except:
                                                                contact=ngo.email
                                                        rl=RequestLocation.objects.create(city=city,
                                                        content=content,area=area,
                                                        num_people=num_people,expiration_date=expiration_date,
                                                        location_url=location_url,ngo_username=ngo.admin_name,contact=contact)
                                                        rl.save()
                                                        return

                                                        
                                        return render(request, 'MainApp/ngo_dashboard.html', context)
                                elif request.method=="POST":
                                        city=request.POST["city"]
                                        state=request.POST["state"]
                                        district=request.POST["district"]
                                        pincode=reqest.POST["pincode"]
                                        landmark=request.POST["landmark"]
                                        houseno=request.POST["houseno"]
                                        area=request.POST["area"]
                                        street=request.POST["street"]
                                        address=AddressModel.objects.create(city=city,
                                                        state=state,district=district,
                                                        pincode=pincode,landmark=landmark,
                                                        house_no=houseno,area=area,street=street).save()
                                                        ngo.address=address
                                                        ngo.location_url=request.POST["locationurl"]
                                                        ngo.save()
                                        return
                                else:
                                        #error return
                                        pass 

                        else:
                                #redirect to login and flush session
                                pass
                else:
                        #errorpage
                        pass
        else:
                #redirect to login
                pass

        return render(request, 'MainApp/ngo_dashboard.html', context)

def donor_dashboard(request):
        context = {}
        if "logged_in" in request.session:
                if "donor" in  request.session:
                        context["logged_in"] = True
                        fd=FoodDonorModel.objects.filter(id=request.session["donor"]).first()
                        if fd:
                                if fd.verified:
                                        context["email"]=True
                                if fd.address:
                                        context["completed"]=True
                                if request.method=="GET":
                                        if "ajax" in request.GET:
                                                if "post" in request.GET:
                                                        sender_id=request.session["id"]
                                                        content=request.GET["content"]
                                                        packaging=request.GET["packaging"]
                                                        dead_time=request.GET["deadtime"]
                                                        approx_weight=request.GET["approx_weight"]
                                                        num_people=request.GET["numpeople"]
                                                        location_url=fd.location_url
                                                        destination=request.GET["destination"]
                                                        fm=FoodModel.objects.create(approx_weight=approx_weight,
                                                        num_people=num_people).save()
                                                        pm=PostModel.objects.create(sender_id=sender_id,
                                                        content=content,packaging=packaging,
                                                        dead_time=dead_time,food_model=fm,location_url=location_url)
                                                        pm.save()     
                                        else:
                                                return render(request, 'MainApp/donor_dashboard.html', context)
                                elif request.method=="POST":
                                        city=request.POST["city"]
                                        state=request.POST["state"]
                                        district=request.POST["district"]
                                        pincode=reqest.POST["pincode"]
                                        landmark=request.POST["landmark"]
                                        houseno=request.POST["houseno"]
                                        area=request.POST["area"]
                                        street=request.POST["street"]
                                        address=AddressModel.objects.create(city=city,
                                                        state=state,district=district,
                                                        pincode=pincode,landmark=landmark,
                                                        house_no=houseno,area=area,street=street).save()
                                                        fd.address=address
                                                        fd.location_url=request.POST["locationurl"]
                                                        fd.save()
                                else:
                                        #return invalid request error
                                        pass

        else:
                pass
        return render(request, 'MainApp/donor_dashboard.html', context)

def volunteer_dashboard(request):
        context = {}
        if "logged_in" in request.session:
                if "volunteer" in request.session:
                        context["logged_in"] = True
                        vt=VolunteerModel.objects.filter(id=request.session['volunteer']).first()
                        if vt:
                                if vt.verified:
                                        context["email"]=True
                                if vt.address:
                                        context["completed"]=True
                                if request.method=="GET":
                                        if "ajax" in request.GET:
                                                pass
                                        else:
                                                return render(request, 'MainApp/donor_dashboard.html', context)
                                elif request.method=="POST":
                                        city=request.POST["city"]
                                        state=request.POST["state"]
                                        district=request.POST["district"]
                                        pincode=reqest.POST["pincode"]
                                        landmark=request.POST["landmark"]
                                        houseno=request.POST["houseno"]
                                        area=request.POST["area"]
                                        street=request.POST["street"]
                                        address=AddressModel.objects.create(city=city,
                                                        state=state,district=district,
                                                        pincode=pincode,landmark=landmark,
                                                        house_no=houseno,area=area,street=street).save()
                                                        vt.address=address
                                                        #fd.location_url=request.POST["locationurl"]
                                                        vt.save()
                                else:
                                        #return invalid request error
                                        pass
        else:
                pass
        return render(request, 'MainApp/volunteer_dashboard.html', context)










