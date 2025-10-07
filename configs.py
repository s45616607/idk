from os import getenv

class Config:
    def __init__(self):
        self.API_ID = int(getenv("API_ID", "24140079"))
        self.API_HASH = str(getenv("API_HASH", "d4ba07c6bbfd05e8b52dd77880ff254b"))
        self.BOT_TOKEN = str(getenv("BOT_TOKEN", "7134707061:"))
        self.CHANNEL_ID = int(getenv("CHANNEL_ID", "-100"))
        self.USER_BOT = getenv("USER_BOT", "@H34oBot")
        self.MONGO_URI = getenv("MONGO_URI", "")
        self.session = getenv("session", "")
        self.admin_id = int(getenv("admin_id", "926877758"))


cfg = Config()
