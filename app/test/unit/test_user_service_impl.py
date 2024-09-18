from loguru import logger

from app.api.service.impl.user_service_impl import UserServiceImpl


def test_format_user_name(async_client):
    """
    Test the 'format_user_name' method of UserServiceImpl, ensures it correctly formats first and last names.
    """
    logger.info("Starting test: test_format_user_name.")
    logger.debug("Attempting to format user name with first name 'john' and last name 'doe'.")

    user_service = UserServiceImpl()

    full_name = user_service.format_user_name("john", "doe")

    logger.debug(f"Formatted name received: {full_name}")

    assert full_name == "John Doe", "The formatted name should be 'John Doe'"

    logger.info("Finalizing test: test_format_user_name.")
