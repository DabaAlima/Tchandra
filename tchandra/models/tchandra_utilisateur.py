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
# from workalendar.europe import France
# cal = France()

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

TYPE_PERSONNE=[
    ('Tchandra','Tchandra'),
    ('Relais communautaire','Relais Communautaire'),
    ('Personnel de sante','Personnel de santé'),
    ('Femme enceinte','Femme enceinte'),
]

NIVEAU_INSTRUCTION = [
    ('non_scolarise','Non scolarisé'),
    ('primaire','Primaire'),
    ('college','Collége'),
    ('lycee','Lycée'),
    ('universite','Université'),
    ('formation_professionnelle','Formation Professionnelle'),
    ('ecole_coranique','Ecole Coranique'),
    ('autre','Autre'),
]

VILLAGE_RESIDENCE = [
    ('watta','Watta'),
    ('kouri','Kouri'),
    ('wouni','Wouni'),
    ('deila_zone_1','Deila (zone 1)'),
    ('adringa_zone_1','Adringa (zone 1)'),
    ('fitra','Fitra'),
    ('aringa','Aringa'),
    ('rorom','Rorom')
]

CENTRE_SANTE_RATTACHEMENT = [
    ('centre_sante_watta','Centre de santé de Watta'),
    ('centre_sante_dibinintchi','Centre de santé de Dibinintchi'),
]

PROFESSION = [
    ('sage_femme','Sage-femme'),
    ('infirmier','Infirmier'),
    ('medecin','Médecin'),
    ('autre','Autre')
]


class Utilisateur(models.Model):
    """
    Class Utilisateur de TCHANDRA.
    """
    _name = 'tchandra.utilisateur'
    _inherit = ['mail.thread']
    _description = 'Utilisateur TCHANDRA'
    
    #liste des champs de la classe
    #title = fields.Selection(TITLE, string='Civilité')
    name = fields.Char(String="Code", compute='compute_name', store=True)
    lastname = fields.Char(String="Nom")
    firstname =fields.Char(String="Prénom")
    age =fields.Integer(string='Age')
    type_de_personne=fields.Selection(TYPE_PERSONNE, string="Type d'utilisateur")
    village_residence=fields.Selection(VILLAGE_RESIDENCE, string="Village de résidence")
    niveau_instruction=fields.Selection(NIVEAU_INSTRUCTION, string="Niveau d'instruction")
    centre_sante=fields.Selection(CENTRE_SANTE_RATTACHEMENT, string="Centre de santé de rattachement")
    profession=fields.Selection(PROFESSION, string="Profession")
    dateEnregistrement=fields.Datetime(string="Date d'enregistrement", compute='_compute_date_creation')
    fingerprint =fields.Integer(string='Empreinte digitale')
    tchandra=fields.Boolean(string="Tchandra", compute='_is_tchandra')
    relais_communautaire=fields.Boolean(string="Relais communautaire", compute='_is_relais_communautaire')
    personnel_sante=fields.Boolean(string="Personnel de santé", compute='_is_personnel_sante')
    femme_enceinte=fields.Boolean(string="Femme enceinte", compute='_is_femme_enceinte')
    mobile = fields.Char(string='Portable 1')
    mobile2 = fields.Char(string='Portable 2')
    phone = fields.Char(string='Téléphone professionnel')
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
        res= super(Utilisateur, self).create(vals)

        if 'id' in vals and res.id != vals['id']:
            res = res.incremente_id(vals['id'])
        res = res[0] if type(res) == list else res

        if not res.name:
            if res.firstname:
                res.name = res.lastname.replace(' ','')+""+res.firstname.replace(' ','')
            else:
                res.name= res.lastname.replace(' ','')
            res.name = res.name.lower()
        return res
        #creation
    @api.depends('firstname','lastname')
    def compute_name(self):
        for res in self:
            if res.firstname:
                res.name = res.lastname.replace(' ','')+""+res.firstname.replace(' ','')
            else:
                res.name= res.lastname.replace(' ','')
            res.name = res.name.lower()
    @api.depends('create_date')
    def _compute_date_creation(self):
        for res in self:
            if res.create_date:
                res.dateEnregistrement = res.create_date
    @api.depends('type_de_personne')
    def _is_tchandra(self):
        for res in self:
            res.tchandra = False
            if res.type_de_personne == 'Tchandra':
                res.tchandra = True
    @api.depends('type_de_personne')
    def _is_relais_communautaire(self):
        for res in self:
            res.relais_communautaire = False
            if res.type_de_personne == 'Relais communautaire':
                res.relais_communautaire = True
    @api.depends('type_de_personne')
    def _is_personnel_sante(self):
        print self
        for res in self:
            res.personnel_sante = False
            if res.type_de_personne == 'Personnel de sante':
                res.personnel_sante = True
    @api.depends('type_de_personne')
    def _is_femme_enceinte(self):
        for res in self:
            res.femme_enceinte = False
            if res.type_de_personne == 'Femme enceinte':
                res.femme_enceinte = True