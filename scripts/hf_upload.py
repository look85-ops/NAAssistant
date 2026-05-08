import argparse
import os
import sys
from pathlib import Path

from huggingface_hub import HfApi, create_repo, upload_file, upload_folder


def ensure_space(api: HfApi, space_id: str):
    # Try create as Gradio space; if exists, ignore
    try:
        create_repo(repo_id=space_id, repo_type="space", space_sdk="gradio", exist_ok=True)
    except Exception:
        pass


def ensure_model_repo(api: HfApi, model_id: str):
    create_repo(repo_id=model_id, repo_type="model", exist_ok=True)


def upload_lora(api: HfApi, model_id: str, lora_dir: Path):
    if not lora_dir.is_dir():
        raise FileNotFoundError(f"LoRA directory not found: {lora_dir}")
    upload_folder(
        folder_path=str(lora_dir),
        repo_id=model_id,
        repo_type="model",
        path_in_repo="",
        commit_message="Upload LoRA adapter",
        allow_patterns=[
            "adapter_model.safetensors",
            "adapter_config.json",
            "chat_template.jinja",
            "tokenizer.json",
            "tokenizer_config.json",
            "README.md",
        ],
    )


def upload_space_files(api: HfApi, space_id: str, space_src: Path):
    # Ensure required files exist
    app_path = space_src / "app.py"
    req_path = space_src / "requirements.txt"
    app_streamlit_path = space_src / "app_streamlit.py"
    if not app_path.is_file() or not req_path.is_file():
        raise FileNotFoundError("Space sources missing app.py or requirements.txt")

    # Upload app and requirements
    upload_file(
        path_or_fileobj=str(app_path),
        path_in_repo="app.py",
        repo_id=space_id,
        repo_type="space",
        commit_message="Add app.py",
    )
    upload_file(
        path_or_fileobj=str(req_path),
        path_in_repo="requirements.txt",
        repo_id=space_id,
        repo_type="space",
        commit_message="Add requirements.txt",
    )

    # Optionally upload streamlit app if present
    if app_streamlit_path.is_file():
        upload_file(
            path_or_fileobj=str(app_streamlit_path),
            path_in_repo="app_streamlit.py",
            repo_id=space_id,
            repo_type="space",
            commit_message="Add Streamlit app",
        )

    # Minimal README to set Gradio runtime
    readme = """---
title: CUCPO Chat
emoji: 🗣️
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 4.31.0
app_file: app.py
pinned: false
---

CUCPO LoRA chat Space. Uses `unsloth/DeepSeek-R1-Distill-Qwen-7B-bnb-4bit` with LoRA.
"""
    upload_file(
        path_or_fileobj=readme.encode("utf-8"),
        path_in_repo="README.md",
        repo_id=space_id,
        repo_type="space",
        commit_message="Configure Gradio runtime via README",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token-file", required=False)
    parser.add_argument("--model-dir", required=True, help="Local path to LoRA directory")
    parser.add_argument("--model-repo", required=True, help="Model repo id for LoRA (e.g., Thrgbbnh/cucpo_lora)")
    parser.add_argument("--space-id", required=True, help="Space id (e.g., Thrgbbnh/CU_CPO)")
    parser.add_argument("--space-src", required=True, help="Local path to Space source folder")
    args = parser.parse_args()

    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")
    if not token and args.token_file:
        token = Path(args.token_file).read_text(encoding="utf-8").strip()
    if not token:
        print("HF token not provided. Set HF_TOKEN env or use --token-file.", file=sys.stderr)
        sys.exit(1)

    api = HfApi(token=token)

    # Ensure repos
    ensure_model_repo(api, args.model_repo)
    ensure_space(api, args.space_id)

    # Upload LoRA
    upload_lora(api, args.model_repo, Path(args.model_dir))

    # Upload Space app
    upload_space_files(api, args.space_id, Path(args.space_src))

    print("Done. Space build will start shortly.")


if __name__ == "__main__":
    main()
