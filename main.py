from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.facebook import FacebookSSO
from starlette.requests import Request

app = FastAPI()

FACEBOOK_CLIENT_ID = ""
FACEBOOK_CLIENT_SECRET = ""

FACEBOOK_REDIRECT_URI = "http://localhost:8000/v1/facebook/callback"

import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


facebook_sso = FacebookSSO(
    FACEBOOK_CLIENT_ID,
    FACEBOOK_CLIENT_SECRET,
    FACEBOOK_REDIRECT_URI,
    allow_insecure_http=True
)


@app.get("/v1/facebook/login", tags=['Facebook SSO'])
async def facebook_login():
    with facebook_sso:
        return await facebook_sso.get_login_redirect()


@app.get("/v1/facebook/callback", tags=['Facebook SSO'])
async def facebook_callback(request: Request):
    try:
        with facebook_sso:
            user = await facebook_sso.verify_and_process(request)

        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        return RedirectResponse(url="/error", status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
