# transaction.py

from enum import Enum
from functools import wraps
from meditranslate.app.db.session import AsyncScopedSession

# Enum for transaction propagation types
class Propagation(Enum):
    REQUIRED = "required"  # Use an existing transaction if available
    REQUIRED_NEW = "required_new"  # Start a new transaction regardless of existing ones

# Transactional decorator for managing database transactions
class Transactional:
    def __init__(self, propagation: Propagation = Propagation.REQUIRED):
        """
        Initializes the Transactional decorator with the specified propagation type.

        Args:
            propagation (Propagation): The type of transaction propagation.
        """
        self.propagation = propagation

    def __call__(self, function):
        """
        Decorates a function to manage transactions automatically.

        Args:
            function (Callable): The function to wrap with transaction handling.

        Returns:
            Callable: The wrapped function with transaction management.
        """
        @wraps(function)
        async def wrapper(*args, **kwargs):
            try:
                if self.propagation == Propagation.REQUIRED_NEW:
                    result = await self._run_new_transaction(function, *args, **kwargs)
                else:
                    result = await self._run_existing_transaction(function, *args, **kwargs)
            except Exception as e:
                await AsyncScopedSession.rollback()  # Rollback on error
                raise e
            return result

        return wrapper

    async def _run_existing_transaction(self, function, *args, **kwargs):
        """
        Executes a function within an existing transaction.

        Args:
            function: The function to execute.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Any: Result of the function execution.
        """
        result = await function(*args, **kwargs)
        await AsyncScopedSession.commit()  # Commit changes
        return result

    async def _run_new_transaction(self, function, *args, **kwargs):
        """
        Starts a new transaction, executes a function, and commits the transaction.

        Args:
            function: The function to execute.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Any: Result of the function execution.
        """
        AsyncScopedSession.begin()  # Begin a new transaction
        result = await function(*args, **kwargs)
        await AsyncScopedSession.commit()  # Commit changes
        return result
