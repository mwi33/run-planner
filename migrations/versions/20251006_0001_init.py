import sqlalchemy as sa
from alembic import op

revision = "20251006_0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "session",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sim", sa.String(length=32), nullable=False, server_default="iRacing"),
        sa.Column("track", sa.String(length=64), nullable=False),
        sa.Column("car", sa.String(length=64), nullable=False),
        sa.Column("goal", sa.Text(), nullable=False, server_default=""),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
        ),
    )
    op.create_table(
        "run_plan",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), sa.ForeignKey("session.id"), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("fuel_target_l", sa.Float(), nullable=False, server_default="0"),
        sa.Column("tyre_set_label", sa.String(length=32), nullable=False, server_default=""),
        sa.Column("manifest_hash", sa.String(length=64), nullable=False, server_default=""),
    )
    op.create_table(
        "decision",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_plan_id", sa.Integer(), sa.ForeignKey("run_plan.id"), nullable=False),
        sa.Column("rule", sa.String(length=64), nullable=False),
        sa.Column("input_summary", sa.Text(), nullable=False),
        sa.Column("recommendation", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
        ),
        sa.Column("outcome", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("decision")
    op.drop_table("run_plan")
    op.drop_table("session")
