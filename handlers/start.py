from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from keyboards import positions_keyboard, remove_keyboard
from states import ApplicationForm
from database import async_session, User

router = Router()

WELCOME_TEXT = (
    "👋 <b>Ilmkon School — Ishga qabul botiga xush kelibsiz!</b>\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "🏫 <b>Ilmkon School</b> — zamonaviy xususiy o'quv muassasasi bo'lib,\n"
    "biz o'z jamoamizga <b>malakali va g'ayratli mutaxassislarni</b> qabul qilamiz.\n\n"
    "📋 <b>Ariza topshirish tartibi:</b>\n"
    "1️⃣ Lavozimni tanlang\n"
    "2️⃣ Savollarga ketma-ket javob bering\n"
    "3️⃣ Arizangizni tekshirib tasdiqlang\n\n"
    "⚡ <i>Savollarni diqqat bilan o'qing va to'liq javob bering.</i>\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "⬇️ <b>Qaysi lavozimga topshirmoqchisiz?</b>"
)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        if not user:
            session.add(User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name,
            ))
            await session.commit()
    await state.set_state(ApplicationForm.choosing_position)
    await message.answer(WELCOME_TEXT, reply_markup=positions_keyboard(), parse_mode="HTML")


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    if await state.get_state() is None:
        await message.answer("❗ Faol ariza yo'q. /start bosing.", parse_mode="HTML")
        return
    await state.clear()
    await message.answer(
        "🚫 <b>Ariza bekor qilindi.</b>\n\n/start — qaytadan boshlash.",
        reply_markup=remove_keyboard(), parse_mode="HTML",
    )
