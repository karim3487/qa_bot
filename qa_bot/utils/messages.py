from aiogram import html


class MESSAGES_RU:
    class Info:
        answer_from_admin = "Ответ от администратора:"
        answer_from_api = "Ответ на Ваш вопрос:"
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
                return "\n".join([prefix, html.italic(html.quote(answer)), feedback])

            @staticmethod
            def from_admin(answer: str) -> str:
                return (
                    MESSAGES_RU.Info.AnswerWithReactions._format_response_with_reactions(
                        MESSAGES_RU.Info.answer_from_admin,
                        answer,
                        MESSAGES_RU.Reactions.to_answer,
                    )
                )

            @staticmethod
            def from_api(answer: str) -> str:
                return (
                    MESSAGES_RU.Info.AnswerWithReactions._format_response_with_reactions(
                        MESSAGES_RU.Info.answer_from_api,
                        answer,
                        MESSAGES_RU.Reactions.to_answer,
                    )
                )

        class ResponseFromApi:
            @staticmethod
            def _format_response_from_api(answer: str, feedback: str) -> str:
                return "\n".join(
                    [
                        MESSAGES_RU.Info.answer_from_api,
                        html.italic(html.quote(answer)),
                        feedback,
                    ]
                )

            @staticmethod
            def ok(answer: str) -> str:
                return MESSAGES_RU.Info.ResponseFromApi._format_response_from_api(
                    answer, MESSAGES_RU.Info.ThanksForFeedback.ok
                )

            @staticmethod
            def nok(answer: str) -> str:
                return MESSAGES_RU.Info.ResponseFromApi._format_response_from_api(
                    answer, MESSAGES_RU.Info.ThanksForFeedback.nok
                )

        class ResponseFromAdmin:
            @staticmethod
            def _format_response_from_admin(answer: str, feedback: str) -> str:
                return "\n".join(
                    [
                        MESSAGES_RU.Info.answer_from_admin,
                        html.italic(html.quote(answer)),
                        feedback,
                    ]
                )

            @staticmethod
            def ok(answer: str) -> str:
                return MESSAGES_RU.Info.ResponseFromAdmin._format_response_from_admin(
                    answer, MESSAGES_RU.Info.ThanksForFeedback.ok
                )

            @staticmethod
            def nok(answer: str) -> str:
                return MESSAGES_RU.Info.ResponseFromAdmin._format_response_from_admin(
                    answer, MESSAGES_RU.Info.another_questions
                )

        @staticmethod
        def cleared_message(asker_username_url: str, answering_username_url: str, question: str, answer_text: str):
            return "\n".join(
                [
                    f"Пользователь {asker_username_url} задал вопрос:",
                    html.code(html.quote(question)),
                    f"\n✅ На него ответил администратор {answering_username_url}:",
                    f"{html.quote(answer_text)}",
                ]
            )

        @staticmethod
        def question_after_reaction(question: str, answer: str) -> str:
            return "\n".join(
                [
                    "Вопрос",
                    html.code(html.quote(question)),
                    "Ответ от системы",
                    html.italic(html.quote(answer)),
                    "\nПользователю не помог ответ от системы",
                ]
            )

        @staticmethod
        def question_without_answer(
                username_url: str, question: str, answers: list[str, ...]
        ) -> str:
            return "\n".join(
                [
                    f"Пользователь {username_url} задал вопрос:",
                    html.code(html.quote(question)),
                    f"\n{html.bold('Предложения системы:')}",
                    f"\n".join(
                        [
                            f"\n#️⃣ {html.bold(i + 1)}. {html.quote(answer)}"
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
        def add_answer(answer: str) -> str:
            return "\n".join(
                [
                    "✅ Ответ добавлен в БД:",
                    html.italic(html.quote(answer)),
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
            "Не получается найти сообщение с таким ID!\nПопробуйте еще раз"
        )
        question_from_another_user = "Кечиресиз, сиз бул суроону берген эмессиз"
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
                f"Пример: {html.code('/ответ 12 Ваш_ответ')}"
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
        to_answer = "\nЖооп сизге жардам бере алдыбы?\n" "👍 – Ооба\n" "👎 – Жок"


class MESSAGES_KY(MESSAGES_RU):
    class Info(MESSAGES_RU.Info):
        answer_from_admin = "Администратордун жообу:"
        answer_from_api = "Сиздин сурооңуздун жообу:"
        another_questions = "\nКалган суроолорду жазыңыз:"
        waiting = (
            "Күтө туруңуз, администратор бир аз убакыттан кийин сурооңузга жооп берет."
        )

        class ThanksForFeedback(MESSAGES_RU.Info.ThanksForFeedback):
            ok = "\nПикириңиз үчүн рахмат, жардам берүүгө дайым даярбыз"
            nok = "\nПикириңиз үчүн рахмат, администратор бир аз убакыттан кийин сурооңузга жооп берет"

        class AnswerWithReactions(MESSAGES_RU.Info.AnswerWithReactions):
            @staticmethod
            def _format_response_with_reactions(
                    prefix: str, answer: str, feedback: str
            ) -> str:
                return "\n".join([prefix, html.italic(html.quote(answer)), feedback])

            @staticmethod
            def from_admin(answer: str) -> str:
                return (
                    MESSAGES_KY.Info.AnswerWithReactions._format_response_with_reactions(
                        MESSAGES_KY.Info.answer_from_admin,
                        answer,
                        MESSAGES_KY.Reactions.to_answer,
                    )
                )

            @staticmethod
            def from_api(answer: str) -> str:
                return (
                    MESSAGES_KY.Info.AnswerWithReactions._format_response_with_reactions(
                        MESSAGES_KY.Info.answer_from_api,
                        answer,
                        MESSAGES_KY.Reactions.to_answer,
                    )
                )
        
        class ResponseFromApi(MESSAGES_RU.Info.ResponseFromApi):
            @staticmethod
            def _format_response_from_api(answer: str, feedback: str) -> str:
                return "\n".join(
                    [
                        MESSAGES_KY.Info.answer_from_api,
                        html.italic(html.quote(answer)),
                        feedback,
                    ]
                )

            @staticmethod
            def ok(answer: str) -> str:
                return MESSAGES_KY.Info.ResponseFromApi._format_response_from_api(
                    answer, MESSAGES_KY.Info.ThanksForFeedback.ok
                )

            @staticmethod
            def nok(answer: str) -> str:
                return MESSAGES_KY.Info.ResponseFromApi._format_response_from_api(
                    answer, MESSAGES_KY.Info.ThanksForFeedback.nok
                )
            
        class ResponseFromAdmin(MESSAGES_RU.Info.ResponseFromAdmin):
            @staticmethod
            def _format_response_from_admin(answer: str, feedback: str) -> str:
                return "\n".join(
                    [
                        MESSAGES_KY.Info.answer_from_admin,
                        html.italic(html.quote(answer)),
                        feedback,
                    ]
                )

            @staticmethod
            def ok(answer: str) -> str:
                return MESSAGES_KY.Info.ResponseFromAdmin._format_response_from_admin(
                    answer, MESSAGES_KY.Info.ThanksForFeedback.ok
                )

            @staticmethod
            def nok(answer: str) -> str:
                return MESSAGES_KY.Info.ResponseFromAdmin._format_response_from_admin(
                    answer, MESSAGES_KY.Info.another_questions
                )

        @staticmethod
        def cleared_message(asker_username_url: str, answering_username_url: str, question: str, answer_text: str):
            return "\n".join(
                [
                    f"Пользователь {asker_username_url} задал вопрос:",
                    html.code(html.quote(question)),
                    f"\n✅ На него ответил администратор {answering_username_url}:",
                    f"{html.quote(answer_text)}",
                ]
            )

        @staticmethod
        def question_after_reaction(question: str, answer: str) -> str:
            return "\n".join(
                [
                    "Суроо",
                    html.code(html.quote(question)),
                    "Ответ от системы",
                    html.italic(html.quote(answer)),
                    "\nКолдонуучуга системанын жообу жардам бере алган жок",
                ]
            )

        @staticmethod
        def question_without_answer(
                username_url: str, question: str, answers: list[str, ...]
        ) -> str:
            return "\n".join(
                [
                    f"Колдонуучунун {username_url} суроосуна:",
                    html.code(html.quote(question)),
                    f"\nСистеманын сунушу:",
                    f"\n".join(
                        [
                            f"\n#️⃣ {html.bold(i + 1)}. {html.quote(answer)}"
                            for i, answer in enumerate(answers)
                        ]
                    ),
                ]
            )

