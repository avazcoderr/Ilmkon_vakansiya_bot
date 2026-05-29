import re
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_GROUP_ID
from data.questions import POSITIONS, get_questions
from keyboards import (
    positions_keyboard, choices_keyboard, confirm_keyboard,
    phone_keyboard, remove_keyboard,
)
from states import ApplicationForm
from database import async_session, Application, Answer

router = Router()


# ─── Yordamchi funksiyalar ──────────────────────────────────────────────────

async def send_question(message: Message, question: dict, index: int, total: int) -> None:
    header = f"❓ <b>Savol {index + 1} / {total}</b>\n━━━━━━━━━━━━━━━━\n\n"
    text = header + question["text"]

    if question["input_type"] == "choice":
        await message.answer(text, reply_markup=choices_keyboard(question["choices"]), parse_mode="HTML")
    elif question["input_type"] == "phone":
        await message.answer(text, reply_markup=phone_keyboard(), parse_mode="HTML")
    elif question["input_type"] == "photo":
        await message.answer(
            text + "\n\n<i>📌 Rasmni to'g'ridan-to'g'ri yuboring (fayl emas, rasm sifatida).</i>",
            reply_markup=remove_keyboard(), parse_mode="HTML",
        )
    elif question["input_type"] == "document":
        await message.answer(
            text + "\n\n<i>📌 Faylni hujjat (document) sifatida yuboring.</i>",
            reply_markup=remove_keyboard(), parse_mode="HTML",
        )
    else:
        await message.answer(text, reply_markup=remove_keyboard(), parse_mode="HTML")


def build_preview(position_key: str, answers: dict, questions: list[dict]) -> str:
    pos_label = POSITIONS[position_key]
    lines = [
        "📋 <b>ARIZANGIZNI TEKSHIRING</b>",
        "━━━━━━━━━━━━━━━━━━━━",
        f"💼 <b>Lavozim:</b> {pos_label}",
        "",
    ]
    for q in questions:
        val = answers.get(q["key"])
        if not val:
            continue
        display = "✅ Yuborilgan" if q["input_type"] in ("photo", "document") else val
        lines.append(f"▪️ <b>{q['label']}:</b> {display}")
    lines += [
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "❓ <b>Ma'lumotlar to'g'rimi?</b>",
        "",
        "✅ To'g'ri bo'lsa — <b>«Yuborish»</b> ni bosing.",
        "🔄 Noto'g'ri bo'lsa — <b>«Qaytadan boshlash»</b> ni bosing.",
    ]
    return "\n".join(lines)


async def save_and_notify(bot, user_telegram_id, position_key, answers, questions):
    async with async_session() as session:
        app = Application(
            user_telegram_id=user_telegram_id,
            position_key=position_key,
            position_label=POSITIONS[position_key],
            status="completed",
            completed_at=datetime.utcnow(),
        )
        session.add(app)
        await session.flush()
        for q in questions:
            val = answers.get(q["key"])
            if not val:
                continue
            session.add(Answer(
                application_id=app.id,
                field_key=q["key"],
                field_label=q["label"],
                value=val,
                value_type=q["input_type"] if q["input_type"] in ("photo", "document") else "text",
            ))
        await session.commit()
        app_id = app.id

    from keyboards import admin_decision_keyboard
    pos_label     = POSITIONS[position_key]
    now           = datetime.now().strftime("%d.%m.%Y %H:%M")
    photo_file_id = None
    caption_lines = [
        "🆕 <b>YANGI ARIZA — ILMKON SCHOOL</b>",
        "━━━━━━━━━━━━━━━━━━━━",
        f"🆔 <b>Ariza №:</b> {app_id}",
        f"💼 <b>Lavozim:</b> {pos_label}",
        f"📅 <b>Sana:</b> {now}",
        f"👤 <b>Telegram ID:</b> <code>{user_telegram_id}</code>",
        "━━━━━━━━━━━━━━━━━━━━",
    ]
    for q in questions:
        val = answers.get(q["key"])
        if not val:
            continue
        if q["input_type"] == "photo":
            photo_file_id = val
            continue
        if q["input_type"] == "document":
            continue
        caption_lines.append(f"▪️ <b>{q['label']}:</b> {val}")

    admin_kb  = admin_decision_keyboard(user_telegram_id, app_id)
    full_text = "\n".join(caption_lines)
    if len(full_text) > 1020:
        full_text = full_text[:1017] + "..."

    if photo_file_id:
        await bot.send_photo(ADMIN_GROUP_ID, photo=photo_file_id,
                             caption=full_text, parse_mode="HTML", reply_markup=admin_kb)
    else:
        await bot.send_message(ADMIN_GROUP_ID, full_text, parse_mode="HTML", reply_markup=admin_kb)


async def _next_or_confirm(message, state, position, answers, questions, next_index):
    """Keyingi savolga o'tish yoki tasdiqlash ekranini ko'rsatish."""
    if next_index < len(questions):
        await state.update_data(question_index=next_index, answers=answers, waiting_custom=False)
        await send_question(message, questions[next_index], next_index, len(questions))
    else:
        await state.update_data(answers=answers, waiting_custom=False)
        await state.set_state(ApplicationForm.confirming)
        await message.answer(build_preview(position, answers, questions),
                             reply_markup=confirm_keyboard(), parse_mode="HTML")


# ─── Handlerlar ─────────────────────────────────────────────────────────────

@router.callback_query(ApplicationForm.choosing_position, F.data.startswith("position:"))
async def position_selected(callback: CallbackQuery, state: FSMContext) -> None:
    position_key = callback.data.split(":", 1)[1]
    if position_key not in POSITIONS:
        await callback.answer("❌ Noto'g'ri tanlov!", show_alert=True)
        return
    questions = get_questions(position_key)
    await state.set_state(ApplicationForm.answering)
    await state.update_data(position=position_key, question_index=0, answers={}, waiting_custom=False)
    await callback.message.edit_text(
        f"✅ <b>{POSITIONS[position_key]}</b> lavozimi tanlandi!\n\n"
        f"📝 Jami <b>{len(questions)} ta savol</b> bor. Boshlaylik!",
        parse_mode="HTML",
    )
    await send_question(callback.message, questions[0], 0, len(questions))
    await callback.answer()


@router.callback_query(ApplicationForm.answering, F.data.startswith("choice:"))
async def handle_choice(callback: CallbackQuery, state: FSMContext) -> None:
    answer_value = callback.data.split(":", 1)[1]
    data         = await state.get_data()
    position     = data["position"]
    index        = data["question_index"]
    answers      = data["answers"]
    questions    = get_questions(position)
    current_q    = questions[index]

    await callback.message.edit_reply_markup(reply_markup=None)

    # ── "Boshqa" tanlansa — aniqlashtirish so'raladi ─────────────────────
    if answer_value == "Boshqa":
        await callback.answer()
        await callback.message.answer(
            "✏️ <b>Aniqroq yozing</b>\n\n"
            "<i>Tanlagan variantingizni o'zingiz yozing.\n"
            "📌 Namuna: <code>Fransuz tili</code></i>",
            reply_markup=remove_keyboard(),
            parse_mode="HTML",
        )
        await state.update_data(answers=answers, waiting_custom=True)
        return

    answers[current_q["key"]] = answer_value
    await callback.answer(f"✅ Qabul qilindi: {answer_value}")
    await _next_or_confirm(callback.message, state, position, answers, questions, index + 1)


@router.message(ApplicationForm.answering)
async def handle_text_input(message: Message, state: FSMContext) -> None:
    data       = await state.get_data()
    position   = data["position"]
    index      = data["question_index"]
    answers    = data["answers"]
    questions  = get_questions(position)
    current_q  = questions[index]
    input_type = current_q["input_type"]

    # ── "Boshqa" dan keyin aniq javob kutilmoqda ─────────────────────────
    if data.get("waiting_custom"):
        if not message.text or len(message.text.strip()) < 2:
            await message.answer("⚠️ Iltimos, to'liqroq yozing.", parse_mode="HTML")
            return
        answers[current_q["key"]] = message.text.strip()
        await _next_or_confirm(message, state, position, answers, questions, index + 1)
        return

    # ── Validatsiya ──────────────────────────────────────────────────────

    if input_type == "choice":
        await message.answer("⚠️ Iltimos, <b>tugmalardan birini tanlang</b>, matn yozmang.",
                             parse_mode="HTML")
        return

    elif input_type == "phone":
        if message.contact:
            phone = message.contact.phone_number
            if not phone.startswith("+"):
                phone = "+" + phone
            answer_value = phone
        elif message.text:
            raw     = message.text.strip()
            cleaned = re.sub(r"[\s\-\(\)]", "", raw)
            if not re.match(r"^\+?[0-9]{9,13}$", cleaned):
                await message.answer(
                    "⚠️ <b>Telefon raqam noto'g'ri formatda!</b>\n\n"
                    "Iltimos, to'g'ri formatda kiriting:\n"
                    "📌 Namuna: <code>+998 90 123 45 67</code>\n\n"
                    "Yoki tugmani bosib ulashing 👇",
                    reply_markup=phone_keyboard(), parse_mode="HTML",
                )
                return
            if not cleaned.startswith("+"):
                cleaned = "+" + cleaned
            answer_value = cleaned
        else:
            await message.answer("⚠️ Telefon raqamingizni yuboring.",
                                 reply_markup=phone_keyboard(), parse_mode="HTML")
            return

    elif input_type == "photo":
        if not message.photo:
            await message.answer("⚠️ Iltimos, <b>rasm yuboring</b>.\n"
                                 "<i>Faylni rasm sifatida yuborish kerak (document emas).</i>",
                                 parse_mode="HTML")
            return
        answer_value = message.photo[-1].file_id

    elif input_type == "document":
        if not message.document:
            await message.answer("⚠️ Iltimos, <b>CV faylini hujjat sifatida yuboring</b>.\n"
                                 "<i>Format: PDF yoki Word (.doc/.docx)</i>", parse_mode="HTML")
            return
        answer_value = message.document.file_id

    elif input_type == "text":
        if not message.text:
            await message.answer("⚠️ Iltimos, <b>matn ko'rinishida javob yuboring</b>.",
                                 parse_mode="HTML")
            return
        if len(message.text.strip()) < 2:
            await message.answer("⚠️ Javob juda qisqa. Iltimos, to'liqroq yozing.",
                                 parse_mode="HTML")
            return
        answer_value = message.text.strip()
    else:
        return

    # ── Keyingi savol yoki tasdiq ────────────────────────────────────────
    answers[current_q["key"]] = answer_value
    await _next_or_confirm(message, state, position, answers, questions, index + 1)


@router.callback_query(ApplicationForm.confirming, F.data.startswith("confirm:"))
async def handle_confirm(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    action = callback.data.split(":", 1)[1]

    if action == "restart":
        await state.clear()
        await callback.message.edit_text(
            "🔄 <b>Ariza bekor qilindi.</b>\n\nQaytadan boshlash uchun lavozimni tanlang:",
            parse_mode="HTML", reply_markup=positions_keyboard(),
        )
        await state.set_state(ApplicationForm.choosing_position)
        await callback.answer("🔄 Qaytadan boshlanmoqda...")
        return

    if action == "yes":
        data      = await state.get_data()
        position  = data["position"]
        answers   = data["answers"]
        questions = get_questions(position)

        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer("⏳ <b>Arizangiz yuborilmoqda...</b>", parse_mode="HTML")

        await save_and_notify(
            bot=bot,
            user_telegram_id=callback.from_user.id,
            position_key=position,
            answers=answers,
            questions=questions,
        )
        await state.clear()

        await callback.message.answer(
            f"🎉 <b>Arizangiz muvaffaqiyatli yuborildi!</b>\n\n"
            f"💼 <b>Lavozim:</b> {POSITIONS[position]}\n\n"
            "👥 Ilmkon School HR qo'mitasi tez orada siz bilan bog'lanadi.\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ Ko'rib chiqish muddati: <b>3–5 ish kuni</b>\n"
            "📞 Savol bo'lsa: <b>95-975-88-88</b>\n\n"
            "<i>Ilmkon School jamoasiga qo'shilishga umid qilamiz! 🏫</i>",
            parse_mode="HTML",
        )
        await callback.answer("✅ Ariza yuborildi!")


# ─── Eski tugmalarni ushlash (bot qotib qolmasin) ───────────────────────────

@router.callback_query()
async def handle_stale_callback(callback: CallbackQuery) -> None:
    await callback.answer(
        "⚠️ Bu tugma endi ishlamaydi. /start bosib qaytadan boshlang.",
        show_alert=True,
    )