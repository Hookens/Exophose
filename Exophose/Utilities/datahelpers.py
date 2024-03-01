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