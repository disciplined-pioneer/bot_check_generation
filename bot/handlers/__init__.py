from bot.handlers.start import router as start
from bot.handlers.price import router as price
from bot.handlers.topic import router as topic
from bot.handlers.info_about import router as info_about
from bot.handlers.submit_request import router as submit_request


routers = [
    start,
    price,
    topic,
    info_about,
    submit_request
]
