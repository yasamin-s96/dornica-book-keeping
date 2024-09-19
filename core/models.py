from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from core.connections.database_connection import Base
from core.enums import *


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(sa.String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(sa.String(11), nullable=True)
    is_verified: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    role_id: Mapped[int] = mapped_column(
        sa.ForeignKey("roles.id", onupdate="CASCADE", ondelete="RESTRICT")
    )
    ip_check: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    is_active: Mapped[str] = mapped_column(sa.Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        default=sa.func.now(),
    )


class AllowedIPs(Base):
    __tablename__ = "allowed_ips"
    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT")
    )
    ip: Mapped[str] = mapped_column(sa.String(length=15))
    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        default=sa.func.now(),
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    slug: Mapped[RoleSlug] = mapped_column(sa.Enum(RoleSlug), nullable=False)

    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), server_onupdate=sa.func.now()
    )


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(
        sa.ForeignKey("roles.id", onupdate="CASCADE", ondelete="RESTRICT")
    )
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    slug: Mapped[str] = mapped_column(sa.Enum(PermissionSlug), nullable=False)

    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()
    )


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    nationality: Mapped[str] = mapped_column(sa.String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(
        sa.ForeignKey("authors.id", onupdate="CASCADE", ondelete="RESTRICT")
    )
    category_id: Mapped[int] = mapped_column(
        sa.ForeignKey("categories.id", onupdate="CASCADE", ondelete="RESTRICT")
    )
    publication_year: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    stock: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    is_active: Mapped[str] = mapped_column(sa.Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()
    )


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(
        sa.ForeignKey("books.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
        default=None,
    )
    path: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    filename: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    format: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    size: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    in_use: Mapped[bool] = mapped_column(sa.Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    parent_id: Mapped[int] = mapped_column(
        sa.ForeignKey("categories.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()
    )


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(
        sa.ForeignKey("books.id", onupdate="CASCADE", ondelete="RESTRICT")
    )
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT")
    )
    loan_date: Mapped[datetime] = mapped_column(sa.TIMESTAMP, nullable=False)
    return_date: Mapped[datetime] = mapped_column(sa.TIMESTAMP, nullable=False)
    extended: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()
    )


class LoginHistory(Base):
    __tablename__ = "login_history"

    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )

    ip_address: Mapped[str] = mapped_column(sa.String(15), nullable=False)

    login_time: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP, default=sa.func.now(), nullable=False
    )

    logout_time: Mapped[datetime] = mapped_column(sa.TIMESTAMP, nullable=True)

    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        default=sa.func.now(),
    )
