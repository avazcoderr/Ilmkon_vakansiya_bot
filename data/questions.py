"""
Ilmkon School — Barcha lavozimlar uchun savol-javob ma'lumotlari.
input_type: text | choice | phone | photo | document
"""

# ─── Lavozimlar ro'yxati ────────────────────────────────────────────────────

POSITIONS: dict[str, str] = {
    "teacher":      "👩‍🏫 O'qituvchi",
    "director":     "🧑‍💼 Rahbar / Director",
    "tutor":        "👨‍🏫 Sinf Rahbari (Tutor)",
    "kindergarten": "👶 Bog'cha Xodimi",
    "receptionist": "🏢 Receptionist",
}

# ─── Yordamchi funksiya ─────────────────────────────────────────────────────

def _q(key, label, text, input_type, choices=None):
    return {
        "key": key,
        "label": label,
        "text": text,
        "input_type": input_type,
        "choices": choices or [],
    }


# ═══════════════════════════════════════════════════════════════════════════
# 👩‍🏫  O'QITUVCHI
# ═══════════════════════════════════════════════════════════════════════════

TEACHER_QUESTIONS = [
    _q(
        key="subject",
        label="Fan",
        text=(
            "📚 <b>Qaysi fan o'qituvchisi sifatida ishga topshirmoqchisiz?</b>\n\n"
            "<i>O'qitmoqchi bo'lgan fanningizni quyidagi tugmalardan tanlang.\n"
            "Agar ro'yxatda yo'q bo'lsa — <b>«Boshqa»</b> ni tanlang.</i>"
        ),
        input_type="choice",
        choices=[
            "Matematika", "Fizika", "Kimyo", "Biologiya",
            "Ingliz tili", "Rus tili", "O'zbek tili va adabiyot",
            "Tarix", "Geografiya", "Informatika", "Boshqa"
        ],
    ),
    _q(
        key="fullname",
        label="Ism Familiya",
        text=(
            "👤 <b>Ism familiyangiz</b>\n\n"
            "<i>To'liq ism, familiya va otangizning ismini kiriting.\n"
            "📌 Namuna: <code>Aliyev Jasur Bahodir o'g'li</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="age",
        label="Yosh",
        text=(
            "🎂 <b>Yoshingiz</b>\n\n"
            "<i>Hozirgi yoshingizni raqamda yozing.\n"
            "📌 Namuna: <code>27</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="phone",
        label="Telefon raqam",
        text=(
            "📞 <b>Telefon raqamingiz</b>\n\n"
            "<i>Bog'lanish uchun asosiy telefon raqamingizni yuboring.\n"
            "📲 Tugmani bosib ulashing <b>yoki</b> qo'lda yozing.\n"
            "📌 Namuna: <code>+998 90 123 45 67</code></i>"
        ),
        input_type="phone",
    ),
    _q(
        key="location",
        label="Yashash joyi",
        text=(
            "📍 <b>Qayerda yashaysiz?</b>\n\n"
            "<i>Tuman yoki shahar nomini kiriting.\n"
            "📌 Namuna: <code>Surxondaryo viloyati, Denov tumani</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="university",
        label="Ta'lim muassasasi",
        text=(
            "🎓 <b>Qaysi universitetni tugatgansiz yoki o'qiyapsiz?</b>\n\n"
            "<i>O'qigan yoki o'qiyotgan oliy ta'lim muassasasi va yo'nalishingizni yozing.\n"
            "📌 Namuna: <code>TDPU — Matematika o'qituvchiligi (2019)</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="experience",
        label="O'qituvchilik tajribasi",
        text=(
            "📅 <b>O'qituvchilik tajribangiz qancha?</b>\n\n"
            "<i>Umumiy pedagogik ish stajingizni tanlang.</i>"
        ),
        input_type="choice",
        choices=["Tajribam yo'q", "1–3 yil", "3–5 yil", "5–10 yil", "10+ yil"],
    ),
    _q(
        key="last_job",
        label="Oxirgi ish joyi",
        text=(
            "🏢 <b>Oxirgi ish joyingiz va ketish sababi</b>\n\n"
            "<i>Oxirgi ishlagan tashkilotingiz nomini va u yerdan ketish sababingizni qisqacha yozing.\n"
            "📌 Namuna: <code>№45-maktab — shartnoma muddati tugadi</code>\n"
            "Agar avval ishlamagan bo'lsangiz: <code>Avval ishlamaganman</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="why_teacher",
        label="Nega o'qituvchi?",
        text=(
            "💡 <b>Nega o'qituvchi bo'lishni tanladingiz?</b>\n\n"
            "<i>Bu savol sizning kasbga bo'lgan munosabatingizni tushunishga yordam beradi.\n"
            "Samimiy va qisqacha javob yozing (2–4 jumla).</i>"
        ),
        input_type="text",
    ),
    _q(
        key="unique_quality",
        label="Farqli jihatingiz",
        text=(
            "⭐ <b>Sizni boshqa nomzodlardan ajratib turadigan jihat nima?</b>\n\n"
            "<i>O'zingizning kuchli tomonlaringiz, maxsus usullaringiz yoki\n"
            "qo'shimcha bilimlaringiz haqida yozing.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="expected_salary",
        label="Kutilgan maosh",
        text=(
            "💰 <b>Ish haqidan kutgan maoshingiz</b>\n\n"
            "<i>Oylik kutilgan maoshingiz oralig'ini tanlang.\n"
            "Bu ma'lumot HR qo'mitasi uchun mo'ljallangan.</i>"
        ),
        input_type="choice",
        choices=["3–5 mln so'm", "5–7 mln so'm", "7–10 mln so'm", "10+ mln so'm"],
    ),
    _q(
        key="computer_level",
        label="Kompyuter bilimi",
        text=(
            "💻 <b>Kompyuter bilim darajangiz</b>\n\n"
            "<i>Kompyuter va ofis dasturlari (Word, Excel, PowerPoint, Google Docs)\n"
            "bilan ishlash darajangizni tanlang.</i>"
        ),
        input_type="choice",
        choices=["🟢 Boshlang'ich", "🟡 O'rta daraja", "🔵 Yuqori daraja"],
    ),
    _q(
        key="photo",
        label="Rasm",
        text=(
            "📷 <b>Rasmingizni yuboring</b>\n\n"
            "<i>Yaqinda olingan, aniq ko'rinadigan shaxsiy rasmingizni yuboring.\n"
            "⚠️ Pasport yoki hujjat rasmi bo'lmasa ham bo'ladi — oddiy, tushunarli rasm kifoya.</i>"
        ),
        input_type="photo",
    ),
]


# ═══════════════════════════════════════════════════════════════════════════
# 🧑‍💼  RAHBAR / DIRECTOR
# ═══════════════════════════════════════════════════════════════════════════

DIRECTOR_QUESTIONS = [
    _q(
        key="position_type",
        label="Lavozim turi",
        text=(
            "🏷 <b>Qaysi lavozimga topshirmoqchisiz?</b>\n\n"
            "<i>Murojaat qilmoqchi bo'lgan boshqaruv lavozimini tanlang.</i>"
        ),
        input_type="choice",
        choices=["Direktor", "O'quv ishlari bo'yicha direktor o'rinbosari", "Tarbiya ishlari bo'yicha direktor o'rinbosari", "Administrator"],
    ),
    _q(
        key="fullname",
        label="Ism Familiya",
        text=(
            "👤 <b>Ism familiyangiz</b>\n\n"
            "<i>To'liq ism, familiya va otangizning ismini kiriting.\n"
            "📌 Namuna: <code>Karimov Bobur Salim o'g'li</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="age",
        label="Yosh",
        text=(
            "🎂 <b>Yoshingiz</b>\n\n"
            "<i>Hozirgi yoshingizni raqamda yozing.\n"
            "📌 Namuna: <code>34</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="phone",
        label="Telefon raqam",
        text=(
            "📞 <b>Telefon raqamingiz</b>\n\n"
            "<i>Bog'lanish uchun asosiy telefon raqamingizni yuboring.\n"
            "📲 Tugmani bosib ulashing <b>yoki</b> qo'lda yozing.\n"
            "📌 Namuna: <code>+998 90 123 45 67</code></i>"
        ),
        input_type="phone",
    ),
    _q(
        key="location",
        label="Yashash joyi",
        text=(
            "📍 <b>Qayerda yashaysiz?</b>\n\n"
            "<i>Viloyat va tuman nomini kiriting.\n"
            "📌 Namuna: <code>Surxondaryo viloyati, Denov tumani</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="education",
        label="Ta'lim",
        text=(
            "🎓 <b>Ta'limingiz (universitet va yo'nalish)</b>\n\n"
            "<i>Oliy ta'lim muassasasi, yo'nalish va bitiruv yilini yozing.\n"
            "📌 Namuna: <code>TATU — Axborot texnologiyalari (2015)</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="total_experience",
        label="Umumiy ish tajribasi",
        text=(
            "📅 <b>Umumiy ish tajribangiz qancha?</b>\n\n"
            "<i>Barcha sohalardagi ish stajingizni tanlang.</i>"
        ),
        input_type="choice",
        choices=["1–3 yil", "3–5 yil", "5–10 yil", "10+ yil"],
    ),
    _q(
        key="management_experience",
        label="Rahbarlik tajribasi",
        text=(
            "👔 <b>Oldin rahbar lavozimida ishlaganmisiz?</b>\n\n"
            "<i>Mudir, rahbar, boshliq yoki boshqaruv lavozimlarida ishlagan bo'lsangiz — «Ha» ni tanlang.\n"
            "Ijobiy javob bergan holda qayerda va qancha vaqt ishlagan bo'lsangiz — quyida yozing.</i>"
        ),
        input_type="choice",
        choices=["✅ Ha, ishlaganman", "❌ Yo'q, ishlamaganman"],
    ),
    _q(
        key="conflict_resolution",
        label="Nizolarni hal qilish",
        text=(
            "🤝 <b>Xodimlar orasidagi nizoni qanday hal qilasiz?</b>\n\n"
            "<i>Jamoadagi kelishmovchilik yoki ziddiyatga duch kelganingizda\n"
            "qanday yondashuv qo'llashingizni tasvirlab bering (3–5 jumla).</i>"
        ),
        input_type="text",
    ),
    _q(
        key="school_discipline",
        label="Maktab tartibini saqlash",
        text=(
            "📋 <b>Maktabda tartib-intizomni qanday saqlaysiz?</b>\n\n"
            "<i>O'quvchilar va xodimlar orasida intizomni ta'minlash\n"
            "bo'yicha o'z yondashuvingizni qisqacha yozing.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="development_plans",
        label="Rivojlantirish rejalari",
        text=(
            "🚀 <b>Ilmkon Schoolni qanday rivojlantirmoqchisiz?</b>\n\n"
            "<i>Maktabga qo'shilsangiz, birinchi 3–6 oyda amalga oshirmoqchi bo'lgan\n"
            "1–3 ta konkret g'oyangizni yozing.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="why_this_school",
        label="Nega Ilmkon School?",
        text=(
            "🏫 <b>Nega aynan Ilmkon Schoolda ishlamoqchisiz?</b>\n\n"
            "<i>Tashkilotga qo'shilish motivatsiyangizni samimiy tarzda yozing.\n"
            "Bu javob qo'mita uchun muhim hisoblanadi.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="computer_level",
        label="Kompyuter bilimi",
        text=(
            "💻 <b>Kompyuter bilim darajangiz</b>\n\n"
            "<i>MS Office, Google Workspace va boshqaruv tizimlari bilan\n"
            "ishlash darajangizni tanlang.</i>"
        ),
        input_type="choice",
        choices=["🟢 Boshlang'ich", "🟡 O'rta daraja", "🔵 Yuqori daraja"],
    ),
    _q(
        key="photo",
        label="Rasm",
        text=(
            "📷 <b>Rasmingizni yuboring</b>\n\n"
            "<i>Aniq, professional ko'rinishdagi shaxsiy rasmingizni yuboring.</i>"
        ),
        input_type="photo",
    ),
]


# ═══════════════════════════════════════════════════════════════════════════
# 👨‍🏫  SINF RAHBARI (TUTOR)
# ═══════════════════════════════════════════════════════════════════════════

TUTOR_QUESTIONS = [
    _q(
        key="fullname",
        label="Ism Familiya",
        text=(
            "👤 <b>Ism familiyangiz</b>\n\n"
            "<i>To'liq ism, familiya va otangizning ismini kiriting.\n"
            "📌 Namuna: <code>Yusupova Zulfiya Hamid qizi</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="age",
        label="Yosh",
        text=(
            "🎂 <b>Yoshingiz</b>\n\n"
            "<i>Yoshingizni raqamda yozing.\n"
            "📌 Namuna: <code>24</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="phone",
        label="Telefon raqam",
        text=(
            "📞 <b>Telefon raqamingiz</b>\n\n"
            "<i>Asosiy bog'lanish raqamingizni yuboring.\n"
            "📲 Tugmani bosib ulashing <b>yoki</b> qo'lda yozing.\n"
            "📌 Namuna: <code>+998 93 456 78 90</code></i>"
        ),
        input_type="phone",
    ),
    _q(
        key="location",
        label="Yashash joyi",
        text=(
            "📍 <b>Qayerda yashaysiz?</b>\n\n"
            "<i>Viloyat va tuman nomini kiriting.\n"
            "📌 Namuna: <code>Surxondaryo viloyati, Denov tumani</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="education",
        label="Ta'lim",
        text=(
            "🎓 <b>Ta'limingiz</b>\n\n"
            "<i>O'qigan yoki o'qiyotgan oliy ta'lim muassasasi va yo'nalishingizni yozing.\n"
            "📌 Namuna: <code>NamDU — Pedagogika va psixologiya (2022)</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="children_experience",
        label="Bolalar bilan tajriba",
        text=(
            "👦 <b>Bolalar bilan ishlash tajribangiz</b>\n\n"
            "<i>Avval o'quvchilar yoki bolalar bilan ishlagan bo'lsangiz — qayerda,\n"
            "qancha vaqt va qanday formatda ishlagan bo'lsangiz yozing.\n"
            "Tajriba yo'q bo'lsa ham, qisqacha tushuntiring.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="class_management",
        label="Sinf boshqaruvi",
        text=(
            "🏫 <b>Sinfni qanday boshqarasiz?</b>\n\n"
            "<i>O'quvchilar tartibini saqlash, motivatsiya va sinf muhitini\n"
            "shakllantirishga yondashuvingizni tasvirlab bering.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="unmotivated_student",
        label="Motivatsiyasiz o'quvchi",
        text=(
            "😔 <b>O'quvchi darsni xohlamasa nima qilasiz?</b>\n\n"
            "<i>Darsga qiziqqisi kelmaydigan yoki faol bo'lmagan o'quvchi bilan\n"
            "qanday ishlashingizni tasvirlab bering (konkret misol keltiring).</i>"
        ),
        input_type="text",
    ),
    _q(
        key="parent_relations",
        label="Ota-ona bilan munosabat",
        text=(
            "👨‍👩‍👧 <b>Ota-ona bilan qanday ishlaysiz?</b>\n\n"
            "<i>Ota-onalar bilan muloqot, ma'lumot yetkazish va hamkorlik qilish\n"
            "uslubingizni qisqacha yozing.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="strength",
        label="Kuchli jihatingiz",
        text=(
            "💪 <b>Sizning eng kuchli jihatingiz nima?</b>\n\n"
            "<i>Sinf rahbari sifatida o'zingizning eng asosiy qobiliyat yoki\n"
            "xususiyatingizni aytib bering.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="computer_level",
        label="Kompyuter bilimi",
        text=(
            "💻 <b>Kompyuter bilim darajangiz</b>\n\n"
            "<i>Asosiy ofis dasturlari va raqamli vositalar bilan\n"
            "ishlash darajangizni tanlang.</i>"
        ),
        input_type="choice",
        choices=["🟢 Boshlang'ich", "🟡 O'rta daraja", "🔵 Yuqori daraja"],
    ),
    _q(
        key="why_tutor",
        label="Nega sinf rahbari?",
        text=(
            "❓ <b>Nega sinf rahbari bo'lishni xohlaysiz?</b>\n\n"
            "<i>Bu lavozimga motivatsiyangizni 2–3 jumlada yozing.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="photo",
        label="Rasm",
        text=(
            "📷 <b>Rasmingizni yuboring</b>\n\n"
            "<i>Aniq ko'rinadigan shaxsiy rasmingizni yuboring.</i>"
        ),
        input_type="photo",
    ),
]


# ═══════════════════════════════════════════════════════════════════════════
# 👶  BOG'CHA XODIMI
# ═══════════════════════════════════════════════════════════════════════════

KINDERGARTEN_QUESTIONS = [
    _q(
        key="position_type",
        label="Lavozim turi",
        text=(
            "🏷 <b>Qaysi lavozimga topshirmoqchisiz?</b>\n\n"
            "<i>Bog'chada ishlash uchun murojaat qilmoqchi bo'lgan lavozimni tanlang.</i>"
        ),
        input_type="choice",
        choices=["Tarbiyachi", "Yordamchi tarbiyachi", "Psixolog", "Logoped", "Musiqa rahbari", "Boshqa"],
    ),
    _q(
        key="fullname",
        label="Ism Familiya",
        text=(
            "👤 <b>Ism familiyangiz</b>\n\n"
            "<i>To'liq ism, familiya va otangizning ismini kiriting.\n"
            "📌 Namuna: <code>Mirzayeva Dilnoza Akbar qizi</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="birth_date",
        label="Tug'ilgan sana",
        text=(
            "📅 <b>Tug'ilgan sanangiz</b>\n\n"
            "<i>Tug'ilgan sanangizni kiriting.\n"
            "📌 Namuna: <code>15.03.1998</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="phone",
        label="Telefon raqam",
        text=(
            "📞 <b>Telefon raqamingiz</b>\n\n"
            "<i>Bog'lanish uchun asosiy raqamingizni yuboring.\n"
            "📲 Tugmani bosib ulashing <b>yoki</b> qo'lda yozing.\n"
            "📌 Namuna: <code>+998 94 567 89 01</code></i>"
        ),
        input_type="phone",
    ),
    _q(
        key="location",
        label="Yashash joyi",
        text=(
            "📍 <b>Yashash manzilingiz</b>\n\n"
            "<i>Viloyat va tuman nomini kiriting.\n"
            "📌 Namuna: <code>Surxondaryo viloyati, Denov tumani</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="education",
        label="Ta'lim",
        text=(
            "🎓 <b>Ta'limingiz</b>\n\n"
            "<i>O'qigan ta'lim muassasasi, yo'nalish va bitiruv yilini yozing.\n"
            "O'rta maxsus ta'lim ham bo'lishi mumkin.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="pedagogical_courses",
        label="Pedagogik kurslar",
        text=(
            "📜 <b>Pedagogik kurslardan o'tganmisiz?</b>\n\n"
            "<i>Maktabgacha ta'lim, tarbiyachilik yoki bolalar psixologiyasi bo'yicha\n"
            "qo'shimcha kurslar o'tagan bo'lsangiz — «Ha» ni tanlang.</i>"
        ),
        input_type="choice",
        choices=["✅ Ha, o'tganman", "❌ Yo'q, o'tmaganman"],
    ),
    _q(
        key="children_experience",
        label="Bolalar bilan tajriba",
        text=(
            "👦 <b>Bolalar bilan ishlash tajribangiz</b>\n\n"
            "<i>Kichik yoshdagi bolalar (2–7 yosh) bilan qanday ishlagan bo'lsangiz yozing.\n"
            "Tajriba yo'q bo'lsa ham, o'z yondashuvingizni ifodalang.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="emergency_action",
        label="Favqulodda vaziyat",
        text=(
            "🚨 <b>Favqulodda vaziyatda qanday harakat qilasiz?</b>\n\n"
            "<i>Masalan: bola yiqilib qoldi, to'satdan kasal bo'ldi yoki yo'qoldi.\n"
            "Bunday holda qanday harakat qilishingizni tasvirlab bering.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="kindergarten_role",
        label="Bog'cha xodimining roli",
        text=(
            "💭 <b>Bog'cha xodimining asosiy vazifasi nima deb o'ylaysiz?</b>\n\n"
            "<i>Bu savol sizning pedagogik qarashlaringizni aniqlashga yordam beradi.\n"
            "O'z fikringizni 2–3 jumlada yozing.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="team_experience",
        label="Jamoa bilan ishlash",
        text=(
            "🤝 <b>Jamoa bilan ishlash tajribangiz</b>\n\n"
            "<i>Oldingi ish yoki o'qishda jamoa bilan birgalikda ishlash tajribangizni yozing.\n"
            "Qiyinchiliklar bo'lgan bo'lsa — ularni qanday yenggandingiz ham qo'shing.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="computer_level",
        label="Kompyuter bilimi",
        text=(
            "💻 <b>Kompyuter bilim darajangiz</b>\n\n"
            "<i>Asosiy ofis dasturlari bilan ishlash darajangizni tanlang.</i>"
        ),
        input_type="choice",
        choices=["🟢 Boshlang'ich", "🟡 O'rta daraja", "🔵 Yuqori daraja"],
    ),
    _q(
        key="photo",
        label="Rasm",
        text=(
            "📷 <b>Rasmingizni yuboring</b>\n\n"
            "<i>Aniq ko'rinadigan shaxsiy rasmingizni yuboring.</i>"
        ),
        input_type="photo",
    ),
]


# ═══════════════════════════════════════════════════════════════════════════
# 🏢  RECEPTIONIST
# ═══════════════════════════════════════════════════════════════════════════

RECEPTIONIST_QUESTIONS = [
    _q(
        key="fullname",
        label="Ism Familiya",
        text=(
            "👤 <b>Ism familiyangiz</b>\n\n"
            "<i>To'liq ism, familiya va otangizning ismini kiriting.\n"
            "📌 Namuna: <code>Xasanova Nilufar Ravshan qizi</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="age",
        label="Yosh",
        text=(
            "🎂 <b>Yoshingiz</b>\n\n"
            "<i>Yoshingizni raqamda kiriting.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="phone",
        label="Telefon raqam",
        text=(
            "📞 <b>Telefon raqamingiz</b>\n\n"
            "<i>Asosiy bog'lanish raqamingizni yuboring.\n"
            "📲 Tugmani bosib ulashing <b>yoki</b> qo'lda yozing.\n"
            "📌 Namuna: <code>+998 91 234 56 78</code></i>"
        ),
        input_type="phone",
    ),
    _q(
        key="location",
        label="Yashash joyi",
        text=(
            "📍 <b>Qayerda yashaysiz?</b>\n\n"
            "<i>Viloyat va tuman nomini kiriting.\n"
            "📌 Namuna: <code>Surxondaryo viloyati, Denov tumani</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="education",
        label="Ta'lim",
        text=(
            "🎓 <b>Ta'limingiz</b>\n\n"
            "<i>O'qigan ta'lim muassasasi va yo'nalishingizni yozing.\n"
            "📌 Namuna: <code>TDIU — Menejment (3-kurs)</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="direction",
        label="Mutaxassislik yo'nalishi",
        text=(
            "📖 <b>Mutaxassislik yo'nalishingiz</b>\n\n"
            "<i>Diplom yoki o'qish yo'nalishingizni aniqroq yozing.\n"
            "📌 Namuna: <code>Biznes-menejment, Iqtisodiyot</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="previous_work",
        label="Oldingi ish tajribasi",
        text=(
            "💼 <b>Oldin receptionist yoki xizmat ko'rsatish sohasida ishlaganmisiz?</b>\n\n"
            "<i>Call-markaz, qabulxona, mijozlar xizmati, ofis menejeri kabi lavozimlarda\n"
            "ishlagan bo'lsangiz — «Ha» ni tanlang va pastda qayerda ishlagan bo'lsangiz yozing.</i>"
        ),
        input_type="choice",
        choices=["✅ Ha, ishlaganman", "❌ Yo'q, bu soha yangi"],
    ),
    _q(
        key="computer_level",
        label="Kompyuter bilimi",
        text=(
            "💻 <b>Kompyuter bilim darajangiz</b>\n\n"
            "<i>MS Office (Word, Excel), elektron pochta va ofis dasturlari bilan\n"
            "ishlash darajangizni tanlang.</i>"
        ),
        input_type="choice",
        choices=["🟢 Boshlang'ich", "🟡 O'rta daraja", "🔵 Yuqori daraja"],
    ),
    _q(
        key="phone_style",
        label="Telefon qo'ng'iroqlariga javob berish",
        text=(
            "📟 <b>Telefon qo'ng'iroqlariga javob berish uslubingiz</b>\n\n"
            "<i>Kiruvchi qo'ng'iroqqa qanday javob berasiz?\n"
            "Odatdagi murojaat jumlangizni yozing.\n"
            "📌 Namuna: <code>Ilmkon School, assalomu alaykum, qanday yordam bera olaman?</code></i>"
        ),
        input_type="text",
    ),
    _q(
        key="client_communication",
        label="Mijoz bilan muomala",
        text=(
            "🤝 <b>Norozilik bildirgan mijoz bilan qanday muomala qilasiz?</b>\n\n"
            "<i>Qiyin yoki asabiy mijoz bilan muloqotda qanday harakat qilishingizni\n"
            "konkret misol bilan tasvirlab bering.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="stress_management",
        label="Stress ostida ishlash",
        text=(
            "⚡ <b>Stressli vaziyatda o'zingizni qanday tutasiz?</b>\n\n"
            "<i>Bir vaqtda ko'p ish, shoshilinch vaziyat yoki qiyin mijozlar bo'lganda\n"
            "o'zingizni qanday boshqarishingizni yozing.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="multitasking",
        label="Ko'p vazifani boshqarish",
        text=(
            "🗂 <b>Bir vaqtda bir nechta ishni boshqarish qobiliyatingiz</b>\n\n"
            "<i>Telefon jiringlayotganda, mijoz kutib turgan va hujjat to'ldirishingiz\n"
            "kerak bo'lgan vaqtda qanday harakat qilasiz?</i>"
        ),
        input_type="text",
    ),
    _q(
        key="why_receptionist",
        label="Nega receptionist?",
        text=(
            "💡 <b>Nega receptionist bo'lmoqchisiz?</b>\n\n"
            "<i>Bu lavozimga qiziqishingiz va motivatsiyangizni\n"
            "samimiy tarzda 2–3 jumlada yozing.</i>"
        ),
        input_type="text",
    ),
    _q(
        key="photo",
        label="Rasm",
        text=(
            "📷 <b>Rasmingizni yuboring</b>\n\n"
            "<i>Professional yoki oddiy, lekin aniq ko'rinadigan rasmingizni yuboring.</i>"
        ),
        input_type="photo",
    ),
]


# ─── Umumiy kirish nuqtasi ───────────────────────────────────────────────────

QUESTIONS_MAP: dict[str, list[dict]] = {
    "teacher":      TEACHER_QUESTIONS,
    "director":     DIRECTOR_QUESTIONS,
    "tutor":        TUTOR_QUESTIONS,
    "kindergarten": KINDERGARTEN_QUESTIONS,
    "receptionist": RECEPTIONIST_QUESTIONS,
}


def get_questions(position_key: str) -> list[dict]:
    return QUESTIONS_MAP.get(position_key, [])