#!/usr/bin/bash
docker run --name phpmyadmin -d -e PMA_ARBITRARY=1 -p 5000:80 phpmyadmin

