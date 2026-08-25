from datetime import timedelta
from sqlalchemy import select,delete
from app.models import Customer,Transaction,Alert
def scan_customer(db,customer_id):
    tx=list(db.scalars(select(Transaction).where(Transaction.customer_id==customer_id).order_by(Transaction.occurred_at)))
    if not tx:return []
    alerts=[]
    def add(name,severity,score,reason,ids):
        a=Alert(customer_id=customer_id,rule_name=name,severity=severity,score=score,explanation=reason,transaction_ids=",".join(map(str,ids)));db.add(a);alerts.append(a)
    amounts=sorted(x.amount for x in tx); median=amounts[len(amounts)//2]
    large=[x for x in tx if x.amount>=max(5000,median*8)]
    if large:add("Unusual transaction size","high",80,f"{len(large)} transaction(s) were at least $5,000 and far above the customer's median transaction of ${median:,.2f}.",[x.id for x in large[-5:]])
    transfers=[x for x in tx if x.transaction_type=="transfer" and x.amount>=3000]
    for i,x in enumerate(transfers):
        window=[y for y in transfers[i:] if y.occurred_at<=x.occurred_at+timedelta(hours=24)]
        if len(window)>=3:
            add("Rapid large transfers","high",90,f"{len(window)} transfers of at least $3,000 occurred within 24 hours, totaling ${sum(y.amount for y in window):,.2f}.",[y.id for y in window]);break
    near=[x for x in tx if x.transaction_type=="transfer" and 8500<=x.amount<10000]
    if len(near)>=3:add("Repeated near-threshold transfers","medium",70,f"{len(near)} transfers fell between $8,500 and $10,000, a pattern that merits review.",[x.id for x in near[-6:]])
    new=[x for x in tx if x.is_new_counterparty and x.transaction_type=="transfer" and x.amount>=3000]; cps={x.counterparty for x in new}
    if len(cps)>=3:add("Multiple new counterparties","high",85,f"Large transfers were sent to {len(cps)} newly observed counterparties.",[x.id for x in new[-6:]])
    db.commit();return alerts
def scan_all(db):
    db.execute(delete(Alert));db.commit();out=[]
    for cid in db.scalars(select(Customer.id)):out.extend(scan_customer(db,cid))
    return out
