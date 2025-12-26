LOG_BUFFER = []
class Logger:
    def log(msg:str):
        LOG_BUFFER.append(msg)
        if len(LOG_BUFFER) > 500:
            LOG_BUFFER.pop(0)