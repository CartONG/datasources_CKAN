voir la doc ici :
https://github.com/ckan/ckanext-scheming


# Modifier le Schema ckan-cartong

Les modifications se font dans le ficher en local

```
ckanext-cartong_theme/ckanext/cartong_theme/scheming/cartong_dataset.json
```

Puis il faut ensuite publier le modification sur le serveur avec git

```
cd /usr/lib/ckan/default/src/ckanext-cartong_theme

git pull https://github.com/geodatup/ckanext-cartong_theme.git

```

et enfin redemarer Apache
```
sudo /etc/init.d/apache2 restart

```

