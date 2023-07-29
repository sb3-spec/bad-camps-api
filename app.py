from fastapi import FastAPI, Depends, Request, Form, status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from algoliasearch.search_client import SearchClient

from sqlalchemy.orm import Session
from db import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

client = SearchClient.create("XMRKYIS0X8", "8d3b9f33bc2480e85964011f4b4af319")


app = FastAPI()
# Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db 
    finally:
        db.close()
        
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("base.html",
                                      {"request": request})
    
    
@app.post("/add")
async def add(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    
    if type(body) == list:
        
        for item in body:
            try:
                new_camp = models.Camp(name=item["name"], description=item["description"])
            except:
                return {"error": "Could not add to db"}
            
            db.add(new_camp)
            db.commit()
        return body
            
    try:
        new_camp = models.Camp(name=body["name"], description=body["description"])

    except:
        return {"error": "Could not add to db"}
    db.add(new_camp)
    db.commit()
    
    return body

@app.get("/createIndex")
async def create_index(request: Request, db: Session = Depends(get_db)):
    index = client.init_index("dev_CAMPS")
    
    camps = db.query(models.Camp).all()
    
    new_camps = [{"name": camp.name, "description": camp.description} for camp in camps]   
    
    index.replace_all_objects(new_camps, {
        'autoGenerateObjectIDIfNotExist': True
    })
    
    return camps


@app.get("/camps")
async def get_camps(request: Request, db: Session = Depends(get_db)):
    camps = db.query(models.Camp).all()
    
    return camps