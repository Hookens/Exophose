# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from datetime import datetime

class ExoRole:
    def __init__(self, id: str, guild_id: int):
        self.id: int = int(id)
        self.guild_id = int(guild_id)

class CreatedRole(ExoRole):
    def __init__(self, id: str, guild_id: int, user_id: int, created_date: datetime):
        super().__init__(id, guild_id)
        self.user_id = int(user_id)
        self.created_date = created_date

class AllowedRole(CreatedRole):
    def __init__(self, id: str, guild_id: int, user_id: int, max_roles: int, allow_badges: bool, created_date: datetime, updated_user_id: int, updated_date: datetime):
        super().__init__(id, guild_id, user_id, created_date)
        self.max_roles = max_roles
        self.allow_badges = allow_badges
        self.updated_user_id = int(updated_user_id) if updated_user_id is not None else None
        self.updated_date = updated_date
        self.is_everyone = id == guild_id

class Bundle():
    def __init__(self, id: int, guild_id: str, name: str):
        self.id = id
        self.guild_id = int(guild_id)
        self.name = name

class BundleRole():
    def __init__(self, bundle_id: int, id: str, guild_id: str):
        self.id = int(id)
        self.bundle_id = bundle_id
        self.guild_id = int(guild_id)