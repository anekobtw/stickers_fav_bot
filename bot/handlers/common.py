"""
Handling uptime, queries, stickers and simple messages
"""

import os

from aiogram import Bot, F, Router, exceptions, types
from aiogram.filters import Command
from dotenv import load_dotenv
from yandexfreetranslate import YandexFreeTranslate


# Load environment variables and initialize bot and router
load_dotenv()
BOT_USERNAME = os.getenv("BOT_USERNAME")
bot = Bot(token=os.getenv("TOKEN"))
router = Router()
yt = YandexFreeTranslate()
yt = YandexFreeTranslate(api = "ios")


@router.message(F.text, Command("start"))
async def start_command_handler(message: types.Message) -> None:
    """Sends welcome text"""
    print(message.from_user.language_code)
    if message.from_user.language_code == "en":
        msg = "Send me a sticker to add to the sticker set. Send me that sticker <b>from the pack created by the bot</b> to remove it."
    elif message.from_user.language_code == "ru":
        msg = "Отправь мне стикер, чтобы добавить его в стикер пак. Отправь мне этот же стикер <b>с пака созданного ботом</b>, чтобы удалить его."
    else:
        msg = yt.translate("en", message.from_user.language_code, "Send me a sticker to add to the sticker set. Send me that sticker <b>from the pack created by the bot</b> to remove it.")
    await message.answer(text=msg)


@router.message(F.sticker)
async def handle_sticker_message(message: types.Message) -> None:
    """Adding an emoji to the user's sticker set. If there is no sticker set, create one"""
    name = f"set{message.from_user.id}_by_{BOT_USERNAME}"
    sticker = message.sticker
    input_sticker = types.InputSticker(
        sticker=sticker.file_id,
        format="static",
        emoji_list=[sticker.emoji] if sticker.emoji else [],
        mask_position=sticker.mask_position,
        keywords=None,
    )

    try:
        sticker_set = await bot.get_sticker_set(name=name)

        if sticker in sticker_set.stickers:
            await bot.delete_sticker_from_set(sticker=sticker.file_id)
            await message.answer("Sticker Deleted!")
            return
        else:
            await bot.add_sticker_to_set(
                user_id=message.from_user.id, name=name, sticker=input_sticker
            )

    except exceptions.TelegramBadRequest:
        await bot.create_new_sticker_set(
            user_id=message.from_user.id,
            name=name,
            title=f"@{BOT_USERNAME} ❤️",
            stickers=[input_sticker],
        )

    sticker_set = await bot.get_sticker_set(name=name)
    await message.answer_sticker(
        sticker=sticker_set.stickers[-1].file_id, reply_to_message_id=message.message_id
    )
