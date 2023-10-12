from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.shortcuts import redirect


class AmenitiesAdmin(admin.StackedInline):
    model = Amenities
    extra = 0


class KeyPointsAdmin(admin.StackedInline):
    model = KeyPoints
    extra = 0


class ReviewCardAdmin(admin.StackedInline):
    model = ReviewCard
    extra = 0


class FloorPlanAdmin(admin.StackedInline):
    model = FloorPlan
    extra = 0


class NearbyPlacesAdmin(admin.StackedInline):
    model = NearbyPlaces
    extra = 0


class GalleryImageAdmin(admin.StackedInline):
    model = GalleryImage
    extra = 0


class ListingAdmin(admin.ModelAdmin):
    inlines = [
        KeyPointsAdmin,
        AmenitiesAdmin,
        FloorPlanAdmin,
        NearbyPlacesAdmin,
        GalleryImageAdmin,
        ReviewCardAdmin,
    ]


# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Amenities)
admin.site.register(FloorPlan)
admin.site.register(FloorPlanType)
admin.site.register(NearbyPlaces)
admin.site.register(BaseInfo)
admin.site.register(GalleryImage)


# ----------------------- >>>>>>>>>>>>>>>>>>>>


# Register your models here.
class StagesAdmin(admin.StackedInline):
    model = LeadStage
    extra = 0

    readonly_fields = ("date",)


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("date", "name", "mobile", "message")


class FileAdmin(admin.ModelAdmin):
    list_display = ("file", "loadcsv")

    def loadcsv(self, obj):
        return format_html(
            f"""<button onclick="window.open('/loadcsv')">Load CSV</button>"""
        )


class LeadAdmin(admin.ModelAdmin):

    search_fields = ("name", "mobile", "occupation", "wa_num")
    list_display = (
        "name",
        "date",
        "Call",
        "product_interested",
        "m_details",
        "wa_num",
        "SendWhatsapp",
        "Whatsapp",
        "call_log",
        "LeadStage",
    )
    ordering = ["-date"]
    inlines = [StagesAdmin]
    list_filter = [
        "priority",
        "product_interested",
        "leadstage__stage",
        "occupation_type",
        "Location__location",
    ]

    ## Problem --> some leads not showing of locations
    # def get_queryset(self, request):
    #     qs = super(LeadAdmin, self).get_queryset(request)
    #     agent_locs = request.user.agentaccess_set.all()

    #     if not agent_locs:
    #         print("------- > main return")
    #         return qs

    #     else:
    #         q_sets = [ qs.filter(Location=agent.location) for agent in agent_locs]
    #         m_ = q_sets[0]

    #         print(" ------- > filtered return")
    #         if(len(m_)>1):
    #             for q in q_sets:
    #                 m_ = m_ | q

    #         return m_

    def Call(self, obj):
        objs_ = obj.mobile
        if objs_:
            return format_html(
                f'<img src="https://cdn2.iconfinder.com/data/icons/font-awesome/1792/phone-512.png" style="width: 12px;"/><a href="/callredirect/{objs_.strip()}"> {objs_} </a>'
            )
        else:
            return " -- "

    def Called(self, obj):
        if obj.called:
            return format_html(
                """<img src="/static/admin/img/icon-yes.svg" alt="False">"""
            )
        else:
            return format_html(
                f"""<button onclick="window.open('/called/{obj.id}')">Called</button>"""
            )

    def m_details(self, obj):
        occ = " : " + obj.occupation if (obj.occupation) else ""

        return format_html(
            f"""<p>{obj.Source.source  if(obj.Source) else ""} {"from " + obj.Location.location if(obj.Location) else obj.location_str} {occ}"""
            + "</p>"
        )

    def Whatsapp(self, obj):
        return format_html(
            f"""<button onclick="window.open('https://wa.me/{obj.mobile.strip()}')">Whatsapp</button>"""
        )

    def SendWhatsapp(self, obj):
        return format_html(
            f"""<button onclick="window.open('/sndwa/{obj.id}')">SEND WA</button>"""
        )

    def LeadStage(self, obj):
        stage_ = obj.leadstage_set.last()
        if stage_:
            s = stage_.stage.stage
            r = stage_.remarks

            return format_html(
                f"""
                <b>{s if("WA " not in s) else "*"}</b> : {"" if(r==None or r=="None") else r}
            """
            )

    def call_log(self, obj):
        c_ = obj.calllog_set.last()
        if c_:
            return f"{c_.date}".split(".")[0]
        else:
            return "-"


class DownloadLeadsAdmin(admin.ModelAdmin):
    def response_post_save_add(self, request, obj):

        location_ = obj.loc.location

        # get sets
        s_ = LeadLocation.objects.filter(location=location_)
        filtered_leads = [
            l
            for l in Lead.objects.all()
            if (l.Location and l.Location.location == location_)
        ]

        # set first location instance to all leads
        for l in filtered_leads:
            l.Location = s_[0]
            l.save()

        # delete other instances of location
        if len(s_) > 1:
            [s.delete() for s in s_[1:]]

        csv = "date,name,mobile,email,location,occupation<br/>"
        for l in filtered_leads:
            row = f"{l.date},{l.name},{l.mobile},{l.email},{l.Location},{l.occupation}<br/>"
            csv += row

        return HttpResponse(csv)


class CallLogAdmin(admin.ModelAdmin):
    list_display = ("agent", "lead", "date")


class ConstructionUpdatesAdmin(admin.ModelAdmin):
    list_display = ("date", "unit_no", "image_tag", "text")


class TravelledKmsAdmin(admin.ModelAdmin):
    list_display = ("agent", "kms", "date")
    exclude = ["agent"]

    def save_model(self, request, obj, form, change):
        obj.agent = request.user
        super().save_model(request, obj, form, change)


class JCBAdmin(admin.ModelAdmin):
    list_display = ("mode", "date", "agent")
    exclude = ["agent"]

    def save_model(self, request, obj, form, change):
        obj.agent = request.user
        super().save_model(request, obj, form, change)


class ElectricityReadingAdmin(admin.ModelAdmin):
    exclude = ["agent"]

    def save_model(self, request, obj, form, change):
        obj.agent = request.user
        super().save_model(request, obj, form, change)


class ReimbursementAdmin(admin.ModelAdmin):
    list_display = ("date", "agent", "amount", "remarks")


class InventoryAdmin(admin.ModelAdmin):
    list_display = ("Item", "qty", "item_type", "remarks")


class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_date", "name", "unit_type", "unit_no", "remarks")


class LeadListAdmin(admin.ModelAdmin):
    def response_add(self, request, obj, post_url_continue=None):
        return redirect(f"/list/{obj.id}")

    def response_change(self, request, obj):
        return redirect(f"/list/{obj.id}")


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "mode", "amount", "category", "head")

    def save_model(self, request, obj, form, change):
        b_ = Balance.objects.first()

        if obj.mode == "Income":
            amt = int(obj.amount) + int(b_.cash)
            b_.cash = str(amt)

        else:
            amt = int(b_.cash) - int(obj.amount)
            b_.cash = str(amt)

        # save balance
        b_.save()
        super().save_model(request, obj, form, change)


admin.site.register(Lead, LeadAdmin)
admin.site.register(LeadLocation)
admin.site.register(LeadSource)
admin.site.register(LeadStage)
admin.site.register(Product)
admin.site.register(Construction_Updates, ConstructionUpdatesAdmin)
admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(NotifyEmails)
admin.site.register(Stage)
admin.site.register(AppLeads)
admin.site.register(Review)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Reimbursement, ReimbursementAdmin)
admin.site.register(JCB, JCBAdmin)
admin.site.register(ElectricityReading, ElectricityReadingAdmin)
admin.site.register(DownloadLeads, DownloadLeadsAdmin)
admin.site.register(MarkLeads)
admin.site.register(AgentAccess)
admin.site.register(Balance)
admin.site.register(TourPics)
admin.site.register(LeadList, LeadListAdmin)
admin.site.register(CashCategory)
admin.site.register(TravelledKms, TravelledKmsAdmin)
admin.site.register(CallLog, CallLogAdmin)
admin.site.register(FileUpload, FileAdmin)
admin.site.register(Transaction, TransactionAdmin)
