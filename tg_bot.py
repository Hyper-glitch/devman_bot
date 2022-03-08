def send_notification(username, lesson_title, is_lesson_failed, lesson_url, telegram_bot, chat_id):
    if is_lesson_failed:
        text = "Unfortunately your work has mistakes"
    else:
        text = "Good job, keep going br!"

    telegram_bot.send_message(chat_id=chat_id,
                              text=f"{username}, the teacher checked the work <<{lesson_title}>>" +
                                   f"\nHere is an url for the lesson: {lesson_url}\n" + text
                              )
