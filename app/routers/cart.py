from .. import schemas
from fastapi import HTTPException,APIRouter
from app.DB import get_db_connection
from app.schemas import CartItemRequest

router = APIRouter(
    tags=['cart']
)
@router.post("/cart")
def add_to_cart(item: CartItemRequest):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Always get price from DB!
            cur.execute("SELECT price FROM menu_table WHERE menu_id = %s", (item.menu_id,))
            row = cur.fetchone()
            print(row)
            if not row:
                raise HTTPException(status_code=404, detail="Menu item not found!")

            # ✅ Use index 0
            price = row["price"]

            
            # Insert with real price
            cur.execute(
                "INSERT INTO cart_items (user_id, menu_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (item.user_id, item.menu_id, item.quantity, price)
            )
        conn.commit()
    return {"message": "Item added to cart!"}


@router.get("/cart/{user_id}")
def view_cart(user_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.menu_id, m.menu_name, m.price, c.quantity
                FROM cart_items c
                JOIN menu_table m ON c.menu_id = m.menu_id
                WHERE c.user_id = %s
            """, (user_id,))
            rows = cur.fetchall()

            if not rows:
                # ✅ Return 404 or 200 with custom message
                raise HTTPException(status_code=404, detail="❌ This user has no items in the cart!")

            items = [dict(row) for row in rows]

            return {"cart": items}
