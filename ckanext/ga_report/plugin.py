import logging
import ckan.lib.helpers as h
import ckan.plugins as p
from ckan.plugins import implements, toolkit
from webhelpers.html import literal
from ckanext.ga_report.helpers import (most_popular_datasets,
                                       popular_datasets,
                                       single_popular_dataset,
                                       month_option_title,
                                       join_x, join_y)

log = logging.getLogger('ckanext.ga-report')

def custom_gravatar(*pargs, **kargs):
    gravatar = h.gravatar(*pargs, **kargs)
    pos = gravatar.find('/>')
    gravatar = gravatar[:pos] + literal(' alt="User\'s profile gravatar" ') + gravatar[pos:]
    return gravatar

class GAReportPlugin(p.SingletonPlugin):
    implements(p.IConfigurer, inherit=True)
    implements(p.IRoutes, inherit=True)
    implements(p.ITemplateHelpers, inherit=True)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')

    def get_helpers(self):
        """
        A dictionary of extra helpers that will be available to provide
        ga report info to templates.
        """
        return {
            'ga_report_installed': lambda: True,
            'popular_datasets': popular_datasets,
            'most_popular_datasets': most_popular_datasets,
            'single_popular_dataset': single_popular_dataset,
            'month_option_title': month_option_title,
            'gravatar': custom_gravatar,
            'join_x': join_x,
            'join_y': join_y,
        }

    def after_map(self, map):
        # GaReport
        map.connect(
            '/site-usage',
            controller='ckanext.ga_report.controller:GaReport',
            action='index'
        )
        map.connect(
            '/site-usage_{month}.csv',
            controller='ckanext.ga_report.controller:GaReport',
            action='csv'
        )
        map.connect(
            '/site-usage/downloads',
            controller='ckanext.ga_report.controller:GaReport',
            action='downloads'
        )
        map.connect(
            '/site-usage/downloads_{month}.csv',
            controller='ckanext.ga_report.controller:GaReport',
            action='csv_downloads'
        )

        # GaDatasetReport
        map.connect(
            '/site-usage/publisher',
            controller='ckanext.ga_report.controller:GaDatasetReport',
            action='publishers'
        )
        map.connect(
            '/site-usage/publishers_{month}.csv',
            controller='ckanext.ga_report.controller:GaDatasetReport',
            action='publisher_csv'
        )
        map.connect(
            '/site-usage/dataset/datasets_{id}_{month}.csv',
            controller='ckanext.ga_report.controller:GaDatasetReport',
            action='dataset_csv'
        )
        map.connect(
            '/site-usage/dataset',
            controller='ckanext.ga_report.controller:GaDatasetReport',
            action='read'
        )
        map.connect(
            '/site-usage/dataset/{id}',
            controller='ckanext.ga_report.controller:GaDatasetReport',
            action='read_publisher'
        )
        return map
