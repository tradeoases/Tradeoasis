from celery.decorators import task
from celery.utils.log import get_task_logger
from auth_app.email import send_account_activation_email

# this output messages to the celery log
logger = get_task_logger(__name__)


@task(name="send_account_activation_email_task")
def send_account_activation_email_task(name, email, subject):
    logger.info("Sent Activation email")
    return send_account_activation_email(name, email, subject)
