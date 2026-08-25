from datetime import datetime
from sqlalchemy import String,Float,DateTime,ForeignKey,Text,Integer
from sqlalchemy.orm import Mapped,mapped_column
from app.db import Base
class Customer(Base):
    __tablename__="customers"; id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(120)); home_state:Mapped[str]=mapped_column(String(32)); risk_tier:Mapped[str]=mapped_column(String(16),default="low")
class Transaction(Base):
    __tablename__="transactions"; id:Mapped[int]=mapped_column(primary_key=True)
    customer_id:Mapped[int]=mapped_column(ForeignKey("customers.id"),index=True); occurred_at:Mapped[datetime]=mapped_column(DateTime,index=True)
    amount:Mapped[float]=mapped_column(Float); transaction_type:Mapped[str]=mapped_column(String(32)); counterparty:Mapped[str]=mapped_column(String(120))
    state:Mapped[str]=mapped_column(String(32)); is_new_counterparty:Mapped[int]=mapped_column(Integer,default=0)
class Alert(Base):
    __tablename__="alerts"; id:Mapped[int]=mapped_column(primary_key=True); customer_id:Mapped[int]=mapped_column(ForeignKey("customers.id"),index=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); rule_name:Mapped[str]=mapped_column(String(80)); severity:Mapped[str]=mapped_column(String(16))
    score:Mapped[int]=mapped_column(Integer); explanation:Mapped[str]=mapped_column(Text); transaction_ids:Mapped[str]=mapped_column(Text)
class Investigation(Base):
    __tablename__="investigations"; id:Mapped[int]=mapped_column(primary_key=True); alert_id:Mapped[int]=mapped_column(ForeignKey("alerts.id"),index=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); report:Mapped[str]=mapped_column(Text)
