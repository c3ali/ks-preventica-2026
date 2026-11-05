# Invitation K&S CONSULTING — Préventica Maroc 2026

Invitation partageable et cliquable sur WhatsApp, avec aperçu visuel.

- **Page (aperçu WhatsApp)** : https://c3ali.github.io/ks-preventica-2026/
- **Visuel direct** : https://c3ali.github.io/ks-preventica-2026/img/invitation-ks-preventica-2026.jpg
- **Inscription badge (code exposant K&S)** : https://preventica.ma/participer?origin=EIX226707

## 1. Lien de partage WhatsApp (à coller dans un message /转发)

Ouvre WhatsApp avec le message pré-rempli. L'aperçu affiche le visuel officiel K&S,
et le lien est cliquable.

```
https://wa.me/?text=K%26S%20CONSULTING%20a%20le%20plaisir%20de%20vous%20inviter%20%C3%A0%20Pr%C3%A9ventica%20Maroc%202026%2C%20l%27%C3%A9v%C3%A9nement%20de%20r%C3%A9f%C3%A9rence%20en%20Afrique%20pour%20la%20Sant%C3%A9%20au%20Travail%20et%20la%20S%C3%A9curit%C3%A9%20Globale.%0A%0A10%2C%2011%2C%2012%20Novembre%202026%0AFoire%20Internationale%20de%20Casablanca%0AStand%20G09%20-%20Atelier%0A9h%20%C3%A0%2018h%20%3A%20mardi%2C%20mercredi%20-%209h%20%C3%A0%2017h%20%3A%20jeudi%0A%0A80%20conf%C3%A9rences%20%E2%80%A2%20200%20exposants%20%E2%80%A2%206500%20visiteurs%0A%0ABadge%20visiteur%20gratuit%20%3A%0Ahttps%3A%2F%2Fc3ali.github.io%2Fks-preventica-2026%2F
```

## 2. Message texte seul (coller dans la discussion)

```
K&S CONSULTING a le plaisir de vous inviter à Préventica Maroc 2026, l'événement de référence en Afrique pour la Santé au Travail et la Sécurité Globale.

10, 11, 12 Novembre 2026
Foire Internationale de Casablanca
Stand G09 - Atelier
9h à 18h : mardi, mercredi - 9h à 17h : jeudi

80 conférences • 200 exposants • 6500 visiteurs

Badge visiteur gratuit :
https://c3ali.github.io/ks-preventica-2026/
```

## 3. Variante « visuel direct »

Si l'on veut que le lien ouvre directement l'image (au lieu de la page) :

```
https://wa.me/?text=Invitation%20K%26S%20CONSULTING%20-%20Pr%C3%A9ventica%20Maroc%202026%20-%20Stand%20G09%0A%0Ahttps%3A%2F%2Fc3ali.github.io%2Fks-preventica-2026%2Fimg%2Finvitation-ks-preventica-2026.jpg
```

## 4. Comment ça fonctionne

| Étape | Mécanisme |
|---|---|
| Le lien pointe vers la page | Une URL publique est indispensable : un message texte seul ne déclenche aucun aperçu. |
| WhatsApp lit les balises Open Graph | `og:image`, `og:title`, `og:description` sont servis par GitHub Pages. |
| Le visuel s'affiche en aperçu | L'image est en `image/jpeg`, 1080×600 (ratio 1,8 — format attendu). |
| Clic sur l'aperçu | Ouvre la page, où le visuel et le bouton mènent à `preventica.ma/participer?origin=EIX226707`. |

À noter : `preventica.ma/participer` ne déclare aucun `og:image` — partager ce lien
directement produirait un aperçu sans image. La page d'atterrissage est donc
indispensable pour afficher le visuel K&S.

## 5. Déploiement

Repo : https://github.com/c3ali/ks-preventica-2026 (branche `main`, GitHub Pages activé).

```powershell
cd C:\Users\DELL\Documents\ks-preventica-2026
git add -A
git commit -m "mise a jour"
git push origin main
```

Le visuel source : `C:\Users\DELL\Downloads\votre-logo-K&S CONSULTING-rs-exposants26.jpg`
(copié tel quel dans `img/`, sans retouche).
