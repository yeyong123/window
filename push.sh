git add .
git commit -m "$1$2"
git push origin master
git push dev master

ssh 5mutian_one 'cd /srv/www/flask_windo && git pull origin master --no-edit'
