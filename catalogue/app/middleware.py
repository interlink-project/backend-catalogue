
from typing import Any, Optional, Union

from starlette.requests import HTTPConnection, Request
from starlette_context.plugins import Plugin

from app.general import deps
from app.general.authentication import decode_token
from app.locales import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGE_CODES


class UserPlugin(Plugin):
    # The returned value will be inserted in the context with this key
    key = "user"

    async def process_request(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[Any]:
        token = deps.get_current_token(request=request)
        if token:
            return decode_token(token)
        return None


class LanguagePlugin(Plugin):
    # The returned value will be inserted in the context with this key
    key = "language"

    async def process_request(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[Any]:
        try:
            header_lang = request.headers.get("accept-language")
            used_language = header_lang if header_lang in SUPPORTED_LANGUAGE_CODES else DEFAULT_LANGUAGE
        except:
            used_language = DEFAULT_LANGUAGE
        print("LANGUAGE", used_language)
        return used_language
