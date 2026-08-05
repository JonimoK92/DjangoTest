
```markdown
# Description

## What I implemented

J’ai pu implémenter l’ensemble des fonctionnalités demandées. Cela m’a pris un peu plus de temps que les deux heures initialement prévues, mais je tenais à terminer le travail correctement, pas seulement dans le cadre du test, mais également pour moi-même.

Ces derniers jours, j’ai investi beaucoup de temps dans l’apprentissage et la compréhension de Django, un framework backend que je n'avais jamais utilisé auparavant après avoir principalement utilisé Laravel. Je souhaitais donc aller jusqu’au bout de cette réalisation afin de ne pas terminer ce test avec un sentiment d’inachevé. Grâce à ce test et mon expérience préalable avec les API Rest, les routes, et les framework backend j'ai pu tout de même finir ce test dans un délai raisonnable.

Les fonctionnalités implémentés sont :
  - Créer et supprimer  des livres
  - Voir les informations d'un livre spécifique
  - Système de validation pour les ISBN (unique) et la date de publication (inférieur ou égal a 2026)
  - Apparition d'un champ "available" précisant si le livre est disponible pour être emprunté
  - La pagination via Django REST Framework
  - Le filtre pour la recherche du titre et de l'auteur (http://127.0.0.1:8000/api/books/?search=titre)
  - Le filtre pour avoir les livres selon leur disponibilité (http://127.0.0.1:8000/api/books/?available=true)
  - Création de l'emprunt via la route POST /api/books/{id}/borrow/
  - Création de la date de rendu via la route POST /api/loans/{id}/returnbook/
  - Un livre ne peut pas être emprunté si il est déjà emprunté
  - Un emprunt ne peut pas être retourné si il a déjà été retourné une fois
  - La date limite pour l'emprunt ne peut pas être antérieur à la date de l'emprunt

Je n'ai pas pu tout tester en profondeur ce qui veut dire qu'il pourrait y avoir des bugs ou des mini-détails que j'ai manqué.

---

## Technical decisions

  ## Views

J'avais initialement essayé d'utiliser les generic views avec ListCreateApiView et DestroyApiView, mais après avoir regardé la documentation plus en profondeur je me suis rendu compte que utiliser ModelViewSet notamment pour ce test était plus logique car il me fournissait sans que je ne fasse quoi que ce soit des routes CRUD standards (POST,GET,PUT,PATCH,DELETE), cela me permet de gagner beaucoup de temps en m'évitant d'écrire des routes séparés a chaque fois.

 Cela permet de garder l'architecture simple tout en avançant plus vite. Mais pour un projet d'une plus grande envergure je ne pense pas que ModelViewSet serait le choix le plus approprié, généralement la simplicité offre moins de liberté, cela peut limiter la personnalisation et la flexibilité nécessaire pour des besoins plus complexe.

  ## Logique métier

Toute la logique métier est ici gérer dans les fichiers serializer et views

Les serializers sont utilisés pour gérer la validation de certaines données (date limite pour les empruts, ISBN et année de publication pour les livres), ils vérifient les données entrantes (avec fields et les règles de validation) avant leur enregistrement en base de donnée, et surtout ils permettent de transformer les objets Django en données JSON exploitables par l'API.

Les views sont eux responsable de la gestions des requêtes HTTP et défini les différentes actions effectué par l'API. Ils récupèrent les données nécessaire, et génèrent les réponses adaptés aux requêtes reçues.

En me basant sur mon expérience avec Laravel je pense que pour des projets plus complexes il faudrait séparer davantage la logique métier dans des "services" dédies afin de garder les serializers et les views léger rendant le code plus scalable/facile à maintenir.

  ## Availability

J'ai pu rajouter le champs available dans le détails des livres mais ce n'est pas un champs enregistré dans la base de données, c'est une donnée dérivé.

J'ai utilisé les conditions que vous avez précisez pour savoir si un livre est disponible : un livre est considéré comme disponible uniquement s'il n'existe aucun emprunt associé dont la date de retour (`return_date`) n'a pas encore été renseignée.

  ## Filtres

Pour le filtre j'ai utilisé la bibliothèque django-filter qui est intégrée à Django Rest Framework qui permet de filtrer de manière simple sans avoir à écrire la logique de filtrage. C'était suffisant pour ce test mais ne suffira surement pas pour implémenter un système de filtrage plus complexe.

  ## Status HTTP

Les différents status HTTP utilisés dans l'API permettent d'indiquer clairement le résultat d'une requête :
  - '200 OK' est retourné lorsqu’une opération de lecture ou une modification réussit
  - '204 No Content' lorsqu’une suppression est effectuée correctement sans contenu à retourner
  - '400 Bad Request' lorsqu’une requête contient des données invalides
  - '404 Not Found' lorsqu’une ressource demandée n’existe pas
  - '500 Internal Server Error' en cas d’erreur inattendue côté serveur.

  ## DELETE

Pour le système de suppression, j'ai conservé le comportement CRUD fourni par le `ModelViewSet`, en effet dans le modèle Loan le comportement en cas de suppression d'un livre est déjà spécifié " on_delete=models.CASCADE", qui spécifie qu'en cas de suppression d'un livre, tout les emprunts associés seront supprimés.

---

## Tools used

Pour réaliser ce test, j'ai utilisé plusieurs ressources afin de m'aider dans la compréhension et l'implémentation des fonctionnalités demandées :

- La documentation officielle de Django.
- La documentation officielle de Django REST Framework.
- ChatGPT pour m'aider à comprendre certains concepts ou certaines syntaxes que je ne maîtrisais pas totalement.
- Quelques ressources vidéo consultées en amont pour revoir certains concepts de Django et Django REST Framework.

J'ai principalement utilisé la documentation de Django REST Framework, qui m'a permis de comprendre et d'utiliser plusieurs fonctionnalités importantes comme les `ModelViewSet`, les filtres, les actions personnalisées avec `@action`, les réponses HTTP (`Response`), les codes de statut, ainsi que d'autres fonctionnalités comme `Exists` et `OuterRef`.

La documentation Django m'a principalement aidé pour approfondir certaines syntaxes,l'utilisation de certaines fonctionnalités natives du framework.

J'ai également utilisé ChatGPT comme support  afin d'obtenir des explications sur des concepts ou des syntaxes que je ne comprenais pas complètement. Mon objectif était de comprendre les choix effectués et le fonctionnement du code, plutôt que de simplement reprendre une solution sans en maîtriser le fonctionnement, cela m'a permis par exemple de faire/modifier certaines parties du code qui ne me semblait pas optimale en terme de simplicité et en terme d'architecture.

---

## Difficulties encountered

La principale difficulté rencontrée concernait la gestion de la disponibilité des livres.


Au départ, j'avais ajouté un champ `available` directement dans le serializer pour afficher l'information, mais je devais également permettre le filtrage des livres disponibles. le problème est que cette donnée n'était pas stockée en base de données mais dérivée des emprunts en cours. La difficulté était donc de réussir à filtrer directement sur cette donnée calculée.

J'ai étudié plusieurs approches avant de retenir l'utilisation de `Exists` et `OuterRef` . Cette solution permet de vérifier efficacement l'existence d'un emprunt actif pour chaque livre sans ajouter de champ redondant dans le modèle.


La création des actions personnalisées avec `@action` a également demandé un temps de compréhension notamment pour comprendre comment ajouter des routes spécifiques comme :
- `POST /api/books/{id}/borrow/`
- `POST /api/loans/{id}/returnbook/`

Enfin, j'ai rencontré quelques difficultés lors des tests via l'interface navigable de Django REST Framework, notamment concernant les méthodes HTTP autorisées (`GET` et `POST`) ainsi que l'envoi des données nécessaires aux actions personnalisées. L'accès initial à certaines routes se faisait avec une requête `GET`, alors que les actions comme `borrow` et `returnbook` étaient volontairement limitées à la méthode `POST`. J'ai dû comprendre que l'interface DRF permettait d'afficher un formulaire associé à l'action.

Une difficulté particulière concernait la route `borrow`, qui est rattachée au `BookViewSet` car elle représente l'action "emprunter un livre". Cependant, le formulaire affiché par défaut utilisait le `BookSerializer`, car l'action appartenait au ViewSet des livres. J'ai donc dû mettre en place un serializer spécifique pour cette action (BorrowSerializer) et utiliser `get_serializer_class()` afin que DRF utilise le `BorrowSerializer` uniquement lors de l'appel à cette route.

Cette compréhension du fonctionnement des serializers associés aux actions personnalisées m'a permis de corriger le comportement du formulaire et de mieux comprendre la manière dont Django REST Framework gère les différentes actions d'un ViewSet.

Ces difficultés m'ont surtout permis de mieux comprendre la manière dont Django REST Framework structure une API et comment organiser les différentes responsabilités dans une application.

---

## Possible improvements

Plusieurs axes d'amélioration pourraient être envisagés avec davantage de temps :

  - Renforcer la validation des données, par exemple avec l'ISBN je rajouterais des règles plus strictes sur son format et     sa longueur afin de garantir une meilleure cohérence des données enregistrées.

  - Ajouter davantage de possibilités de filtrage, par exemple en permettant de filtrer les livres selon leur année de          publication.

  - Mettre en place des tests automatisés couvrant les principales fonctionnalités et règles métier si c'était un projet de     plus grande envergure.

  - Étudier une séparation plus poussée de la logique métier dans des services dédiés. Pour ce projet de taille limitée, la     logique présente dans les ViewSets était largement suffisante, mais pour un projet de plus grande envergure tenter cette     approche serait logique

  - Ajouter certaines contraintes directement au niveau du modèle Django et de la base de données afin d'alléger certaines     règles métiers. Cela nécessiterait cependant de modifier les modèles et de générer de nouvelles migrations, ce que           j'ai éviter de faire afin de privilégier l'implémentation des fonctionnalités demandées.
