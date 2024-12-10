from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from typing import Optional
from models import Movie, UpdateMovie


# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client['crunchbase']
collection = db['movies']

router = APIRouter()

def serialize_movie(movie):
    return {
        "id": str(movie["_id"]),
        "title": movie.get("title", "Unknown"),
        "plot": movie.get("plot", "No plot available"),
        "genres": movie.get("genres", []),
        "runtime": movie.get("runtime", 0),
        "directors": movie.get("directors", []),
        "cast": movie.get("cast", []),
        "year": movie.get("year", None),
    }

# Route pour lister tous les films
@router.get("/movies")
async def list_all_movies():
    try:
        movies = db.movies.find({}, {"title": 1, "_id": 0})
        return [movie["title"] for movie in movies if "title" in movie]
    except Exception as e:
        return {"error": str(e)}

# Route pour rechercher un film
@router.get("/movies/search")
async def get_movie(name: Optional[str] = None, actor: Optional[str] = None):
    query = {}
    if name:
        query["title"] = name
    elif actor:
        query["cast"] = actor
    else:
        raise HTTPException(status_code=400, detail="Provide either 'name' or 'actor' as a parameter.")

    movies = list(collection.find(query))
    if not movies:
        raise HTTPException(status_code=404, detail="No movie found with the given criteria.")
    return [serialize_movie(movie) for movie in movies]

# Route pour ajouter un film
@router.post("/movies")
async def add_movie(movie: Movie):
    if collection.find_one({"title": movie.title}):
        raise HTTPException(status_code=400, detail="Movie with this title already exists.")
    result = collection.insert_one(movie.dict())
    return {"id": str(result.inserted_id), "message": "Movie added successfully."}

# Route pour mettre à jour un film
@router.put("/movies/{title}")
async def update_movie(title: str, updates: UpdateMovie):
    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update.")

    result = collection.update_one({"title": title}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found.")
    return {"message": "Movie updated successfully."}


