
Pour l'instant seules les extentions de CKAN sont git :

- ckanext-cartong-theme
- ckanext-spatial
- ckanext-scheming


## Install et init d'un nouveau repository
```
git init
```

### config git

```
git config --global user.name ***
git config --global user.email ***
```

### Pense bête des commandes git utiles

```
git add -A .
git commit -m "init"
git remote add origin https://github.com/***/ckanext-cartong_theme.git
git push origin master
git pull https://github.com/***/ckanext-cartong_theme.git master

```


Clone des sources

```
pip install -e "git+https://github.com/okfn/ckanext-spatial.git#egg=ckanext-spatial"

cd /usr/lib/ckan/default/src/ckanext-spatial

pip install -r pip-requirements.txt
python setup.py develop
```

Ajouter les extentions dans le fichier CKAN production.ini

/etc/ckan/default/production.ini

```

ckan.plugins = (...) spatial_metadata spatial_query

ckanext.spatial.search_backend = solr
```

Ajouter ces paramètres pour modifier les tuiles du widget spatial. (ou mettre à jour CKAN pour que son comportement par defaut ne prennent pas les tuiles mapquests non disponible)

```
# Spatial Widget config
# workaround to get different basemap on the widget
ckanext.spatial.common_map.type = custom
ckanext.spatial.common_map.custom.url = https://{s}.tile.thunderforest.com/transport/{z}/{x}/{y}.png
ckanext.spatial.common_map.attribution = Maps &copy; <a href="http://www.thunderforest.com">Thunderforest</a>, Data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap co$
```




Configurer le schema solr


```
sudo nano  ckan/lib/default/src/ckan/ckan/config/solr/schema.xml

```
```
    <field name="bbox_area" type="float" indexed="true" stored="true" />
    <field name="maxx" type="float" indexed="true" stored="true" />
    <field name="maxy" type="float" indexed="true" stored="true" />
    <field name="minx" type="float" indexed="true" stored="true" />
    <field name="miny" type="float" indexed="true" stored="true" />
```

```
paster --plugin=ckan search-index rebuild --config=/etc/ckan/default/production.ini
```
Peut nécéssiter un redemarage de jetty8


```
paster --plugin=ckanext-spatial spatial initdb --config=/etc/ckan/default/production.ini
paster --plugin=ckanext-spatial spatial extents --config=/etc/ckan/default/production.ini

```

Check pgis tables

```
 sudo -u postgres psql -d ckan_default
 \d package_extent

```




# Utilisation de JTS pour les requetes spatial à partir de polygon JSON
https://gist.github.com/u10313335/5649488bc3a4037e1357

~~~
sudo apt-get install unzip
wget http://downloads.sourceforge.net/project/jts-topo-suite/jts/1.13/jts-1.13.zip
unzip jts-1.13.zip
cp lib/*.jar /usr/share/solr/web/WEB-INF/lib/
cp lib/*.jar /opt/solr-5.5.5/server/lib/
~~~
service solr restart



ckanext.spatial.search_backend = solr-spatial-field


# Modification des templates de saisie des données
##Modifier le template pour avoir le widget spatial search
ceci est créer dans l'extention cartong-extention-template
##Modifier le template pour avoir le widget spatial pour un dataset
ceci est créer dans l'extention cartong-extention-template







# info pour Moissonage Phase 2
extention à installer Spatial Harvesters

The spatial extension provides some harvesters for importing ISO19139-based metadata into CKAN, as well as providing a base class for writing new ones. The harvesters use the interface provided by ckanext-harvest, so you will need to install and set it up first.


