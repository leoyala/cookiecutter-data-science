import toml


packages = [
    "pip",
    "python-dotenv",

]

basic = [
    "ipython",
    "jupyterlab",
    "matplotlib",
    "notebook",
    "numpy",
    "pandas",
    "scikit-learn",
]

dev = [
    "mypy==1.10.1",
    "bandit==1.7.9",
    "black==24.4.2",
    "flake8==7.1.0",
    "isort[colors]==5.13.2",
    "pytest",
    "pytest-cov",
    "pre-commit",
]

scaffold = [
    "typer",
    "loguru",
    "tqdm",
]


def write_dependencies_to_pyproject(packages, dev):
    with open("pyproject.toml", "r") as f:
        pyproject_data = toml.load(f)
    pyproject_data["project"]["dependencies"].extend(packages)
    pyproject_data["project"]["optional-dependencies"]["dev"].extend(dev)
    with open("pyproject.toml", "w") as f:
        toml.dump(pyproject_data, f)


def write_dependencies(
    dependencies, packages, pip_only_packages, repo_name, module_name, python_version
):
    if dependencies == "requirements.txt":
        with open(dependencies, "w") as f:
            lines = sorted(packages)

            lines += ["" "-e ."]

            f.write("\n".join(lines))
            f.write("\n")

    elif dependencies == "environment.yml":
        with open(dependencies, "w") as f:
            lines = [
                f"name: {repo_name}",
                "channels:",
                "  - conda-forge",
                "dependencies:",
            ]

            lines += [f"  - python={python_version}"]
            lines += [f"  - {p}" for p in packages if p not in pip_only_packages]

            lines += ["  - pip:"]
            lines += [f"    - {p}" for p in packages if p in pip_only_packages]
            lines += ["    - -e ."]

            f.write("\n".join(lines))

    elif dependencies == "Pipfile":
        with open(dependencies, "w") as f:
            lines = ["[packages]"]
            lines += [f'{p} = "*"' for p in sorted(packages)]

            lines += [f'"{module_name}" ={{editable = true, path = "."}}']

            lines += ["", "[requires]", f'python_version = "{python_version}"']

            f.write("\n".join(lines))
