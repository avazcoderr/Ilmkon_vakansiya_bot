import asyncio
import logging
from datetime import datetime

from aiogram import Bot
from config import ADMIN_GROUP_ID, REMINDER_HOURS
from database import async_session, queries

logger = logging.getLogger(__name__)


async def reminder_loop(bot: Bot) -> None:
    logger.info("⏰ Eslatma scheduler ishga tushdi.")
    while True:
        await asyncio.sleep(3600)
        try:
            async with async_session() as s:
                apps = await queries.get_pending_for_reminder(s, REMINDER_HOURS)
            if not apps:
                continue
            lines = [
                "⏰ <b>ESLATMA — Javobsiz Arizalar</b>",
                "━━━━━━━━━━━━━━━━━━━━",
                f"<b>{len(apps)} ta ariza</b> hali ko'rib chiqilmagan "
                f"({REMINDER_HOURS} soatdan ko'proq):\n",
            ]
            for app in apps[:10]:
                hours_ago = int((datetime.utcnow() - app.created_at).total_seconds() / 3600)
                lines.append(
                    f"▪️ <b>#{app.id}</b> | {app.position_label} | "
                    f"{app.created_at.strftime('%d.%m %H:%M')} ({hours_ago}s oldin)"
                )
            if len(apps) > 10:
                lines.append(f"\n...va yana <b>{len(apps) - 10}</b> ta")
            lines.append("\n📋 <code>/arizalar</code> — ro'yxatni ko'rish")
            await bot.send_message(ADMIN_GROUP_ID, "\n".join(lines), parse_mode="HTML")
        except Exception as e:
            logger.error(f"⏰ Eslatma xatosi: {e}")
