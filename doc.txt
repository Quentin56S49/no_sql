### **Lancer et utiliser l'application**

#### **1. Prérequis**
- Assurez-vous d'avoir Python installé sur votre machine.
- Installez les dépendances nécessaires en utilisant `pip` :
  ```sh
  pip install fastapi uvicorn neo4j pymongo python-dotenv
  ```

#### **2. Mettre en place MongoDB en local**
- Téléchargez et installez MongoDB Community Edition depuis le site officiel : https://www.mongodb.com/try/download/community
- Suivez les instructions d'installation pour votre système d'exploitation.
- Démarrez le serveur MongoDB en exécutant la commande suivante dans un terminal :
  ```sh
  mongod --dbpath <path_to_your_db_directory>
  ```
  Remplacez `<path_to_your_db_directory>` par le chemin vers le répertoire où vous souhaitez stocker les données MongoDB.

#### **3. Insérer les données dans MongoDB**
- Assurez-vous que le serveur MongoDB est en cours d'exécution.
- Ouvrez un terminal et naviguez vers le répertoire contenant le fichier `movies.json`.
- Exécutez la commande suivante pour insérer les données dans la base de données MongoDB :
  ```sh
  mongoimport --db crunchbase-c --collection movies --file movies.json --jsonArray
  ```
- Cette commande va importer les données du fichier `movies.json` dans la collection `movies` de la base de données `crunchbase-c`.

#### **4. Mettre en place Neo4j en local**
- Téléchargez et installez Neo4j Desktop depuis le site officiel : https://neo4j.com/download/
- Suivez les instructions d'installation pour votre système d'exploitation.
- Démarrez Neo4j Desktop et créez une nouvelle base de données locale.
- Notez l'URI, le nom d'utilisateur et le mot de passe de votre base de données Neo4j.

#### **5. Lancer l'application**
- Ouvrez un terminal et naviguez vers le répertoire contenant vos fichiers `main.py` et `routesNeo4j.py`.
- Exécutez la commande suivante pour démarrer le serveur FastAPI :
  ```sh
  uvicorn main:app --reload
  ```
- Le serveur sera démarré et accessible à l'adresse `http://127.0.0.1:8000`.

#### **6. Utiliser l'application**
- Ouvrez votre navigateur et accédez à `http://127.0.0.1:8000/docs` pour voir la documentation interactive générée par Swagger.
- Vous pouvez tester les différentes routes directement depuis cette interface.

#### **7. Routes disponibles**

Les routes pour MongoDB :

#### **1. Lister tous les films**
- **Point de terminaison** : `/movies`
- **Méthode HTTP** : GET
- **Description** : Renvoie la liste de tous les films présents dans la base de données MongoDB.
- **Paramètres** : Aucun.
- **Réponse attendue** : Une liste contenant les titres de tous les films.
  - **Exemple de réponse** :
    ```json
    ["Inception", "The Matrix", "Interstellar"]
    ```

#### **2. Rechercher un film**
- **Point de terminaison** : `/movies/search`
- **Méthode HTTP** : GET
- **Description** : Rechercher un ou plusieurs films en fonction du titre du film ou d'un acteur.
- **Paramètres** :
  - `name` (optionnel) : Le titre du film recherché.
  - `actor` (optionnel) : Le nom d'un acteur.
- **Comportement** :
  - Si `name` est fourni, retourne les films correspondant au titre donné.
  - Si `actor` est fourni, retourne les films où cet acteur figure.
  - Si aucun paramètre n'est fourni, une erreur 400 est levée.
- **Réponses attendues** :
  - **Succès (films trouvés)** :
    ```json
    [
        {
            "id": "64c8...",
            "title": "Inception",
            "plot": "A skilled thief is offered a chance to have his past crimes forgiven...",
            "genres": ["Action", "Sci-Fi"],
            "runtime": 148,
            "directors": ["Christopher Nolan"],
            "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"],
            "year": 2010
        }
    ]
    ```
  - **Erreur 404 (aucun film trouvé)** :
    ```json
    {"detail": "No movie found with the given criteria."}
    ```

#### **3. Ajouter un film**
- **Point de terminaison** : `/movies`
- **Méthode HTTP** : POST
- **Description** : Ajouter un nouveau film à la base de données.
- **Paramètres** : Corps de la requête en JSON contenant les informations du film. Exemple :
  ```json
  {
      "title": "Inception",
      "plot": "A skilled thief is offered a chance to have his past crimes forgiven...",
      "genres": ["Action", "Sci-Fi"],
      "runtime": 148,
      "directors": ["Christopher Nolan"],
      "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"],
      "year": 2010
  }
  ```
- **Comportement** :
  - Si un film avec le même titre existe déjà, une erreur 400 est levée.
- **Réponses attendues** :
  - **Succès** :
    ```json
    {"id": "64c8...", "message": "Movie added successfully."}
    ```
  - **Erreur 400 (film existant)** :
    ```json
    {"detail": "Movie with this title already exists."}
    ```

#### **4. Mettre à jour un film**
- **Point de terminaison** : `/movies/{title}`
- **Méthode HTTP** : PUT
- **Description** : Met à jour les informations d'un film existant en fonction de son titre.
- **Paramètres** :
  - `title` (dans l'URL) : Le titre du film à mettre à jour.
  - Corps de la requête en JSON contenant les champs à mettre à jour. Exemple :
    ```json
    {
        "plot": "A thief with the ability to enter people's dreams and steal secrets...",
        "runtime": 150
    }
    ```
- **Comportement** :
  - Seuls les champs spécifiés dans le corps de la requête sont mis à jour.
  - Si aucun champ valide n'est fourni, une erreur 400 est levée.
  - Si le film n'est pas trouvé, une erreur 404 est levée.
- **Réponses attendues** :
  - **Succès** :
    ```json
    {"message": "Movie updated successfully."}
    ```
  - **Erreur 404 (film non trouvé)** :
    ```json
    {"detail": "Movie not found."}
    ```
  - **Erreur 400 (aucun champ à mettre à jour)** :
    ```json
    {"detail": "No valid fields to update."}
    ```

Les routes pour Neo4J :

#### **1. Lister tous les films dans Neo4j**
- **Point de terminaison** : `/neo4j/movies`
- **Méthode HTTP** : GET
- **Description** : Renvoie la liste de tous les films présents dans la base de données Neo4j.
- **Paramètres** : Aucun.
- **Réponse attendue** : Une liste contenant les détails de chaque film, notamment son identifiant, titre, tagline, année de sortie, et elementId.
  - **Exemple de réponse** :
    ```json
    [
        {
            "identity": 12345,
            "title": "Inception",
            "tagline": "Your mind is the scene of the crime",
            "released": 2010,
            "elementId": "0:12345"
        },
        {
            "identity": 67890,
            "title": "The Matrix",
            "tagline": "Welcome to the Real World",
            "released": 1999,
            "elementId": "0:67890"
        }
    ]
    ```

#### **2. Compter les films communs entre MongoDB et Neo4j**
- **Point de terminaison** : `/neo4j/common-movies-count`
- **Méthode HTTP** : GET
- **Description** : Renvoie le nombre de films ayant le même titre dans les bases de données MongoDB et Neo4j.
- **Paramètres** : Aucun.
- **Réponse attendue** : Un objet JSON contenant le nombre de films communs.
  - **Exemple de réponse** :
    ```json
    {"common_movies_count": 42}
    ```

#### **3. Obtenir les critiques d'un film**
- **Point de terminaison** : `/neo4j/movie-reviewers`
- **Méthode HTTP** : GET
- **Description** : Renvoie une liste des personnes ayant écrit une critique pour un film spécifique.
- **Paramètres** :
  - `movie_title` (obligatoire) : Le titre du film.
- **Réponse attendue** : Une liste des noms des critiques.
  - **Exemple de réponse** :
    ```json
    {"reviewers": ["Alice", "Bob", "Charlie"]}
    ```
- **Erreur possible** :
  - **Erreur 500 (erreur serveur)** : En cas de problème avec la requête Neo4j ou d'autres erreurs.

#### **4. Obtenir les films notés par un utilisateur**
- **Point de terminaison** : `/neo4j/user-ratings`
- **Méthode HTTP** : GET
- **Description** : Renvoie le nombre de films notés par un utilisateur spécifique et une liste des films correspondants.
- **Paramètres** :
  - `user_name` (obligatoire) : Le nom de l'utilisateur.
- **Réponse attendue** : Un objet JSON contenant le nom de l'utilisateur, le nombre total de films qu'il a notés et la liste des titres de ces films.
  - **Exemple de réponse** :
    ```json
    {
        "user": "Alice",
        "number_of_rated_movies": 3,
        "rated_movies": ["Inception", "The Matrix", "Interstellar"]
    }
    ```
- **Erreur possible** :
  - **Erreur 500 (erreur serveur)** : En cas de problème avec la requête Neo4j ou d'autres erreurs.

