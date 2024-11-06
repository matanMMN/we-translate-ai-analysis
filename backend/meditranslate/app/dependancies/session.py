from typing import Annotated
from meditranslate.app.db.session import AsyncSession,get_session
from fastapi import Depends

SessionDep = Annotated[AsyncSession, Depends(get_session)]
