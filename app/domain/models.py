from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Session(Base):
    __tablename__ = "session"
    id: Mapped[int] = mapped_column(primary_key=True)
    sim: Mapped[str] = mapped_column(String(32), default="iRacing")
    track: Mapped[str] = mapped_column(String(64))
    car: Mapped[str] = mapped_column(String(64))
    goal: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    run_plans: Mapped[list["RunPlan"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class RunPlan(Base):
    __tablename__ = "run_plan"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("session.id"))
    name: Mapped[str] = mapped_column(String(80))
    fuel_target_l: Mapped[float] = mapped_column(Float, default=0.0)
    tyre_set_label: Mapped[str] = mapped_column(String(32), default="")
    manifest_hash: Mapped[str] = mapped_column(String(64), default="")
    session: Mapped["Session"] = relationship(back_populates="run_plans")
    decisions: Mapped[list["Decision"]] = relationship(
        back_populates="run_plan", cascade="all, delete-orphan"
    )


class Decision(Base):
    __tablename__ = "decision"
    id: Mapped[int] = mapped_column(primary_key=True)
    run_plan_id: Mapped[int] = mapped_column(ForeignKey("run_plan.id"))
    rule: Mapped[str] = mapped_column(String(64))
    input_summary: Mapped[str] = mapped_column(Text)
    recommendation: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    outcome: Mapped[str | None] = mapped_column(String(32), default=None)
    run_plan: Mapped["RunPlan"] = relationship(back_populates="decisions")
