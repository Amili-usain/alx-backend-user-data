#!/usr/bin/env python3
"""
Module for authentication using Session auth
"""

from .auth import Auth
from models.user import User
from uuid import uuid4

class SessionAuth(Auth):
    """ SessionAuth class provides authentication using session IDs.
    """

    user_id_by_session_id = {}  # Dictionary to store user IDs by session IDs

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session for the specified user.
        Args:
            user_id (str, optional): ID of the user. Defaults to None.
        Returns:
            str: The generated session ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with the specified session ID.
        Args:
            session_id (str, optional): The session ID. Defaults to None.
        Returns:
            str: The user ID associated with the session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the currently authenticated user based on the session ID i
the request.
        Args:
            request (object, optional): The request object. Defaults to None.
        Returns:
            object: User object representing the currently authenticated user.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
        Destroys the session associated with the session ID in the request.
        Args:
            request (object, optional): The request object. Defaults to None.
        Returns:
            bool: True if session was destroyed successfully, False otherwise.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
