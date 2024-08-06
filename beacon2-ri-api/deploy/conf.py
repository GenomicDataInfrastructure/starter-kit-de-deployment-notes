"""Beacon Configuration."""

#
# Beacon general info
#
beacon_id = 'de.dkfz.ghga.beacon'  # ID of the Beacon
beacon_name = 'Beaconv2 at DKFZ.de in Heidelberg, Germany'  # Name of the Beacon service
api_version = 'v2.0.0'  # Version of the Beacon implementation
uri = 'https://beacon.gdi.dkfz.de/api/'

#
# Beacon granularity
#
default_beacon_granularity = "record"
max_beacon_granularity = "record"

#
#  Organization info
#
org_id = 'dkfz.de'  # Id of the organization
org_name = 'The German Cancer Research Center (Deutsches Krebsforschungszentrum, DKFZ)'  # Full name
org_description = ('The German Cancer Research Center (known as the Deutsches Krebsforschungszentrum or simply DKFZ in German)'
                   'is a national cancer research center based in Heidelberg, Germany.' 
                   'It is a member of the Helmholtz Association of German Research Centres,' 
                   'the largest scientific organization in Germany.')
org_adress = ('C/ Im Neuenheimer Feld 280,'
              '69120, Heidelberg, Germany')
org_welcome_url = 'https://dkfz.de/'
org_contact_url = 'mailto:contact@ghga.de'
org_logo_url = 'https://hub.dkfz.de/s/y8R5ZkYHD2LoTs7'
org_info = ''

#
# Project info
#
#description = (r"This <a href='https://beacon-project.io/'>Beacon</a> "
#               r"is based on the GA4GH Beacon "
#               r"<a href='https://github.com/ga4gh-beacon/specification-v2/blob/master/beacon.yaml'>v2.0</a>")
description = r"This is the german Beacon hosted at the dkfz.de it is currently based on synthetic data hosted at the <a href='https://ega-archive.org/datasets/EGAD00001003338'>EGA</a>. The dataset contains 2504 samples including genetic data based on 1K Genomes data, and 76 individual attributes and phenotypic data derived from UKBiobank."
version = 'v2.0'
welcome_url = 'https://beacon.gdi.dkfz.de/'
alternative_url = 'https://beacon.gdi.dkfz.de/api'
create_datetime = '2021-11-29T12:00:00.000000'
update_datetime = ''
# update_datetime will be created when initializing the beacon, using the ISO 8601 format

#
# Service
#
service_type = 'org.ga4gh:beacon:1.0.0'  # service type
service_url = 'https://beacon.biodata.pt/api/service-info'
entry_point = False
is_open = True
documentation_url = 'https://github.com/EGA-archive/beacon-2.x/'  # Documentation of the service
environment = 'test'  # Environment (production, development or testing/staging deployments)

# GA4GH
ga4gh_service_type_group = 'org.ga4gh'
ga4gh_service_type_artifact = 'beacon'
ga4gh_service_type_version = '1.0'

# Beacon handovers
beacon_handovers = [
    {
        'handoverType': {
            'id': 'CUSTOM:000001',
            'label': 'Project description'
        },
        'note': 'Project description',
        'url': 'https://www.nist.gov/programs-projects/genome-bottle'
    }
]

#
# Database connection
#
database_host = 'mongo'
database_port = 27017
database_user = 'root'
database_password = 'example'
database_name = 'beacon'
database_auth_source = 'admin'
# database_schema = 'public' # comma-separated list of schemas
# database_app_name = 'beacon-appname' # Useful to track connections

#
# Web server configuration
# Note: a Unix Socket path is used when behind a server, not host:port
#
beacon_host = '0.0.0.0'
beacon_port = 5050
beacon_tls_enabled = False
beacon_tls_client = False
beacon_cert = '/etc/ega/server.cert'
beacon_key = '/etc/ega/server.key'
CA_cert = '/etc/ega/CA.cert'

#
# Permissions server configuration
#
permissions_url = 'http://beacon-permissions:5051/'

#
# IdP endpoints (OpenID Connect/Oauth2)
#
# or use Elixir AAI (see https://elixir-europe.org/services/compute/aai)
#
idp_user_info = 'https://beacon-network-demo2.ega-archive.org/auth/realms/Beacon/protocol/openid-connect/userinfo'
lsaai_user_info = 'https://login.elixir-czech.org/oidc/userinfo'
trusted_issuers = ['https://beacon-network-demo2.ega-archive.org/auth/realms/Beacon', 'https://login.elixir-czech.org/oidc/']


#
# UI
#
autocomplete_limit = 16
autocomplete_ellipsis = '...'

#
# Ontologies
#
ontologies_folder = "ontologies"
