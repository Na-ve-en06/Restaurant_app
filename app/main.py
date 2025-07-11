from fastapi import FastAPI
from .routers import user,cart,order,menu,auth
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

origins = ["*"]   

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,    
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(menu.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "🍔 Welcome to the Online Restaurant !!"}


