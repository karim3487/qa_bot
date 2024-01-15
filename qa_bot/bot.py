import asyncio

import aiojobs
import orjson
from aiogram import Bot, Dispatcher
from aiohttp import web

from qa_bot import handlers, utils, web_handlers
from qa_bot.data import config
from qa_bot.middlewares import StructLoggingMiddleware
from qa_bot.utils.commands import set_default_commands


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(handlers.user.prepare_router())
    dp.include_router(handlers.groups.prepare_router())
    dp.include_router(handlers.admin_group.prepare_router())
    dp.include_router(handlers.support_group.prepare_router())


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(StructLoggingMiddleware(logger=dp["aiogram_logger"]))

def setup_commands(dp: Dispatcher) -> None:
    dp.startup.register(set_default_commands)


def setup_logging(dp: Dispatcher) -> None:
    dp["aiogram_logger"] = utils.logging.setup_logger().bind(type="aiogram")
    dp["db_logger"] = utils.logging.setup_logger().bind(type="db")
    dp["cache_logger"] = utils.logging.setup_logger().bind(type="cache")
    dp["business_logger"] = utils.logging.setup_logger().bind(type="business")


async def setup_aiogram(dp: Dispatcher) -> None:
    setup_logging(dp)
    logger = dp["aiogram_logger"]
    logger.debug("Configuring aiogram")
    setup_handlers(dp)
    setup_middlewares(dp)
    setup_commands(dp)
    logger.info("Configured aiogram")


async def aiohttp_on_startup(app: web.Application) -> None:
    dp: Dispatcher = app["dp"]
    workflow_data = {"app": app, "dispatcher": dp}
    if "bot" in app:
        workflow_data["bot"] = app["bot"]
    await dp.emit_startup(**workflow_data)


async def aiohttp_on_shutdown(app: web.Application) -> None:
    dp: Dispatcher = app["dp"]
    for i in [app, *app._subapps]:  # dirty
        if "scheduler" in i:
            scheduler: aiojobs.Scheduler = i["scheduler"]
            scheduler._closed = True
            while scheduler.pending_count != 0:
                dp["aiogram_logger"].info(
                    f"Waiting for {scheduler.pending_count} tasks to complete"
                )
                await asyncio.sleep(1)
    workflow_data = {"app": app, "dispatcher": dp}
    if "bot" in app:
        workflow_data["bot"] = app["bot"]
    await dp.emit_shutdown(**workflow_data)


async def aiogram_on_startup_webhook(dispatcher: Dispatcher, bot: Bot) -> None:
    await setup_aiogram(dispatcher)
    webhook_logger = dispatcher["aiogram_logger"].bind(
        webhook_url=config.MAIN_WEBHOOK_ADDRESS
    )
    webhook_logger.debug("Configuring webhook")
    await bot.set_webhook(
        url=config.MAIN_WEBHOOK_ADDRESS.format(
            token=config.BOT_TOKEN, bot_id=config.BOT_TOKEN.split(":")[0]
        ),
        allowed_updates=dispatcher.resolve_used_update_types(),
        secret_token=config.MAIN_WEBHOOK_SECRET_TOKEN,
    )
    webhook_logger.info("Configured webhook")


async def aiogram_on_shutdown_webhook(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher["aiogram_logger"].debug("Stopping webhook")
    await bot.session.close()
    await dispatcher.storage.close()
    dispatcher["aiogram_logger"].info("Stopped webhook")


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dispatcher)
    dispatcher["aiogram_logger"].info("Started polling")


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher["aiogram_logger"].debug("Stopping polling")
    await bot.session.close()
    await dispatcher.storage.close()
    dispatcher["aiogram_logger"].info("Stopped polling")


async def setup_aiohttp_app(bot: Bot, dp: Dispatcher) -> web.Application:
    scheduler = aiojobs.Scheduler()
    app = web.Application()
    subapps: list[tuple[str, web.Application]] = [
        ("/tg/webhooks/", web_handlers.tg_updates_app),
    ]
    for prefix, subapp in subapps:
        subapp["bot"] = bot
        subapp["dp"] = dp
        subapp["scheduler"] = scheduler
        app.add_subapp(prefix, subapp)
    app["bot"] = bot
    app["dp"] = dp
    app["scheduler"] = scheduler
    app.on_startup.append(aiohttp_on_startup)
    app.on_shutdown.append(aiohttp_on_shutdown)
    return app


def main() -> None:
    aiogram_session_logger = utils.logging.setup_logger().bind(type="aiogram_session")

    session = utils.smart_session.SmartAiogramAiohttpSession(
        json_loads=orjson.loads,
        logger=aiogram_session_logger,
    )
    bot = Bot(config.BOT_TOKEN, parse_mode="HTML", session=session)

    dp = Dispatcher()
    dp["aiogram_session_logger"] = aiogram_session_logger

    dp.startup.register(aiogram_on_startup_polling)
    dp.shutdown.register(aiogram_on_shutdown_polling)
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()
