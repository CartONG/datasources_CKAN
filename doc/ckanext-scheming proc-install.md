# go to ckanext-cartong-theme


# install et init du repo sur l poste de dev
git init
# config git
git config --global user.name hugo.roussaffa
git config --global user.email geodatup@gmail.com

# .gitignore
git add -A .
git commit -m "init"

git remote add origin https://github.com/geodatup/ckanext-cartong_theme.git
git push origin master
git pull https://github.com/geodatup/ckanext-cartong_theme.git master