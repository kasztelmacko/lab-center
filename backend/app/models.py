import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties for User
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model for User, database table inferred from class name
class User(UserBase, table=True):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    labs: list["Lab"] = Relationship(back_populates="owner")
    user_labs: list["UserLab"] = Relationship(back_populates="user")
    borrowings: list["Borrowing"] = Relationship(back_populates="user")


# Properties to return via API for User, id is always required
class UserPublic(UserBase):
    user_id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties for Lab
class LabBase(SQLModel):
    lab_name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class LabCreate(LabBase):
    pass


# Properties to receive via API on update, all are optional
class LabUpdate(LabBase):
    lab_name: str | None = Field(default=None, max_length=255)  # type: ignore
    description: str | None = Field(default=None, max_length=255)


# Database model for Lab, database table inferred from class name
class Lab(LabBase, table=True):
    lab_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.user_id", nullable=False, ondelete="CASCADE")
    owner: User | None = Relationship(back_populates="labs")
    items: list["Item"] = Relationship(back_populates="lab")
    user_labs: list["UserLab"] = Relationship(back_populates="lab")


# Properties to return via API for Lab, id is always required
class LabPublic(LabBase):
    lab_id: uuid.UUID
    owner_id: uuid.UUID


class LabsPublic(SQLModel):
    data: list[LabPublic]
    count: int


# Shared properties for Item
class ItemBase(SQLModel):
    item_name: str = Field(max_length=255)
    quantity: int = Field(default=0)
    lab_id: uuid.UUID = Field(foreign_key="lab.lab_id", nullable=False, ondelete="CASCADE")


# Properties to receive via API on creation
class ItemCreate(ItemBase):
    pass


# Properties to receive via API on update, all are optional
class ItemUpdate(ItemBase):
    item_name: str | None = Field(default=None, max_length=255)  # type: ignore
    quantity: int | None = Field(default=None)
    lab_id: uuid.UUID | None = Field(default=None, foreign_key="lab.lab_id", ondelete="CASCADE")


# Database model for Item, database table inferred from class name
class Item(ItemBase, table=True):
    item_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    lab_id: uuid.UUID = Field(foreign_key="lab.lab_id", nullable=False, ondelete="CASCADE")
    lab: Lab | None = Relationship(back_populates="items")
    borrowings: list["Borrowing"] = Relationship(back_populates="item")


# Properties to return via API for Item, id is always required
class ItemPublic(ItemBase):
    item_id: uuid.UUID
    lab_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Database model for UserLab, database table inferred from class name
class UserLab(SQLModel, table=True):
    userlab_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.user_id", nullable=False, ondelete="CASCADE")
    lab_id: uuid.UUID = Field(foreign_key="lab.lab_id", nullable=False, ondelete="CASCADE")
    user: User | None = Relationship(back_populates="user_labs")
    lab: Lab | None = Relationship(back_populates="user_labs")

class AddUsersToLab(SQLModel):
    emails: list[EmailStr]

class RemoveUsersFromLab(SQLModel):
    emails: EmailStr


# Database model for Borrowing, database table inferred from class name
class Borrowing(SQLModel, table=True):
    borrow_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.user_id", nullable=False, ondelete="CASCADE")
    item_id: uuid.UUID = Field(foreign_key="item.item_id", nullable=False, ondelete="CASCADE")
    borrowed_at: str | None = Field(default=None)
    returned_at: str | None = Field(default=None)
    user: User | None = Relationship(back_populates="borrowings")
    item: Item | None = Relationship(back_populates="borrowings")

class BorrowItem(SQLModel):
    start_date: str
    end_date: str


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)