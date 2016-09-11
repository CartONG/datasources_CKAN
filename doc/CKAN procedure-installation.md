Faire les mises à jour des dépots
```
sudo apt-get update
```

# Installation serveur web
Arreter apache (si existant)
```
sudo /etc/init.d/apache2 stop
```

Installer nginx apache2 etc..
```
sudo apt-get install -y nginx apache2 libapache2-mod-wsgi libpq5
```

Arreter nginx
```
sudo /etc/init.d/nginx stop
```

Redemarer apache
```
sudo /etc/init.d/apache2 start
```
Redemarer nginx
```
sudo /etc/init.d/nginx restart
```


Installation des dépendances 

***Attention*** :installer openjdk-7-jdk au lieu du openjdk-6-jdk

```
sudo apt-get install python-dev postgresql libpq-dev python-pip python-virtualenv git-core solr-jetty openjdk-7-jdk libapache2-mod-rpaf 
```


# Installer CKAN dans un environment virtuel Python

Creer le projet dans home
```
mkdir -p ~/ckan/lib
sudo ln -s ~/ckan/lib /usr/lib/ckan
mkdir -p ~/ckan/etc
sudo ln -s ~/ckan/etc /etc/ckan
```

Creer le virtual env 
```
sudo mkdir -p /usr/lib/ckan/default
sudo chown `whoami` /usr/lib/ckan/default
virtualenv --no-site-packages /usr/lib/ckan/default
```


Activer le virtual env
```
. /usr/lib/ckan/default/bin/activate

```

Clone des sources
```
pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.5.2#egg=ckan'
```

Installer les packages python CKAN specifiques dans l'environnement virtuel
```
pip install -r /usr/lib/ckan/default/src/ckan/requirements.txt
```



# Créer la base postgres

Créer un nouvel utilisateur

```
sudo -u postgres createuser -S -D -R -P ckan_default

mdp : ************
```

Créer la base ckan_default
```

sudo -u postgres createdb -O ckan_default ckan_default -E utf-8
```

Verrifier l'existance de la nouvelle base
```
sudo -u postgres psql -l
```


# Create a CKAN config file

Creer le dossier contenant les fichiers de config du site
```
sudo mkdir -p /etc/ckan/default
sudo chown -R `whoami` /etc/ckan/
```

Créer le fichier ini (dev)
```

paster make-config ckan /etc/ckan/default/development.ini
```

modifier le fichier development.ini
```

sqlalchemy.url = postgresql://ckan_default:************@localhost/ckan_default

site_url=http://datasources.cartong.org/
```

#Configurer Jetty pour Solr
```
sudo nano /etc/defautl/jetty8


NO_START=0            # (line 4)
JETTY_HOST=127.0.0.1  # (line 16)
JETTY_PORT=8983       # (line 19)
JAVA_HOME=/usr/lib/jvm/java-6-openjdk-amd64/
```

Démarrer jetty
```
sudo /etc/init.d/jetty8 start
```

Verifier que tout va bien sur le site

```
wget http://localhost:8983

--2016-04-07 16:04:27--  http://localhost:8983/
Resolving localhost (localhost)... 127.0.0.1
Connecting to localhost (localhost)|127.0.0.1|:8983... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1082 (1.1K) [text/html]
Saving to: ‘index.html’

index.html                            100%[==========================================================================>]   1.06K  --.-KB/s   in 0s

2016-04-07 16:04:27 (201 MB/s) - ‘index.html’ saved [1082/1082]
```
et sur Solr

```

wget http://localhost:8983/solr

--2016-04-07 16:05:57--  http://localhost:8983/solr
Resolving localhost (localhost)... 127.0.0.1
Connecting to localhost (localhost)|127.0.0.1|:8983... connected.
HTTP request sent, awaiting response... 302 Found
Location: http://localhost:8983/solr/ [following]
--2016-04-07 16:05:57--  http://localhost:8983/solr/
Reusing existing connection to localhost:8983.
HTTP request sent, awaiting response... 200 OK
Length: 446 [text/html]
Saving to: ‘solr’

solr                                  100%[==========================================================================>]     446  --.-KB/s   in 0s

2016-04-07 16:05:58 (98.9 MB/s) - ‘solr’ saved [446/446]
```


Remplacer le schema.xml de solr par défaut par un lien symbolique vers les sources CKAN
Replace the default schema.xml file with a symlink to the CKAN schema file included in the sources.
```
sudo mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak
sudo ln -s /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
```

#Link to who.ini
who.ini (the Repoze.who configuration file) needs to be accessible in the same directory as your CKAN config file, so create a symlink to it:
```
ln -s /usr/lib/ckan/default/src/ckan/who.ini /etc/ckan/default/who.ini

```
redermarer jetty8
```
sudo /etc/init.d/jetty8 restart
```

Terminer la config solr
modifier dans development.ini de ckan
```
solr_url=http://127.0.0.1:8983/solr
```


Initialier les tables de la db
```
cd /usr/lib/ckan/default/src/ckan
paster db init -c /etc/ckan/default/development.ini
```

Test du runserver
```
cd /usr/lib/ckan/default/src/ckan
paster serve /etc/ckan/default/development.ini
```


# Deploiement en Production
```
cp /etc/ckan/default/development.ini /etc/ckan/default/production.ini

nano /etc/ckan/default/apache.wsgi
```
```
import os
activate_this = os.path.join('/usr/lib/ckan/default/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from paste.deploy import loadapp
config_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'production.ini')
from paste.script.util.logging_config import fileConfig
fileConfig(config_filepath)
application = loadapp('config:%s' % config_filepath)
```


Installer le server mail
```
sudo apt-get install postfix

internet site
datasource.cartong.org
```


Modifier le Apache config file ckan_defaut
```
<VirtualHost 127.0.0.1:8080>
    ServerName datasources.cartong.org
    ServerAlias www.datasources.cartong.org
    WSGIScriptAlias / /etc/ckan/default/apache.wsgi

    # Pass authorization info on (needed for rest api).
    WSGIPassAuthorization On

    # Deploy as a daemon (avoids conflicts between CKAN instances).
    WSGIDaemonProcess ckan_default display-name=ckan_default processes=2 threads=15

    WSGIProcessGroup ckan_default

    ErrorLog /var/log/apache2/ckan_default.error.log
    CustomLog /var/log/apache2/ckan_default.custom.log combined

    <IfModule mod_rpaf.c>
        RPAFenable On
        RPAFsethostname On
        RPAFproxy_ips 127.0.0.1
    </IfModule>

    <Directory />
        Require all granted
    </Directory>

</VirtualHost>
```

Créer le fichier de config nginx 
```
nano /etc/nginx/sites-available/ckan
```
```
proxy_cache_path /tmp/nginx_cache levels=1:2 keys_zone=cache:30m max_size=250m;
proxy_temp_path /tmp/nginx_proxy 1 2;

server {
    client_max_body_size 100M;
    location / {
        proxy_pass http://127.0.0.1:8080/;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
        proxy_cache cache;
        proxy_cache_bypass $cookie_auth_tkt;
        proxy_no_cache $cookie_auth_tkt;
        proxy_cache_valid 30m;
        proxy_cache_key $host$scheme$proxy_host$request_uri;
        # In emergency comment out line to force caching
        # proxy_ignore_headers X-Accel-Expires Expires Cache-Control;
    }

}

```

Finir la confiuration des serveurs web nginx et apache2
```
sudo a2ensite ckan_default
sudo a2dissite 000-default
sudo rm -vi /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/ckan /etc/nginx/sites-enabled/ckan_default
```
Redemarer apache
```
sudo /etc/init.d/apache2 restart
```
Redemarer nginx
```
sudo /etc/init.d/nginx restart
```



Créer un super admin user sudatasource
```
. /usr/lib/ckan/default/bin/activate
cd /usr/lib/ckan/default/src/ckan
paster sysadmin add sudatasource -c /etc/ckan/default/production.ini
```


Installer l'extention Postgis
```
sudo apt-get install postgresql-9.4-postgis
```

Créer les fonctions et les tables spatialref
```
sudo -u postgres psql -d ckan_default -f /usr/share/postgresql/9.4/contrib/postgis-2.1/postgis.sql
sudo -u postgres psql -d ckan_default -f /usr/share/postgresql/9.4/contrib/postgis-2.1/spatial_ref_sys.sql
```

Changer le proprietaire des tables
```
sudo -u postgres psql -d ckan_default -c 'ALTER VIEW geometry_columns OWNER TO ckan_default;'
sudo -u postgres psql -d ckan_default -c 'ALTER TABLE spatial_ref_sys OWNER TO ckan_default;'
```
Verification 
```
sudo -u postgres psql -d ckan_default -c "SELECT postgis_full_version()"
```

installer d'autre package / dépendance pour la gestion spatial
```
sudo apt-get install python-dev libxml2-dev libxslt1-dev libgeos-c1
```



# make a git

dans ckanext-cartong-theme


# install et init du repo sur l poste de dev
```
git init
```
# config git
git config --global user.name ***
git config --global user.email ***

# .gitignore

# command git
```
git add -A .
git commit -m "init"
git remote add origin https://github.com/***/ckanext-cartong_theme.git
git push origin master
git pull https://github.com/***/ckanext-cartong_theme.git master
git pull https://github.com/geodatup/ckanext-cartong_theme.git master

```

# troubleshouting

```
OSError: [Errno 13] Permission denied: '/tmp/default/sessions/container_file_lock/a'

```
ajouter cartong au groupe www-data

```
sudo usermod -a -G www-data cartong
```