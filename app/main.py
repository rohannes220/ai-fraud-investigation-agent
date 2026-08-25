from pathlib import Path
from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select,func
from app.db import get_db
from app.models import Customer,Transaction,Alert
from app.services.rules import scan_all
from app.services.investigator import investigate
app=FastAPI(title="AI Fraud Investigation Agent")
STATIC=Path(__file__).parent/"static"
@app.get("/")
def home():return FileResponse(STATIC/"index.html")
@app.get("/health")
def health():return {"status":"ok"}
@app.get("/dashboard")
def dashboard(db=Depends(get_db)):
    return {"customers":db.scalar(select(func.count(Customer.id))),"transactions":db.scalar(select(func.count(Transaction.id))),"alerts":db.scalar(select(func.count(Alert.id))),"high_risk_alerts":db.scalar(select(func.count(Alert.id)).where(Alert.severity=="high"))}
@app.get("/alerts")
def alerts(db=Depends(get_db)):
    rows=db.execute(select(Alert,Customer).join(Customer).order_by(Alert.score.desc())).all()
    return [{"id":a.id,"customer":c.name,"rule":a.rule_name,"severity":a.severity,"score":a.score,"explanation":a.explanation} for a,c in rows]
@app.post("/scan")
def scan(db=Depends(get_db)):return {"alerts_created":len(scan_all(db))}
@app.post("/alerts/{alert_id}/investigate")
def inv(alert_id:int,db=Depends(get_db)):
    try:x=investigate(db,alert_id)
    except ValueError as e:raise HTTPException(404,str(e))
    return {"id":x.id,"report":x.report}
app.mount("/static",StaticFiles(directory=STATIC),name="static")
