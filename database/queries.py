from datetime import datetime, timedelta, date
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Application, Answer, ApplicationNote

PER_PAGE = 5


# ── Arizalar ro'yxati ────────────────────────────────────────────────────────

async def get_applications_page(
    session: AsyncSession,
    page: int = 0,
    position: str = "all",
    status: str = "all",
) -> tuple[list, int]:
    q = select(Application)
    if position != "all":
        q = q.where(Application.position_key == position)
    if status != "all":
        q = q.where(Application.status == status)
    total = await session.scalar(select(func.count()).select_from(q.subquery())) or 0
    q = q.order_by(desc(Application.created_at)).limit(PER_PAGE).offset(page * PER_PAGE)
    return (await session.execute(q)).scalars().all(), total


# ── Ariza detali ─────────────────────────────────────────────────────────────

async def get_application_detail(session: AsyncSession, app_id: int):
    app = await session.get(Application, app_id)
    if not app:
        return None, [], []
    answers = (await session.execute(
        select(Answer).where(Answer.application_id == app_id)
    )).scalars().all()
    notes = (await session.execute(
        select(ApplicationNote)
        .where(ApplicationNote.application_id == app_id)
        .order_by(ApplicationNote.created_at)
    )).scalars().all()
    return app, answers, notes


# ── Holat yangilash ──────────────────────────────────────────────────────────

async def update_status(session: AsyncSession, app_id: int, status: str) -> bool:
    app = await session.get(Application, app_id)
    if not app:
        return False
    app.status = status
    await session.commit()
    return True


# ── Statistika ───────────────────────────────────────────────────────────────

async def get_stats(session: AsyncSession) -> dict:
    from data.questions import POSITIONS

    today_start = datetime.combine(date.today(), datetime.min.time())
    week_start  = today_start - timedelta(days=today_start.weekday())
    month_start = today_start.replace(day=1)

    total   = await session.scalar(select(func.count(Application.id))) or 0
    today   = await session.scalar(select(func.count(Application.id)).where(Application.created_at >= today_start)) or 0
    week    = await session.scalar(select(func.count(Application.id)).where(Application.created_at >= week_start)) or 0
    month   = await session.scalar(select(func.count(Application.id)).where(Application.created_at >= month_start)) or 0

    by_status = {}
    for st in ["completed", "accepted", "rejected", "in_progress", "cancelled"]:
        by_status[st] = await session.scalar(
            select(func.count(Application.id)).where(Application.status == st)
        ) or 0

    by_position = {}
    for key in POSITIONS:
        by_position[key] = await session.scalar(
            select(func.count(Application.id)).where(Application.position_key == key)
        ) or 0

    # Oxirgi 7 kunlik dinamika
    daily = {}
    for i in range(6, -1, -1):
        d = today_start - timedelta(days=i)
        d_end = d + timedelta(days=1)
        cnt = await session.scalar(
            select(func.count(Application.id))
            .where(Application.created_at >= d)
            .where(Application.created_at < d_end)
        ) or 0
        daily[d.strftime("%d.%m")] = cnt

    return {
        "total": total, "today": today, "week": week, "month": month,
        "by_status": by_status, "by_position": by_position, "daily": daily,
    }


# ── Qidirish ─────────────────────────────────────────────────────────────────

async def search_applications(session: AsyncSession, query: str) -> list:
    app_ids_q = (
        select(Answer.application_id)
        .where(Answer.value.ilike(f"%{query}%"))
        .where(Answer.field_key.in_(["fullname", "phone"]))
        .distinct()
    )
    app_ids = [r[0] for r in (await session.execute(app_ids_q)).fetchall()]
    if not app_ids:
        return []
    return (await session.execute(
        select(Application).where(Application.id.in_(app_ids))
        .order_by(desc(Application.created_at)).limit(20)
    )).scalars().all()


# ── Izoh qo'shish ────────────────────────────────────────────────────────────

async def add_note(session, app_id, admin_id, admin_name, text) -> ApplicationNote:
    note = ApplicationNote(
        application_id=app_id,
        admin_telegram_id=admin_id,
        admin_name=admin_name,
        text=text,
    )
    session.add(note)
    await session.commit()
    return note


# ── Eslatma ──────────────────────────────────────────────────────────────────

async def get_pending_for_reminder(session: AsyncSession, hours: int) -> list:
    threshold = datetime.utcnow() - timedelta(hours=hours)
    return (await session.execute(
        select(Application)
        .where(Application.status == "completed")
        .where(Application.created_at <= threshold)
        .order_by(Application.created_at)
    )).scalars().all()


# ── Eksport ──────────────────────────────────────────────────────────────────

async def get_all_for_export(session: AsyncSession) -> list:
    apps = (await session.execute(
        select(Application).order_by(desc(Application.created_at))
    )).scalars().all()
    rows = []
    for app in apps:
        answers = (await session.execute(
            select(Answer).where(Answer.application_id == app.id)
        )).scalars().all()
        rows.append((app, answers))
    return rows
