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

MOTIF_SORTIE_SUIVI = [
    ('avortement','Avortement'),
    ('deces_maternel_avant','Décès maternel avant accouchement'),
    ('deces_maternel_apres','Décès maternel après accouchement'),
    ('demenagement','Déménagement'),
    ('perdue_de_vue','Perdue de vue'),
]

class SortieSuivi(models.Model):
    """
    Class Sortie Suivi de TCHANDRA.
    """
    _name = 'tchandra.sortie.suivi'
    _description = 'Sortie suivi dans TCHANDRA'
    
    #liste des champs de la classe
    date_creation=fields.Datetime(string="Date de création du formulaire", compute='_compute_date_creation')
    date_derniere_modification=fields.Datetime(string="Date de dernière modification", compute='_compute_date_modification')
    motif_sortie_suivi=fields.Selection(MOTIF_SORTIE_SUIVI, string="Motif de sortie du suivi")
    jour_date_sortie=fields.Integer(string="Jour date de sortie")
    mois_date_sortie=fields.Integer(string="Mois date de sortie")
    annee_date_sortie=fields.Integer(string="Année date de sortie")
    date_sortie_non_connue=fields.Boolean(string="Date non connue")
    grossesse = fields.One2many('tchandra.grossesse', 'sortie_suivi', string='Sortie suivi')

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
        res= super(SortieSuivi, self).create(vals)

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