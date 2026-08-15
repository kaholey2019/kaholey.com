# Kaholey — Site photographe paysage

Portfolio statique et responsive pour Kaholey, photographe paysage basé à Pékin, construit en HTML, CSS et JavaScript. Aucune installation nécessaire : ouvrez `index.html` dans un navigateur pour le consulter.

## Architecture

- `index.html` — accueil avec sélection de travaux, approche et aperçu des prestations.
- `portfolio.html` — galerie complète avec filtres et lightbox.
- `services.html` — prestations, méthode et questions fréquentes.
- `a-propos.html` — parcours, valeurs et philosophie.
- `contact.html` — coordonnées et formulaire de contact.
- `404.html` — page d'erreur.

Le design system partagé se trouve dans `css/style.css` et les interactions dans `js/main.js`. Les icônes SVG sont centralisées dans `assets/icons.svg`.

## Déploiement

Le public visé est à la fois international et chinois. L'architecture recommandée est donc double :

Phase actuelle : le site est publié temporairement sur `https://kaholey.netlify.app`. Les balises canonical et le sitemap pointent vers cette adresse jusqu'à l'achat de `kaholey.com`.

1. **International — Netlify** : publier le dossier sur Netlify avec `kaholey.com` comme domaine principal. Le fichier `netlify.toml` gère les en-têtes de cache, la sécurité et les redirections vers `www.kaholey.com`.
2. **Chine — hébergement domestique** : publier une copie du site sur Aliyun OSS, Tencent COS ou un hébergement avec CDN chinois, sous un sous-domaine comme `cn.kaholey.com`. Un ICP 备案 est généralement nécessaire pour un domaine pointant vers un hébergement en Chine continentale.

Le contenu du site étant statique, la même archive peut être déployée sur les deux plateformes.

## Personnaliser

- Le nom, les coordonnées et les réseaux sociaux se modifient dans `index.html`.
- Les photos sélectionnées depuis ta photothèque sont optimisées en `.webp` dans `assets/images/`. Pour les changer, remplacez les fichiers en conservant les mêmes noms, ou mettez à jour les chemins dans `index.html`.
- Les tarifs et les prestations se modifient dans la section `Prestations`.
- Le formulaire ouvre le client mail avec les informations saisies. Pour envoyer les demandes vers un service tiers, adaptez la fonction `submit` de `js/main.js`.

## Lancer un serveur local (optionnel)

```bash
python3 -m http.server 8000
```

Puis ouvrez `http://localhost:8000`.
