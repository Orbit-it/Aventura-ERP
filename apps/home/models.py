# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from pyexpat import model
from tkinter import CASCADE
from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField
from traitlets import default

# Create your models here.

class Fournisseur(models.Model):
    name = models.CharField(max_length=64)
    adress = models.CharField(max_length=64)
    contact = models.CharField(max_length=64)
    tel = models.CharField(max_length=20)
    email = models.EmailField()
    type = models.CharField(max_length=10)


class Projet(models.Model):
    name = models.CharField(max_length=64)
    

class Article(models.Model):
    ref_intern = models.CharField(max_length=10)
    ref_fourn = models.CharField(max_length=10)
    designation = models.CharField(max_length=64)
    founisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, default="0")
    pu = models.FloatField()
    unite = models.CharField(max_length=10, default="P")
    stock_magasin = models.FloatField(default=0)
    stock_en_commande = models.FloatField(default=0)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, default="0")

class List_item_on_Demande(models.Model):
    user_dem = models.CharField(max_length=64)
    article_dem = models.CharField(max_length=30)
    fournisseur_dem = models.CharField(max_length=64)
    quantity_dem = models.FloatField()
    unity_dem = models.CharField(max_length=10, default="PIECE")
    pu_dem = models.FloatField()
    prix_dem = models.FloatField(default=0)

   
class Demande(models.Model):
    identifier_demande = models.CharField(max_length=64, default="")
    user_demande = models.CharField(max_length=64, default="")
    article_demande = models.CharField(max_length=64, default="")
    fournisseur_demande = models.CharField(max_length=64, default="")
    quantity_demande = models.IntegerField(default=0)
    pu_demande = models.FloatField(default=0)
    is_approuved = models.BooleanField(default=0)
    unity_demande = models.CharField(max_length=10, default="PIECE")
    prix_demande = models.FloatField(default=0)
    etat_demande = models.CharField(max_length=64, default="")
    date = models.DateTimeField(auto_now_add=True)

    def __srt__(self):
        return str(self.pk)

class DimensionAchat(models.Model):
    identifier_dim = models.CharField(max_length=64, default="")
    user_dim = models.CharField(max_length=64)
    fournisseur_dim = models.CharField(max_length=64, default="")
    projet_dim = models.CharField(max_length=64, default="")
    type_achat_dim = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True)
    dls_dim = models.DateTimeField(default="2022-12-12")
    numero_dim = models.CharField(default="", max_length=64)

class AprouvedAchat(models.Model):
    user_name = models.CharField(max_length=64)
    type_achat = models.CharField(max_length=64)
    identifier= models.CharField(max_length=64, default="")
    fournisseur = models.CharField(max_length=64, default="")
    projet = models.CharField(max_length=64, default="")
    date = models.DateTimeField(auto_now=True)
    dls = models.DateTimeField(auto_now=True)
    is_ready = models.BooleanField(default=0)


class RefusedAchat(models.Model):
    user_name = models.CharField(max_length=64)
    type_achat = models.CharField(max_length=64)
    numero = models.CharField(max_length=64, default="")
    identifier= models.CharField(max_length=64, default="")
    fournisseur = models.CharField(max_length=64, default="")
    date = models.DateTimeField(auto_now=True)



class Permission(models.Model):
    user_permission = models.CharField(max_length=64, default="")
    admin_permission = models.BooleanField(default=False)
    achat_permission = models.BooleanField(default=False)
    magasin_permission = models.BooleanField(default=False)
    production_permission = models.BooleanField(default=False)
    maintenance_permission = models.BooleanField(default=False)



class List_item_on_Commande(models.Model):
    user_com = models.CharField(max_length=64, default="")
    article_com = models.CharField(max_length=64, default="")
    ref_com = models.CharField(max_length=64, default="")
    fournisseur_com = models.CharField(max_length=64, default="")
    quantity_com = models.FloatField(default=0)
    unity_com = models.CharField(max_length=10, default="P")
    pu_com = models.FloatField(default=0)
    prix_com = models.FloatField(default=0)      

class Commande(models.Model):
    identifier_commande = models.CharField(max_length=64, default="")
    user_commande = models.CharField(max_length=64, default="")
    article_commande = models.CharField(max_length=30, default="")
    fournisseur_commande = models.CharField(max_length=64, default="")
    ref_fourn_commande = models.CharField(max_length=64, default="")
    projet = models.CharField(max_length=64, default="")
    quantity_commande = models.FloatField(default=0)
    quantity_receptionnee = models.FloatField(default=0)
    quantity_restante = models.FloatField(default=0)
    pu_commande = models.FloatField(default=0)
    unity_commande = models.CharField(max_length=10, default="PIECE")
    prix_commande = models.FloatField(default=0)
    motif_commande = models.CharField(max_length=300, default="")
    date = models.DateTimeField(auto_now_add=True)
    is_approuved = models.BooleanField(default=0)
    is_refused = models.BooleanField(default=0)
    is_confirmed = models.CharField(max_length=10, default="NON")
    numero_commande = models.CharField(max_length=64, default="")
    is_ready = models.BooleanField(default=0)   # commande prete pour suivi

    def __srt__(self):
        return str(self.pk)   

class CommandeAchat(models.Model):
    nom_fournisseur = models.CharField(max_length=64, default="")
    email_fournisseur = models.CharField(max_length=64, default="")
    numero_commande = models.CharField(max_length=64, default="")
    ref_projet = models.CharField(max_length=300, default="")
    date_souhaitee = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=0)
    is_sent = models.BooleanField(default=0)
    type = models.CharField(max_length=64, default="LOCAL")
    is_planified = models.BooleanField(default=0)
    date_env = models.DateTimeField(auto_now_add=True)


  
# chatting class model
# 
class Message(models.Model):
    user_from = models.CharField(max_length=64)
    user_to = models.CharField(max_length=64)
    content = models.CharField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)        

# Bon de commande par fournisseur
class BC_Fournisseur(models.Model):
    remarque = models.CharField(max_length=300, default="")
    prix_total = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)


# Suivi des commandes

class SuiviCommande(models.Model):
    nom_fournisseur = models.CharField(max_length=64, default="")
    numero_commande = models.CharField(max_length=64, default="")
    suivi_position = models.CharField(max_length=64, default="") 
    numero_facture= models.CharField(max_length=64, default="")
    etat_paiement = models.CharField(max_length=64, default="")
    etat_commande = models.CharField(max_length=64, default="")
    date_position = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)
    

# Suivi des commandes

class Sortiedirecte(models.Model):
    user_name = models.CharField(max_length=64, default="")
    designation = models.CharField(max_length=64, default="")
    quantity = models.FloatField(default=0)
    unity = models.CharField(max_length=64, default="P")
    motif= models.CharField(max_length=300, default="")
    operateur= models.CharField(max_length=64, default="")
    date = models.DateTimeField(auto_now_add=True)

class Operateur(models.Model):
    matricule = models.IntegerField(default=0)
    user_name = models.CharField(max_length=64, default="")
    site = models.CharField(max_length=64, default="Composite")
    fonction = models.CharField(max_length=64, default="")

class Bc(models.Model):
    ref_bc = models.CharField(default="TOUS PROJETS", max_length=64)
    dls_bc = models.DateTimeField(auto_now_add=False)
    fournisseur_bc = models.CharField(default="", max_length=64)
    num_bc = models.CharField(default="", max_length=64)   
    date = models.DateTimeField(auto_now_add=True)
    is_recalled = models.BooleanField(default=0) 
    is_send_approval = models.BooleanField(default=0)   
    
    
