
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponseRedirectBase
from projects.models import *
from projects.forms import BrochureForm, EnquiryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import pandas, re, json, requests as req
from datetime import date, timedelta, datetime
from django.db import models
from django.db.models import Count
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key[
    "api-key"
] = "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"



def notify(n_, m_, e_, msg_):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )
    subject = "New Lead from Website"
    sender = {"name": "NotifyBOT", "email": "vaqasam@gmail.com"}
    html_content = f"<html><body><h1>{n_}</h1><h3>{m_}</h3><h3>{e_}</h3><h3>{msg_}</h3></body></html>"
    to = [
        {"email": e, "name": "n_"}
        for e in NotifyEmails.objects.all().values_list("email", flat=True)
    ]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, html_content=html_content, sender=sender, subject=subject
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


# Create your views here.
@login_required()
def mark_called(request, index):

    lead = Lead.objects.get(id=index)
    lead.called = True
    lead.save()

    return HttpResponse(f"{lead.name} : {lead.mobile} is marked Called")


@login_required()
def sendwa(request, index):

    lead = Lead.objects.get(id=index)

    server = BaseInfo.objects.first().test_server

    url = f"http://{server}/send_msg"
    myobj = {"mobile": lead.mobile}

    x = req.post(url, json=myobj)

    return HttpResponse(x.text)


# Get Leads csv
@login_required()
def lipa(request):

    res = ""
    # fetch lead and create call log
    leads = Lead.objects.all()
    for l in leads:
        # filter bad leads
        l_filter = [i for i in l.leadstage_set.all() if ("BAD" in i.stage.stage)]
        b_filter = [i for i in l.leadstage_set.all() if ("Booked" in i.stage.stage)]

        if len(l_filter) + len(b_filter) == 0:
            res += f"{l.name},{l.mobile}<br>"

        # fix the , in name shit
        l.name = l.name.replace(",", " ")
        # l.mobile = l.mobile.replace("+910","+91")
        l.save()

    return HttpResponse(res)

# Create your views here.
@login_required()
def call_redirect(request, num):

    # fetch lead and create call log
    lead = Lead.objects.get(mobile=num)
    CallLog(lead=lead, agent=request.user).save()

    HttpResponseRedirectBase.allowed_schemes += ["tel"]

    return HttpResponseRedirect(f"tel:{num}")


@login_required()
def loadcsv(request):
    f = FileUpload.objects.last()
    data = pandas.read_csv(f.file.path, sep="\t")
    data.date = pandas.to_datetime(data.date)
    for _, row in data.iterrows():
        try:
            n_ = row["number"]
            if not pandas.isna(n_):
                n_ = re.sub("[\)\( +\-]", "", str(n_))
                n_ = "+" + "91" + n_ if (len(n_) == 10) else "+" + n_

            lead = Lead(
                name=row["name"],
                date=row["date"],
                mobile=n_,
                alternate_num=row["alternate number"],
                email=row["email"],
                lead_type=row["type"],
            )

            if not pandas.isna(row["location"]):
                locs = LeadLocation.objects.filter(location=row["location"])
                if not locs:
                    lead.Location = LeadLocation.objects.get_or_create(
                        location=row["location"]
                    )[0]
                else:
                    lead.Location = locs[0]

            if not pandas.isna(row["source"]):
                lead.Source = LeadSource.objects.get_or_create(source=row["source"])[0]

            if not pandas.isna(row["JOB_TITLE"]):
                lead.occupation = f'{row["JOB_TITLE"]} : {row["COMPANY_NAME"]}'

            lead.save()

        except IntegrityError as e:
            print(row)

    return HttpResponse("Loaded the shit up")


@csrf_exempt
# post leads with zapier
def lepost(request):
    if request.method == "POST":
        pss = "askjdhakjsdhkJKJHKH-08-09"

        # if password is correct
        if request.POST["pass"] == pss:
            feilds = [
                "name",
                "mobile",
                "email",
                "occupation",
                "location_str",
                "p_interest",
                "wa_num",
                "adset_name",
                "campaign_name",
            ]
            m_ = request.POST["mobile"]
            m = m_.replace(" ", "")
            m = m[1:] if (m[0] == "0") else m
            m = f"+91{m}" if ("+" not in m) else m
            m = m.replace("+910", "+91")

            lead_exist = Lead.objects.filter(mobile=m)

            # ----- Send notification to WA
            a_ = req.post('http://0.0.0.0:8800/queueshit', 
                                json= {
                'msg': f'{request.POST["name"]}\n{request.POST["mobile"]} \n {request.POST["wa_num"]} \n {request.POST["occupation"]}'
            }, headers={
                'API-Key': 'aksjdajkdKJGJHVJHUYFUYF809080987687'
            })

            if not lead_exist:

                l_ = Lead()

                l_.date = date.today()
                for f in feilds:
                    setattr(l_, f, request.POST[f])

                l_.Source = LeadSource.objects.get(source="FB")
                l_.lead_type = "PAID"

                # set appointment
                # t_ = request.POST["appointment_dt"].split(":")
                # t_ = ":".join(t_[:2])

                # l_.appointment_dt =  datetime.strptime(t_ , "%Y-%m-%dT%H:%M")

                # save lead

                l_.save()

                print(" ---------- >> ")

            else:
                l_ = lead_exist[0]
                s = Stage.objects.get(stage="Submitted Again")
                r_ = "\n".join([request.POST[f] for f in feilds])

                LeadStage(stage=s, lead=lead_exist[0], remarks=r_).save()

            notify(
                n_=request.POST.get("name"),
                m_=request.POST.get("phone"),
                e_=request.POST.get("email"),
                msg_="New Lead from FB",
            )

            return HttpResponse(l_.name, "setted")

        else:
            return HttpResponse("Password Incorrect motha fucka")
    else:
        return HttpResponse(f"Fuck you and your freinds :> :>")


@login_required()
def newleads(request):
    new_l = "<br>".join(
        [
            f"{l.name},{l.mobile[1:]}"
            for l in Lead.objects.all()
            if (not l.leadstage_set.all())
        ]
    )
    resp = "name,mobile<br>"

    return HttpResponse(resp + new_l)


@login_required()
def LeadListView(request, mod_id):
    l_ = LeadList.objects.get(id=int(mod_id))
    exec(l_.filter_string)

    return HttpResponse(
        "\n".join(rows),
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    # return HttpResponse("hi")


def tour(request):

    b_form = BrochureForm()
    if request.method == "POST" and "submitted_form" not in request.session:
        post = request.POST
        m_ = post.get("phone")
        m = m_.replace(" ", "")
        m = m[1:] if (m[0] == "0") else m
        m = f"+91{m}" if ("+" not in m) else m
        m = m.replace("+910", "+91")

        msg_ = (
            f'Interested in { post.get("interested_in")}'
            if ("interested_in" in post)
            else post.get("msg")
        )

        a_ = Enquiry(
            name=post.get("name"),
            mobile=m,
            email=post.get("email"),
            message=msg_,
        )
        a_.save()

        lead_exist = Lead.objects.filter(mobile=m)

        if not lead_exist:
            try:
                s_ = LeadSource.objects.get(source="Website")
                b_ = Lead(
                    name=post.get("name"),
                    mobile=m,
                    email=post.get("email"),
                    date=datetime.now(),
                    p_interest=msg_,
                    Source=s_,
                )
                b_.save()

            except Exception as e:
                open("/home/ubuntu/ascent/e.txt", "w").write(str(e))

        else:
            l_ = lead_exist[0]
            s = Stage.objects.get(stage="Submitted Again")
            r_ = "From Enquiry"

            LeadStage(stage=s, lead=lead_exist[0], remarks=r_).save()

        request.session["submitted_form"] = True

        # send notification email
        notify(
            n_=post.get("name"),
            m_=post.get("phone"),
            e_=post.get("email"),
            msg_=msg_,
        )

    context = {
        "main_gate": TourPics.objects.get(scene_text="Main Gate"),
        "entrance": TourPics.objects.get(scene_text="Entrance"),
        "a3_front": TourPics.objects.get(scene_text="a3_front"),
        "a3_first_floor": TourPics.objects.get(scene_text="a3_first_floor"),
        "a3_terrace": TourPics.objects.get(scene_text="a3_terrace"),
        "b3_terrace": TourPics.objects.get(scene_text="b3_terrace"),
        "b_form": b_form,
    }
    return render(request, "projects/comp/tour1.html", context=context)


# -------------------------------------------------------------------- Analysis Shit
@login_required()
def dash(request):
    context = {}
    colors = [
        "Red",
        "Blue",
        "Yellow",
        "Green",
        "Purple",
        "Orange",
        "Violet",
        "Green",
        "Orange",
        "Pink",
        "Grey",
        "Red",
        "Blue",
        "Yellow",
    ]

    td_ = datetime.today()
    expired_leads = []
    upcoming_leads = []
    main_leads = []
    stages = [i.stage for i in Stage.objects.all()] + ["None"]
    stages_dict = {i: 0 for i in stages}

    for lead in Lead.objects.all():
        s = lead.leadstage_set.last()
        stage_ = s.stage.stage if (s) else "None"
        stages_dict[stage_] += 1
        main_leads.append(lead)

        if stage_ != "None" and s.call_by:
            if s.call_by >= td_:
                upcoming_leads.append(lead)
            else:
                expired_leads.append(lead)

    # Call Logs
    # ld_ = date.today() - timedelta(7)
    # f_logs = CallLog.objects.filter(date__gte=ld_)
    # log_dist = (
    #     f_logs.values("agent__username").annotate(dcount=Count("agent")).order_by()
    # )

    # context["stages"] = list(stages_dict.keys())
    # context["stage_values"] = list(stages_dict.values())
    # context["leads"] = main_leads
    context["u_leads"] = upcoming_leads
    context["e_leads"] = expired_leads
    # context["log_dist_names"] = [i["agent__username"] for i in log_dist]
    # context["log_dist_nums"] = [i["dcount"] for i in log_dist]
    # context["log_colors"] = colors[: len(log_dist)]
    # context["call_logs"] = f_logs

    return render(request, "projects/analysis/dash.html", context=context)


def json_api(request, query):

    if request.method == "GET" and query == "alkdjlLKJLKHKJGJHMNBJHF345234LIPOO":
        print("getting response ---")
        response_data = {
            "dates": [],
            "names": [],
            "mob": [],
            "occ": [],
            "details": [],
            "locs": [],
        }

        a_ = AppLeads.objects.last()
        exec(a_.code)

        for lead in rows[::-1]:
            s = lead.leadstage_set.last()
            loc = lead.Location.location if (lead.Location) else lead.location_str
            s_ = lead.Source.source if (lead.Source) else "-"
            i_ = lead.product_interested.product if (lead.product_interested) else ""
            p_ = lead.purpose

            response_data["dates"].append(str(lead.date))
            response_data["names"].append(lead.name)
            response_data["mob"].append(lead.mobile)
            response_data["locs"].append(loc)
            response_data["occ"].append(lead.occupation)
            response_data["details"].append(f"{s_} : {p_} {i_}")

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        return HttpResponse("Baap se panga mat lo Bete")


def privacy(request):
    p_ = open('/home/vaqasahmed/prop23/static/privacy.txt','r').read().replace('\n',"<br/s>")
    return(HttpResponse(p_))

@csrf_exempt
def fresh_leads(request):
    if request.method == "POST":
        pass_ = request.POST.get(
            "pass"
        )  # Assuming the code is sent as a parameter named 'code'
        if pass_ == "JMGHJSDGJHkjshakjha0989y87mnasVNVasdjkh":

            if request.POST.get("type") == "fresh":
                # Get the cutoff date for CallLog
                cutoff_date = datetime.now() - timedelta(days=2)

                # Query the leads based on the criteria
                leads = (
                    Lead.objects.annotate(num_leadstages=Count("leadstage"))
                    .filter(
                        models.Q(calllog__isnull=True)
                        | models.Q(calllog__date__lt=cutoff_date),
                        num_leadstages__lte=1,
                    )
                    .order_by("-date")
                )[:50]

                leads_data = []
                for lead in leads:
                    s = lead.leadstage_set.last()
                    stage_ = s.stage.stage if (s) else "None"
                    lead_data = {
                        "date": lead.date,
                        "source": lead.Source.source if lead.Source else None,
                        "name": lead.name,
                        "mobile": lead.mobile,
                        "location": lead.Location.location
                        if lead.Location
                        else lead.location_str,
                        "occupation": lead.occupation,
                    }
                    leads_data.append(lead_data)

                return JsonResponse({"data": leads_data})

            else:
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=7)

                rows = []
                for lead in Lead.objects.all():
                    s = lead.leadstage_set.last()
                    stage_ = s.stage.stage if (s) else "None"
                    if stage_ in ["Site visit scheduled", "Need follow-up"]:
                        if s.call_by and start_date <= s.call_by.date() <= end_date:
                            d_ = {
                                "date": lead.date,
                                "source": lead.Source.source if lead.Source else None,
                                "name": lead.name,
                                "mobile": lead.mobile,
                                "location": lead.Location.location
                                if lead.Location
                                else lead.location_str,
                                "occupation": lead.occupation,
                                "CallBy": s.call_by,
                                "remarks": s.remarks,
                                "LastCalled": lead.calllog_set.last().date.date() if(lead.calllog_set.last()) else "-",
                            }
                            # print(stage_, lead)
                            rows.append(d_)
                return JsonResponse({"data": rows})

        return "Fuckoff"


@csrf_exempt
def mark_call(request):
    if request.method == "POST":
        pass_ = request.POST.get(
            "pass"
        )  # Assuming the code is sent as a parameter named 'code'
        if pass_ == "JMGHJSDGJHkjshakjha0989y87mnasVNVasdjkh":
            user = User.objects.get(username__contains="vaq")
            c = CallLog(
                agent=user, lead=Lead.objects.get(mobile=request.POST.get("mobile"))
            )
            c.save()
