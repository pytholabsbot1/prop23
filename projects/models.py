from typing import List
from django.db import models
from datetime import datetime
from cropperjs.models import CropperImageField
from django.db import IntegrityError
from django.http import HttpResponse
from django.conf import settings
from django.utils.safestring import mark_safe
import requests as req


class BaseInfo(models.Model):
    mobile = models.CharField(max_length=50)
    whatsapp = models.CharField(max_length=50)
    test_server = models.CharField(max_length=100, null=True, blank=True)


# Create your models here.
class Listing(models.Model):
    # top
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    starting_price = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    duration = models.CharField(max_length=200, null=True, blank=True)
    project_type = models.CharField(max_length=200, null=True, blank=True)
    alert = models.CharField(max_length=200, null=True, blank=True)

    tour = models.ImageField(null=True, blank=True)
    # details
    description = models.TextField(max_length=10000)
    listing_image = CropperImageField(aspectratio=1.5, null=True)
    total_area = models.CharField(max_length=200, null=True, blank=True)
    unit_types = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True)
    total_units = models.CharField(max_length=200, null=True, blank=True)
    bathrooms = models.CharField(max_length=200, null=True, blank=True)
    open_area = models.CharField(max_length=200, null=True, blank=True)
    rera = models.CharField(max_length=200, null=True, blank=True)

    card_key = models.CharField(max_length=200, null=True, blank=True)

    brochure = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    image = CropperImageField(aspectratio=1.5, null=True)
    project = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)
    video = models.FileField(null=True, blank=True)


class Amenities(models.Model):
    amenity = models.CharField(max_length=50)
    project = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.amenity


class KeyPoints(models.Model):
    head = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    project = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.head


class ReviewCard(models.Model):
    photo = CropperImageField(aspectratio=1, null=True)
    head = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    occ = models.CharField(max_length=50)
    remarks = models.CharField(max_length=100)
    project = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.head


class FloorPlanType(models.Model):
    title = models.CharField(max_length=50)
    yt_link = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class FloorPlan(models.Model):
    title = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    tp = models.ForeignKey(
        FloorPlanType, null=True, on_delete=models.CASCADE, blank=True
    )
    plan = models.FileField(null=True, blank=True)
    sold_out = models.BooleanField(null=True, default=False)

    project = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class NearbyPlaces(models.Model):
    place = models.CharField(max_length=500)
    distance = models.CharField(max_length=50)
    project = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.place


class Enquiry(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    message = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class NotifyEmails(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ----------------------- >>>>>>>>>>>>>>>>>>>>
# Variables
lead_type_choices = (("ORGANIC", "ORGANIC"), ("PAID", "PAID"))

employment_type_choices = (
    ("SALARIED", "SALARIED"),
    ("BUSINESS", "BUSINESS"),
    ("RETIRED", "RETIRED"),
)


# FUCKIN MODELS FOR LEADS
class LeadLocation(models.Model):
    location = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.location


class LeadSource(models.Model):
    source = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.source


class Product(models.Model):
    product = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.product


class Lead(models.Model):

    name = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True, unique=True)
    called = models.BooleanField(default=False, null=True)
    priority = models.BooleanField(default=False, null=True)

    alternate_num = models.CharField(max_length=50, null=True, blank=True)
    wa_num = models.CharField(max_length=50, null=True, blank=True)
    appointment_dt = models.DateTimeField(null=True, blank=True)
    adset_name = models.CharField(max_length=100, null=True, blank=True)
    campaign_name = models.CharField(max_length=100, null=True, blank=True)
    p_interest = models.CharField(max_length=100, null=True, blank=True)

    email = models.CharField(max_length=50, null=True, blank=True)

    Location = models.ForeignKey(
        LeadLocation, null=True, blank=True, on_delete=models.CASCADE
    )

    ## added fields
    location_str = models.CharField(max_length=1000, null=True, blank=True)
    purpose = models.CharField(max_length=50, null=True, blank=True)
    details = models.TextField(blank=True, null=True)

    Source = models.ForeignKey(
        LeadSource, null=True, blank=True, on_delete=models.CASCADE
    )
    occupation = models.CharField(max_length=500, null=True, blank=True)
    product_interested = models.ForeignKey(
        Product, blank=True, null=True, on_delete=models.CASCADE
    )

    lead_type = models.CharField(
        max_length=50, choices=lead_type_choices, null=True, blank=True
    )
    occupation_type = models.CharField(
        max_length=50, choices=employment_type_choices, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # # data to be sent to api
        # if not self.id:
        #     data = {
        #         "mobile": self.mobile,
        #     }

        #     r_ = req.post("http://127.0.0.1:5000/send_msg", data=data)
        #     print(r_.text)

        super(Lead, self).save(*args, **kwargs)


class Stage(models.Model):
    stage = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.stage


class FileUpload(models.Model):
    file = models.FileField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(FileUpload, self).save(*args, **kwargs)


class LeadStage(models.Model):
    stage = models.ForeignKey(Stage, null=True, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    call_by = models.DateTimeField(null=True, blank=True)
    lead = models.ForeignKey(Lead, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.stage.stage

    def save(self, *args, **kwargs):
        # data to be sent to api

        if self.call_by:
            data = {
                "stage": self.stage.stage,
                "name": self.lead.name,
                "mobile": self.lead.mobile,
                "dt": self.call_by.isoformat(),
            }

            # r_ = req.post("http://127.0.0.1:5000/schedule", data=data)
            # print(r_.text)

        super(LeadStage, self).save(*args, **kwargs)


## SPECIAL MODELS ------------------------ >>>>


class MarkLeads(models.Model):
    text = models.TextField(null=True)
    stage = models.ForeignKey(Stage, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.stage.stage

    def save(self, *args, **kwargs):

        nums = []
        for n in self.text.split("\n"):
            n = f"+{n}"
            n_ = Lead.objects.get(mobile=n.strip())
            nums.append(n_)

            print(f" ------ > {n_}")

        _ = [LeadStage(stage=self.stage, lead=n).save() for n in nums]

        super(MarkLeads, self).save(*args, **kwargs)


class DownloadLeads(models.Model):
    loc = models.ForeignKey(LeadLocation, null=True, on_delete=models.SET_NULL)


class AgentAccess(models.Model):
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    location = models.ForeignKey(LeadLocation, on_delete=models.CASCADE)


class CallLog(models.Model):
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.agent} : {self.lead}"


class ElectricityReading(models.Model):
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    photo = CropperImageField(aspectratio=1.5, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.date}"


class TravelledKms(models.Model):
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    kms = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.agent} : {self.kms}"


class JCB(models.Model):
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(null=True, blank=True, default=datetime.now)

    mode = models.CharField(
        max_length=50,
        choices=(("START", "START"), ("STOP", "STOP")),
        null=True,
        blank=True,
    )

    photo = CropperImageField(aspectratio=1.5, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.agent} : {self.mode}"


class Reimbursement(models.Model):
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(null=True, blank=True, default=datetime.now)

    amount = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.agent} : {self.amount}"


class Balance(models.Model):
    cash = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"cash : {self.cash}"


class CashCategory(models.Model):
    category = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.category


class Transaction(models.Model):
    date = models.DateTimeField(null=True, blank=True, default=datetime.now)
    mode = models.CharField(
        max_length=50,
        choices=(("Income", "Income"), ("Expense", "Expense")),
        null=True,
        blank=True,
    )
    amount = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(CashCategory, on_delete=models.CASCADE)
    head = models.TextField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.head


class LeadList(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    filter_string = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Inventory(models.Model):
    Item = models.CharField(max_length=50, null=True, blank=True)
    item_type = models.CharField(
        max_length=50, null=True, blank=True, default="Discrete"
    )
    qty = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.Item


class Booking(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    booking_date = models.CharField(max_length=50, null=True, blank=True)
    unit_no = models.CharField(max_length=50, null=True, blank=True)
    unit_type = models.CharField(
        max_length=50, null=True, blank=True, default="Discrete"
    )
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.unit_no


# new add
class Review(models.Model):
    head = models.CharField(max_length=200, null=True)
    body = models.TextField(null=True, blank=True)
    cus_img = CropperImageField(aspectratio=1, null=True)
    cus_name = models.CharField(max_length=50, null=True)
    cus_designation = models.CharField(max_length=50, null=True)
    cus_prod = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.cus_name


class Construction_Updates(models.Model):
    unit_no = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, null=True, blank=True)
    image = CropperImageField(aspectratio=1.5, null=True)
    text = models.TextField(null=True, blank=True)

    def image_tag(self):
        return mark_safe(
            '<img src="/media/%s" width="150" height="150" />' % (self.image)
        )

    image_tag.short_description = "Image"
    image_tag.allow_tags = True

    def __str__(self):
        return self.unit_no.unit_no


class AppLeads(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    code = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class TourPics(models.Model):
    sequence = models.IntegerField(default=0, null=True)
    pitch = models.CharField(max_length=20, null=True, blank=True)
    yaw = models.CharField(max_length=20, null=True, blank=True)
    scene_text = models.CharField(max_length=20, null=True, blank=True)
    scene_id = models.CharField(max_length=20, null=True, blank=True)
    scene_img = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.scene_text
