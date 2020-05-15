docker run -it \
--rm \
mysql:latest \
mysql \
-h${MYSQL_HOST} \
-u${MYSQL_USER} \
-p${MYSQL_PASSWORD}