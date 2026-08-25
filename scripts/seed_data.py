from datetime import datetime,timedelta
import random
from sqlalchemy import delete
from app.db import SessionLocal
from app.models import Customer,Transaction,Alert,Investigation
random.seed(42);db=SessionLocal()
for m in [Investigation,Alert,Transaction,Customer]:db.execute(delete(m))
db.commit()
people=[("Jordan Lee","MA","low"),("Maya Patel","NJ","low"),("Daniel Brooks","NY","medium"),("Sofia Martinez","TX","low"),("Ethan Kim","CA","low"),("Avery Johnson","IL","medium"),("Noah Williams","PA","low"),("Olivia Chen","WA","low")]
base=datetime(2026,7,1,9)
for name,state,risk in people:
    c=Customer(name=name,home_state=state,risk_tier=risk);db.add(c);db.flush()
    for i in range(24):
        db.add(Transaction(customer_id=c.id,occurred_at=base+timedelta(days=i*2,hours=random.randint(0,8)),amount=round(random.uniform(25,650),2),transaction_type=random.choice(["card","ach","transfer"]),counterparty=random.choice(["Utility Co","Market Street","Metro Wireless","Rent Services","Online Retail"]),state=state,is_new_counterparty=0))
for cid,vals in [(1,[8900,9200,9700]),(3,[8700,9100,9600,8800])]:
    for j,amt in enumerate(vals):
        db.add(Transaction(customer_id=cid,occurred_at=datetime(2026,8,20,10)+timedelta(hours=j*4),amount=amt,transaction_type="transfer",counterparty=f"New Recipient {cid}-{j+1}",state="FL" if cid==1 else "NV",is_new_counterparty=1))
db.commit();db.close();print("Seeded synthetic customers and transactions.")
