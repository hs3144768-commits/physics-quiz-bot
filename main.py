import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = 8770038370:AAHSUbpadC6WhCJtzhDjucHIdxPRea_VqRM

questions = [
    {
        "q": "ما هي وحدة قياس سعة المتسعة؟",
        "options": ["الفولت", "الفاراد", "الأوم", "الأمبير"],
        "answer": 1,
    },
    {
        "q": "تزداد سعة المتسعة بزيادة:",
        "options": [
            "المسافة بين الصفيحتين",
            "فرق الجهد",
            "مساحة الصفائح",
            "المقاومة"
        ],
        "answer": 2,
    },
    {
        "q": "العلاقة بين الشحنة وسعة المتسعة وفرق الجهد هي:",
        "options": [
            "Q = CV",
            "Q = C/V",
            "Q = V/C",
            "Q = C + V"
        ],
        "answer": 0,
    },
    {
        "q": "عند زيادة المسافة بين صفيحتي المتسعة فإن سعتها:",
        "options": ["تزداد", "تقل", "تبقى ثابتة", "تصبح صفراً"],
        "answer": 1,
    },
    {
        "q": "ما هي وحدة قياس فرق الجهد؟",
        "options": ["الفاراد", "الأمبير", "الفولت", "الكولوم"],
        "answer": 2,
    },
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["score"] = 0
    context.user_data["question"] = 0

    keyboard = [
        [InlineKeyboardButton("🚀 ابدأ الاختبار", callback_data="start_quiz")]
    ]

    await update.message.reply_text(
        "📚 أهلاً بك في روبوت اختبار الفيزياء\n\n"
        "⚡ الفصل الأول: المتسعات\n\n"
        "اضغط الزر حتى نبدأ 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def send_question(query, context):
    index = context.user_data.get("question", 0)

    if index >= len(questions):
        score = context.user_data.get("score", 0)

        keyboard = [
            [InlineKeyboardButton("🔄 إعادة الاختبار", callback_data="start_quiz")]
        ]

        await query.edit_message_text(
            f"🎉 انتهى الاختبار!\n\n"
            f"🏆 درجتك: {score} من {len(questions)}\n\n"
            f"اضغط لإعادة الاختبار 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    q = questions[index]

    keyboard = []
    for i, option in enumerate(q["options"]):
        keyboard.append([
            InlineKeyboardButton(
                option,
                callback_data=f"answer_{i}"
            )
        ])

    await query.edit_message_text(
        f"📝 السؤال {index + 1} من {len(questions)}\n\n"
        f"{q['q']}",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "start_quiz":
        context.user_data["score"] = 0
        context.user_data["question"] = 0
        await send_question(query, context)
        return

    if query.data.startswith("answer_"):
        selected = int(query.data.split("_")[1])
        index = context.user_data.get("question", 0)

        if index >= len(questions):
            return

        correct = questions[index]["answer"]

        if selected == correct:
            context.user_data["score"] += 1
            message = "✅ إجابة صحيحة!"
        else:
            correct_answer = questions[index]["options"][correct]
            message = f"❌ إجابة خاطئة!\n\n✅ الصحيح: {correct_answer}"

        context.user_data["question"] += 1

        await query.edit_message_text(message)

        await send_question(query, context)


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN غير موجود")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 البوت يعمل...")
    app.run_polling()


if __name__ == "__main__":
    main()
