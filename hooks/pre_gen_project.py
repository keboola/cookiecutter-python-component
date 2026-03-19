import logging
import subprocess

repo_url = "{{ cookiecutter.repository_url }}"
if repo_url:
    try:
        result = subprocess.run(["git", "version"], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.strip()
            version = version_line.split()[-1]
            logging.info(f"Git version: {version}")

            req_version = (2, 28, 0)
            cur_version = tuple(map(int, version.split(".")))
            if cur_version < req_version:
                req_version_str = ".".join(map(str, req_version))
                logging.error(f"Git version {req_version_str} or higher is required.")
        else:
            logging.error("Failed to get git version")
    except FileNotFoundError:
        logging.error(
            "Git is not installed! Either install it or leave the repository_url empty"
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e!r}")
