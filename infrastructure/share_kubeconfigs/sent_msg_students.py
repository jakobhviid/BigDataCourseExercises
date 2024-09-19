import os
import time
from pathlib import Path

from dotenv import load_dotenv
from src.msg import N_EMAILS, SLEEP_TIME, EmailClient
from src.students import KUBECONFIG_PATTERN, STUDENT_MAIL_PATTERN

if __name__ == "__main__":

    load_dotenv(Path(__file__).resolve().parent / ".env")

    data_path: Path = Path(os.getenv("DATA_DIR", "..."))
    assert data_path != "...", "Please cd into directory of this file."

    # Path to folder with kubeconfig files
    data_path_kubeconfig: Path = data_path / os.getenv("KUBECONFIGS_DIR", "...")
    k8sconfigs = list(data_path_kubeconfig.rglob(f"*{KUBECONFIG_PATTERN}"))

    k8sconfigs_batches = [
        k8sconfigs[i * N_EMAILS : (i + 1) * N_EMAILS]
        for i in range((len(k8sconfigs) + N_EMAILS - 1) // N_EMAILS)
    ]

    for k8sconfigs in k8sconfigs_batches:
        ec = EmailClient(
            email=os.getenv("EMAIL", "<client_email>"),
            password=os.getenv("PASSWORD", "<client_password>"),
        )
        for k8sconfig in k8sconfigs:

            receiver_email = k8sconfig.name.replace(
                KUBECONFIG_PATTERN, STUDENT_MAIL_PATTERN
            )

            msg = ec.create_msg(
                receiver_email=receiver_email,
                subject="Kubeconfig for Kubernetes in Big Data and Data Science Technology, E24",
                body="Dear student,\n\nHere is the kubeconfig file for the Kubernetes cluster you need for exercises in the course Big Data and Data Science Technology, E24.\n\nBest regards,\nAnders Launer Bæk-Petersen\n\n",
                attachment=k8sconfig,
            )
            ec.send_msg(receiver_email, msg)

        time.sleep(SLEEP_TIME)
