import base64
from datetime import datetime as dt
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from .models import AddressModel, NGOModel, VolunteerModel, FoodDonorModel

# support functions
def generate_username(name):
    new = '_'.join(name.split(' ')).lower()
    now = dt.now()
    new += now.strftime("%m%d%H") 
    return new


def send_the_mail(request, u, user_type ,template_path, subject):
    current_site = get_current_site(request)
    email_subject = subject
    t = Token()
    msg_plain = ""
    html_message = render_to_string(template_path, {
        'user': u,
        'domain': current_site.domain,
        'uname': urlsafe_base64_encode(force_bytes(u.username)),
        'token': t.create_token(),
        'user_type': user_type
    })
    to_email = u.email
    send_mail(email_subject, msg_plain, 'mohit.djmail@gmail.com', [to_email], html_message=html_message)


class Token:
    def create_token(self):
        time_stamp_bytes = str(dt.now().strftime(
            "%d %H:%M:%S")).encode('ascii')
        base64_ts_bytes = base64.b64encode(time_stamp_bytes)
        base64_time_stamp = base64_ts_bytes.decode('ascii')

        token = base64_time_stamp
        return token

    def check_validity(self, token, time):
        tk1 = token
        tk2 = self.create_token()

        dt_obj_ts1 = dt.strptime(base64.b64decode(
            tk1).decode('ascii'), "%d %H:%M:%S")
        dt_obj_ts2 = dt.strptime(base64.b64decode(
            tk2).decode('ascii'), "%d %H:%M:%S")

        time_delta = dt_obj_ts2 - dt_obj_ts1
        minutes = float(format(time_delta.total_seconds() / 60, '.3f'))

        if minutes < time:
            return True
        else:
            return False


# Create your views here.
def ngo_login(request):
    context={}
    data={}
    if request.method=="GET":
        if "ajax" in request.GET:
            if "email_password_reset" in request.GET:
                email = request.GET["email_password_reset"]
                n=NGOModel.objects.filter(email=email).first()
                if n:
                    send_the_mail(request, n, "NGO","AuthenticationAndVerification/email_related_templates/reset_password_email.html", "Password reset")
                    data["matched"]=True
                else:
                    data["mismatch"]=False
            return JsonResponse(data)
        return render(request,"AuthenticationAndVerification/ngo_login.html",context)
    elif request.method=="POST":
        username = request.POST["email_or_uname"]
        ngo = NGOModel.objects.filter(username=username).first()
        if not ngo:
            ngo = NGOModel.objects.filter(email=username).first()
        if ngo:
            password=request.POST["password"]
            if ngo.password==password:
                request.session["logged_in"] = True
                request.session["ngo"] = ngo.id
                return redirect("ngo_dashboard")
            else:
                context["mismatch"]=True
        else:
            context["mismatch"]=True
        return render(request,"AuthenticationAndVerification/ngo_login.html",context)
    else:
        return render(request,"Z_error_templets/error_404.html")



def donor_login(request):
    context={}
    if request.method=="GET":
        if "ajax" in request.GET:
            data = {}
            if "email_password_reset" in request.GET:
                email = request.GET["email_password_reset"]
                f=FoodDonorModel.objects.filter(email=email).first()
                if f:
                    send_the_mail(request, f,"food_donor","AuthenticationAndVerification/email_related_templates/reset_password_email.html", "Password reset")
                    data["matched"]=True
                else:
                    data["mismatch"]=False
            return JsonResponse(data)

        return render(request,"AuthenticationAndVerification/donor_login.html",context)
    elif request.method=="POST":
        username = request.POST["email_or_uname"]
        fooddonor=FoodDonorModel.objects.filter(username=username).first()
        if not fooddonor:
            fooddonor = FoodDonorModel.objects.filter(email=username).first()
        if fooddonor:
            password=request.POST["password"]
            if fooddonor.password==password:
                request.session["logged_in"] = True
                request.session["donor"] = fooddonor.id
                return redirect("donor_dashboard")
            else:
                context["mismatch"]=True
        else:
            context["mismatch"]=True
        return render(request,"AuthenticationAndVerification/donor_login.html",context)
    else:
        return render(request,"Z_error_templets/error_404.html")


def volunteer_login(request):
    context={}
    if request.method=="GET":
        if "ajax" in request.GET:
            if "email_password_reset" in request.GET:
                data = {}
                email = request.GET["email_password_reset"]
                v=VolunteerModel.objects.filter(email=email).first()
                if v:
                    send_the_mail(request, v, "volunteer","AuthenticationAndVerification/email_related_templates/reset_password_email.html", "Password reset")
                    data["matched"]=True
                else:
                    data["mismatch"]=False
            return JsonResponse(data)
        return render(request,"AuthenticationAndVerification/volunteer_login.html",context)
    elif request.method=="POST":
        username = request.POST["email_or_uname"]
        volunteer = VolunteerModel.objects.filter(username=username).first()
        if not volunteer:
            volunteer = VolunteerModel.objects.filter(email=username).first()

        if volunteer:
            password=request.POST["password"]
            if volunteer.password==password:
                request.session["logged_in"] = True
                request.session["volunteer"] = volunteer.id
                return redirect("volunteer_dashboard")
            else:
                context["mismatch"]=True
        else:
            context["mismatch"]=True
        return render(request,"AuthenticationAndVerification/volunteer_login.html",context)
    else:
        return render(request,"Z_error_templets/error_404.html")


def ngo_register(request):
    if request.method=="GET":
        if "ajax" in request.GET:
            data={}
            if "email" in request.GET:
                email = request.GET["email"]
                v=NGOModel.objects.filter(email=email).first()
                if v:
                    data["match"]=True
                else:
                    data["match"]=False
            elif "contact_number" in request.GET:
                contact_number = request.POST["contact_number"]
                v=NGOModel.objects.filter(contact_number=contact_number).first()
                if v:
                    data["match"]=True
                else:
                    data["match"]=False
            else:
                data["invalid"]=True
            return JsonResponse(data)
        return render(request,"AuthenticationAndVerification/ngo_register.html")
    elif request.method=="POST":
        name=request.POST["name"]
        admin_name = request.POST["head_name"]
        contact_number = request.POST["contactNo"]
        email =request.POST["email"]
        password = request.POST["password"]
        ngo_type = request.POST["ngo_type"]
        username = generate_username(name)
        ngo = NGOModel.objects.create(
            name=name,
            username=username,
            admin_name=admin_name,
            contact_number=contact_number,
            email=email,
            password=password,
            ngo_type=ngo_type)
        ngo.save()
        request.session["logged_in"] = True
        request.session["ngo"] = ngo.id
        return redirect("ngo_dashboard")
    else:
        return render(request,"Z_error_templets/error_404.html")



def donor_register(request):
    if request.method=="GET":
        if "ajax" in request.GET:
            data={}
            if "email" in request.GET:
                email = request.GET["email"]
                v=FoodDonorModel.objects.filter(email=email).first()
                if v:
                    data["match"]=True
                else:
                    data["match"]=False
            elif "contact_number" in request.GET:
                contact_number = request.GET["contact_number"]
                v=FoodDonorModel.objects.filter(contact_number=contact_number).first()
                if v:
                    data["match"]=True
                else:
                    data["match"]=False
            else:
                data["invalid"]=True
            return JsonResponse(data)
        return render(request,"AuthenticationAndVerification/donor_register.html")
    elif request.method=="POST":
        name=request.POST["name"]
        donor_type =request.POST["donor_type"]
        contact_number = request.POST["contactNo"]
        email =request.POST["email"]
        password = request.POST["password"]
        username = generate_username(name)
        fooddonor = FoodDonorModel.objects.create(
            name=name,
            username=username,
            donor_type=donor_type,
            contact_number=contact_number,
            email=email,
            password=password)
        fooddonor.save()
        request.session["logged_in"] = True
        request.session["donor"] = fooddonor.id
        return redirect("donor_dashboard")
    else:
        return render(request,"Z_error_templets/error_404.html")


def volunteer_register(request):
    if request.method=="GET":
        if "ajax" in request.GET:
            data={}
            if "email" in request.GET:
                email = request.GET["email"]
                v=VolunteerModel.objects.filter(email=email).first()
                if v:
                    data["match"]=True
                else:
                    data["match"]=False
            elif "contact_number" in request.GET:
                contact_number = request.GET["contact_number"] 
                v=VolunteerModel.objects.filter(contact_number=contact_number).first()
                if v:
                    data["match"]=True
                else:
                    data["match"]=False
            else:
                data["invalid"]=True
            return JsonResponse(data)
        return render(request,"AuthenticationAndVerification/volunteer_register.html")
    elif request.method=="POST":
        full_name=request.POST["firstName"] +" "+ request.POST["lastName"]
        contact_number = request.POST["contactNo"]
        email =request.POST["email"]
        password = request.POST["password"]
        username = generate_username(full_name)
        volunteer=VolunteerModel.objects.create(
            full_name=full_name, 
            contact_number=contact_number,
            username=username,
            email=email,
            password=password,)
        volunteer.save()
        request.session["logged_in"] = True
        request.session["volunteer"] = volunteer.id
        return redirect("volunteer_dashboard")
    else:
        return render(request,"Z_error_templets/error_404.html")


def delete_session(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect('/')


def activate_email(request, uname_b64, user_type, token):
    context = {}
    try:
        uname = urlsafe_base64_decode(uname_b64).decode()
        user = None
        if user_type == "NGO":
            user = NGOModel.objects.get(username=uname)
            d_board = "ngo_dashboard"
        elif user_type == "Volunteer":
            user = VolunteerModel.objects.get(username=uname)
            d_board = "volunteer_dashboard"
        elif user_type == "food_donor":
            user = FoodDonorModel.objects.get(username=uname)
            d_board = "donor_dashboard"
    except():
        user = None
    t = Token()
    if user is None:
        context["msg"] = "invalid activation link"
    elif t.check_validity(token, 40) is False:
        context["msg"] = "this activation link has been disposed"
    else:
        user.verified = True
        user.save()
        context['verified'] = True
        return redirect(d_board)
    return render(request, 'AuthenticationAndVerification/activate.html', context)


def reset_password(request, uname_b64, user_type, token):
    context = {}
    if request.method == "POST":
        uname = urlsafe_base64_decode(uname_b64).decode()
        user = None
        if user_type == "NGO":
            user = NGOModel.objects.get(username=uname)
        elif user_type == "Volunteer":
            user = VolunteerModel.objects.get(username=uname)
        elif user_type == "food_donor":
            user = FoodDonorModel.objects.get(username=uname)

        password = request.POST['password']
        user.password = password
        user.save()
        context['verified'] = True
        context["updated"] = True
        return render(request, 'AuthenticationAndVerification/reset_password.html', context)
    else:
        try:
            uname = urlsafe_base64_decode(uname_b64).decode()
            user = None
            if user_type == "NGO":
                user = NGOModel.objects.get(username=uname)
            elif user_type == "Volunteer":
                user = VolunteerModel.objects.get(username=uname)
            elif user_type == "food_donor":
                user = FoodDonorModel.objects.get(username=uname)
        except():
            user = None

        t = Token()
        if user is None:
            context["msg"] = "invalid password reset link"
        elif t.check_validity(token, 40) is False:
            context["msg"] = "this password reset has been disposed"
        else:
            context['uname'] = uname_b64
            context['token'] = token
            context['verified'] = True
            return render(request, 'AuthenticationAndVerification/reset_repassword.html', context)

    return render(request, 'AuthenticationAndVerification/reset_password.html', context)

def ajax_verify_email(request):
    if "ngo" in request.session:
        id_ = request.session["ngo"]
        ngo = NGOModel.objects.filter(id=id_).first()
        send_the_mail(request, ngo, "NGO", "AuthenticationAndVerification/email_related_templates/activate_email.html", "Account Activation")
        data = {}
        data["mail_sent"] = True
        return JsonResponse(data)

    elif "donor" in  request.session:
        id_ = request.session["donor"]
        donor = FoodDonorModel.objects.filter(id=id_).first()
        send_the_mail(request, donor, "food_donor","AuthenticationAndVerification/email_related_templates/activate_email.html", "Account Activation")
        data = {}
        data["mail_sent"] = True
        return JsonResponse(data)

    else:
        id_ = request.session["volunteer"]
        volunteer = VolunteerModel.objects.filter(id=id_).first()
        send_the_mail(request, volunteer, "volunteer","AuthenticationAndVerification/email_related_templates/activate_email.html", "Account Activation")
        data = {}
        data["mail_sent"] = True
        return JsonResponse(data)

