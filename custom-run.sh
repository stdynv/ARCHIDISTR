#!/bin/sh

# Définition de la variable d'environnement GF_PATHS_PLUGINS
GF_PATHS_PLUGINS=/usr/share/grafana/plugins

# Lancer deux applications simultanément.
npm run server --prefix $GF_PATHS_PLUGINS/mongodb-grafana & # Seconde application
P2=$!
/run.sh & # Première application
P1=$!
wait $P1 $P2 # Attendre la fin des deux applications