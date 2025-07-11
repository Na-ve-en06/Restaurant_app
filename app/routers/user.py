from .. import schemas
from fastapi import HTTPException,APIRouter
from app.DB import get_db_connection
from app.schemas import UserCreate, UserAddressUpdate
from app.utils import hash_password  # make sure it's imported

router = APIRouter(
    tags=['users']
)


@router.post("/users")
def create_user(user: UserCreate):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT email_id FROM user_info WHERE email_id = %s", (user.email_id,))
    if cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists!")

    cur.execute("SELECT phone_number FROM user_info WHERE phone_number = %s", (user.phone_number,))
    if cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Phone number already exists!")

    # 🔒 Hash the password
    hashed_password = hash_password(user.password)

    cur.execute("""
        INSERT INTO user_info (name, email_id, phone_number, password, is_admin)
        VALUES (%s, %s, %s, %s, %s) RETURNING user_id
    """, (user.name, user.email_id, user.phone_number, hashed_password, user.is_admin))

    user_id = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return {
        "message": "✅ User created successfully!",
        "user_id": user_id
    }


@router.put("/users/{user_id}/address")
def add_address(user_id: int, address_update: UserAddressUpdate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:

            for addr in address_update.addresses:
                # If any address is marked as default, clear other defaults for this user
                if addr.is_default:
                    cur.execute(
                        "UPDATE user_address SET is_default = FALSE WHERE user_id = %s",
                        (user_id,)
                    )

                cur.execute("""
                    INSERT INTO user_address (user_id, address, city, state, zip_code, is_default)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    user_id,
                    addr.address,
                    addr.city,
                    addr.state,
                    addr.zip_code,
                    addr.is_default
                ))

            conn.commit()

    return {
        "message": f"✅ Added {len(address_update.addresses)} new address(es) for user_id {user_id}!"
    }


# @router.post("/users")
# def create_user(user: UserCreate):
#     conn = get_db_connection()
#     cur = conn.cursor()

#     # ✅ Check if email already exists
#     cur.execute("SELECT email_id FROM user_info WHERE email_id = %s", (user.email_id,))
#     if cur.fetchone():
#         cur.close()
#         conn.close()
#         raise HTTPException(status_code=400, detail="Email already exists!")

#     # ✅ Check if phone number exists
#     cur.execute("SELECT phone_number FROM user_info WHERE phone_number = %s", (user.phone_number,))
#     if cur.fetchone():
#         cur.close()
#         conn.close()
#         raise HTTPException(status_code=400, detail="Phone number already exists!")

#     # ✅ Insert new user if unique
#     cur.execute("""
#         INSERT INTO user_info (name, email_id, phone_number, password, is_admin)
#         VALUES (%s, %s, %s, %s, %s)  RETURNING user_id
#     """, (user.name, user.email_id, user.phone_number, user.password, user.is_admin))
#     user_id = cur.fetchone()
#     print(user_id)  # Gets the user_id
#     conn.commit()
#     cur.close()
#     conn.close()

#     return {
#         "message": "✅ User created successfully!",
#         "user_id": user_id
#     }