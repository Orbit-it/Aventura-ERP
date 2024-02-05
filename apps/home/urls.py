# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from django.conf.urls import url
from apps.home import views
from .views import *

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path("send_demande", views.send_demande),
    path("edit_commande", views.edit_commande),
    path("update_qty", views.update_qty),
    path("bon_de_commande/<str:num_cmd>/<str:fournisseur>", views.bon_de_commande),
    path("mailing_commande/<str:fournisseur>/<str:numero_commande>", views.mailing_commande),
    path("confirm_commande_etranger/<str:num_cmd>/<str:nom_fourn>", views.confirm_commande_etranger),
    path("confirm_commande_local/<str:num_cmd>/<str:nom_fourn>", views.confirm_commande_local),
    path("confirm_all_line/<str:num_cmd>/<str:nom_fourn>", views.confirm_all_line),
    path("unconfirm_all_line/<str:num_cmd>/<str:nom_fourn>", views.unconfirm_all_line),
    path("confirm_commande_line/<int:id>", views.confirm_commande_line),
    path("unconfirm_commande_line/<int:id>", views.unconfirm_commande_line),
    path("envoyer_commande/<str:identifier>/<str:fournisseur>/<str:ref>", views.envoyer_commande),
    path("envoyer_commande_from_demande/<str:identifier>/<str:fournisseur>", views.envoyer_commande_from_demande),
    path("new_bc", views.new_bc),
    path("update_qty", views.update_qty, name="update_qty"),
    path("update_line", views.update_line, name="update_line"),
    path("new_commande_validation/<int:id>", views.new_commande_validation),
    path("new_commande_update/<int:id>", views.new_commande_update),
    path("rappeler_cmd/<int:id>", views.rappeler_cmd),
    path("cancel_bc/<str:bc>", views.cancel_bc),
    path("new_line_bc/<str:num_bc>/<str:project>/<str:fourn>", views.new_line_bc),
    path('approuver_dmd/<int:id>', views.approuver_dmd),
    path('approuver_cmd/<int:id>', views.approuver_cmd),
    path('refused_cmd/<int:id>', views.refused_cmd),
    path('grouper_cmd/<int:id>', views.grouper_cmd),
    path('annuler_cmd/<int:id>/<str:identifier>', views.annuler_cmd),
    path('delete_item_demande/<int:id_item>', views.delete_item_demande),
    path('refused_commande_line/<int:id>', views.refused_commande_line),
    path('delete_item_commande/<int:id_item>', views.delete_item_commande),
    path('planified_transport/<str:num_cmd>', views.planified_transport),
    #SUIVI POSITION COMMANDE
    path("commande_livrer/<str:num_cmd>", views.commande_livrer),
    path("commande_chez_gts/<str:num_cmd>", views.commande_chez_gts, name="suivi"),
    path("commande_en_transit/<str:num_cmd>", views.commande_en_transit),
    path("commande_receptionnee/<str:num_cmd>", views.commande_receptionnee),
    #SUIVI ETAT COMMANDE
    path("commande_normal/<str:num_cmd>", views.commande_normal),
    path("commande_manquant/<str:num_cmd>", views.commande_manquant),
    
    
    

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    re_path("suivi.html", views.pages, name='suivi'),
    re_path("magasin.html", views.pages, name='magasin'),
    

]
