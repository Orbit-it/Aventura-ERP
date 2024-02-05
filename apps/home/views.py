# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import io
import os
from turtle import color, width
from django.views.decorators.csrf import csrf_exempt
from unicodedata import name
import winsound
from mmap import PAGESIZE
from PIL import Image
from numpy import size
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter, A4
from datetime import MAXYEAR, date, datetime
from logging import PlaceHolder
from msilib.schema import ListView
from click import command
from matplotlib.style import context
import matplotlib.pyplot as plt
from zmq import device
from .models import *
from django import forms
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
from reportlab.lib import colors
import random
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

# demande d'achat
item_demande_art = []
item_demande_fourn = []
item_demande_qty = []
item_demande_unity = []
item_demande_pu = []

# demande d'appro
item_appro_art = []
item_appro_fourn = []
item_appro_qty = []
item_appro_unity = []
item_appro_projet = []



# commande achat
item_commande_art = []
item_commande_ref = []
item_commande_fourn = []
item_commande_qty = []
item_commande_unity = []
item_commande_pu = []

# Sortie directe
item_sortie_art = []
item_sortie_qty = []
item_sortie_unity = []
item_sortie_motif = []
item_sortie_user = []

# send commande
ref_bateau = []
date_livraison_sht = []
rmq = []

ref_bc_list = []
fournisseur_bc_list = []
dls_bc_list = []



# list de mes commandes


list_cmd_fournissuer = []


Unity =(
    "P",
    "ML",
    "M²",
    "M³",
    "L",
    "Kg",
    "ROULEAUX"
    )


# the demande form
class Add_item_demandeForm(forms.Form):
    article_item = forms.CharField(label="", required=True)
    fournisseur_item = forms.CharField(label="", required=True)
    quantity_item = forms.FloatField(label="", required=True, min_value=0)
    unity_item = forms.CharField(label="", required=True)
    pu_item = forms.FloatField(label="", min_value=0)

# the appro form
class Add_item_approForm(forms.Form):
    article_item = forms.CharField(label="", required=True)
    fournisseur_item = forms.CharField(label="", required=True)
    quantity_item = forms.FloatField(label="", required=True, min_value=0)
    unity_item = forms.CharField(label="", required=True)
    projet_item = forms.CharField(label="", required=True)


# the commande form
class Add_item_commandeForm(forms.Form):
    article_item_cmd = forms.CharField(label="", required=True)
    ref_item_cmd = forms.CharField(label="", required=False)
    fournisseur_item_cmd = forms.CharField(label="", required=True)
    quantity_item_cmd = forms.FloatField(label="", required=True, min_value=0)
    unity_item_cmd = forms.CharField(label="", required=True)
    pu_item_cmd = forms.FloatField(label="", min_value=0, required=False)

# the Sortie Directe form
class SortieDirecteForm(forms.Form):
    article_item_sortie = forms.CharField(label="", required=True)
    quantity_item_sortie = forms.FloatField(label="", required=True, min_value=0)
    unity_item_sortie = forms.CharField(label="", required=True)
    motif_item_sortie = forms.CharField(label="",required=True) 
    user_item_sortie = forms.CharField(label="",required=True)    


# the sending_commande form
class Send_commandeForm(forms.Form):
    rmq = forms.CharField(label="Remarque", required=False)


class OpenBCForm(forms.Form):
    ref_bc = forms.CharField(label="", required=True)
    dls_bc = forms.DateField(label='', required=False)
    fournisseur_bc = forms.CharField(label="", required=True)

class ValidationQuantityForm(forms.Form):
    qty = forms.FloatField(label="", required=False)


class MotifForm(forms.Form):
    motif_refus = forms.CharField(label="", required=False)    

    


    

@login_required(login_url="/login/")
def index(request):
    

# dispach des modules de chaque user en fonction de ses autorisations

    curent_user = Permission.objects.get(user_permission = request.user.username)

    achat = "achat_users.html"
    magasin = "refused_access.html"
    suivi = "refused_access.html"
    home = "index.html"

    if curent_user.admin_permission == True:
        achat = "achat.html" 
        home = "index_admin.html"
    elif curent_user.magasin_permission == True and curent_user.achat_permission == True:    
        achat = "achat_achat.html" 
        magasin = "magasin.html"
    elif curent_user.achat_permission == True:
        achat = "achat_achat.html"
        suivi = "achat_rania.html"
    elif curent_user.magasin_permission == True:
        magasin = "magasin.html"
        achat = "refused_access.html"    


# end dispaching

    context = {'segment': 'index', 'achat': achat, 'magasin': magasin, 'suivi': suivi}

    html_template = loader.get_template('home/'+home)
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):

    msg = None


    msg_appro = None

    msg_commande = None

    msg_sortie_directe = None

    msg_bc = None

    msg_line = None

    
# dispach des modules de chaque user en fonction de ses autorisations

    curent_user = Permission.objects.get(user_permission = request.user.username)

    achat = "achat_users.html"
    magasin = "refused_access.html"

    if curent_user.admin_permission == True:
        achat = "achat.html" 
    elif curent_user.achat_permission == True and curent_user.magasin_permission == False:
        achat = "achat_achat.html"
    elif curent_user.magasin_permission == True and curent_user.achat_permission == True:
        magasin = "magasin.html" 
        achat = "achat_achat.html"
    elif curent_user.magasin_permission == True and curent_user.achat_permission == False:
        magasin = "magasin.html"    
   

# end dispaching

# Dispatch des Commandes par Fournisseur

    mes_list = AprouvedAchat.objects.all()

    for element in mes_list:
        if element.fournisseur not in list_cmd_fournissuer:
            list_cmd_fournissuer.append(element.fournisseur)


# End dispatching

# formulaire de demande d'achat---------------------------------------------------------------------------------

    if request.method == "POST":
        if 'demande' in request.POST:
            form_item_demande = Add_item_demandeForm(request.POST)
            if form_item_demande.is_valid():
                article_item = form_item_demande.cleaned_data["article_item"]
                fournisseur_item = form_item_demande.cleaned_data["fournisseur_item"]
                quantity_item = form_item_demande.cleaned_data["quantity_item"]
                unity_item = form_item_demande.cleaned_data["unity_item"]
                pu_item = form_item_demande.cleaned_data["pu_item"]

                # insert in the database
                List_item_on_Demande.objects.create(user_dem = request.user.username ,
                article_dem = article_item,
                fournisseur_dem = fournisseur_item, 
                quantity_dem = quantity_item, 
                unity_dem = unity_item, 
                pu_dem = pu_item, 
                prix_dem = float(pu_item)*float(quantity_item))
            
            else:
                msg = ' Valeurs Invalides: Veuillez saisir un article conforme aux différents champs'

    
    query_result = List_item_on_Demande.objects.filter(user_dem = request.user.username) #filtrer les item pour chaque user

    query_demande_achat = DimensionAchat.objects.filter(type_achat_dim = "Demande").order_by('date').reverse  #filtr the Demande Achat list and order them by date

    waiting_aprouved_demande = DimensionAchat.objects.filter(type_achat_dim = "Demande").count()

    aprouved = AprouvedAchat.objects.filter(type_achat = "Demande").count()

    aprouved_list_dmd = AprouvedAchat.objects.filter(type_achat = "Demande").order_by('date').reverse  # filter the aprouved demande list

    demande_total = waiting_aprouved_demande + aprouved

    demande_by_user = DimensionAchat.objects.filter(user_dim = request.user.username, type_achat_dim = "Demande").count() #filter the Demande of a specific user
    
# End Formulaire de demande d'achat------------------------------------------------------------------------------

# formulaire de sortie directe---------------------------------------------------------------------------------

    if request.method == "POST":
        if 'sortie_directe' in request.POST:
            form_item_sortie_directe = SortieDirecteForm(request.POST)
            if form_item_sortie_directe.is_valid():
                article_sortie = form_item_sortie_directe.cleaned_data["article_item_sortie"]
                quantity_sortie = form_item_sortie_directe.cleaned_data["quantity_item_sortie"]
                unity_sortie = form_item_sortie_directe.cleaned_data["unity_item_sortie"]
                motif_sortie = form_item_sortie_directe.cleaned_data["motif_item_sortie"]
                user_sortie = form_item_sortie_directe.cleaned_data["user_item_sortie"]

                if article_sortie not in item_sortie_art:
                    item_sortie_art.append(article_sortie)
                    item_sortie_qty.append(quantity_sortie)
                    item_sortie_unity.append(unity_sortie)
                    item_sortie_motif.append(motif_sortie)
                    item_sortie_user.append(user_sortie)

                for i in range(len(item_sortie_art)):
                    # insert in the database
                    Sortiedirecte.objects.create(user_name = request.user.username ,designation = item_sortie_art[i],
                    quantity = item_sortie_qty[i], unity = item_sortie_unity[i] , motif = item_sortie_motif[i],
                    operateur = item_sortie_user[i])
            else:
                msg_sortie_directe = ' Valeurs Invalides: Veuillez saisir tous les champs pour effectuer une sortie directe'

            item_sortie_art.clear()
            item_sortie_qty.clear()
            item_sortie_unity.clear()
            item_sortie_motif.clear()
            item_sortie_user.clear()
    
   

    sortie_direct =Sortiedirecte.objects.filter(user_name = request.user.username).order_by('date').reverse  #the sortie directe list and order them by date
    sortie_direct_count =Sortiedirecte.objects.filter(user_name = request.user.username).count()  # nombre sortie directe

# formulaire de demande d'appro ---------------------------------------------------------------------------------

    if request.method == "POST":
        form_item_appro = Add_item_approForm(request.POST)
        if form_item_appro.is_valid():
            article_item_appro = form_item_appro.cleaned_data["article_item_appro"]
            fournisseur_item_appro = form_item_appro.cleaned_data["fournisseur_item_appro"]
            quantity_item_appro = form_item_appro.cleaned_data["quantity_item_appro"]
            unity_item_appro = form_item_appro.cleaned_data["unity_item_appro"]
            projet_item_appro = form_item_appro.cleaned_data["projet_item_appro"]

            if article_item_appro not in item_appro_art:
                item_appro_art.append(article_item_appro)
                item_appro_fourn.append(fournisseur_item_appro)
                item_appro_qty.append(quantity_item_appro)
                item_appro_unity.append(unity_item_appro)
                item_appro_projet.append(projet_item_appro)

            for i in range(len(item_demande_art)):
                # insert in the database
                List_item_on_Demande.objects.create(user_dem = request.user.username ,article_dem = item_demande_art[i], fournisseur_dem = item_demande_fourn[i], quantity_dem = item_demande_qty[i], unity_dem = item_demande_unity[i] , pu_dem = item_demande_pu[i], prix_dem = item_demande_pu[i]*item_demande_qty[i])
        else:
            msg_appro = ' Valeurs Invalides: Veuillez saisir un article conforme aux différents champs'

    item_appro_art.clear()
    item_appro_fourn.clear()
    item_appro_qty.clear()
    item_appro_unity.clear()
    item_appro_projet.clear()
    
    
# End Formulaire de demande d'appro------------------------------------------------------------------------------


# formulaire de Commande Achat---------------------------------------------------------------------------------

    if request.method == "POST":
        form_item_commande = Add_item_commandeForm(request.POST)
        if form_item_commande.is_valid():
            article_item_cmd = form_item_commande.cleaned_data["article_item_cmd"]
            ref_item_cmd = form_item_commande.cleaned_data["ref_item_cmd"]
            fournisseur_item_cmd = form_item_commande.cleaned_data["fournisseur_item_cmd"]
            quantity_item_cmd = form_item_commande.cleaned_data["quantity_item_cmd"]
            unity_item_cmd = form_item_commande.cleaned_data["unity_item_cmd"]
            pu_item_cmd = form_item_commande.cleaned_data["pu_item_cmd"]

            if article_item_cmd not in item_commande_art:
                item_commande_art.append(article_item_cmd)
                item_commande_ref.append(ref_item_cmd)
                item_commande_fourn.append(fournisseur_item_cmd)
                item_commande_qty.append(quantity_item_cmd)
                item_commande_unity.append(unity_item_cmd)
                item_commande_pu.append(pu_item_cmd)

            for j in range(len(item_commande_art)):
                # insert in the database
                List_item_on_Commande.objects.create(user_com = request.user.username ,
                article_com = item_commande_art[j], ref_com = item_commande_ref[j], fournisseur_com = item_commande_fourn[j],
                quantity_com = item_commande_qty[j], unity_com = item_commande_unity[j] ,
                pu_com = item_commande_pu[j],
                prix_com = item_commande_pu[j]*item_commande_qty[j])
        else:
            msg_commande = ' Valeurs Invalides: Veuillez saisir un article conforme aux différents champs'

    item_commande_art.clear()
    item_commande_ref.clear()
    item_commande_fourn.clear()
    item_commande_qty.clear()
    item_commande_unity.clear()
    item_commande_pu.clear()
    
    query_result_cmd = List_item_on_Commande.objects.filter(user_com = request.user.username)#filtrer les item pour chaque user

    query_commande_achat = DimensionAchat.objects.filter(type_achat_dim = "Commande").order_by('date').reverse

    pending_cmd = DimensionAchat.objects.filter(type_achat_dim = "Commande").order_by('date').reverse

    aprouved_list_cmd = AprouvedAchat.objects.filter(type_achat = "Commande", is_ready = 0).order_by('date').reverse  # filter the aprouved demande list

    refused_list_cmd_achat = RefusedAchat.objects.filter(type_achat = "Commande", user_name = "Sonia").order_by('date').reverse  # filter the refused demande list

    waiting_aprouved_commande = DimensionAchat.objects.filter(type_achat_dim = "Commande").count()

    aprouved_commande = AprouvedAchat.objects.filter(type_achat = "Commande").count()

    users = Operateur.objects.all()

    
    refused_commande_count = RefusedAchat.objects.filter(type_achat = "Commande").count()

    commande_total = waiting_aprouved_commande + aprouved_commande

    envoie_commande_list = CommandeAchat.objects.filter(is_sent = 0).order_by('date_env').reverse #list des commandes pretes à envoyer

    after_envoie_commande_list = CommandeAchat.objects.filter(is_sent = 1) #list des commandes déjà envoyer

    transport_planifies = CommandeAchat.objects.filter(is_planified = 1)
    transport_planifies_nombre = transport_planifies.count()

    transport_non_planifies = CommandeAchat.objects.filter(is_planified = 0)
    transport_non_planifies_nombre = transport_non_planifies.count()

   # Suivi commande------------------------------------------------------------------------------------------

    suivi_commande = SuiviCommande.objects.all()

    name_fourn_suivi = []
    

    decompte_fournisseur_suivi = {}

    for comm in suivi_commande:
        if comm.nom_fournisseur not in name_fourn_suivi:
            name_fourn_suivi.append(comm.nom_fournisseur)
            decompte_fournisseur_suivi[comm.nom_fournisseur] = 1
        elif comm.nom_fournisseur in name_fourn_suivi:
            decompte_fournisseur_suivi[comm.nom_fournisseur] += 1   
            
        
# Formulaire Entete bc optionnelle

    if request.method == "POST":
        if 'entete_bc' in request.POST:
            form_item_send = Send_commandeForm(request.POST)
            if form_item_send.is_valid():
                rmq = form_item_send.cleaned_data["rmq"]
                BC_Fournisseur.objects.create(remarque = rmq)
            
# Formulaire Entete bc 

    if request.method == "POST":
        if 'open_bc' in request.POST:
            form_bc = OpenBCForm(request.POST)
            if form_bc.is_valid():
                fournisseur_bc = form_bc.cleaned_data["fourn_bc"]
                ref_bc = form_bc.cleaned_data["ref_bc"]
                dls_bc = form_bc.cleaned_data["dls_bc"]
                
                ref_bc_list.append(ref_bc)
                dls_bc_list.append(dls_bc)
                fournisseur_bc_list.append(fournisseur_bc)
                
                for z in range(len(ref_bc_list)):
                    # insert in the database
                    Bc.objects.create(dls_bc = dls_bc_list[z],
                    ref_bc = ref_bc_list[z], fournisseur_bc = fournisseur_bc_list[z])
            else:
                msg_bc = ' Entête Invalide: Veuilllez réessayer !'

            print(ref_bc_list)
            ref_bc_list.clear()
            dls_bc_list.clear()
            fournisseur_bc_list.clear()
           


# End of Formulaire Entete bc    

# Motif de refus

    if request.method == "POST":
        if 'motif_refus' in request.POST:
            form_item_motif = MotifForm(request.POST)
            id_line = refused_commande_line()
            if form_item_motif.is_valid():
                motif_refus = form_item_motif.cleaned_data["motif_refus"]
                line = Commande.objects.filter(id = id_line)
                line.update(is_refused = 0, motif_commande = motif_refus)
            


# End of Motif de refus

 #Formulaire Entete bc optionnelle

    if request.method == "POST":
        if 'valider' in request.POST:
            form_item_val = ValidationQuantityForm(request.POST)
            if form_item_send.is_valid():
                qty = form_item_send.cleaned_data["ref_bateaux"]
                
            


# End of Formulaire Entete bc optionnelle   
       
       
   
# End Suivi Commande------------------------------------------------------------------------------------------------

# End Formulaire de commande Achat------------------------------------------------------------------------------



    new_bc_list = Bc.objects.filter(is_send_approval = 0).order_by('date').reverse()


    article = Article.objects.all()
    fournisseur = Fournisseur.objects.all()
    
    ind = "Indefinit"
  
    # demande and commande creation
    demande = Demande.objects.all()
    commande = Commande.objects.all()
    commande_pending = Commande.objects.filter(is_approuved = 0)
    context = {'article': article, 'fournisseur': fournisseur, 'demande': demande, 'commande': commande, 'achat': achat,
     'magasin_link': magasin,
     'ind': ind,
     'msg_bc': msg_bc,
     'msg_appro': msg_appro,
     'transport_planifies': transport_planifies,
     'planifies': transport_planifies_nombre,
     'transport_non_planifies': transport_non_planifies,
     'non_planifies': transport_non_planifies_nombre,
     'form_item_demande': Add_item_demandeForm, 
     'form_item_commande': Add_item_commandeForm,
     'form_send_commande': Send_commandeForm,
     'form_sortie_directe': SortieDirecteForm,
     'form_open_bc': OpenBCForm,
     "decompte": decompte_fournisseur_suivi,
     'envoie_commande_list': envoie_commande_list,
     'after_envoie_commande_list': after_envoie_commande_list,
     'suivi_commande': suivi_commande,
     "demande_total": demande_total,
     'commande_total': commande_total,
     'unity': Unity,
     'msg': msg,
     'msg_commande': msg_commande,
     'query_result': query_result,
     'query_result_cmd': query_result_cmd,
     'query_demande': query_demande_achat,
     'query_commande': query_commande_achat,
     'aprouved': aprouved,
     'list_cmd_fournisseur': list_cmd_fournissuer,
     'aprouved_list_dmd': aprouved_list_dmd,
     'aprouved_list_cmd': aprouved_list_cmd,
     'refused_list_cmd_achat': refused_list_cmd_achat,
     'aprouved_commande': aprouved_commande,
     'waiting_aprouved_demande': waiting_aprouved_demande,
     'waiting_aprouved_commande': waiting_aprouved_commande,
     'demande_by_user': demande_by_user,
     'refused_commande': refused_commande_count,
     'msg_sortie_directe': msg_sortie_directe,
     'sortie_directe': sortie_direct,
     'sortie_directe_count': sortie_direct_count,
     'users': users,
     'pending_cmd': pending_cmd,
     'commande_pending': commande_pending,
     'new_bc_list' : new_bc_list,
     }
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.

   

        
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# Send Demande d'achat-------------------------------------------------------------  
        
@login_required(login_url="/login/")
def send_demande(request):
    my_list = List_item_on_Demande.objects.filter(user_dem = request.user.username)
    elm_count = my_list.count()
    print(elm_count)

    random_values = range(100)

    key = random.choice(random_values) # cle pour identifier chaque demande

    DimensionAchat.objects.create(user_dim = request.user.username,type_achat_dim = "Demande", identifier_dim = request.user.username+str(key))
    
    for data in my_list:
        Demande.objects.create(user_demande = data.user_dem,
        article_demande = data.article_dem,
        fournisseur_demande = data.fournisseur_dem,
        quantity_demande = data.quantity_dem,
        pu_demande = data.pu_dem,
        unity_demande = data.unity_dem,
        prix_demande = data.prix_dem,
        identifier_demande = data.user_dem+str(key))

    my_list.delete()


    return HttpResponse(""" <html><script>window.location.replace('/add_demande.html');</script> </html> """)    

# End of the function for sending Demande    

# Send Commande Achat--------------------------------------------------------------------------------------------------

          
@login_required(login_url="/login/")
def edit_commande(request):
    my_list_cmd = List_item_on_Commande.objects.filter(user_com = request.user.username)

    fournisseur = []
    
    random_values = range(1000)
    random_letters = list(map(chr, range(97, 123)))

    key_num = random.choice(random_values) # cle pour identifier chaque demande
    key_let = random.choice(random_letters) # cle pour identifier chaque demande

    
    
    for data in my_list_cmd:
        Commande.objects.create(user_commande = data.user_com,
        article_commande = data.article_com,
        ref_fourn_commande = data.ref_com,
        fournisseur_commande = data.fournisseur_com,
        quantity_commande = data.quantity_com,
        pu_commande = data.pu_com,
        unity_commande = data.unity_com,
        prix_commande = data.prix_com,
        identifier_commande = data.user_com+str(key_num)+str(key_let))

        fournisseur.append(data.fournisseur_com)

    DimensionAchat.objects.create(user_dim = request.user.username,type_achat_dim = "Commande",fournisseur_dim = fournisseur[1], identifier_dim = request.user.username+str(key_num)+str(key_let))
    
    email = EmailMessage(

        subject = f'Demande de Validation from {request.user.username}',
        body = f"Bonjour Romain, \n\n{request.user.username} vient de lancer une commande en attente d'approbation. Pour ouvrir la commande, veuillez cliquer sur ce lien: http://192.168.100.169/liste_commande.html \n\n \n Cordialement ",
        from_email = 'alerte@stgi-marine.com',
        to = ['stgi@stgi-marine.com', 'mansour@stgi-marine.com'],
        
    )
    
    email.send()
    
    fournisseur.clear()

    my_list_cmd.delete()


    return HttpResponse(""" <html><script>window.location.replace('/add_commande.html');</script> </html> """)    


# End of the function for sending Commande

# Approbation function for Demande

         
@login_required(login_url="/login/")
def approuver_dmd(request, id):
    my_dmd = DimensionAchat.objects.filter(id = id)

    dim_dmd = DimensionAchat.objects.get(id = id)

    list_fourn = []

    specific_lines_dmd = Demande.objects.filter(identifier_demande = dim_dmd.identifier_dim)
    specific_lines_dmd.update(is_approuved = 1)
    for line in specific_lines_dmd:
        if line.fournisseur_demande not in list_fourn:
            list_fourn.append(line.fournisseur_demande)
        
    

    for fourn in list_fourn:
        AprouvedAchat.objects.create(user_name = dim_dmd.user_dim, type_achat = dim_dmd.type_achat_dim, identifier = dim_dmd.identifier_dim, fournisseur = fourn)

    my_dmd.delete()

    return HttpResponse(""" <html><script>window.location.replace('/liste_demande.html');</script> </html> """)    

# End of function for the Demande Approbation

# Approbation function for Commande        
@login_required(login_url="/login/")
def approuver_cmd(request, id):
    my_cmd = DimensionAchat.objects.filter(id = id)

    dim_cmd = DimensionAchat.objects.get(id = id)

    

    specific_lines_cmd = Commande.objects.filter(numero_commande = dim_cmd.numero_dim)
    specific_lines_cmd.update(is_approuved = 1)
    
    AprouvedAchat.objects.create(user_name = dim_cmd.user_dim,
    type_achat = dim_cmd.type_achat_dim, identifier = dim_cmd.numero_dim,
    projet =  dim_cmd.projet_dim, fournisseur = dim_cmd.fournisseur_dim)


    my_cmd.delete()

    return HttpResponse(""" <html><script>window.location.replace('/liste_commande.html');</script> </html> """)    
# End of function for the Commande Approbation

# Function to refused commande
@login_required(login_url="/login/")
def refused_cmd(request, id):
    my_cmd = DimensionAchat.objects.filter(id = id)

    dim_cmd = DimensionAchat.objects.get(id = id)

    list_fourn = []

    specific_lines_cmd = Commande.objects.filter(numero_commande = dim_cmd.numero_dim)
    specific_lines_cmd.update(is_refused = 1)
    
    

   
    RefusedAchat.objects.create(user_name = dim_cmd.user_dim, type_achat = dim_cmd.type_achat_dim, numero = dim_cmd.numero_dim, fournisseur = dim_cmd.fournisseur_dim)


    my_cmd.delete()

    return HttpResponse(""" <html><script>window.location.replace('/liste_commande.html');</script> </html> """)    
# End of function for the Commande Approbation


# Grouper function for Commande        
@login_required(login_url="/login/")
def grouper_cmd(request, id):
    
    my_cmd = AprouvedAchat.objects.filter(id = id)

    dim_cmd = AprouvedAchat.objects.get(id = id)

    last_aprouved_cmd = AprouvedAchat.objects.filter(fournisseur = dim_cmd.fournisseur)
    old_keys = []
    for aprv_cmd in last_aprouved_cmd:
        old_keys.append(aprv_cmd.identifier)

    if len(old_keys) != 1:
        if old_keys[0] != old_keys[len(old_keys)-1]:
            specific_lines_cmd = Commande.objects.filter(identifier_commande = dim_cmd.identifier, fournisseur_commande = dim_cmd.fournisseur)
            specific_lines_cmd.update(identifier_commande =old_keys[0])
            my_cmd.delete()
            return HttpResponse(""" <html><script>window.location.replace('/list_commande_achat.html');</script> </html> """)
        specific_lines_cmd = Commande.objects.filter(identifier_commande = old_keys[0], fournisseur_commande = dim_cmd.fournisseur)     
        specific_lines_cmd.update(identifier_commande = old_keys[1])
        my_cmd.delete()
        return HttpResponse(""" <html><script>window.location.replace('/list_commande_achat.html');</script> </html> """)        
    return HttpResponse(""" <html><script>window.location.replace('/list_commande_achat.html');</script> </html> """)  

# End of function for the Commande Approbation



# Grouper function for Commande        
@login_required(login_url="/login/")
def annuler_cmd(request, id, identifier):
    
    my_cmd = RefusedAchat.objects.filter(id = id)

    my_line = Commande.objects.filter(identifier_commande = identifier, is_refused = 0)

    my_cmd.delete()
    my_line.delete()
        
    return HttpResponse(""" <html><script>window.location.replace('/list_commande_achat.html');</script> </html> """)  

# End of function for the Commande Approbation

# supprimer un element selectionné sur le formulaire de demande         
@login_required(login_url="/login/")
def delete_item_demande(request, id_item):
    my_item = List_item_on_Demande.objects.filter(id = id_item)

    my_item.delete()

    return HttpResponse(""" <html><script>window.location.replace('/add_demande.html');</script> </html> """)    



# supprimer un element selectionné sur le formulaire de commande         
@login_required(login_url="/login/")
def delete_item_commande(request, id_item):
    my_item = List_item_on_Commande.objects.filter(id = id_item)

    my_item.delete()

    return HttpResponse(""" <html><script>window.location.replace('/add_commande.html');</script> </html> """)


# Genration the 'Bon de Commande' in pdf version------------------------------------------------------------
def bon_de_commande(request, num_cmd, fournisseur):
    # action="/bon_de_commande/{{commande_aprv.num_cmd}}/{{commande_aprv.fournisseur}}
     #Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    save_on = os.path.join(os.path.expanduser("~"), "Downloads/")
    id_cmd = CommandeAchat.objects.get(numero_commande = num_cmd, nom_fournisseur = fournisseur)

    dls_recup = AprouvedAchat.objects.get(identifier = num_cmd)

    _startDate = dls_recup.dls.strftime('%d/%m/%Y')
   
    fournisseur_cmd = Fournisseur.objects.get(name = fournisseur)

    if fournisseur_cmd.type == "LOCAL":
        devise = "TND"
    else:
        devise = "€"
   
    # Create the PDF object, using the buffer as its "file."
    #
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFontSize(10)
    
    img = "C://inetpub/wwwroot/aventura/apps/home/cap.png"

    p.drawImage(img, 35,650, width=550,height=150,mask=None)  #LOGO STGI

    entete = BC_Fournisseur.objects.all()

    for ent in entete:
        remarque = ent.remarque

    my_list_commande = Commande.objects.filter(numero_commande = num_cmd, fournisseur_commande = fournisseur)

    tot = []
    total = []
    fourn = []

    for row in my_list_commande:
        price = row.prix_commande
        tot.append(price)
        fourn.append(row.fournisseur_commande)

    
    # Ente du Bon de Commande
    p.drawString(20, 610, "Référence Projet :"),                 p.drawString(220, 610, id_cmd.ref_projet)
    p.drawString(20, 585, "Fournisseur :"),                      p.drawString(220, 585, fournisseur)
    p.drawString(20, 560, "Date de Livraison souhaitée :"),      p.drawString(220, 560, _startDate)
    p.drawString(20, 535, "Remarque :"),                         p.drawString(220, 535, "")

   
    
    total.append(sum(tot))
    prix_total = total[0]

    length = my_list_commande.count()

    length = my_list_commande.count()

    number_of_line = 17

    if length < 17:
        number_of_line = length

    #number_of_line = my_list_commande.count()
    posi = []
    y_positions = [] #position de chaque ligne de commande

    grid = ()

    list_grid = list(grid)

    
    #number_of_line = length

    start_count = 485 - number_of_line*20

    total_position = start_count - 30

    for i in range(number_of_line+1):
        y_positions.append(start_count + i*20) # 20 represente l'ecart entre deux ligne


    

    for z in y_positions:
        list_grid.append(z-5)
                                       #(400,535,555)
    
    list_grid.append(505)

    grid = tuple(list_grid)


    # Entete du tableau
    p.drawString(18, 488, "Réf.Fourn"),
    #p.drawString(85, 488, "Réf"), 
    p.drawString(210, 488, "Désignation"), 
    p.drawString(420, 488, "Qté"), 
    p.drawString(460, 488, "U"), 
    p.drawString(490, 488, "PU"), 
    p.drawString(553, 488, "Total"),
    
    # Grille du Tableau
    p.grid((15,100,410,450,480,537,597),grid) #xList_from_left_to right   yList_from_bottom_to Top

    # Footer du PDF.
    footer = "C://inetpub/wwwroot/aventura/apps/home/footer.png"
    

   
    




    step = 0
    step2 = 0

    
    for line, y in zip(my_list_commande, y_positions): # affichage des lignes de commande
        if step < 17:
            if len(line.article_commande) >= 65:
                first = line.article_commande[0:65]
                last = line.article_commande[65:len(line.article_commande)]
                z = y - 4
                p.drawString(105, y+5, first)
                p.drawString(105, z, last)
            else:
                p.drawString(105, y, line.article_commande)
            if len(line.ref_fourn_commande) >= 12:
                    first_r = line.ref_fourn_commande[0:12]
                    last_r = line.ref_fourn_commande[12:len(line.ref_fourn_commande)]
                    z = y - 4
                    p.drawString(18, y+5, first_r)
                    p.drawString(18, z, last_r)    
            else:    
                p.drawString(18,y, line.ref_fourn_commande)       
            p.drawString(415, y, str(line.quantity_commande))
            p.drawString(460, y, line.unity_commande)
            p.drawString(485, y, str(round(line.pu_commande, 3)))
            p.drawString(540, y, str(round(line.prix_commande, 3)))
            step = step + 1

    # Total et image Footer en cas d'une seule page
    if length < 17:
        p.drawString(470, total_position, "TOTAL: ")
        p.drawString(520, total_position, str(round(prix_total,2))+' '+ devise)       
        p.drawImage(footer, 8,15, width=600,height=120,mask=None)  #FOOTER STGI          
    # End de Total et image Footer en cas d'une seule page
    
    p.setFontSize(25)
    p.drawString(450, 610, "N° "+ num_cmd)
    

    if length > 17:


        p.showPage()

        p.drawImage(img, 35,650, width=550,height=150,mask=None)  #LOGO STGI

        number_of_line = length - 17

        start_count2 = 585 - number_of_line*20

        total_position = start_count2 - 30

        

        for i in range(number_of_line+1):
            posi.append(start_count2 + i*20) # 20 represente l'ecart entre deux ligne


        
        second_list = []
        for z in posi:
            second_list.append(z-5)
                                        #(400,535,555)
        
        second_list.append(605)
        

        grid = tuple(second_list)


        # Entete du tableau
        p.drawString(18, 588, "Réf.Fourn"), 
        p.drawString(210, 588, "Désignation"), 
        p.drawString(420, 588, "Qté"), 
        p.drawString(460, 588, "U"), 
        p.drawString(490, 588, "PU"), 
        p.drawString(553, 588, "Total"),
        
        # Grille du Tableau
        p.grid((15,100,410,450,480,537,597),grid) #xList_from_left_to right   yList_from_bottom_to Top



        for line, y in zip(my_list_commande[17:100], posi): # affichage des lignes de commande
                if len(line.article_commande) >= 50:
                    first = line.article_commande[0:50]
                    last = line.article_commande[50:len(line.article_commande)]
                    z = y - 4
                    p.drawString(105, y+5, first)
                    p.drawString(105, z, last)
                else:
                    p.drawString(105, y, line.article_commande)
                if len(line.ref_fourn_commande) >= 12:
                    first_r = line.ref_fourn_commande[0:12]
                    last_r = line.ref_fourn_commande[12:len(line.ref_fourn_commande)]
                    z = y - 4
                    p.drawString(18, y+5, first_r)
                    p.drawString(18, z, last_r)    
                else:    
                    p.drawString(18,y, line.ref_fourn_commande)    
                p.drawString(415, y, str(line.quantity_commande))
                p.drawString(460, y, line.unity_commande)
                p.drawString(485, y, str(round(line.pu_commande,2)))
                p.drawString(540, y, str(round(line.prix_commande,2)))
        
        
                
        
        p.drawString(470, total_position, "TOTAL: ")
        p.drawString(520, total_position, str(round(prix_total,2))+' '+ devise)

        #p.drawString(500, 610, "N° ")
        


        # Close the PDF object cleanly, and we're done.
        
        

        
        
        
        p.drawImage(footer, 8,15, width=600,height=120,mask=None)  #FOOTER STGI    
    
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)

    #push = CommandeAchat.objects.create(nom_fournisseur = fournisseur, numero_commande = num_cmd )


    return FileResponse(buffer, as_attachment=False, filename='BC_'+fournisseur+"_"+num_cmd+'.pdf' ) 

    # supprimer un element selectionné sur le formulaire de commande     
    # 
    # 
@login_required(login_url="/login/")
def envoyer_commande(request,identifier, fournisseur, ref):

    my_dls_recup = AprouvedAchat.objects.get(identifier = identifier)
    fourn = Fournisseur.objects.get(name = fournisseur)

    my_cmd = CommandeAchat.objects.create(nom_fournisseur = fournisseur, numero_commande = identifier,
    ref_projet = ref, date_souhaitee = my_dls_recup.dls,
    email_fournisseur = fourn.email)


    recup_aprv_cmd = AprouvedAchat.objects.filter(fournisseur = fournisseur, identifier = identifier)

    recup_aprv_cmd.update(is_ready = 1)

   
    return HttpResponse(""" <html><script>window.location.replace('/send_commande.html');</script> </html> """)  

@login_required(login_url="/login/")
def envoyer_commande_from_demande(request,identifier, fournisseur):

    my_cmd = CommandeAchat.objects.create(nom_fournisseur = fournisseur)

    recup_cmd = CommandeAchat.objects.filter(nom_fournisseur = fournisseur, numero_commande = "")

    recup_id = CommandeAchat.objects.get(nom_fournisseur = fournisseur, numero_commande = "")

    new_cmd = recup_cmd.update(numero_commande = str(3000 + recup_id.id))

    commande = Commande.objects.create(fournisseur_commande = fournisseur, identifier_commande = identifier, numero_commande = str(3000 + recup_id.id) )

   
    return HttpResponse(""" <html><script>window.location.replace('/send_commande.html');</script> </html> """)  

@login_required(login_url="/login/")
def mailing_commande(request, fournisseur, numero_commande):

    recup_fourniseur = Fournisseur.objects.get(name = fournisseur)

    

    recup_cmd = CommandeAchat.objects.filter(nom_fournisseur = fournisseur, numero_commande = numero_commande)

    mail_cmd = recup_cmd.update(is_sent = 1)

    email = EmailMessage(
        subject = f'Bon de commande N° {numero_commande}',
        body = f"Bonjour, \n\nVeuillez trouver ci-joint notre nouvelle commande N° {numero_commande}, \n\nVeuillez metttre en copie l'adresse mail suivante pour la gestion des commandes: gestioncommande@stgi-marine.com \n\nMerci d'accuser réception de ce mail et nous faire parvenir la confirmation de commande avec le délai de livraison. \n\n \n Cordialement ",
        from_email = request.user.email,
        to = [recup_fourniseur.email, 'mansour@stgi-marine.com', 'stgi@stgi-marine', 'supplychain@stgi-marine.com','gestioncommande@stgi-marine.com'],
        
    )
    email.attach_file(f'C:/DATA/BC_AVENTURA/BC_{fournisseur}_{numero_commande}.pdf')
    email.send()


   
    return HttpResponse(""" <html><script>window.location.replace('/commande_envoyees.html');</script> </html> """)       

@login_required(login_url="/login/")
def confirm_commande_etranger(request, num_cmd, nom_fourn):

    my_cmd = CommandeAchat.objects.filter(nom_fournisseur = nom_fourn, numero_commande = num_cmd)

    my_cmd.update(is_confirmed = 1)

    my_cmd_oncommande = Commande.objects.filter(fournisseur_commande = nom_fourn, numero_commande = num_cmd, is_confirmed = "OUI")

    my_cmd_oncommande.update(is_ready = 1)

    suivi_commande = SuiviCommande.objects.create(nom_fournisseur = nom_fourn,
     numero_commande = str(num_cmd),
     suivi_position = "CHEZ LE FOURNISSEUR",
     )

    return HttpResponse(""" <html><script>window.location.replace('/commande_envoyees.html');</script> </html> """)

@login_required(login_url="/login/")
def confirm_commande_local(request, num_cmd, nom_fourn):

    my_cmd = CommandeAchat.objects.filter(nom_fournisseur = nom_fourn, numero_commande = num_cmd)

    my_cmd.update(is_confirmed = 1)

    my_cmd_oncommande = Commande.objects.filter(fournisseur_commande = nom_fourn, numero_commande = num_cmd, is_confirmed = "OUI")

    my_cmd_oncommande.update(is_ready = 1)

    suivi_commande = SuiviCommande.objects.create(nom_fournisseur = nom_fourn,
     numero_commande = str(num_cmd),
     suivi_position = "EN ATTENTE DE LIVRAISON",
     )

    return HttpResponse(""" <html><script>window.location.replace('/commande_envoyees.html');</script> </html> """)


@login_required(login_url="/login/")
def confirm_all_line(request, num_cmd, nom_fourn):

    my_cmd_oncommande = Commande.objects.filter(fournisseur_commande = nom_fourn, numero_commande = num_cmd)

    my_cmd_oncommande.update(is_confirmed = "OUI")

    return HttpResponse(""" <html><script>window.location.replace('/commande_envoyees.html');</script> </html> """)    

@login_required(login_url="/login/")
def unconfirm_all_line(request, num_cmd, nom_fourn):

    my_cmd_oncommande = Commande.objects.filter(fournisseur_commande = nom_fourn, numero_commande = num_cmd)

    my_cmd_oncommande.update(is_confirmed = "NON")
        

    return HttpResponse(""" <html><script>window.location.replace('/commande_envoyees.html');</script> </html> """)    


@login_required(login_url="/login/")
def confirm_commande_line(request,id):

    my_cmd_oncommande = Commande.objects.filter(id = id)

    my_cmd_oncommande.update(is_confirmed = "OUI")

    return HttpResponse(""" <html><script>window.location.replace('/commande_envoyees.html');</script> </html> """)

def unconfirm_commande_line(request,id):
    
    my_cmd_oncommande = Commande.objects.filter(id = id)

    my_cmd_oncommande.update(is_confirmed = "NON")

    return HttpResponse(""" <html><script>window.location.replace('/commande_envoyees.html');</script> </html> """)    


# functions for the 'suivi de commande'-----------------------------------------------------------------------------------------------------------

@login_required(login_url="/login/")
def commande_livrer(request, num_cmd):

    my_cmd = SuiviCommande.objects.filter( numero_commande = num_cmd)

    my_cmd.update(suivi_position = "DEPART FOURNISSEUR", move = 1000)

    


    return HttpResponse(""" <html><script>window.location.replace('/suivi.html');</script> </html> """)

@login_required(login_url="/login/")
def commande_chez_gts(request, num_cmd):

    pos_gts = SuiviCommande.objects.filter( numero_commande = num_cmd)

    pos_gts.update(suivi_position = "ARRIVEE CHEZ GTS")

    return redirect("suivi")
    #return HttpResponse(""" <html><script>window.location.replace('/suivi.html');</script> </html> """)

@login_required(login_url="/login/")
def commande_en_transit(request, num_cmd):

    my_cmd = SuiviCommande.objects.filter( numero_commande = num_cmd)

    my_cmd.update(suivi_position = "EN TRANSIT")


    return HttpResponse(""" <html><script>window.location.replace('/suivi.html');</script> </html> """)

@login_required(login_url="/login/")
def commande_receptionnee(request, num_cmd):

    my_cmd = SuiviCommande.objects.filter( numero_commande = num_cmd)

    my_cmd.update(suivi_position = "RECEPTIONNEE")


    return HttpResponse(""" <html><script>window.location.replace('/suivi.html');</script> </html> """)

# Etat commande///////////////////////////////////////////

@login_required(login_url="/login/")
def commande_normal(request, num_cmd):

    my_cmd = SuiviCommande.objects.filter( numero_commande = num_cmd)

    my_cmd.update(etat_commande = "NORMAL")


    return HttpResponse(""" <html><script>window.location.replace('/suivi.html');</script> </html> """)  

@login_required(login_url="/login/")
def commande_manquant(request, num_cmd):

    my_cmd = SuiviCommande.objects.filter( numero_commande = num_cmd)

    my_cmd.update(etat_commande = "MANQUANT")


    return HttpResponse(""" <html><script>window.location.replace('/suivi.html');</script> </html> """)      

@login_required(login_url="/login/")
def commande_endomager(request, num_cmd):

    my_cmd = SuiviCommande.objects.filter( numero_commande = num_cmd)

    my_cmd.update(etat_commande = "ENDOMAGER")


    return HttpResponse(""" <html><script>window.location.replace('/suivi.html');</script> </html> """)

@login_required(login_url="/login/")
def planified_transport(request, num_cmd):

    my_cmd = CommandeAchat.objects.filter( numero_commande = num_cmd)

    my_cmd.update(is_planified = 1)


    return HttpResponse(""" <html><script>window.location.replace('/transport_non_planifies.html');</script> </html> """)


@login_required(login_url="/login/")
def refused_commande_line(request, id):

    my_cmd = Commande.objects.filter( id = id)

    

    if request.method == 'POST':
        if 'motif_refus' in request.POST:
            motif = request.POST['motif_refus_txt']


            my_cmd.update(is_refused = 1, motif_commande = motif)       

        RefusedAchat.objects.create(user_name = my_cmd.user_commande,
        type_achat = "Commande", numero = my_cmd.numero_commande, 
        fournisseur = my_cmd.fournisseur_commande,
        identifier = my_cmd.projet)

    return HttpResponse(""" <html><script>window.location.replace('/liste_commande.html');</script> </html> """)


@login_required(login_url="/login/")
def update_qty(request):
    id = request.POST.get('id','')
    value = request.POST.get('value','')
    type = request.POST.get('type','')

    com_line = Commande.objects.filter(id = id)

    com_line.update(quantity_commande = value)

    

    return JsonResponse({"success":"updated"})

@login_required(login_url="/login/")
def new_bc(request):

    com = Bc.objects.all()

    list_id = []

    for row in com:
        list_id.append(row.id)

    

    id = list_id[len(list_id)-1]

    num_bcom = 5000 + id + 1

    if request.method == 'POST':
        if 'open_bc' in request.POST:
            fourn = request.POST['fourn_bc']
            ref = request.POST['ref_bc']
            dls = request.POST['dls_bc']
            if ref == "":
                ref = "Réf:"
               
            my_new_bc = Bc(fournisseur_bc = fourn, ref_bc = ref, dls_bc = dls, num_bc = num_bcom)

            my_new_bc.save()
     
    return HttpResponse(""" <html><script>window.location.replace('/new_commande.html');</script> </html> """)


@login_required(login_url="/login/")
def new_line_bc(request, num_bc, project, fourn):

    if request.method == 'POST':
        if 'line_bc' in request.POST:
            article = request.POST['article_line_bc']
            ref = request.POST['ref_line_bc']
            qty = request.POST['qty_line_bc']
            unity = request.POST['unity_line_bc']
            pu = request.POST['pu_line_bc']

            my_new_bc_line = Commande(user_commande = request.user.username,
                projet = project,
                numero_commande = num_bc,
                article_commande = article,
                ref_fourn_commande = ref,
                fournisseur_commande = fourn,
                quantity_commande = qty,
                pu_commande = pu,
                unity_commande = unity,
                prix_commande = float(pu)*float(qty),
                identifier_commande = "NEW")

            my_new_bc_line.save()
     
    return HttpResponse(""" <html><script>window.location.replace('/new_commande.html');</script> </html> """)
  
@login_required(login_url="/login/")
def cancel_bc(request, bc):

    com = Bc.objects.filter(num_bc = bc)

    com_line = Commande.objects.filter(numero_commande = bc)

    com.delete()
    com_line.delete()

    return HttpResponse(""" <html><script>window.location.replace('/new_commande.html');</script> </html> """)
  
@login_required(login_url="/login/")
def new_commande_validation(request, id):
   
    recup = Bc.objects.get(id = id)
   
    DimensionAchat.objects.create(user_dim = request.user.username,type_achat_dim = "Commande",
    fournisseur_dim = recup.fournisseur_bc, projet_dim = recup.ref_bc, dls_dim = recup.dls_bc,
    numero_dim = recup.num_bc)
    
    email = EmailMessage(

        subject = f'Demande de Validation from {request.user.username}',
        body = f"Bonjour Romain, \n\n{request.user.username} vient de lancer une commande en attente d'approbation. Pour ouvrir la commande, veuillez cliquer sur ce lien: http://192.168.100.169/liste_commande.html \n\n \n Cordialement ",
        from_email = 'alerte@stgi-marine.com',
        to = ['mansour@stgi-marine.com', 'stgi@stgi-marine.com'],
        
    )
    
    email.send()

    validation = Bc.objects.filter(id = id)

    validation.update(is_send_approval = 1)
    


    return HttpResponse(""" <html><script>window.location.replace('/new_commande.html');</script> </html> """)    
    
@login_required(login_url="/login/")
def new_commande_update(request, id):
   
    recup = Bc.objects.filter(id = id)
    num = Bc.objects.get(id = id)

    line_cmd = Commande.objects.filter(numero_commande = num.num_bc)

    if request.method == 'POST':
        if 'update_bc' in request.POST:
            fourn = request.POST['update_fourn_bc']
            ref = request.POST['update_ref_bc']
            dls = request.POST['update_dls_bc']

            if ref == "":
                ref = "Réf:"
          
            recup.update(fournisseur_bc = fourn, ref_bc = ref, dls_bc = dls)
            line_cmd.update(fournisseur_commande = fourn)
            
     
    return HttpResponse(""" <html><script>window.location.replace('/new_commande.html');</script> </html> """)


@login_required(login_url="/login/")
def rappeler_cmd(request, id):

    cmd_dim = DimensionAchat.objects.get(id = id)

    cmd = Bc.objects.filter(num_bc = cmd_dim.numero_dim)

    cmd.update(is_recalled = 1, is_send_approval = 0)
    cmd_dim_del = DimensionAchat.objects.filter(id = id)
    cmd_dim_del.delete()

    return HttpResponse(""" <html><script>window.location.replace('/new_commande.html');</script> </html> """)

@csrf_exempt
def update_qty(request):
    id = request.POST.get('id', '')
    value = request.POST.get('value', '')
    cmd_line = Commande.objects.filter(id = id)

    get_pu = Commande.objects.get(id = id)

    pu = get_pu.pu_commande
 
    cmd_line.update(quantity_commande = value, prix_commande = round(float(value)*pu, 3))
            
     
    return JsonResponse({"success":"updated"})



@csrf_exempt
def update_line(request):
    id = request.POST.get('id', '')
    type = request.POST.get('type', '')
    value = request.POST.get('value', '')
    

    cmd_line = Commande.objects.filter(id = id)

   

    if type == "article":
        cmd_line.update(article_commande = value)
    if type == "ref":
        cmd_line.update(ref_fourn_commande = value)    
    if type == "quantity":
        get_pu = Commande.objects.get(id = id)
        pu = get_pu.pu_commande
        cmd_line.update(quantity_commande = value) 
        cmd_line.update(prix_commande = round(float(value)*pu, 3))
    if type == "unity":
        cmd_line.update(unity_commande = value)
    if type == "pu":
        get_qty = Commande.objects.get(id = id)
        qty = get_qty.quantity_commande
        cmd_line.update(pu_commande = value)
        cmd_line.update(prix_commande = round(float(value)*qty, 3))             
     
    return JsonResponse({"success":"updated"})
