from pathlib import Path
s=Path(__file__).resolve().parents[2]/'stage/ca549816cdd1'
p=s/'app/models.py';t=p.read_text()
t=t.replace('Boolean, DateTime, Enum as SqlEnum','Boolean, Enum as SqlEnum').replace('from sqlalchemy.orm import DeclarativeBase','from app.time_types import UTCDateTime\nfrom sqlalchemy.orm import DeclarativeBase')
t=t.replace('DateTime(timezone=True)','UTCDateTime()')
for name in ['Stream','Dashboard','SavedQuery','AlertRule','Pipeline']:
    start=t.index('class '+name+'(Base):');end=t.find('\n\nclass ',start+1);end=end if end!=-1 else len(t)
    block=t[start:end];needle='    id: Mapped[int] = mapped_column(primary_key=True)'
    assert needle in block;block=block.replace(needle,needle+'\n    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")\n    __mapper_args__ = {"version_id_col": version}')
    t=t[:start]+block+t[end:]
p.write_text(t)
