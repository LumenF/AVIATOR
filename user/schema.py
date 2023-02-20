from typing import Optional

from ninja import Schema


class CreateUserSchema(Schema):

    telegram_id: int

    username: Optional[str] or None
    first_name: Optional[str] or None
    last_name: Optional[str] or None

    tel: Optional[str] or None
    email: Optional[str] or None

    language_code: Optional[str] or None
    is_premium: bool
    added_to_attachment_menu: bool
    can_join_groups: bool
    can_read_all_group_messages: bool
    supports_inline_queries: bool
    is_bot: bool

    channel: int


class ResponseCreateUserSchema(CreateUserSchema):
    is_blocked_bot: bool

    is_staff: bool
    is_ban_user: bool


class ResponseGetUserSchema(ResponseCreateUserSchema):
    pass


class UpdateUserSchema(Schema):

    telegram_id: str

    first_name: Optional[str] or None
    tel: Optional[str] or None
    email: Optional[str] or None
    city: Optional[str] or None
