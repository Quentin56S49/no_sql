# main.py
from fastapi import FastAPI
from routes import router as mongo_router
from routesNeo4j import router as neo4j_router
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI instance
app = FastAPI()

# Include the MongoDB router
app.include_router(mongo_router)

# Include the Neo4j router with a prefix
app.include_router(neo4j_router, prefix="/neo4j")
