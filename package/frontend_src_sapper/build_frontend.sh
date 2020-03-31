
npm run export
cp __sapper__/export/* ../frontend/ -R

DEFAULT_DIR="/sandbox/cfg/nginx/default_openresty_threebot/html/"
[ ! -d "$DEFAULT_DIR" ] && mkdir $DEFAULT_DIR

cp __sapper__/export/* $DEFAULT_DIR -R