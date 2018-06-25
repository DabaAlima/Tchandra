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

class Grossesse(models.Model):
    """
    Class Grossesse de TCHANDRA.
    """
    _name = 'tchandra.grossesse'
    _description = 'Grossesse dans TCHANDRA'
    
    #liste des champs de la classe
    date_enregistrement=fields.Datetime(string="Date d'enregistrement de la grossesse", compute='_compute_date_creation')
    enregistree_par = fields.Char(String="Enregistrée par")
    has_given_birth = fields.Boolean(String="A accouché")
    date_activite_accouchement=fields.Datetime(string="Date d'identification de l'activité d'accouchement")
    date_accouchement=fields.Date(string="Date accouchement")
    femme_enceinte_grossesse = fields.Many2one('tchandra.femme.enceinte', string='femme_enceinte_grossesse')
    cpn_initiale = fields.Many2one('tchandra.cpn.initiale', string='cpn_initiale')
    autre_cpn = fields.One2many('tchandra.cpn.autre', 'grossesse_autre_cpn', string="Autres CPN")
    visite_non_planifiee = fields.One2many('tchandra.visite.non.planifiee', 'grossesse_vnp', string="Visites non planifiées")
    accouchement = fields.Many2one('tchandra.accouchement', string='accouchement')
    sortie_suivi = fields.Many2one('tchandra.sortie.suivi', string='sortie_suivi')
    suivi = fields.Many2one('tchandra.suivi', string='suivi')
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
        res= super(Grossesse, self).create(vals)
        if 'id' in vals and res.id != vals['id']:
            res = res.incremente_id(vals['id'])
        res = res[0] if type(res) == list else res
        return res
        #creation
    @api.depends('create_date')
    def _compute_date_creation(self):
        for res in self:
            if res.create_date:
                res.date_enregistrement = res.create_date
    @api.depends('write_date')
    def _compute_date_modification(self):
        for res in self:
            if res.write_date:
                res.date_derniere_modification = res.write_date