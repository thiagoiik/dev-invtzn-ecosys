import os
import requests
from django.conf import settings

class UnsplashService:
    API_URL = "https://api.unsplash.com/search/photos"

    @classmethod
    def search_photos(cls, query, page=1, per_page=20):
        access_key = getattr(settings, 'UNSPLASH_ACCESS_KEY', '')
        if not access_key:
            return {"results": [], "total": 0, "total_pages": 0, "error": "UNSPLASH_ACCESS_KEY no está configurada."}

        headers = {
            "Authorization": f"Client-ID {access_key}",
            "Accept-Version": "v1"
        }
        params = {
            "query": query,
            "page": page,
            "per_page": per_page
        }

        try:
            response = requests.get(cls.API_URL, headers=headers, params=params, timeout=10)
            if response.status_code != 200:
                return {"results": [], "total": 0, "total_pages": 0, "error": f"Error Unsplash API ({response.status_code}): {response.text}"}
            
            data = response.json()
            results = []
            for item in data.get("results", []):
                results.append({
                    "id": item.get("id"),
                    "url": item.get("urls", {}).get("regular"),
                    "thumb": item.get("urls", {}).get("small"),
                    "author": item.get("user", {}).get("name"),
                    "author_link": item.get("user", {}).get("links", {}).get("html")
                })
            
            return {
                "results": results,
                "total": data.get("total", 0),
                "total_pages": data.get("total_pages", 0)
            }
        except requests.exceptions.RequestException as e:
            return {"results": [], "total": 0, "total_pages": 0, "error": f"Fallo de conexión a Unsplash: {str(e)}"}

class JamendoService:
    API_URL = "https://api.jamendo.com/v3.0/tracks/"

    @classmethod
    def search_tracks(cls, query, limit=20):
        client_id = getattr(settings, 'JAMENDO_CLIENT_ID', '')
        if not client_id:
            return {"results": [], "error": "JAMENDO_CLIENT_ID no está configurada."}

        params = {
            "client_id": client_id,
            "format": "json",
            "limit": limit,
            "audioformat": "mp32",
            "search": query
        }

        try:
            response = requests.get(cls.API_URL, params=params, timeout=10)
            if response.status_code != 200:
                return {"results": [], "error": f"Error Jamendo API ({response.status_code}): {response.text}"}
            
            data = response.json()
            results = []
            for item in data.get("results", []):
                results.append({
                    "id": item.get("id"),
                    "title": item.get("name"),
                    "artist": item.get("artist_name"),
                    "duration": item.get("duration"),
                    "cover": item.get("album_image"),
                    "audio": item.get("audio")
                })
            
            return {
                "results": results
            }
        except requests.exceptions.RequestException as e:
            return {"results": [], "error": f"Fallo de conexión a Jamendo: {str(e)}"}

