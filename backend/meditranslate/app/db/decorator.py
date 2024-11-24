# decorator.py

from uuid import uuid4
from .session import reset_session_context, AsyncScopedSession, set_session_context

def standalone_session(func):
    """
    Decorator to provide a unique, standalone session for the decorated function.

    Args:
        func: The function to wrap with a standalone session.

    Returns:
        Callable: The wrapped function.
    """
    async def wrapper(*args, **kwargs):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)  # Set new session context

        try:
            await func(*args, **kwargs)
        except Exception as e:
            await AsyncScopedSession.rollback()  # Rollback on error
            raise e
        finally:
            await AsyncScopedSession.remove()  # Cleanup session
            reset_session_context(context=context)  # Reset context

    return wrapper
