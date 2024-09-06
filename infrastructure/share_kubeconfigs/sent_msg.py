from pathlib import Path

from src.msg import EmailClient
from src.students import KUBECONFIG_PATTERN, STUDENT_MAIL_PATTERN

if __name__ == "__main__":

    ec = EmailClient(email="<client_email>", password="<client_password>")
    # Path to folder with kubeconfig files
    data_path: Path = Path("...")
    for k8sconfig in data_path.rglob(f"*{KUBECONFIG_PATTERN}"):

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
