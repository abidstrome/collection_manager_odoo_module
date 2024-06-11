import requests
from odoo import models, fields, api
from odoo.exceptions import UserError

class ImportCollections(models.TransientModel):
    _name = 'collection.manager.collection.import'
    _description = 'Import Collections'

    api_token = fields.Char(string='API Token', required=True)

    def import_collections(self):
        Collection = self.env['collection.manager.collection']
        url = 'https://treasurex.onrender.com/api/v1/collections'
        headers = {'Authorization': f'Token {self.api_token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            collections_data = response.json()
            for data in collections_data:
                Collection.create({
                    'name': data['name'],
                    'description': data['description'],
                    'owner_id': self.env.user.id,
                    'category_id': data.get('category_id')
                })
        else:
            raise UserError(f'Failed to import collections: {response.json().get("error", "Unknown error")}')