import requests
from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class Collection(models.Model):
    _name = 'collection.manager.collection'
    _description = 'Collection'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    owner_id = fields.Many2one('res.users', string='Owner', required=True)
    category_id = fields.Many2one('collection.manager.category', string='Category')
    item_count = fields.Integer(string='Number of Items')

    def action_import_collections(self):
        view_id = self.env.ref('collection_manager.view_import_collections_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import Collections',
            'view_mode': 'form',
            'res_model': 'collection.manager.collection.import',
            'view_id': view_id,
            'target': 'new',
        }

    @api.model
    def import_collections(self, api_token):
        url = 'https://treasurex.onrender.com/api/v1/collections'
        headers = {'Authorization': api_token}
        response = requests.get(url, headers=headers)
        _logger.info(f"API response status: {response.status_code}")
        _logger.info(f"API response content: {response.text}")

        if response.status_code == 200:
            collections_data = response.json()
            for data in collections_data:
                self.create({
                    'id': data['id'],
                    'name': data['name'],
                    'description': data['description'],
                    'owner_id': self.env.user.id,
                    'category_id': data.get('category_id'),
                    'item_count': data.get('item_count')
                })
        else:
            raise UserError(f'Failed to import collections: {response.json().get("error", "Unknown error")}')


    @api.model
    def create(self, vals):
        record = super(Collection, self).create(vals)
        
        return record

    def write(self, vals):
        result = super(Collection, self).write(vals)
        
        return result

    def unlink(self):
        result = super(Collection, self).unlink()
        
        return result

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
                    'category_id': data.get('category_id'),
                    'item_count': data.get('item_count')
                })
        else:
            raise UserError(f'Failed to import collections: {response.json().get("error", "Unknown error")}')
