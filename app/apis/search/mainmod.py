from __future__ import annotations

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Any
from loguru import logger
from datetime import datetime

from app.apis.search.submod import get_all_countries_from_pg

def get_all_search(db_session, type_search, text_seatch):

    try:
        result = None
        if type_search == "Users":
            if text_seatch == "cat":
                result = {
                    "search_Users" : [
                        {
                            "id" : 0,
                            "profile_url" : f"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Cat_-_different_coloured_eyes_%282005_photo%3B_cropped_2022%29.JPG/480px-Cat_-_different_coloured_eyes_%282005_photo%3B_cropped_2022%29.JPG",
                            "profile_name" : "Cat Sarnya",
                            "username" : "sarny9",
                            "follwers" : 100
                        },
                        {
                            "id" : 1,
                            "profile_url" : f"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Cat_with_clipped_ear_%28cropped%29.jpg/480px-Cat_with_clipped_ear_%28cropped%29.jpg",
                            "profile_name" : "Cat Sarn",
                            "username" : "sarny9",
                            "follwers" : 100
                        },
                        {
                            "id" : 2,
                            "profile_url" : f"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/A_cat_%286513884943%29.jpg/480px-A_cat_%286513884943%29.jpg",
                            "profile_name" : "Cat",
                            "username" : "sarny9",
                            "follwers" : 100
                        },
                    ]
                }
            elif text_seatch == "dog":
                result = {
                    "search" : [
                        {
                            "id" : 0,
                            "profile_url" : f"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Cat_-_different_coloured_eyes_%282005_photo%3B_cropped_2022%29.JPG/480px-Cat_-_different_coloured_eyes_%282005_photo%3B_cropped_2022%29.JPG",
                            "profile_name" : "dog Sarnya",
                            "username" : "sarny9",
                            "follwers" : 100
                        },
                        {
                            "id" : 1,
                            "profile_url" : f"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Cat_with_clipped_ear_%28cropped%29.jpg/480px-Cat_with_clipped_ear_%28cropped%29.jpg",
                            "profile_name" : "dog Sarn",
                            "username" : "sarny9",
                            "follwers" : 100
                        },
                        {
                            "id" : 2,
                            "profile_url" : f"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/A_cat_%286513884943%29.jpg/480px-A_cat_%286513884943%29.jpg",
                            "profile_name" : "dog",
                            "username" : "sarny9",
                            "follwers" : 100
                        },
                    ]
                }
        elif type_search == "Media":
            if text_seatch == "cat":
                result = {
                    "search_Media" : "Media cat"
                }

        elif type_search == "Hashtags":
            if text_seatch == "dog":
                result = {
                    "search_Media" : "Media dog"
                }

        if result == None:
            raise HTTPException(status_code=404, detail='Not Found')
        if "error_code" in result:
            raise HTTPException(status_code=400, detail='{}'.format(result["msg"]))

        return result
    except Exception as e:
        logger.error(f"{e}")
        if isinstance(e, HTTPException):
            raise
        else:
            raise HTTPException(status_code=500, detail='internal server error: {0}'.format(e))