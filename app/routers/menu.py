from .. import schemas
from fastapi import APIRouter
from app.DB import get_db_connection


router = APIRouter(
    tags=['menu']
)

@router.get("/restaurants")
def get_restaurants(location: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name as restaurants_name,is_non_veg,offer  FROM restaurants WHERE location = %s",(location,))
            table=cur.fetchall()
            print(table)
            restaurants = [dict(table) for table in table]
            return{"restaurants": restaurants}
        

@router.get("/menu")
def get_menu(restaurant_id: int ):
    with get_db_connection() as conn:
        if not conn:
            return {"error": "Could not connect to DB"}
    with conn.cursor() as cur:
        cur.execute("SELECT menu_name,is_non_veg, price FROM menu_table WHERE restaurant_id = %s", (restaurant_id,))
        rows = cur.fetchall()
        print(rows)
        menu = [dict(row) for row in rows]
        return {"menu": menu}
    
