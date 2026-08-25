from sqlalchemy import select
from openai import OpenAI
from app.config import settings
from app.models import Alert,Customer,Transaction,Investigation
def investigate(db,alert_id):
    alert=db.get(Alert,alert_id)
    if not alert:raise ValueError("Alert not found")
    customer=db.get(Customer,alert.customer_id); ids=[int(x) for x in alert.transaction_ids.split(",") if x]
    history=list(db.scalars(select(Transaction).where(Transaction.customer_id==customer.id).order_by(Transaction.occurred_at.desc()).limit(25)))
    evidence="\n".join(f"TX {x.id}: {x.occurred_at.isoformat()} | ${x.amount:.2f} | {x.transaction_type} | {x.counterparty} | {x.state} | new={bool(x.is_new_counterparty)}" for x in history)
    prompt=f'''You are a bank fraud investigation assistant. Do not decide that fraud occurred. Write a concise case note grounded ONLY in supplied evidence. Use headings: Risk Assessment, Evidence, Context, Recommended Review. Distinguish suspicious indicators from proof of fraud.
Customer: {customer.name}; home state: {customer.home_state}; risk tier: {customer.risk_tier}
Triggered rule: {alert.rule_name}; score: {alert.score}/100
Rule explanation: {alert.explanation}
Flagged IDs: {ids}
Recent evidence:
{evidence}'''
    if settings.openai_api_key:
        r=OpenAI(api_key=settings.openai_api_key).chat.completions.create(model=settings.openai_chat_model,messages=[{"role":"user","content":prompt}],temperature=0.2)
        report=r.choices[0].message.content
    else:
        report=f"Risk Assessment\n{alert.severity.upper()} review priority.\n\nEvidence\n{alert.explanation}\n\nContext\nSuspicious activity is not proof of fraud.\n\nRecommended Review\nVerify transaction purpose and counterparties."
    inv=Investigation(alert_id=alert.id,report=report);db.add(inv);db.commit();db.refresh(inv);return inv
