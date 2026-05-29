from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
)
from data.questions import POSITIONS

STATUS_EMOJI = {
    "in_progress": "🔄",
    "completed":   "⏳",
    "accepted":    "✅",
    "rejected":    "❌",
    "cancelled":   "🚫",
}

# ── Foydalanuvchi ─────────────────────────────────────────────────────────────

def positions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=label, callback_data=f"position:{key}")]
        for key, label in POSITIONS.items()
    ])


def choices_keyboard(choices: list[str], cols: int = 2) -> InlineKeyboardMarkup:
    rows, row = [], []
    for i, c in enumerate(choices, 1):
        row.append(InlineKeyboardButton(text=c, callback_data=f"choice:{c}"))
        if i % cols == 0:
            rows.append(row); row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Yuborish",              callback_data="confirm:yes"),
        InlineKeyboardButton(text="🔄 Qaytadan boshlash",    callback_data="confirm:restart"),
    ]])


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📲 Telefon raqamni ulashish", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True,
        input_field_placeholder="Yoki raqamni qo'lda kiriting...",
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


# ── Admin guruh tugmalari ─────────────────────────────────────────────────────

def admin_decision_keyboard(user_telegram_id: int, app_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Qabul qilish",
                             callback_data=f"admin:accept:{user_telegram_id}:{app_id}"),
        InlineKeyboardButton(text="❌ Bekor qilish",
                             callback_data=f"admin:reject:{user_telegram_id}:{app_id}"),
    ]])


# ── Admin panel ───────────────────────────────────────────────────────────────

def admin_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Arizalar",   callback_data="adm_list_0_all"),
         InlineKeyboardButton(text="📊 Statistika", callback_data="adm_stats")],
        [InlineKeyboardButton(text="🔍 Qidirish",   callback_data="adm_search"),
         InlineKeyboardButton(text="📤 Eksport",    callback_data="adm_export")],
        [InlineKeyboardButton(text="🏷 Filtr",      callback_data="adm_filter"),
         InlineKeyboardButton(text="⏰ Eslatma",    callback_data="adm_reminder")],
    ])


def admin_list_keyboard(apps, page: int, total: int, pos_filter: str = "all") -> InlineKeyboardMarkup:
    from database.queries import PER_PAGE
    rows = []
    for app in apps:
        emoji = STATUS_EMOJI.get(app.status, "❓")
        pos   = POSITIONS.get(app.position_key, app.position_key)[:14]
        rows.append([InlineKeyboardButton(
            text=f"{emoji} #{app.id} | {pos} | {app.created_at.strftime('%d.%m')}",
            callback_data=f"adm_view_{app.id}_{page}_{pos_filter}",
        )])
    nav = []
    total_pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"adm_list_{page-1}_{pos_filter}"))
    nav.append(InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data="adm_noop"))
    if (page + 1) * PER_PAGE < total:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"adm_list_{page+1}_{pos_filter}"))
    rows.append(nav)
    rows.append([
        InlineKeyboardButton(text="🏷 Filtr", callback_data="adm_filter"),
        InlineKeyboardButton(text="🔙 Menu",  callback_data="adm_menu"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_filter_keyboard() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text="🌐 Barchasi", callback_data="adm_list_0_all")]]
    for key, label in POSITIONS.items():
        rows.append([InlineKeyboardButton(text=label, callback_data=f"adm_list_0_{key}")])
    rows.append([InlineKeyboardButton(text="🔙 Menu", callback_data="adm_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_detail_keyboard(app_id: int, back_page: int, back_filter: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Qabul",     callback_data=f"adm_accept_{app_id}"),
         InlineKeyboardButton(text="❌ Rad etish", callback_data=f"adm_reject_{app_id}")],
        [InlineKeyboardButton(text="💬 Izoh qo'shish",
                              callback_data=f"adm_note_{app_id}_{back_page}_{back_filter}")],
        [InlineKeyboardButton(text="🔙 Ro'yxatga qaytish",
                              callback_data=f"adm_list_{back_page}_{back_filter}")],
    ])


def back_to_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔙 Menu", callback_data="adm_menu")
    ]])
