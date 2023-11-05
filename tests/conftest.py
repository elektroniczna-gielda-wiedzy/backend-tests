import pytest
from tests.service.entries_service import EntriesService
from tests.service.answer_service import AnswerService
from tests.service.comment_service import CommentService
from tests.service.auth_service import AuthService


def pytest_addoption(parser):
    parser.addoption(
        "--url", action="store", default="http://localhost:8080"
    )


@pytest.fixture(scope="session")
def app_url(request):
    return request.config.getoption('--url')


@pytest.fixture(scope="session")
def get_auth_token(app_url):
    def token(
            email: str,
            password: str,
            remember_me: bool
    ):
        auth_service = AuthService(app_url)
        response = auth_service.login(email, password, remember_me)
        return response.json()['result'][0]['session_token']
    return token


@pytest.fixture(scope="session")
def auth_token_user1(get_auth_token):
    return get_auth_token(
        email="adamkowalski@student.agh.edu.pl",
        password="L0V3Agh2",
        remember_me=True
    )


@pytest.fixture(scope="session")
def auth_token_user2(get_auth_token):
    return get_auth_token(
        email="mariakowalska@student.agh.edu.pl",
        password="L0V3Agh2",
        remember_me=True
    )


@pytest.fixture(scope="session")
def auth_token_user3(get_auth_token):
    return get_auth_token(
        email="marekkrol@student.agh.edu.pl",
        password="L0V3Agh2",
        remember_me=True
    )


@pytest.fixture(scope="session")
def admin_auth_token(get_auth_token):
    return get_auth_token(
        email="admin@student.agh.edu.pl",
        password="3ngin33rZ125",
        remember_me=True
    )


@pytest.fixture(scope="function")
def create_temporary_entry(app_url):
    def entry_cleanup(
            auth_token: str,
            entry_type: int = 2,
            title: str = "Example Title",
            content: str = "Example Content",
            categories: list = None,
            image: str = None
    ):
        if categories is None:
            categories = [1, 16]
        service = EntriesService(auth_token, app_url)
        response = service.add(entry_type, title, content, categories, image)
        assert response.ok
        entry_id = response.json()['result'][0]['entry_id']

        def cleanup():
            cleanup_response = service.delete(entry_id)
            assert cleanup_response.ok

        return entry_id, cleanup

    return entry_cleanup


@pytest.fixture(scope="function")
def create_temporary_answer(app_url):
    def answer_cleanup(
            auth_token: str,
            entry_id: int = 10,
            answer_content: str = "Answer to post",
            image: str = None
    ):
        service = AnswerService(auth_token, app_url)
        response = service.add(entry_id, answer_content, image)
        assert response.ok
        answer_id = response.json()['result'][0]['answer_id']

        def cleanup():
            cleanup_response = service.delete(entry_id, answer_id)
            assert cleanup_response.ok

        return entry_id, answer_id, cleanup

    return answer_cleanup


@pytest.fixture(scope="function")
def create_temporary_comment(app_url):
    def comment_cleanup(
            auth_token: str,
            entry_id: int = 13,
            answer_id: int = 49,
            comment_content: str = "Hejka, dzięki, poczytam o nim"

    ):
        service = CommentService(auth_token, app_url)
        response = service.add(entry_id, answer_id, comment_content)
        assert response.ok
        comment_id = response.json()['result'][0]['comment_id']

        def cleanup():
            cleanup_response = service.delete(entry_id, answer_id, comment_id)
            assert cleanup_response.ok

        return entry_id, answer_id, comment_id, cleanup

    return comment_cleanup
