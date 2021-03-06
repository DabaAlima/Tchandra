# -*- coding: utf-8 -*-
from odoo import models, _,fields, api, exceptions
from odoo.exceptions import UserError, ValidationError
from datetime import date
from odoo import tools
from datetime import datetime
import logging
import threading
from array import *

from dateutil import relativedelta

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

VACCINS = [
    ('1','Ne sait pas'),
    ('2','Non'),
    ('3','Oui')
]

STATUT_VITAL_FEMME = [
    ('vivante','Vivante'),
    ('decedee','Décédée')
]

STATUT_VITAL_ENFANT = [
    ('vivant','Vivant'),
    ('decede','Décédé')
]

class Suivi(models.Model):
    """
    Class Suivi M1 de TCHANDRA.
    """
    _name = 'tchandra.suivi'
    _description = 'Suivi un mois apres accouchement dans TCHANDRA'
    
    #liste des champs de la classe
    date_creation=fields.Datetime(string="Date de création du formulaire", compute='_compute_date_creation')
    date_derniere_modification=fields.Datetime(string="Date de dernière modification", compute='_compute_date_modification')
    statut_vital_femme=fields.Selection(STATUT_VITAL_FEMME, string="Statut vital de la femme")
    date_deces=fields.Date(string="Date du décès")
    statut_vital_enfant=fields.Selection(STATUT_VITAL_ENFANT, string="Statut vital de l'enfant")
    date_deces_enfant=fields.Date(string="Date du décès de l'enfant")
    poids_enfant=fields.Char(string="Poids de l'enfant")
    poids_non_realise=fields.Boolean(string="Mesure non réalisée")
    taille_enfant=fields.Char(string="Taille de l'enfant")
    taille_non_realise=fields.Boolean(string="Mesure non réalisée")
    perimetre_cranien=fields.Char(string="Périmètre crânien")
    perimetre_cranien_non_realise=fields.Boolean(string="Mesure non réalisée")
    bcg=fields.Selection(VACCINS, string="BCG")
    polio=fields.Selection(VACCINS, string="Polio 0")
    hepatite_b=fields.Selection(VACCINS, string="Hépatite B")
    statut_vital_enfant_deux=fields.Selection(STATUT_VITAL_ENFANT, string="Statut vital du deuxième enfant")
    date_deces_enfant_deux=fields.Date(string="Date du décès du deuxième enfant")
    poids_enfant_deux=fields.Char(string="Poids du deuxième enfant")
    poids_non_realise_deux=fields.Boolean(string="Mesure non réalisée")
    taille_enfant_deux=fields.Char(string="Taille du deuxième enfant")
    taille_non_realise_deux=fields.Boolean(string="Mesure non réalisée")
    perimetre_cranien_deux=fields.Char(string="Périmètre crânien du deuxième enfant")
    perimetre_cranien_non_realise_deux=fields.Boolean(string="Mesure non réalisée")
    bcg_deux=fields.Selection(VACCINS, string="BCG")
    polio_deux=fields.Selection(VACCINS, string="Polio 0")
    hepatite_b_deux=fields.Selection(VACCINS, string="Hépatite B")
    statut_vital_enfant_trois=fields.Selection(STATUT_VITAL_ENFANT, string="Statut vital du troisième enfant")
    date_deces_enfant_trois=fields.Date(string="Date du décès du troisème enfant")
    poids_enfant_trois=fields.Char(string="Poids du troisième enfant")
    poids_non_realise_trois=fields.Boolean(string="Mesure non réalisée")
    taille_enfant_trois=fields.Char(string="Taille du troisième enfant")
    taille_non_realise_trois=fields.Boolean(string="Mesure non réalisée")
    perimetre_cranien_trois=fields.Char(string="Périmètre crânien du troisième enfant")
    perimetre_cranien_non_realise_trois=fields.Boolean(string="Mesure non réalisée")
    bcg_trois=fields.Selection(VACCINS, string="BCG")
    polio_trois=fields.Selection(VACCINS, string="Polio 0")
    hepatite_b_trois=fields.Selection(VACCINS, string="Hépatite B")
    statut_vital_enfant_quatre=fields.Selection(STATUT_VITAL_ENFANT, string="Statut vital du quatrième enfant")
    date_deces_enfant_quatre=fields.Date(string="Date du décès du quatrième enfant")
    poids_enfant_quatre=fields.Char(string="Poids du quatrième enfant")
    poids_non_realise_quatre=fields.Boolean(string="Mesure non réalisée")
    taille_enfant_quatre=fields.Char(string="Taille du quatrième enfant")
    taille_non_realise_quatre=fields.Boolean(string="Mesure non réalisée")
    perimetre_cranien_quatre=fields.Char(string="Périmètre crânien du quatrième enfant")
    perimetre_cranien_non_realise_quatre=fields.Boolean(string="Mesure non réalisée")
    bcg_quatre=fields.Selection(VACCINS, string="BCG")
    polio_quatre=fields.Selection(VACCINS, string="Polio 0")
    hepatite_b_quatre=fields.Selection(VACCINS, string="Hépatite B")
    grossesse = fields.One2many('tchandra.grossesse', 'suivi', string='Femmes enceintes')
    @api.one
    def incremente_id(self, vals_id):
        res = self

        while res.id != vals_id:
            copy = res.copy()
            res.unlink()
            res = copy[0]
        
        return res
    
    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        res= super(Suivi, self).create(vals)

        if 'id' in vals and res.id != vals['id']:
            res = res.incremente_id(vals['id'])
        res = res[0] if type(res) == list else res
        return res
        #creation
    @api.depends('create_date')
    def _compute_date_creation(self):
        for res in self:
            if res.create_date:
                res.date_creation = res.create_date
    @api.depends('write_date')
    def _compute_date_modification(self):
        for res in self:
            if res.write_date:
                res.date_derniere_modification = res.write_date