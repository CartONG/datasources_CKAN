# configuration de la config global

le fichier de config est ici (production ou dev ...)
```
cd /ckan/etc/default

```
Permettre l'affichage de la vue "site web", modifier le fichier avec la commande 
```
nano
```

```
ckan.views.default_views = (...) webpage_view

```

Permettre le Cross domain

```
ckan.plugins = (...) resource_proxy

```


# Ajout d'une extention "theme" Cartong_theme
nécéssite l'activation de  l'env virtuel
```
cd /usr/lib/ckan/default/src
paster --plugin=ckan create -t ckanext ckanext-cartong_theme
```

editer le plugin.py 
```
nano /usr/lib/ckan/default/src/ckanext-cartong_theme/ckanext/cartong_theme/plugin.py 
```
editer le setup.py 
```
nano /usr/lib/ckan/default/src/ckanext-cartong_theme/setup.py 
```

Test run setup 
```
python setup.py develop
```

Ajouter le plugin au fichier de config global

```
ckan.plugins = (...) cartong_theme
```