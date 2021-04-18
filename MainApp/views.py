from django.shortcuts import render
from MainApp.models import *
from AuthenticationAndVerification.models import *
from datetime import datetime as dt
from django.http import JsonResponse
# Create your views here.
#for dashboard sid send karna he
#for feed page sid nhi bhejna he
def active_post(sid):
        if sid:
                pm=PostModel.objects.filter(status="Active",sender_id=sid)
        else:
                pm=PostModel.objects.filter(status="Active")
        posts_active={}
        for post in pm:
                post1={}
                post1["id"]=post.id
                k=FoodDonorModel.objects.filter(id=post.sender_id).first()
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
                post1["status"]="active"
                posts_active[post.id]=post1
        return posts_active

def active_request(ngousername):
        if ngousername:
                rs=RequestLocation.objects.filter(ngo_username=ngousername)
        else:
                rs=RequestLocation.objects.all()
        active_requests={}
        for request in rs:
                #if request.expiration_date <= dt.now():
                if True:
                        req={}
                        ngo = NGOModel.objects.filter(id=request.ngo_id).first()
                        req["sender"] = ngo.name
                        req["address"]=request.address
                        req["content"]=request.content
                        req["contact"]=request.contact
                        req["num_people"]=request.num_people
                        req["posted_by"]=request.ngo_username
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
                #if request.expiration_date > dt.now():
                if True:
                        req={}
                        ngo = NGOModel.objects.filter(id=request.ngo_id).first()
                        print(ngo.name)
                        req["sender"] = ngo.name
                        req["address"]=request.address
                        req["content"]=request.content
                        req["contact"]=request.contact
                        req["num_people"]=request.num_people
                        req["posted_by"]=request.ngo_username
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
                        post1["status"]="successfull"
                        post1["pick_up_time"]=post.pick_up_time
                        post1["receiver"]=post.receiver
                        post1["destination"]=post.destination
                        posts_active[post.id]=post1
                return posts_active
        else:
                return None

def active_volunteer(ngoid):
        active_volunteer={}
        vt=VolunteerModel.objects.filter(NGO_model__id=ngoid)
        if vt:
                for volunteer in vt:
                        volunteers={}
                        volunteers["name"]=vt.full_name
                        volunteers["email"]=vt.email
                        if vt.verified:
                                volunteer["verified"]="verified"
                        else:
                                volunteer["verified"]="unverified"
                        active_volunteer[vt.id]=volunteers
        return active_volunteer
def past_work_by_ngo(ngoid):
        pass 

def post_view(request, id):
        context = {}
        if "logged_in" in request.session:
                context["logged_in"] = True
                if "volunteer" in request.session:
                        context["volunteer"]=True
                        pm=PostModel.objects.filter(id=id).first()
                        context["pm"]=pm
                        context["active_requests"]=active_request(ngousername=None)
                        if request.method=="GET":
                                return render(request,"MainApp/post.html",context)
                        elif request.method=="POST":
                                pass              


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
                if request.method=="GET":
                        data = {}
                        if "ajax" in request.GET:
                                if "activepost" in request.GET:
                                        data["active_posts"]=active_post(sid=None)
                                        print(data)
                                        return JsonResponse(data)
                                elif "archivepost" in request.GET:
                                        data["archive_posts"]=archive_post(ngoid=None)
                                        return JsonResponse(data)
                                elif "activerequest" in request.GET:       
                                        data["active_requests"]=active_request(ngousername=None)
                                        return JsonResponse(data)
                                elif "archiverequest" in request.GET:
                                        data["archive_requests"]=archive_request(ngousername=None)
                                        return JsonResponse(data)
                                else:
                                        data["error"]
                                        return JsonResponse(data)
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
                                                data={}
                                                if "profile" in request.GET:
                                                        try:
                                                                city=request.GET["city"]
                                                                state=request.GET["state"]
                                                                district=request.GET["district"]
                                                                pincode=request.GET["pincode"]
                                                                landmark=request.GET["landmark"]
                                                                houseno=request.GET["houseno"]
                                                                area=request.GET["area"]
                                                                street=request.GET["street"]
                                                        except():
                                                                pass
                                                        address = AddressModel.objects.create(city=city,
                                                                state=state,district=district,
                                                                pincode=pincode,landmark=landmark,
                                                                house_no=houseno,area=area,street=street)
                                                        address.save()
                                                        ngo.address=address
                                                        ngo.save()

                                                elif "requestfood" in request.GET:
                                                        content=request.GET["content"]
                                                        address=request.GET["address"]
                                                        num_people=request.GET["num_people"]
                                                        expiration_date=request.GET["expiration_date"]
                                                        location_url=request.GET["location_url"]
                                                        try:
                                                                contact=request.GET["contact"]
                                                        except:
                                                                contact=ngo.email
                                                        rl=RequestLocation.objects.create(address=address,
                                                        content=content,
                                                        num_people=num_people,expiration_date=expiration_date,
                                                        location_url=location_url,ngo_username=ngo.admin_name,ngo_id=ngo.id,contact=contact)
                                                        rl.save()
                                                        data["saved"]=True
                                                        return JsonResponse(data)
                                                elif "volunteer" in request.GET:
                                                        data["volunteers"]=active_volunteer(ngo.id)
                                                        return JsonResponse(data)
                                                

                                                        
                                        return render(request, 'MainApp/ngo_dashboard.html', context)
                                elif request.method=="POST":
                                        state=request.POST["state"]
                                        district=request.POST["district"]
                                        pincode=request.POST["pincode"]
                                        landmark=request.POST["landmark"]
                                        houseno=request.POST["houseno"]
                                        area=request.POST["area"]
                                        street=request.POST["street"]
                                        address=AddressModel.objects.create(
                                                state=state,city=district,
                                                pincode=pincode,landmark=landmark,
                                                house_no=houseno,area=area,street=street)
                                        address.save()
                                        ngo.address=address
                                        ngo.location_url=request.POST["locationurl"]
                                        ngo.save()
                                        context["email"] = True
                                        context["completed"] = True
                                        return render(request, 'MainApp/ngo_dashboard.html', context)
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
                                                data={}
                                                if "requestpost" in request.GET:
                                                        sender_id=request.session["donor"]
                                                        content=request.GET["content"]
                                                        packaging=request.GET["packaging"]
                                                        if packaging == "true":
                                                                packaging = True
                                                        else:
                                                                packaging = False
                                                        dead_time=request.GET["deadtime"]
                                                        approx_weight=request.GET["approx_weight"]
                                                        num_people=request.GET["numpeople"]
                                                        location_url=fd.location_url
                                                        #destination=request.GET["destination"]
                                                        fm=FoodModel.objects.create(approx_weight=approx_weight,
                                                        num_people=num_people)
                                                        fm.save()
                                                        pm=PostModel.objects.create(sender_id=sender_id,
                                                        content=content,packaging=packaging,
                                                        dead_time=dead_time,food_model=fm,location_url=location_url)
                                                        pm.save()
                                                        data["saved"]=True
                                                        return JsonResponse(data)     
                                        else:
                                                return render(request, 'MainApp/donor_dashboard.html', context)
                                elif request.method=="POST":
                                        state=request.POST["state"]
                                        district=request.POST["district"]
                                        pincode=request.POST["pincode"]
                                        landmark=request.POST["landmark"]
                                        houseno=request.POST["houseno"]
                                        area=request.POST["area"]
                                        street=request.POST["street"]
                                        address=AddressModel.objects.create(city=district,
                                                state=state,
                                                pincode=pincode,landmark=landmark,
                                                house_no=houseno,area=area,street=street)
                                        address.save()
                                        fd.address=address
                                        fd.location_url=request.POST["locationurl"]
                                        fd.save()
                                        context["email"] = True
                                        context["completed"] = True
                                        return render(request, 'MainApp/donor_dashboard.html', context)
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
                                        state=request.POST["state"]
                                        district=request.POST["district"]
                                        pincode=request.POST["pincode"]
                                        landmark=request.POST["landmark"]
                                        houseno=request.POST["houseno"]
                                        area=request.POST["area"]
                                        street=request.POST["street"]
                                        address=AddressModel.objects.create(city=district,
                                                state=state,district=district,
                                                pincode=pincode,landmark=landmark,
                                                house_no=houseno,area=area,street=street)
                                        address.save()
                                        vt.address = address
                                        #fd.location_url=request.POST["locationurl"]
                                        vt.save()
                                        context["email"] = True
                                        context["completed"] = True
                                        return render(request, 'MainApp/volunteer_dashboard.html', context)
                                else:
                                        #return invalid request error
                                        pass
        else:
                pass
        return render(request, 'MainApp/volunteer_dashboard.html', context)




