import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI(
    title="User Balance API",
    description="A simple service to manage users and their balances.",
    version="1.0.0",
)


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    balance: float


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    balance: float = 0.0


class TransferRequest(BaseModel):
    from_user_id: int
    to_user_id: int
    amount: float


users_db = {}
user_id_counter = 1


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user_data: CreateUserRequest):
    global user_id_counter
    for user in users_db.values():
        if user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists."
            )

    new_user = User(
        id=user_id_counter,
        name=user_data.name,
        email=user_data.email,
        balance=user_data.balance
    )
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    return new_user


@app.get("/users", response_model=List[User], tags=["Users"])
def get_users():
    return list(users_db.values())


@app.post("/transfer", status_code=status.HTTP_200_OK, tags=["Transfers"])
def transfer_money(transfer_data: TransferRequest):
    from_user = users_db.get(transfer_data.from_user_id)
    to_user = users_db.get(transfer_data.to_user_id)

    if not from_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sender user with id {transfer_data.from_user_id} not found."
        )
    if not to_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receiver user with id {transfer_data.to_user_id} not found."
        )

    if transfer_data.from_user_id == transfer_data.to_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot transfer money to yourself."
        )

    if transfer_data.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transfer amount must be positive."
        )

    if from_user.balance < transfer_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds."
        )

    from_user.balance -= transfer_data.amount
    to_user.balance += transfer_data.amount

    return {"message": f"Transfer successful. New balance for {from_user.name}: {from_user.balance}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
