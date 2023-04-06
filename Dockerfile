# Spécification de l'image de base à utiliser pour la première étape de la construction de l'image.
FROM node:16-alpine AS node

# Utiliser l'image officielle de grafana OSS.
FROM grafana/grafana-oss

# Spécifie l'utilisateur qui exécutera les commandes suivantes.
USER root

# Copie des fichiers de l'image node à l'image en construction. 
COPY --from=node /usr/lib /usr/lib
COPY --from=node /usr/local /usr/local 

# Ajout du fichier du répertoire courrant vers l'image en construction.
# ADD devait être remplacé par COPY pour des questions de sécurité mais avec COPY ça ne fonctionne pas du tout. Retirer les commentaires du RUN chmod si on utilise COPY.
ADD ./custom-run.sh /custom-run.sh
#RUN chmod +x /custom-run.sh

# Installation des dépendances et configuration de grafana
RUN apk update \
    && apk upgrade \
    && apk add --no-cache git \
    && git clone https://github.com/JamesOsgood/mongodb-grafana $GF_PATHS_PLUGINS/mongodb-grafana \
    && sed -i 's/grafana-mongodb-datasource/jamesosgood-grafana-mongodb-datasource/g' $GF_PATHS_PLUGINS/mongodb-grafana/dist/plugin.json \
    && rm -rf $GF_PATHS_PLUGINS/mongodb-grafana/.git \
    && npm ci --silent --prefix $GF_PATHS_PLUGINS/mongodb-grafana \
    && apk del --no-cache git \
    && sed -i 's/;allow_loading_unsigned_plugins =.*/allow_loading_unsigned_plugins = jamesosgood-grafana-mongodb-datasource/g' $GF_PATHS_CONFIG

# Lancement de costum-run.sh
ENTRYPOINT ["/custom-run.sh"]