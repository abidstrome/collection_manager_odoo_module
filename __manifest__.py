{
    'name': 'Collection Manager',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Module to Manage Collections',
    'description': 'Manage Collections with Odoo',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/collection_views.xml',
        'views/import_collections_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}