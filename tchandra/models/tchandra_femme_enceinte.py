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
# SEXE=[
#     ('M', 'M'),
#     ('F', 'F'),
#     ('C mixte', 'C mixte'),
#     ('C M', 'C M'),
#     ('C F', 'C F'),
#     ('X indetermine', 'X indéterminé')
#     ]

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


class FemmeEnceinte(models.Model):
    """
    Class Femme enceinte de TCHANDRA.
    """
    _name = 'tchandra.femme.enceinte'
    _description = 'Femme enceinte dans TCHANDRA'
    
    #liste des champs de la classe
    age =fields.Integer(string='Age')
    gestite =fields.Integer(string='Gestité')
    parite =fields.Integer(string='Parité')
    village_residence=fields.Selection(VILLAGE_RESIDENCE, string="Village de résidence")
    niveau_instruction=fields.Selection(NIVEAU_INSTRUCTION, string="Niveau d'instruction")
    dateEnregistrement=fields.Datetime(string="Date d'enregistrement", compute='_compute_date_creation')
    fingerprint =fields.Integer(string='Empreinte digitale')
    # enregistree_par = fields.Char(String="Enregistrée par")
    # has_given_birth = fields.Boolean(String="A accouché")
    # date_activite_accouchement=fields.Datetime(string="Date d'identification de l'activité d'accouchement")
    # date_accouchement=fields.Date(string="Date accouchement")
    grossesse = fields.One2many('tchandra.grossesse', 'femme_enceinte_grossesse', string="Grossesses")
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
        res= super(FemmeEnceinte, self).create(vals)

        if 'id' in vals and res.id != vals['id']:
            res = res.incremente_id(vals['id'])
        res = res[0] if type(res) == list else res
        return res
        #creation
    @api.depends('create_date')
    def _compute_date_creation(self):
        for res in self:
            if res.create_date:
                res.dateEnregistrement = res.create_date