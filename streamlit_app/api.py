import requests

BASE_URL = "http://127.0.0.1:8000"


def register(name, email, password):
    return requests.post(
        f"{BASE_URL}/Register",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
    )


def login(email, password):
    return requests.post(
        f"{BASE_URL}/login",
        data={
            "username": email,
            "password": password,
        },
    )


def get_tasks():
    return requests.get(f"{BASE_URL}/readall")


def get_task(task_id):
    return requests.get(f"{BASE_URL}/readone/{task_id}")


def create_task(title, description, completed, token):
    return requests.post(
        f"{BASE_URL}/tasks",
        json={
            "title": title,
            "description": description,
            "completed": completed,
        },
        headers={"Authorization": f"Bearer {token}"},
    )


def update_task(task_id, title, description, completed):
    return requests.put(
        f"{BASE_URL}/update/{task_id}",
        json={
            "title": title,
            "description": description,
            "completed": completed,
        },
    )


def delete_task(task_id):
    return requests.delete(f"{BASE_URL}/delone/{task_id}")


def delete_all_tasks():
    return requests.delete(f"{BASE_URL}/delall")
