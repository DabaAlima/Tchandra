# -*- coding: utf-8 -*-
{
    'name': 'tchandra',
    'version': '1.0',
    'category': 'HEALTH',
    'depends': [
        'base',
        'mail',
        'document',
    ],
    'author': 'Mame Daba DIOUF, ALIMA IT NGO',
    'description': 'Application TCHANDRA',
    'website': 'alima-ngo.org',
    'license': 'AGPL-3',
    'data': [
        'data/sequence.xml',
        'views/utilisateur_view.xml',
        'views/femme_enceinte_view.xml',
        'views/grossesse_view.xml',
        'views/identite_femme_enceinte_view.xml',
        'views/cpn_initiale_view.xml',
        'views/cpn_autre_view.xml',
        'views/visite_non_planifiee_view.xml',
        'views/accouchement_view.xml',
        'views/sortie_suivi_view.xml',
        'views/suivi_view.xml',
        'views/menu_view.xml',
        'security/user_groups.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
}
