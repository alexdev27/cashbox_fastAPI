import uvicorn
from os import environ as envs

if __name__ == '__main__':
    uvicorn.run(app='app:app',
                host='0.0.0.0',
                port=8044,
                reload=bool(envs.get('RELOAD', False)),
                debug=bool(envs.get('DEBUG', False)),
                loop='asyncio')
