import os
from huggingface_hub import HfApi


def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN env is required")
    api = HfApi(token=token)
    space_id = "Thrgbbnh/CU_CPO"
    readme = (
        "---\n"
        "title: CUCPO Chat (Streamlit)\n"
        "emoji: \"🗣️\"\n"
        "colorFrom: indigo\n"
        "colorTo: blue\n"
        "sdk: streamlit\n"
        "app_file: app_streamlit.py\n"
        "python_version: \"3.10\"\n"
        "pinned: false\n"
        "---\n\n"
        "Лёгкий профиль Space без аудио-зависимостей. Интерфейс Streamlit.\n"
    )
    api.upload_file(
        path_or_fileobj=readme.encode("utf-8"),
        path_in_repo="README.md",
        repo_id=space_id,
        repo_type="space",
        commit_message="Switch to Streamlit profile",
    )
    print("Updated README.md to use Streamlit profile")


if __name__ == "__main__":
    main()
