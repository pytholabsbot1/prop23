from projects.models import *
import pandas as pd
from datetime import date

td_ = date.today()
expired_leads = []
upcoming_leads = []
stages = [i.stage for i in Stage.objects.all()] + ["None"]
stages_dict = {i : 0 for i in stages}

for lead in Lead.objects.all():
    s = lead.leadstage_set.last()
    stage_ = s.stage.stage if(s) else "None"
    stages_dict[stage_] += 1
    if(stage_ != "None" and s.call_by):
        if(s.call_by >= td_):
            upcoming_leads.append(lead)
        else:
            expired_leads.append(lead)

# ----------------

rows = []
for lead in Lead.objects.all():
    if("BUSINESS" == lead.occupation_type):
        s = lead.leadstage_set.last()
        stage_ = s.stage.stage if(s) else "None"
        loc = lead.Location.location if(lead.Location) else "None"
        s_ = lead.Source.source if(lead.Source) else "None"
        rem_ = s.remarks if(s) else "None"
        d = f"{lead.date}\t{s_}\t{lead.name}\t{loc}\t{lead.occupation}\t{stage_} -- {rem_}"
        rows.append(d)




result = (CallLog.objects
    .values('agent__username')
    .annotate(dcount=Count('agent'))
    .order_by()
)


    #    if("schedul" in stage_):
    #        loc = lead.Location.location if(lead.Location) else "None"
    #        s_ = lead.Source.source if(lead.Source) else "None"
    #        rem_ = s.remarks if(s) else "None"
    #        d = f"{lead.date}\t{s_}\t{lead.name}\t{loc}\t{lead.occupation}\t{rem_}"



global rows

rows = []
for lead in Lead.objects.all():
    s = lead.leadstage_set.last()
    stage_ = s.stage.stage if(s) else "None"
    loc = lead.Location.location if(lead.Location) else "None"
    s_ = lead.Source.source if(lead.Source) else "None"
    rem_ = s.remarks if(s) else "None"
    
    d = f"{lead.date}\t{s_}\t{lead.name}\t{loc}\t{lead.product_interested}\t{lead.occupation}\t{stage_}\t{rem_}"
    rows.append(d)


global rows

rows = []
for lead in Lead.objects.all():
    s = lead.leadstage_set.last()
    stage_ = s.stage.stage if(s) else "None"
    if(stage_ in ["COLD"]):
        loc = lead.Location.location if(lead.Location) else "None"
        s_ = lead.Source.source if(lead.Source) else "None"
        date_ = s.date
        rem_ = s.remarks if(s) else "None"
        d = f"{lead.date}\t{s_}\t{lead.name}\t{lead.mobile.strip()}\t{lead.email}\t{loc}\t{lead.occupation}\t{date_.date()}\t{stage_} : {rem_}"
        rows.append(d)



global rows

agent = "rabindra"
kms = []
for i in TravelledKms.objects.filter(agent__username=agent):
    kms.append(int(i.kms))

paid = []
for i in Reimbursement.objects.filter(agent__username=agent):
    paid.append(int(i.amount))

k_ = f"kms : {sum(kms)}"
a_ = f"paid : {sum(paid)}"

rows = [k_ , a_]

open("t.csv","w").write("\n".join(rows))

a = 0
for lead in Lead.objects.all():
    if(not lead.mobile):
        a = lead
        print(lead)


for e in Enquiry.objects.all().order_by('-id')[:10]:
    try:
        s_ = LeadSource.objects.get(source = "Website")
        b_ = Lead(
                name=e.name,
                mobile=e.mobile,
                email=e.email,
                date= e.date,
                p_interest=e.message,
                Source=s_
                )

        b_.save()

    except:
        print(e.mobile)


global rows

rows = []
for lead in Lead.objects.all():
    s = lead.leadstage_set.last()
    stage_ = s.stage.stage if(s) else "None"
    loc = lead.Location.location if(lead.Location) else lead.location_str
    s_ = lead.Source.source if(lead.Source) else "None"
    rem_ = s.remarks if(s) else "None"
    if(stage_ in ["Revisiting","Booking Consideration", "Submitted Again", "Not Picking Up", "Call Disconnected", "No Commitment", "Wants Plot", "Budget Issue", "Purchase Later", "COLD", "Need follow-up", "Not reachable", "Site visit scheduled", "Site Visit done", "Interested", "WA Intro Sent"]):
        if(lead.product_interested and sum([1 for i in ["4" , "5"] if i in lead.product_interested.product])):
            i_ = lead.product_interested
        elif(lead.p_interest and sum([1 for i in ["4" , "DUPLEX"] if i in lead.p_interest.upper()])):
            i_ = lead.p_interest

        if(i_):
            d = f"{lead.date}\t{s_}\t{lead.name}\t{lead.mobile}\t{lead.email}\t{loc}\t{lead.product_interested}\t{lead.p_interest}\t{lead.occupation}\t{stage_}\t{rem_}"
            rows.append(d)


int_ = []
for lead in Lead.objects.all():
    i_ = ""
    if(lead.product_interested and sum([1 for i in ["4" , "5"] if i in lead.product_interested.product])):
        i_ = lead.product_interested
    elif(lead.p_interest and sum([1 for i in ["4" , "DUPLEX"] if i in lead.p_interest.upper()])):
        i_ = lead.p_interest

    if(i_):
        print(i_)
        int_.append(lead)


global rows

rows = []
i_ = ""
for lead in Lead.objects.all():
    s = lead.leadstage_set.last()
    stage_ = s.stage.stage if(s) else "None"
    loc = lead.Location.location if(lead.Location) else lead.location_str
    s_ = lead.Source.source if(lead.Source) else "None"
    rem_ = s.remarks if(s) else "None"
    if(stage_ in ["Revisiting","Booking Consideration", "Submitted Again", "Not Picking Up", "Call Disconnected", "No Commitment", "Wants Plot", "Budget Issue", "Purchase Later", "COLD", "Need follow-up", "Not reachable", "Site visit scheduled", "Site Visit done", "Interested", "WA Intro Sent"]):
        d = f"{lead.date}\t{s_}\t{lead.name}\t{lead.mobile}\t{loc}\t{lead.occupation}\t{stage_}"
        rows.append(d)




# Get the date range for the last 7 days
start_date = datetime.now().date()
end_date = start_date - timedelta(days=7)

rows = []
for lead in Lead.objects.all():
    s = lead.leadstage_set.last()
    stage_ = s.stage.stage if(s) else "None"
    if(stage_ in ["Site visit scheduled"]):
        print(stage_ , lead)
        rows.append(lead)
        # if(s.call_by and start_date <= s.call_by.date() <= end_date):
