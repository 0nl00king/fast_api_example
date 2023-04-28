from main import app


@app.get("/")
async def root():
    return {"message": "main_page"}
