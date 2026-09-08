from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_profile import UserProfile
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest
)


def register_user(
    db: Session,
    data: RegisterRequest
) -> User:

    # 1. Check whether email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise ValueError("Email already registered")

    # 2. Create user
    user = User(
        email=data.email,
        phone=data.phone,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
        role="USER",
        is_active=True,
        is_verified=False
    )

    db.add(user)

    # Generate the user ID before creating the profile
    db.flush()

    # 3. Create user profile
    profile = UserProfile(
        user_id=user.id,
        user_type=data.user_type
    )

    db.add(profile)

    # 4. Save both records
    db.commit()

    # Refresh user with database-generated values
    db.refresh(user)

    return user


from app.core.security import verify_password, create_access_token
from app.schemas.auth import LoginRequest


def login_user(
    db: Session,
    data: LoginRequest
) -> str:

    # 1. Find user by email
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    # 2. Check whether user exists
    if not user:
        raise ValueError("Invalid email or password")

    # 3. Verify password
    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise ValueError("Invalid email or password")

    # 4. Check whether account is active
    if not user.is_active:
        raise ValueError("User account is inactive")

    # 5. Create JWT
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    return access_token