from aiogram import html


class MESSAGES:
    class Info:
        answer_from_admin = "Ответ от администратора:"
        answer_from_api = "Ответ на Ваш вопрос:"
        answer_sent = "✅ Ответ отправлен"
        another_questions = "\nНапишите оставшиеся вопросы:"
        waiting = (
            "Подождите немного, админ ответит на этот вопрос через некоторое время."
        )

        class ThanksForFeedback:
            ok = "\nСпасибо за отзыв, всегда рады помочь Вам"
            nok = "\nСпасибо за отзыв, администратор скоро ответит на Ваш вопрос"

        class AnswerWithReactions:
            @staticmethod
            def _format_response_with_reactions(
                prefix: str, answer: str, feedback: str
            ) -> str:
                return "\n".join([prefix, html.code(html.quote(answer)), feedback])

            @staticmethod
            def from_admin(answer: str) -> str:
                return (
                    MESSAGES.Info.AnswerWithReactions._format_response_with_reactions(
                        MESSAGES.Info.answer_from_admin,
                        answer,
                        MESSAGES.Reactions.to_answer,
                    )
                )

            @staticmethod
            def from_api(answer: str) -> str:
                return (
                    MESSAGES.Info.AnswerWithReactions._format_response_with_reactions(
                        MESSAGES.Info.answer_from_api,
                        answer,
                        MESSAGES.Reactions.to_answer,
                    )
                )

        class ResponseFromApi:
            @staticmethod
            def _format_response_from_api(answer: str, feedback: str) -> str:
                return "\n".join(
                    [
                        MESSAGES.Info.answer_from_api,
                        html.code(html.quote(answer)),
                        feedback,
                    ]
                )

            @staticmethod
            def ok(answer: str) -> str:
                return MESSAGES.Info.ResponseFromApi._format_response_from_api(
                    answer, MESSAGES.Info.ThanksForFeedback.ok
                )

            @staticmethod
            def nok(answer: str) -> str:
                return MESSAGES.Info.ResponseFromApi._format_response_from_api(
                    answer, MESSAGES.Info.ThanksForFeedback.nok
                )

        class ResponseFromAdmin:
            @staticmethod
            def _format_response_from_admin(answer: str, feedback: str) -> str:
                return "\n".join(
                    [
                        MESSAGES.Info.answer_from_admin,
                        html.code(html.quote(answer)),
                        feedback,
                    ]
                )

            @staticmethod
            def ok(answer: str) -> str:
                return MESSAGES.Info.ResponseFromAdmin._format_response_from_admin(
                    answer, MESSAGES.Info.ThanksForFeedback.ok
                )

            @staticmethod
            def nok(answer: str) -> str:
                return MESSAGES.Info.ResponseFromAdmin._format_response_from_admin(
                    answer, MESSAGES.Info.another_questions
                )

        @staticmethod
        def question_after_reaction(question: str, answer: str) -> str:
            return "\n".join(
                [
                    "Вопрос",
                    html.code(html.quote(question)),
                    "Ответ от системы",
                    html.code(html.quote(answer)),
                    "\nПользователю не помог ответ от системы",
                ]
            )

        @staticmethod
        def question_without_answer(
            username_url: str, question: str, answers: list[str, ...]
        ) -> str:
            return "\n".join(
                [
                    f"Пользователь {username_url} задал вопрос, ответ на который не нашелся в системе:",
                    html.code(html.quote(question)),
                    f"\nПредложения системы:",
                    f"\n".join(
                        [
                            f"\n#️⃣ {i + 1}. {html.code(html.quote(answer))}"
                            for i, answer in enumerate(answers)
                        ]
                    ),
                ]
            )

        @staticmethod
        def another_question(username_url: str, question: str):
            return "\n".join(
                [
                    f"Пользователю {username_url} не понравился ответ. Он задал еще один вопрос:",
                    html.code(html.quote(question)),
                ]
            )

        @staticmethod
        def new_question(question: str, answer_from_api: str) -> str:
            return "\n".join(
                [
                    "Вопрос:",
                    question,
                    "\nОтвет системы:",
                    answer_from_api,
                    "\nПользователю не помог ответ от системы",
                ]
            )

        @staticmethod
        def add_instruction_to_question(
            question: str,
            question_mid: str | int,
            username: str,
        ) -> str:
            return "\n".join(
                [
                    question,
                    "\nЧтобы ответить на вопрос введите:",
                    html.code(f"/ответить {question_mid} Ваш_ответ"),
                    f"\nЗа ответ взялся {username}",
                ]
            )

        @staticmethod
        def add_sent_status(message: str) -> str:
            return "\n".join([message, MESSAGES.Info.answer_sent])

        @staticmethod
        def add_answer(answer: str) -> str:
            return "\n".join(
                [
                    "✅ Ответ добавлен в БД:",
                    html.code(html.quote(answer)),
                ]
            )

        @staticmethod
        def get_chat_id(cid: str | int) -> str:
            return f"ID чата: {html.bold(html.quote(cid))}"

    class Errors:
        add_answer = (
            "Вы должны ответить на какое-нибудь сообщение "
            "этой командой, чтобы добавить ответ в БД."
        )
        cancel_answering = "На этот вопрос отвечает другой администратор."
        not_found_cid_or_mid = (
            "Не получается найти чат с таким ID или сообщение!\n" "Попробуйте еще раз"
        )
        question_from_another_user = "Простите, это не Вы задавали этот вопрос"
        answer_already_exists = "Такой ответ уже есть в БД"
        other = (
            f"Упс! {html.bold('Ошибка!')} Не переживайте, "
            f"ошибка уже {html.bold('отправлена')} разработчику."
        )
        cannot_change_page = "Вы не можете переключиться на эту страницу"

        class AnswerToTheQuestion:
            did_not_reply_to_the_msg = "Вам нужно ответить на сообщение с вопросом"
            no_args = "Вы ввели что-то не то, попробуйте еще раз"
            incorrect_args = (
                "Укажите аргументы команды\n"
                f"Пример: {html.code('/ответ 516712732 12 Ваш_ответ')}"
            )

        @staticmethod
        def report_message(cid: str | int, exception: Exception) -> str:
            return "\n".join(
                [
                    f"Случилась {html.bold('ошибка')} в чате {html.bold(cid)}\n"
                    f"Статус ошибки: {html.code(html.quote(exception))}"
                ]
            )

    class Reactions:
        to_answer = "\nПомог ли вам ответ?\n" "👍 – Да\n" "👎 – Нет"
