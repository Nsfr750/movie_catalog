# struttura/movie_metadata.py
import os
import json
import requests
from typing import Dict, Optional, List
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MovieMetadata:
    title: str
    year: int
    overview: str
    poster_url: str
    backdrop_url: str
    genres: List[str]
    rating: float
    runtime: int
    director: str
    cast: List[Dict[str, str]]
    imdb_id: str

class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"
    
    def __init__(self, api_key: str, language: str = "en-US"):
        self.api_key = api_key
        self.language = language
        self.session = requests.Session()
        self.session.params = {
            'api_key': self.api_key,
            'language': self.language
        }
    
    def search_movie(self, query: str, year: Optional[int] = None) -> Optional[Dict]:
        """Search for a movie by title."""
        params = {'query': query}
        if year:
            params['year'] = year
            
        response = self.session.get(
            f"{self.BASE_URL}/search/movie",
            params=params
        )
        response.raise_for_status()
        results = response.json().get('results', [])
        return results[0] if results else None
    
    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """Get detailed information about a movie."""
        response = self.session.get(
            f"{self.BASE_URL}/movie/{movie_id}",
            params={'append_to_response': 'credits'}
        )
        response.raise_for_status()
        return response.json()
    
    def get_metadata(self, title: str, year: Optional[int] = None) -> Optional[MovieMetadata]:
        """Get complete metadata for a movie."""
        search_result = self.search_movie(title, year)
        if not search_result:
            return None
            
        details = self.get_movie_details(search_result['id'])
        if not details:
            return None
            
        # Get director from credits
        director = next(
            (crew['name'] for crew in details['credits']['crew'] 
             if crew['job'] == 'Director'),
            'Unknown'
        )
        
        # Get top 5 cast members
        cast = [
            {'name': actor['name'], 'character': actor['character']}
            for actor in details['credits']['cast'][:5]
        ]
        
        # Build poster and backdrop URLs
        base_image_url = "https://image.tmdb.org/t/p/original"
        poster_path = details.get('poster_path')
        backdrop_path = details.get('backdrop_path')
        
        return MovieMetadata(
            title=details['title'],
            year=int(details['release_date'][:4]) if details.get('release_date') else year,
            overview=details['overview'],
            poster_url=f"{base_image_url}{poster_path}" if poster_path else "",
            backdrop_url=f"{base_image_url}{backdrop_path}" if backdrop_path else "",
            genres=[genre['name'] for genre in details.get('genres', [])],
            rating=details.get('vote_average', 0),
            runtime=details.get('runtime', 0),
            director=director,
            cast=cast,
            imdb_id=details.get('imdb_id', '')
        )