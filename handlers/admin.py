from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

router = Router()

ACCEPT_MSG = (
    "🎉 <b>Tabriklaymiz!</b>\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Ilmkon School HR qo'mitasi arizangizni ko'rib chiqdi.\n\n"
    "✅ <b>Siz keyingi bosqichga o'tdingiz!</b>\n\n"
    "📞 Yaqin orada siz bilan <b>suhbat (intervyu)</b> o'tkazish uchun\n"
    "telefon orqali bog'lanamiz.\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "<i>Ilmkon School jamoasi sizni kutib qoladi! 🏫</i>"
)

REJECT_MSG = (
    "🙏 <b>Hurmatli nomzod!</b>\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Ilmkon School HR qo'mitasi arizangizni diqqat bilan ko'rib chiqdi.\n\n"
    "Hozircha sizning profilingiz lavozim talablariga to'liq mos kelmadi.\n\n"
    "💌 <b>Ma'lumotlaringiz uchun katta rahmat!</b>\n\n"
    "Kelajakda yangi vakansiyalar ochilganda albatta bog'lanamiz.\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "<i>Omad tilaymiz! Ilmkon School 🏫</i>"
)


@router.callback_query(F.data.startswith("admin:accept:"))
async def admin_accept(callback: CallbackQuery, bot: Bot) -> None:
    parts = callback.data.split(":")
    user_id, app_id = int(parts[2]), parts[3]
    try:
        await bot.send_message(user_id, ACCEPT_MSG, parse_mode="HTML")
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.reply(
            f"✅ <b>QABUL QILINDI</b> | Ariza №{app_id}\n"
            f"👤 Admin: {callback.from_user.full_name}", parse_mode="HTML")
        await callback.answer("✅ Nomzodga qabul xabari yuborildi!", show_alert=True)
    except Exception:
        await callback.answer("❌ Xabar yuborib bo'lmadi.", show_alert=True)


@router.callback_query(F.data.startswith("admin:reject:"))
async def admin_reject(callback: CallbackQuery, bot: Bot) -> None:
    parts = callback.data.split(":")
    user_id, app_id = int(parts[2]), parts[3]
    try:
        await bot.send_message(user_id, REJECT_MSG, parse_mode="HTML")
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.reply(
            f"❌ <b>BEKOR QILINDI</b> | Ariza №{app_id}\n"
            f"👤 Admin: {callback.from_user.full_name}", parse_mode="HTML")
        await callback.answer("✅ Nomzodga rad etish xabari yuborildi!", show_alert=True)
    except Exception:
        await callback.answer("❌ Xabar yuborib bo'lmadi.", show_alert=True)
