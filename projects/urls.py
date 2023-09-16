from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("project/<str:project>",views.property,name="property"),
    path("test",views.PropTest,name="test"),

    path("sndwa/<str:index>", views.sendwa, name="mark"),
    # path("loadcsv", view=views.loadcsv),
    path("mcll", view=views.mark_call),
    path("privacy", view=views.privacy),
    path("lepost", view=views.lepost),
    path("dash", view=views.dash),
    path("fetch_leads", views.fresh_leads, name="ff"),
    path("tour", views.tour, name="tour"),
    path("api/<str:query>", view=views.json_api),
    path("list/<str:mod_id>", view=views.LeadListView),
    path("callredirect/<str:num>", view= views.call_redirect),
]