import os
from pathlib import Path
from huggingface_hub import HfApi, CommitOperationAdd, CommitOperationDelete, create_commit


def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN env is required")
    api = HfApi(token=token)
    space_id = os.environ.get("SPACE_ID", "Thrgbbnh/CU_CPO")
    base_dir = Path(os.environ.get("SPACE_SRC", "spaces/cucpo-chat")).resolve()

    files_to_push = [
        (base_dir / "app_streamlit.py", "app_streamlit.py"),
        (base_dir / "requirements.txt", "requirements.txt"),
    ]

    ops = []
    for local, remote in files_to_push:
        if not local.is_file():
            print(f"Skip missing {local}")
            continue
        content = local.read_bytes()
        ops.append(CommitOperationAdd(path_in_repo=remote, path_or_fileobj=content))

    # Force README to streamlit profile
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
    ).encode("utf-8")
    ops.append(CommitOperationAdd(path_in_repo="README.md", path_or_fileobj=readme))

    # Remove legacy gradio app to avoid accidental pickup
    ops.append(CommitOperationDelete(path_in_repo="app.py"))

    create_commit(
        repo_id=space_id,
        repo_type="space",
        operations=ops,
        commit_message="Force add/replace app_streamlit.py and requirements.txt",
        token=token,
    )
    print("Pushed files via create_commit")


if __name__ == "__main__":
    main()
