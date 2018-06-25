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
SEXE=[
    ('M', 'Masculin'),
    ('F', 'Féminin')
    ]

POSITION = [
    ('cephalique','Céphalique'),
    ('siege','Siége')
]

OUI_NON = [
    ('oui','Oui'),
    ('non','Non')
]

MODE_ADMISSION = [
    ('propre_decision','Propre décision'),
    ('envoyee_par_tchandra','Envoyée par la Tchandra'),
    ('envoyee_par_autre','Envoyée par une autre personne'),
    ('referee_par_centre_sante','Référée par le centre de santé'),
    ('autre','Autre')
]

LIEU_ACCOUCHEMENT_STRUCTURE_SANTE = [
    ('centre_sante_watta','Watta'),
    ('centre_sante_dibinintchi','Dibinintchi'),
    ('hopital_district','Hôpital de district')
]

TYPE_ACCOUCHEMENT = [
    ('voie_basse_sans_instrument','Voie basse sans instrument'),
    ('voie_basse_avec_instrument','Voie basse avec instrument'),
    ('cesarienne','Césarienne')
]

STATUT_VITAL_FEMME = [
    ('vivante','Vivante'),
    ('decedee_pendant_accouchement','Décédée pendant accouchement'),
    ('decedee_apres_accouchement','Décédée après accouchement')
]

STATUT_VITAL_ENFANT = [
    ('vivant','Vivant'),
    ('mort_ne','Mort-né'),
    ('deces_neonatal','Décès néonatal')
]

LIEU_ACCOUCHEMENT_HORS_STRUCTURE_SANTE = [
    ('domicile','A domicile'),
    ('en_chemin','Sur le chemin entre le domicile et le centre de santé'),
    ('autre','Autre')
]

ACCOMPAGNANTS = [
    ('seule','Seule'),
    ('proche','Accompagnée par un proche'),
    ('tchandra','Avec une Tchandra'),
    ('relais_communautaire','Avec un relai communautaire'),
    ('personnel_sante','Avec un personnel de santé qualifié'),
    ('autre','Autre')
]


class Accouchement(models.Model):
    """
    Class Accouchement de TCHANDRA.
    """
    _name = 'tchandra.accouchement'
    _description = 'Accouchement dans TCHANDRA'
    
    #liste des champs de la classe
    date_creation=fields.Datetime(string="Date de création du formulaire", compute='_compute_date_creation')
    date_derniere_modification=fields.Datetime(string="Date de dernière modification", compute='_compute_date_modification')
    date_accouchement=fields.Date(string="Date de l'accouchement")
    mode_admission=fields.Selection(MODE_ADMISSION, string="Mode d'admission")
    autre_personne=fields.Text(string="Autre personne")
    autre_mode_admission=fields.Text(string="Autre mode d'admission")
    lieu_accouchement_structure_sante=fields.Selection(LIEU_ACCOUCHEMENT_STRUCTURE_SANTE, string="Lieu d'accouchement en structure de santé")
    presentation=fields.Selection(POSITION, string="Présentation")
    type_accouchement=fields.Selection(TYPE_ACCOUCHEMENT, string="Type d'accouchement")
    dechirure_perineale=fields.Selection(OUI_NON, string="Déchirure périnéale")
    hemorragie=fields.Selection(OUI_NON, string="Hémorragie de la délivrance")
    placenta=fields.Selection(OUI_NON, string="Placenta praevia")
    referencement=fields.Selection(OUI_NON, string="Référencement vers l'hôpital de district")
    motif_referencement=fields.Text(string="Motif de référencement")
    nombre_nouveau_nes=fields.Integer(string="Nombre de nouveau-nés")
    statut_vital_femme=fields.Selection(STATUT_VITAL_FEMME, string="Statut vital de la femme")
    date_deces_apres_accouchement=fields.Date(string="Date du décès")
    statut_vital_enfant=fields.Selection(STATUT_VITAL_ENFANT, string="Statut vital de l'enfant")
    date_deces_neonatal=fields.Date(string="Date du décès de l'enfant")
    sexe_enfant=fields.Selection(SEXE, string="Sexe de l'enfant")
    poids_naissance=fields.Float(string="Poids de naissance")
    poids_non_realise=fields.Boolean(string="Mesure non réalisée")
    taille_enfant=fields.Integer(string="Taille de l'enfant")
    taille_non_realise=fields.Boolean(string="Mesure non réalisée")
    perimetre_cranien=fields.Integer(string="Périmètre crânien")
    perimetre_cranien_non_realise=fields.Boolean(string="Mesure non réalisée")
    grossesse = fields.One2many('tchandra.grossesse', 'accouchement', string='Femmes enceintes')

    #Hors structure de santé
    lieu_accouchement_hors_structure_sante=fields.Selection(LIEU_ACCOUCHEMENT_HORS_STRUCTURE_SANTE, string="Lieu d'accouchement hors structure de santé")
    autre_lieu_accouchement=fields.Text(string="Autre lieu d'accouchement")
    accompagnants=fields.Selection(ACCOMPAGNANTS, string="Accompagnants lors de l'accouchement")
    autre_accompagnant=fields.Text(string="Autre accompagnant")
    accouchement_hors_structure_sante=fields.Boolean(string="Accouchement hors structure de santé")
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
        res= super(Accouchement, self).create(vals)

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

#     def compute_recence(self):
#         for rec in self:
#             if rec.dateDernierDon:
#                 diff= datetime.strptime(fields.Date.today(), tools.DEFAULT_SERVER_DATE_FORMAT) - datetime.strptime(rec.dateDernierDon, tools.DEFAULT_SERVER_DATE_FORMAT)
#                 print diff.days
#                 if diff.days < 365:
#                     rec.recence='Actif'
#                 elif diff.days > 365 and diff.days < 730:
#                     rec.recence='Inactifs recents'
#                 elif diff.days > 730 and diff.days < 1460:
#                     rec.recence='Inactifs'
#                 elif diff.days > 1460:
#                     rec.recence='Grands inactifs'
#     @api.one
#     @api.depends('engagements')
#     def _is_statut_PA(self):
#         self.statut_PA = False
#         for eng in self.engagements:
#             if eng.statut_engagement and eng.statut_engagement == 'actif':
#                 self.statut_PA = True
        
#     def compute_date_don(self, datetime):
#         # if not cal.is_working_day(datetime):
#         return self.compute_date_don(datetime + relativedelta.relativedelta(days=1))

#     def date_a_prelever(self, date):
#         try:
#             return str(datetime.strptime(date,'%Y/%m/%d')).split(' ')[0]
#         except:
#             t=date.split('/')
#             f=int(t[2])-1
#             t[2]=str(f)
#             return str(self.date_a_prelever('/'.join(t))).split(' ')[0]


        
#     def scheduler_credit_coop(self):
#         """
#         On récuperer tous les donateurs de la base
#         Pour chaque donateur on verifie s'il à un engagement(credit coop) 
#         pour lequel on doit déclencher la création d'un don
#         Param de verification: statut d'engagement, le don correspondant via le code media de l'engagement,
#         date prochaine prélévement, periodicité, mode de versement
#         """
#         raise UserError(_("Test in"))
#         all_donateurs = self.env['crm.alima.donateur'].search([])
#         for donateur in all_donateurs:
#             if donateur.engagements and donateur.dons:
#                 for eng in donateur.engagements:
#                     if eng.statut_engagement == 'actif' and eng.date_prochain_prelevement and datetime.strptime(eng.date_prochain_prelevement, '%Y-%m-%d') < datetime.today():
#                         for don in donateur.dons:
#                             if don.codeMedia.id == eng.code_media.id and don.moyen_paiment == 'Compte bancaire' and don.mode_versement=="avec prelevement":
#                                 #Creation du don credit coop
#                                 date_du_don = self.compute_date_don(datetime.strptime(eng.date_prochain_prelevement, '%Y-%m-%d'))
#                                 create_don = self \
#                                     .env['crm.alima.don'] \
#                                     .search([('donateur', '=', donateur.id),('codeMedia', '=', eng.code_media.id)], limit=1) \
#                                     .copy({
#                                         'date': str(date_du_don),
#                                         'montantEur': eng.montant,
#                                 })

#                                 #Mise à jour de l'engagement aprés la création du don
#                                 if create_don:
#                                     if eng.date_premier_prelevement:
#                                         jour = eng.date_premier_prelevement.split('-')[2]
#                                         date = create_don.date.split('-')
#                                         date[2] = jour
#                                         date = "/".join(date)
#                                         date_prochain = self.date_a_prelever(date)
#                                     else:
#                                         date_prochain = create_don.date

#                                     eng.write({
#                                         'date_dernier_prelevement': create_don.date,
#                                         'date_prochain_prelevement': str(self.compute_date_don(
#                                             datetime.strptime(date_prochain,'%Y-%m-%d')     
#                                                 +
#                                             relativedelta.relativedelta(months=PERIODICITE_MOIS_EN_ENTIER[eng.periodicite])
#                                         )) 

#                                     })
#                                 #Le premier don qu'on rencontre qui vient de credit coop. 
#                                 #On incremente d'un don puis on sort de la boucle
#                                 break


# class ScoreLAI(models.Model):
#     _name = 'crm.alima.score.lai'
#     _description = 'SCORE LAI'

#     """
#     SCORE LAI: creation d'une table pour l'historique
#     """
#     #liste des champs de la classe
#     linkage =fields.Integer(string='Linkage')
#     ability =fields.Integer(string='Ability')
#     interest =fields.Integer(string='Interest')
#     score_LAI = fields.Integer(compute='compute_LAI', store=True)
#     date_debut=fields.Date(string="Date")
#     commentaires_LAI =fields.Text(string='Commentaires LAI')
#     donateur = fields.Many2one('crm.alima.donateur', string='donateur', required=True)

#     @api.depends('linkage', 'ability','interest')
#     def compute_LAI(self):
#         for rec in self:
#             rec.score_LAI = rec.linkage + rec.ability + rec.interest
#     _sql_constraints = [
#         ('check_linkage', "check (linkage <= 5)",
#             "La valeur de linkage doit etre inferieur à 5"),
#         ('check_ability', "check (ability <= 5)",
#             "La valeur de ability doivent etre inferieur à 5"),
#         ('check_interest', "check (interest <= 5)",
#             "La valeur de interest doit etre inferieur à 5"),
#     ]

# class Contacts(models.Model):
#     _name = 'crm.alima.contacts'
#     _description = 'Contacts'

#     code_media=fields.Many2one('crm.alima.code.media', string='code media', ondelete='restrict')
#     libelle=fields.Char(string='libellé')
#     date=fields.Date(string='Date')
#     sens_solliciteur=fields.Selection(SENS_SOLL, string='Sens')
#     canal=fields.Selection(CANAL, string='canal')
#     type_contact=fields.Selection(TYPE_CONTACT, string='Type de contact')
#     contenu=fields.Char(string='Contenu')
#     qualif=fields.Selection(QUALIF, string='Qualificatif')
#     theme=fields.Char(string='Thème')
#     statut_trait=fields.Selection(STATUT_TRAIT, string='Statut traitement')
#     date_traitement=fields.Date(string='Date de traitement')
#     resp_traitement=fields.Many2one('res.users', string='Responsable traitement')
#     org_traitement=fields.Char(string='Organisme dans le cas d\'un échange de contact')
#     date_retour_telemark=fields.Date(string='date retour télémarketing')
#     code_retour_telemark=fields.Date(string='code média retour télémarketing')
#     statut_telemark=fields.Selection(TELEMARK, string='retour tele')
#     donateur = fields.Many2one('crm.alima.donateur', string='donateur', required=True)

#     #liste des fonctions
#     @api.model
#     @api.returns('self', lambda value: value.id)
#     def create(self, vals):
#         res= super(Contacts, self).create(vals)
#         #rec = res.donateur
#         return res

# class Engagement(models.Model):
#     _name = 'crm.alima.engagements'
#     _description = 'Engagements'

#     donateur = fields.Many2one('crm.alima.donateur', string='donateur', required=True)
#     code_media_origine = fields.Many2one('crm.alima.code.media', string='code media origine', ondelete='restrict')
#     code_media = fields.Many2one('crm.alima.code.media', string='code media', ondelete='restrict')
    
#     date_accord_mandat = fields.Date(string='Date d\'accord du mandat')
#     date_engagement_mandat = fields.Date(string='Date d\'engagement du mandat')
#     date_fin_mandat = fields.Date(string='Date de fin du mandat')
#     date_fin_engagement = fields.Date(string='Date fin engagement')
#     motif_fin_engagement = fields.Selection(MOTIF_FIN_ENGAGEMENT, string='Motif fin d\'engagement')
#     code_media_engagement_modifie = fields.Many2one('crm.alima.code.media', string='code media engagement modifié', ondelete='restrict')
#     montant = fields.Float(string="Montant")
#     periodicite = fields.Selection(PERIODICITE, string='Periodicité')
#     statut_engagement = fields.Selection(STATUT_ENGAGEMENT, string='Statut d\'engagement')
#     date_premier_prelevement = fields.Date(string='Date premier prélèvement')
#     date_dernier_prelevement = fields.Date(string='Date dernier prélèvement')
#     montant_supplementaire_prochain_prelevement = fields.Float(string='Montant supplémentaire exceptionnel du prochain prélèvement')
#     date_prochain_prelevement = fields.Date(string='Date prochain prélèvement')
#     nom_banque = fields.Char(string='Nom banque')
#     numero_iban = fields.Char(string='Numéro IBAN')
#     code_bic = fields.Char(string='Code BIC')
#     code_identifiant_debiteur = fields.Char(string='Code identifiant débiteur')
#     reference_unique_mandat = fields.Char(string='Référence unique de mandat')
#     identifiant_cb = fields.Char(string='Identifiant CB')
#     date_expiration_cb = fields.Char(string='Date d\'expiration CB')
#     remarques = fields.Char(string='Remarques')
#     motif_modification = fields.Selection(MOTIF_MODIFICATION, string="Motif modification")

#     @api.model
#     @api.returns('self', lambda value: value.id)
#     def create(self, vals): 
#         vals['code_media_origine'] = vals['code_media']
        
#         return super(Engagement, self).create(vals)

#     @api.multi
#     def write(self, vals):
#         res = self

#         if u'motif_modification' not in vals:
#             #Pour la création d'un engagement
#             rep  =  super(Engagement, self).write(vals)
        
#         elif vals[u'motif_modification'] in [False, u'erreur'] or res.statut_engagement in [False, 'inactif']:    
#             #Pour la correction de saisi d'un engagement
#             rep  =  super(Engagement, self).write(vals)
        
#         else:
#             #creation d'un nouvel engagement avec les même info que l'engagement dérivé
#             new_eng = super(Engagement, self).create({
#                 'donateur': res.donateur.id,
#                 'code_media': res.code_media.id,
#                 'code_media_origine': res.code_media_origine.id,
#                 'date_accord_mandat' : res.date_accord_mandat,
#                 'date_engagement_mandat' : res.date_engagement_mandat,
#                 'date_fin_mandat' : res.date_fin_mandat,
#                 'date_fin_engagement' : res.date_fin_engagement,
#                 'motif_fin_engagement' : res.motif_fin_engagement,
#                 'code_media_engagement_modifie' : res.code_media.id, 
#                 'montant' : res.montant,
#                 'periodicite' : res.periodicite,
#                 'statut_engagement' : res.statut_engagement,
#                 'date_premier_prelevement' : res.date_premier_prelevement,
#                 'date_dernier_prelevement' : res.date_dernier_prelevement,
#                 'montant_supplementaire_prochain_prelevement' : res.montant_supplementaire_prochain_prelevement,
#                 'date_prochain_prelevement' : res.date_prochain_prelevement,
#                 'nom_banque' : res.nom_banque,
#                 'numero_iban' : res.numero_iban,
#                 'code_bic' : res.code_bic,
#                 'code_identifiant_debiteur' : res.code_identifiant_debiteur,
#                 'reference_unique_mandat' : res.reference_unique_mandat,
#                 'identifiant_cb' : res.identifiant_cb,
#                 'date_expiration_cb': res.date_expiration_cb,
#                 'remarques' : res.remarques,  
#             })
#             vals[u'motif_modification'] = False # Pour sortir de la boucle
#             new_eng.write(vals)

#             #desactivation de l'engagement
#             rep  =  super(Engagement, self).write({
#                 'statut_engagement' : 'inactif',
#             })


#         return rep

#     @api.model
#     def default_get(self, fields):    
#         res = super(Engagement, self).default_get(fields)        
#         if 'nom_banque' in fields:        
#             res.update({
#                 'statut_engagement' : 'actif',

#             })    
#         return res

#     @api.multi
#     def unlink(self):
#         res = super(Engagement, self).unlink()
#         return { 'type': 'ir.actions.client', 'tag': 'reload', }

