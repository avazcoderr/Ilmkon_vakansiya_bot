"""Admin panel — statistika, eksport, qidirish, izoh, eslatma."""

from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from filters import IsAdmin
from states import AdminPanel
from keyboards import (
    admin_main_keyboard, admin_list_keyboard, admin_filter_keyboard,
    admin_detail_keyboard, back_to_menu, STATUS_EMOJI,
)
from database import async_session, Application, queries
from data.questions import POSITIONS
from utils.excel import build_excel

router = Router()

STATUS_LABEL = {
    "in_progress": "🔄 Jarayonda",
    "completed":   "⏳ Kutilmoqda",
    "accepted":    "✅ Qabul qilindi",
    "rejected":    "❌ Rad etildi",
    "cancelled":   "🚫 Bekor qilindi",
}

ACCEPT_MSG = (
    "🎉 <b>Tabriklaymiz!</b>\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Ilmkon School HR qo'mitasi arizangizni ko'rib chiqdi.\n\n"
    "✅ <b>Siz keyingi bosqichga o'tdingiz!</b>\n\n"
    "📞 Yaqin orada siz bilan <b>suhbat (intervyu)</b> o'tkazish uchun\n"
    "telefon orqali bog'lanamiz.\n\n"
    "⏰ Telefoningizni yonida tutib yuring.\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "<i>Ilmkon School jamoasi sizni kutib qoladi! 🏫</i>"
)

REJECT_MSG = (
    "🙏 <b>Hurmatli nomzod!</b>\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Ilmkon School HR qo'mitasi arizangizni diqqat bilan ko'rib chiqdi.\n\n"
    "Hozircha sizning profilingiz tanlangan lavozim talablariga\n"
    "to'liq mos kelmadi.\n\n"
    "💌 <b>Ma'lumotlaringiz uchun katta rahmat!</b>\n\n"
    "Kelajakda yangi vakansiyalar ochilganda albatta bog'lanamiz.\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "<i>Omad tilaymiz! Ilmkon School jamoasi 🏫</i>"
)


# ══════════════════════════════════════════════════════════════
# ASOSIY MENYU
# ══════════════════════════════════════════════════════════════

@router.message(IsAdmin(), Command("panel", "admin"))
async def cmd_panel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "🛠 <b>Admin Panel — Ilmkon School</b>\n\nKerakli bo'limni tanlang:",
        reply_markup=admin_main_keyboard(), parse_mode="HTML",
    )


@router.callback_query(IsAdmin(), F.data == "adm_menu")
async def cb_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        "🛠 <b>Admin Panel — Ilmkon School</b>\n\nKerakli bo'limni tanlang:",
        reply_markup=admin_main_keyboard(), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(IsAdmin(), F.data == "adm_noop")
async def cb_noop(callback: CallbackQuery) -> None:
    await callback.answer()


# ══════════════════════════════════════════════════════════════
# ARIZALAR RO'YXATI
# ══════════════════════════════════════════════════════════════

@router.message(IsAdmin(), Command("arizalar"))
async def cmd_arizalar(message: Message) -> None:
    async with async_session() as s:
        apps, total = await queries.get_applications_page(s, page=0)
    await message.answer(
        _list_header("all", 0, total),
        reply_markup=admin_list_keyboard(apps, 0, total),
        parse_mode="HTML",
    )


@router.callback_query(IsAdmin(), F.data.startswith("adm_list_"))
async def cb_list(callback: CallbackQuery) -> None:
    parts      = callback.data.split("_")
    page       = int(parts[2])
    pos_filter = parts[3]
    async with async_session() as s:
        apps, total = await queries.get_applications_page(
            s, page=page,
            position=pos_filter if pos_filter != "all" else "all",
        )
    await callback.message.edit_text(
        _list_header(pos_filter, page, total),
        reply_markup=admin_list_keyboard(apps, page, total, pos_filter),
        parse_mode="HTML",
    )
    await callback.answer()


def _list_header(pos_filter: str, page: int, total: int) -> str:
    from database.queries import PER_PAGE
    start     = page * PER_PAGE + 1
    end       = min((page + 1) * PER_PAGE, total)
    pos_label = POSITIONS.get(pos_filter, "Barchasi") if pos_filter != "all" else "Barchasi"
    return (
        f"📋 <b>Arizalar</b> — {pos_label}\n"
        f"<i>{start}–{end} / {total} ta</i>"
    )


# ══════════════════════════════════════════════════════════════
# FILTR
# ══════════════════════════════════════════════════════════════

@router.callback_query(IsAdmin(), F.data == "adm_filter")
async def cb_filter(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "🏷 <b>Lavozim bo'yicha filtr</b>\n\nQaysi lavozimni ko'rmoqchisiz?",
        reply_markup=admin_filter_keyboard(), parse_mode="HTML",
    )
    await callback.answer()


# ══════════════════════════════════════════════════════════════
# ARIZA DETALI
# ══════════════════════════════════════════════════════════════

@router.callback_query(IsAdmin(), F.data.startswith("adm_view_"))
async def cb_view(callback: CallbackQuery) -> None:
    parts       = callback.data.split("_")
    app_id      = int(parts[2])
    back_page   = int(parts[3])
    back_filter = parts[4]
    async with async_session() as s:
        app, answers, notes = await queries.get_application_detail(s, app_id)
    if not app:
        await callback.answer("❌ Ariza topilmadi!", show_alert=True)
        return
    await callback.message.edit_text(
        _detail_text(app, answers, notes),
        reply_markup=admin_detail_keyboard(app_id, back_page, back_filter),
        parse_mode="HTML",
    )
    await callback.answer()


def _detail_text(app, answers, notes) -> str:
    lines = [
        f"📋 <b>Ariza #{app.id}</b>",
        "━━━━━━━━━━━━━━━━━━━━",
        f"💼 <b>Lavozim:</b> {app.position_label}",
        f"📊 <b>Holat:</b> {STATUS_LABEL.get(app.status, app.status)}",
        f"📅 <b>Sana:</b> {app.created_at.strftime('%d.%m.%Y %H:%M')}",
        f"👤 <b>Telegram ID:</b> <code>{app.user_telegram_id}</code>",
        "━━━━━━━━━━━━━━━━━━━━",
    ]
    for ans in answers:
        if ans.value_type in ("photo", "document"):
            lines.append(f"▪️ <b>{ans.field_label}:</b> ✅ Yuborilgan")
        else:
            val = (ans.value[:120] + "...") if ans.value and len(ans.value) > 120 else ans.value
            lines.append(f"▪️ <b>{ans.field_label}:</b> {val}")
    if notes:
        lines += ["━━━━━━━━━━━━━━━━━━━━", "💬 <b>Izohlar:</b>"]
        for n in notes:
            lines.append(f"  <i>{n.created_at.strftime('%d.%m %H:%M')} ({n.admin_name}):</i> {n.text}")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
# QABUL / RAD — DETAIL VIEWDAN
# ══════════════════════════════════════════════════════════════

@router.callback_query(IsAdmin(), F.data.startswith("adm_accept_"))
async def cb_accept(callback: CallbackQuery, bot: Bot) -> None:
    app_id = int(callback.data.split("_")[2])
    async with async_session() as s:
        app = await s.get(Application, app_id)
        if not app:
            await callback.answer("❌ Topilmadi!", show_alert=True); return
        await queries.update_status(s, app_id, "accepted")
        user_id = app.user_telegram_id
    try:
        await bot.send_message(user_id, ACCEPT_MSG, parse_mode="HTML")
        await callback.answer("✅ Qabul xabari yuborildi!", show_alert=True)
    except Exception:
        await callback.answer("⚠️ Yuborildi (foydalanuvchi botni bloklagan bo'lishi mumkin)", show_alert=True)
    async with async_session() as s:
        app, answers, notes = await queries.get_application_detail(s, app_id)
    await callback.message.edit_text(
        _detail_text(app, answers, notes),
        reply_markup=admin_detail_keyboard(app_id, 0, "all"),
        parse_mode="HTML",
    )


@router.callback_query(IsAdmin(), F.data.startswith("adm_reject_"))
async def cb_reject(callback: CallbackQuery, bot: Bot) -> None:
    app_id = int(callback.data.split("_")[2])
    async with async_session() as s:
        app = await s.get(Application, app_id)
        if not app:
            await callback.answer("❌ Topilmadi!", show_alert=True); return
        await queries.update_status(s, app_id, "rejected")
        user_id = app.user_telegram_id
    try:
        await bot.send_message(user_id, REJECT_MSG, parse_mode="HTML")
        await callback.answer("✅ Rad etish xabari yuborildi!", show_alert=True)
    except Exception:
        await callback.answer("⚠️ Yuborildi (foydalanuvchi botni bloklagan bo'lishi mumkin)", show_alert=True)
    async with async_session() as s:
        app, answers, notes = await queries.get_application_detail(s, app_id)
    await callback.message.edit_text(
        _detail_text(app, answers, notes),
        reply_markup=admin_detail_keyboard(app_id, 0, "all"),
        parse_mode="HTML",
    )


# ══════════════════════════════════════════════════════════════
# IZOH
# ══════════════════════════════════════════════════════════════

@router.callback_query(IsAdmin(), F.data.startswith("adm_note_"))
async def cb_note_start(callback: CallbackQuery, state: FSMContext) -> None:
    parts = callback.data.split("_")
    app_id, back_page, back_filter = int(parts[2]), parts[3], parts[4]
    await state.set_state(AdminPanel.writing_note)
    await state.update_data(note_app_id=app_id, back_page=back_page, back_filter=back_filter)
    await callback.message.answer(
        f"💬 <b>Ariza #{app_id} uchun izoh yozing</b>\n\n"
        "<i>Bekor qilish: /panel</i>", parse_mode="HTML",
    )
    await callback.answer()


@router.message(IsAdmin(), AdminPanel.writing_note)
async def handle_note(message: Message, state: FSMContext) -> None:
    data        = await state.get_data()
    app_id      = data["note_app_id"]
    back_page   = int(data.get("back_page", 0))
    back_filter = data.get("back_filter", "all")
    text        = (message.text or "").strip()
    if len(text) < 3:
        await message.answer("⚠️ Izoh juda qisqa."); return
    async with async_session() as s:
        await queries.add_note(s, app_id, message.from_user.id,
                               message.from_user.full_name or "Admin", text)
        app, answers, notes = await queries.get_application_detail(s, app_id)
    await state.clear()
    await message.answer(
        "✅ Izoh saqlandi!\n\n" + _detail_text(app, answers, notes),
        reply_markup=admin_detail_keyboard(app_id, back_page, back_filter),
        parse_mode="HTML",
    )


# ══════════════════════════════════════════════════════════════
# STATISTIKA  ← asosiy yangilik
# ══════════════════════════════════════════════════════════════

@router.message(IsAdmin(), Command("statistika"))
async def cmd_statistika(message: Message) -> None:
    async with async_session() as s:
        stats = await queries.get_stats(s)
    await message.answer(_stats_text(stats), reply_markup=back_to_menu(), parse_mode="HTML")


@router.callback_query(IsAdmin(), F.data == "adm_stats")
async def cb_stats(callback: CallbackQuery) -> None:
    async with async_session() as s:
        stats = await queries.get_stats(s)
    await callback.message.edit_text(
        _stats_text(stats), reply_markup=back_to_menu(), parse_mode="HTML",
    )
    await callback.answer()


def _stats_text(stats: dict) -> str:
    bs = stats["by_status"]
    bp = stats["by_position"]
    daily = stats.get("daily", {})
    total = stats["total"] or 1  # bo'lishga xavfsiz

    # Holat foizlari
    acc_pct  = bs.get("accepted", 0)  / total * 100
    rej_pct  = bs.get("rejected", 0)  / total * 100
    wait_pct = bs.get("completed", 0) / total * 100

    # Oxirgi 7 kun mini-grafik
    daily_bar = ""
    if daily:
        mx = max(daily.values()) or 1
        for day, cnt in daily.items():
            bar = "█" * round(cnt / mx * 5) or "░"
            daily_bar += f"\n  {day}  {bar}  {cnt}"

    lines = [
        "📊 <b>STATISTIKA — Ilmkon School</b>",
        f"<i>{datetime.now().strftime('%d.%m.%Y %H:%M')} holatida</i>",
        "━━━━━━━━━━━━━━━━━━━━",

        "📦 <b>Umumiy:</b>",
        f"  Jami arizalar:  <b>{stats['total']}</b>",
        f"  Bugun:          <b>{stats['today']}</b>",
        f"  Bu hafta:       <b>{stats['week']}</b>",
        f"  Bu oy:          <b>{stats['month']}</b>",
        "",
        "📈 <b>Holat bo'yicha:</b>",
        f"  ⏳ Kutilmoqda:    <b>{bs.get('completed', 0)}</b>  ({wait_pct:.0f}%)",
        f"  ✅ Qabul qilindi: <b>{bs.get('accepted', 0)}</b>  ({acc_pct:.0f}%)",
        f"  ❌ Rad etildi:    <b>{bs.get('rejected', 0)}</b>  ({rej_pct:.0f}%)",
        f"  🔄 Jarayonda:     <b>{bs.get('in_progress', 0)}</b>",
        f"  🚫 Bekor:         <b>{bs.get('cancelled', 0)}</b>",
        "",
        "💼 <b>Lavozim bo'yicha:</b>",
    ]

    for key, label in POSITIONS.items():
        cnt = bp.get(key, 0)
        bar = "▓" * round(cnt / total * 10) or "░"
        lines.append(f"  {label[:20]}: <b>{cnt}</b> {bar}")

    if daily_bar:
        lines += ["", "📅 <b>Oxirgi 7 kun:</b>" + daily_bar]

    lines += [
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        f"<i>📤 /eksport — Excel yuklab olish</i>",
    ]
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
# EKSPORT  ← asosiy yangilik
# ══════════════════════════════════════════════════════════════

@router.message(IsAdmin(), Command("eksport"))
async def cmd_eksport(message: Message) -> None:
    await _do_export(message)


@router.callback_query(IsAdmin(), F.data == "adm_export")
async def cb_export(callback: CallbackQuery) -> None:
    await callback.answer("📤 Eksport tayyorlanmoqda...")
    await _do_export(callback.message)


async def _do_export(message: Message) -> None:
    await message.answer("⏳ Excel fayl tayyorlanmoqda, biroz kuting...")
    async with async_session() as s:
        rows = await queries.get_all_for_export(s)
    if not rows:
        await message.answer("📭 Hozircha arizalar yo'q."); return

    xlsx_bytes = build_excel(rows)
    now        = datetime.now().strftime("%Y%m%d_%H%M")
    filename   = f"Ilmkon_arizalar_{now}.xlsx"

    await message.answer_document(
        document=BufferedInputFile(xlsx_bytes, filename=filename),
        caption=(
            f"📊 <b>Ilmkon School — Arizalar eksporti</b>\n\n"
            f"📦 Jami: <b>{len(rows)} ta</b> ariza\n"
            f"📅 Sana: <b>{datetime.now().strftime('%d.%m.%Y %H:%M')}</b>\n\n"
            f"📋 <b>Varaqlar:</b>\n"
            f"  1️⃣ Barcha arizalar\n"
            f"  2️⃣ Statistika\n"
            f"  3️⃣ Qabul qilinganlar\n"
            f"  4️⃣ Kutilmoqda"
        ),
        parse_mode="HTML",
    )


# ══════════════════════════════════════════════════════════════
# QIDIRISH
# ══════════════════════════════════════════════════════════════

@router.message(IsAdmin(), Command("qidirish"))
async def cmd_qidirish(message: Message, state: FSMContext) -> None:
    parts = message.text.split(maxsplit=1)
    if len(parts) > 1:
        await _do_search(message, parts[1])
    else:
        await state.set_state(AdminPanel.searching)
        await message.answer(
            "🔍 <b>Qidirish</b>\n\nIsm yoki telefon raqam yozing:\n"
            "<i>Bekor qilish: /panel</i>", parse_mode="HTML",
        )


@router.callback_query(IsAdmin(), F.data == "adm_search")
async def cb_search(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminPanel.searching)
    await callback.message.answer(
        "🔍 <b>Qidirish</b>\n\nIsm yoki telefon raqam yozing:\n"
        "<i>Bekor qilish: /panel</i>", parse_mode="HTML",
    )
    await callback.answer()


@router.message(IsAdmin(), AdminPanel.searching)
async def handle_search(message: Message, state: FSMContext) -> None:
    await state.clear()
    await _do_search(message, (message.text or "").strip())


async def _do_search(message: Message, query: str) -> None:
    if len(query) < 2:
        await message.answer("⚠️ So'rov juda qisqa."); return
    async with async_session() as s:
        apps = await queries.search_applications(s, query)
    if not apps:
        await message.answer(f"🔍 <b>«{query}»</b> bo'yicha hech narsa topilmadi.", parse_mode="HTML"); return
    lines = [f"🔍 <b>«{query}»</b> — {len(apps)} ta natija:\n"]
    for app in apps[:15]:
        emoji = STATUS_EMOJI.get(app.status, "❓")
        lines.append(f"{emoji} <b>#{app.id}</b> | {app.position_label} | {app.created_at.strftime('%d.%m.%Y')}")
    lines.append("\n<i>Ko'rish: /ariza_ID (masalan /ariza_5)</i>")
    await message.answer("\n".join(lines), parse_mode="HTML")


@router.message(IsAdmin(), F.text.regexp(r"^/ariza_(\d+)$"))
async def cmd_view_id(message: Message) -> None:
    app_id = int(message.text.split("_")[1])
    async with async_session() as s:
        app, answers, notes = await queries.get_application_detail(s, app_id)
    if not app:
        await message.answer("❌ Ariza topilmadi!"); return
    await message.answer(
        _detail_text(app, answers, notes),
        reply_markup=admin_detail_keyboard(app_id, 0, "all"),
        parse_mode="HTML",
    )


# ══════════════════════════════════════════════════════════════
# ESLATMA
# ══════════════════════════════════════════════════════════════

@router.callback_query(IsAdmin(), F.data == "adm_reminder")
async def cb_reminder(callback: CallbackQuery) -> None:
    from config import REMINDER_HOURS
    await callback.message.edit_text(
        "⏰ <b>Eslatma sozlamalari</b>\n\n"
        f"Hozirgi sozlama: har <b>{REMINDER_HOURS} soat</b>da bir marta\n"
        "javobsiz arizalar haqida guruhga eslatma keladi.\n\n"
        "⚙️ O'zgartirish uchun <code>.env</code> faylida:\n"
        "<code>REMINDER_HOURS=12</code>\n"
        "deb yozing va botni qayta ishga tushiring.\n\n"
        "✅ <b>Eslatma ishlayapti</b>",
        reply_markup=back_to_menu(), parse_mode="HTML",
    )
    await callback.answer()
