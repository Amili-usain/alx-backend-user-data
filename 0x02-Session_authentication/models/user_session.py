#!/usr/bin/env python3
"""
Module for UserSession class
"""
from models.base import Base


class UserSession(Base):
    """ UserSession class represents a user session.
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a new UserSession object.
        Args:
            *args (list): Positional arguments.
            **kwargs (dict): Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
