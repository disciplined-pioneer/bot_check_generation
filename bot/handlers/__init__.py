from bot.handlers.start import router as start
from bot.handlers.topic import router as topic
from bot.handlers.broadcast import router as broadcast

routers = [
    start,
    broadcast,
    topic
]
