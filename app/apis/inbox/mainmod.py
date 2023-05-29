from __future__ import annotations

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Any
from loguru import logger
from datetime import datetime

from app.apis.inbox.submod import get_all_countries_from_pg

def get_all_inbox_by_profile_uuid(db_session, profile_name_uuid):

    try:
        result = None
        if profile_name_uuid == "xx-xx-001":
            result = [
                {
                    "id" : 0,
                    "group_informaion_uuid" : "group_informaion_uuid-01",
                    "title_chat" : "Figma Plugins",
                    "short_text" : "IOS 13 Design Kit.",
                    "activity_date" : "Sun"
                },
                {
                    "id" : 1,
                    "message_uuid" : "message_uuid-01",
                    "title_chat" : "John Connor",
                    "short_text" : "John Connor is a fictional character in the Terminator franchise.",
                    "activity_date" : "2023-02-22 00:40:29.775332"
                },
            ]
        elif profile_name_uuid == "xx-xx-002":
            result = [
                {
                    "id" : 0,
                    "group_informaion_uuid" : "group_informaion_uuid-02",
                    "title_chat" : "Figma Plugins",
                    "short_text" : "IOS 13 Design Kit.",
                    "activity_date" : "Sun"
                },
                {
                    "id" : 1,
                    "message_uuid" : "message_uuid-01",
                    "title_chat" : "John Connor",
                    "short_text" : "John Connor is a fictional character in the Terminator franchise.",
                    "activity_date" : "2023-02-22 00:40:29.775332"
                },
            ]

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

def get_all_user_history_by_message_uuid(db_session, message_uuid):

    try:
        result = None
        if message_uuid == "message_uuid-01":
            result = [
                {
                    "title_chat" : "John Connor chat",
                    "total_members" : 2,
                    "members" : [
                        {
                            "id" : 0,
                            "username"  : "John Connor",
                        },
                        {
                            "id" : 1,
                            "username"  : "แมวกระโดด8เมตร",
                        },
                    ],
                    "content_chat" : [
                        {
                            "id" : 0,
                            "text"  : "Do you like it?",
                            "activity_date" : "2023-02-22 00:40:29.775332",
                            "file" : f""
                        },
                        {
                            "id" : 1,
                            "text"  : "i think top two are:",
                            "activity_date" : "2023-02-22 00:40:29.775332",
                            "file" : f"https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Fishcake_Kimbap_%2816329470757%29.jpg/480px-Fishcake_Kimbap_%2816329470757%29.jpg"
                        },
                    ]
                }
            ]

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

def get_all_group_history_by_group_uuid(db_session, group_informaion_uuid):

    try:
        result = None
        if group_informaion_uuid == "group_informaion_uuid-01":
            result = [
                {
                    "title_chat" : "Martha chat",
                    "total_members" : 2,
                    "members" : [
                        {
                            "id" : 0,
                            "username"  : "Martha",
                        },
                        {
                            "id" : 1,
                            "username"  : "แมวกระโดด8เมตร",
                        },
                    ],
                    "content_chat" : [
                        {
                            "id" : 0,
                            "text"  : "Do you like it?",
                            "activity_date" : "2023-02-22 00:40:29.775332",
                            "file" : f""
                        },
                        {
                            "id" : 1,
                            "text"  : "i think top two are:",
                            "activity_date" : "2023-02-22 00:40:29.775332",
                            "file" : f"https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Fishcake_Kimbap_%2816329470757%29.jpg/480px-Fishcake_Kimbap_%2816329470757%29.jpg"
                        },
                    ]
                }
            ]

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