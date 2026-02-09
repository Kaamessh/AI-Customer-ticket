from fastapi import FastAPI

app = FastAPI(title="AI Customer Ticket")


@app.get("/")
async def root():
    return {"message": "Welcome to the AI Customer Ticket API!"}
