from bot.handlers.start import router as start
from bot.handlers.price import router as price
from bot.handlers.info_about import router as info_about


routers = [
    start,
    price,
    info_about
]
