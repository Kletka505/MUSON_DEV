from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Sequence

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("birthdate", String, nullable=False),
    Column("phone_number", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

news = Table(
    "news",
    metadata,
    Column("news_id", Integer, primary_key=True),
    Column("title", String),
    Column("image_path", String),
    Column("content", String),
    Column("date", String),

)
releases = Table(
    "releases",
    metadata,
    Column("release_id", Integer, primary_key=True),
    Column("artist", String),
    Column("title", String),
    Column("image_path", String),
    Column("archive_path", String),
    Column("content", String),
    Column("link", String),
)
comments = Table(
    "comments",
    metadata,
    Column("comment_id", Integer, primary_key=True, autoincrement=True),
    Column("release_id", Integer, ForeignKey("releases.release_id"), nullable=False),
    Column("id", Integer, ForeignKey("user.id"), nullable=True),
    Column("content", String)

)

likes = Table(
    "likes",
    metadata,
    Column("like_id", Integer, primary_key=True, autoincrement=True),
    Column("id", Integer, ForeignKey("user.id"), nullable=True),
    Column("release_id", Integer, ForeignKey("releases.release_id"), nullable=False),
)
