# configuration de la config global

Permettre l'affichage de la vue "site web"
ckan.views.default_views = (...) webpage_view


Permettre le Cross domain
ckan.plugins = (...) resource_proxy



# Ajout d'une extention "theme" Cartong_theme
(activer l'env virtuel)
cd /usr/lib/ckan/default/src
paster --plugin=ckan create -t ckanext ckanext-cartong_theme

# go edit plugin.py 

nano /usr/lib/ckan/default/src/ckanext-cartong_theme/ckanext/cartong_theme/plugin.py 

# go edit setup.py 

nano /usr/lib/ckan/default/src/ckanext-cartong_theme/setup.py 

# run setup 
python setup.py develop


# ajouter le plugin au fichier de config global
ckan.plugins = (...) cartong_theme
