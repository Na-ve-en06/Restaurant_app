from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.DB import get_db_connection
from app.schemas import Token
from app.utils import verify_password
from app.oauth2 import create_access_token

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM user_info WHERE email_id = %s",
                (user_credentials.username,)
            )
            user = cur.fetchone()
            print(user)

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid credentials (user not found)"
                )

            if not verify_password(user_credentials.password, user["password"]):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid credentials (wrong password)"
                )

            access_token = create_access_token(
                data={"user_id": user["user_id"]}
            )

            return {"access_token": access_token, "token_type": "bearer"}

# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from app.DB import get_db_connection
# from app.utils import verify_password
# from app.oauth2 import create_access_token
# from app.schemas import Token

# router = APIRouter(tags=["Authentication"])

# @router.post("/login", response_model=Token)
# def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
#     with get_db_connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute("SELECT * FROM user_info WHERE email_id = %s", (user_credentials.username,))
#             user = cur.fetchone()
#             print(user)
#             if not user:
#                 raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")

#             if not verify_password(user_credentials.password, user["password"]):
#                 raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")

#             access_token = create_access_token(data={"user_id": user["user_id"]})
#             return {"access_token": access_token, "token_type": "bearer"}
