from httpx import AsyncClient

from tests.factory.users import create_fake_user

async def _create_user_and_login(
    client: AsyncClient, fake_user=create_fake_user()
) -> None:
    await client.post("/auth/users", json=fake_user)

    response = await client.post("/users/login", json=fake_user)
    access_token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return None
