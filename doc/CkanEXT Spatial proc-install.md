
pip install -e "git+https://github.com/okfn/ckanext-spatial.git#egg=ckanext-spatial"

cd /home/cartong/ckan/lib/default/src/ckanext-spatial

pip install -r pip-requirements.txt


# ajouter les extentions dans le fichier CKAN production.ini
ckan.plugins = (...) spatial_metadata spatial_query

ckanext.spatial.search_backend = solr


# configurer le schema solr

    <field name="bbox_area" type="float" indexed="true" stored="true" />
    <field name="maxx" type="float" indexed="true" stored="true" />
    <field name="maxy" type="float" indexed="true" stored="true" />
    <field name="minx" type="float" indexed="true" stored="true" />
    <field name="miny" type="float" indexed="true" stored="true" />



sudo nano  ckan/lib/default/src/ckan/ckan/config/solr/schema.xml
paster --plugin=ckan search-index rebuild --config=/etc/ckan/default/production.ini

Peut nécéssiter un redemarage de jetty8


paster --plugin=ckanext-spatial spatial initdb --config=/etc/ckan/default/production.ini
paster --plugin=ckanext-spatial spatial extents --config=/etc/ckan/default/production.ini


# chek pgis tables
 sudo -u postgres psql -d ckan_default
 \d package_extent





# modifier le template pour avoir le widget spatial search
#ceci est créer dans l'extention cartong-extention-template
# modifier le template pour avoir le widget spatial pour un dataset
#ceci est créer dans l'extention cartong-extention-template











# info pour Moissonage Phase 2 : extention à installer Spatial Harvesters

The spatial extension provides some harvesters for importing ISO19139-based metadata into CKAN, as well as providing a base class for writing new ones. The harvesters use the interface provided by ckanext-harvest, so you will need to install and set it up first.


