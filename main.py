import signal
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# define signal handler function
def handle_sigterm(*args):
    uvicorn.Server.shutdown()
    raise SystemExit(0)

# register signal handler function for SIGTERM
signal.signal(signal.SIGTERM, handle_sigterm)


if __name__ == "__main__":
    uvicorn.run("app.main:app" ,host='0.0.0.0', port=8081, reload=True, workers=2)