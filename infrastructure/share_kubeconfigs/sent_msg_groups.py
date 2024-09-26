import os
import time
from pathlib import Path

from dotenv import load_dotenv
from src.groups import parse_groups_from_form
from src.msg import SLEEP_TIME, EmailClient
from src.students import KUBECONFIG_PATTERN, STUDENT_MAIL_PATTERN

if __name__ == "__main__":

    load_dotenv(Path(__file__).resolve().parent / ".env")

    data_path: Path = Path(os.getenv("DATA_DIR", "..."))
    assert data_path != "...", "Please cd into directory of this file."

    filename: Path = data_path / os.getenv("FORM_FILENAME_GROUPS")
    df = parse_groups_from_form(filename)

    # Path to folder with kubeconfig files
    data_path_kubeconfig: Path = data_path / os.getenv("KUBECONFIGS_DIR_GROUPS")
    k8sconfigs = list(data_path_kubeconfig.rglob(f"*{KUBECONFIG_PATTERN}"))

    for k8sconfig in k8sconfigs:
        ec = EmailClient(
            email=os.getenv("EMAIL", "<client_email>"),
            password=os.getenv("PASSWORD", "<client_password>"),
        )

        group_id = k8sconfig.name.replace(KUBECONFIG_PATTERN, "")
        for receiver_email in df.loc[df["ID"] == group_id, "value"]:
            receiver_email += STUDENT_MAIL_PATTERN

            msg = ec.create_msg(
                receiver_email=receiver_email,
                subject=f"[{group_id}] - Kubeconfig for the project in Big Data and Data Science Technology, E24",
                body="Dear student,\n\nHere is the kubeconfig file for the Kubernetes cluster you need for your project in the course Big Data and Data Science Technology, E24.\n\nBest regards,\nAnders Launer Bæk-Petersen\n\n",
                attachment=k8sconfig,
            )
            ec.send_msg(receiver_email, msg)

        time.sleep(SLEEP_TIME)
