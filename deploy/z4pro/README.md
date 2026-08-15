# Déploiement sur Z4Pro (ZSpace)

Le site est statique, il peut donc tourner sur le Z4Pro avec Docker.

## Étapes

1. Copier l'ensemble du projet sur le Z4Pro.
2. Ouvrir l'interface Docker du ZSpace et importer `deploy/z4pro/docker-compose.yml`.
3. Démarrer le conteneur `kaholey-site`.
4. Ouvrir le site sur `http://IP_DU_Z4PRO:8080`.

## Accès public

Pour publier le site sur Internet, il faut une adresse publique et un nom de domaine :

- Utiliser le service d'accès distant du ZSpace ou un DDNS.
- Ou exposer le port avec un reverse proxy comme Caddy.
- Ou utiliser un tunnel type Cloudflare Tunnel.

Attention : en Chine continentale, l'hébergement sur une machine personnelle avec un domaine peut nécessiter un ICP 备案, et le port 80 peut être bloqué par le fournisseur d'accès.
