# routesNeo4j.py
from fastapi import APIRouter, HTTPException, FastAPI
from neo4j import GraphDatabase
from typing import List
from pymongo import MongoClient
from models import Neo4jMovie
import os

# Connection to Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j1")
NEO4J_PASS = os.getenv("NEO4J_PASS", "password")
NEO4J_DB = "neo4j"

neo4j_driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASS)
)

# Connection to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client['crunchbase-c']
collection = db['movies']

router = APIRouter()


@router.get("/movies", response_model=List[Neo4jMovie])
async def get_all_neo4j_movies():
    try:
        with neo4j_driver.session(database=NEO4J_DB) as session:
            result = session.run("MATCH (m:Movie) RETURN m")
            movies = []
            for record in result:
                movie_node = record["m"]
                movie = Neo4jMovie(
                    identity=movie_node.id,
                    title=movie_node["title"],
                    tagline=movie_node.get("tagline"),
                    released=movie_node["released"],
                    elementId=movie_node.element_id
                )
                movies.append(movie)
            return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/common-movies-count")
async def get_common_movies_count():
    try:
        # Fetch movie titles from MongoDB
        mongo_movies = set(collection.distinct("title"))

        # Fetch movie titles from Neo4j
        with neo4j_driver.session(database=NEO4J_DB) as session:
            result = session.run("MATCH (m:Movie) RETURN m.title AS title")
            neo4j_movies = set(record["title"] for record in result)

        # Find the intersection of the two sets
        common_movies = mongo_movies.intersection(neo4j_movies)

        return {"common_movies_count": len(common_movies)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/movie-reviewers")
async def get_movie_reviewers(movie_title: str):
    try:
        with neo4j_driver.session(database=NEO4J_DB) as session:
            result = session.run(
                "MATCH (p:Person)-[:REVIEWED]->(m:Movie) "
                "WHERE m.title = $title "
                "RETURN p.name AS name",
                title=movie_title
            )
            reviewers = [record["name"] for record in result]
            return {"reviewers": reviewers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-ratings")
async def get_user_ratings(user_name: str):
    try:
        with neo4j_driver.session(database=NEO4J_DB) as session:
            result = session.run(
                "MATCH (p:Person)-[r:REVIEWED]->(m:Movie) "
                "WHERE p.name = $name "
                "RETURN m.title AS title",
                name=user_name
            )
            rated_movies = [record["title"] for record in result]
            return {
                "user": user_name,
                "number_of_rated_movies": len(rated_movies),
                "rated_movies": rated_movies
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))