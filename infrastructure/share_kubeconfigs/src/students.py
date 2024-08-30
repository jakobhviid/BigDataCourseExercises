from pathlib import Path

KUBECONFIG_PATTERN: str = "-kubeconfig.yaml"
KUBECONFIG_PATH = Path("k8sconfigs")
STUDENT_MAIL_PATTERN: str = "@student.sdu.dk"


def get_created_students(
    config_path: Path, pattern: str = KUBECONFIG_PATTERN
) -> set[str]:

    return set([s.name.replace(pattern, "") for s in config_path.rglob(f"*{pattern}")])


def parse_student_file(filename: str) -> set[str]:
    with open(file=filename, mode="r") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if "@" in line]
    lines = [line.replace("\tStudent", "") for line in lines]
    lines = [line.replace("@student.sdu.dk", "") for line in lines]
    lines = [line.split("\t")[-1] for line in lines]
    lines.sort()

    return set(lines)


def get_missing_students(
    enrolled_students: list[str], created_students: list[str]
) -> None:
    difference = set(enrolled_students) - set(created_students)
    difference = list(difference)
    difference.sort()
    print("\n".join(difference))
