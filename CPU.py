import os
import psutil
import time
import gzip
import shutil
import logging
from collections import Counter
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime
import smtplib

load_dotenv()

# Logging configuration
LOG_DIR = "Logs"


# Defind location logs
ACCESS_LOG_FILE = os.path.join(LOG_DIR, "access.log")
CPU_MEM_LOG_FILE = os.path.join(LOG_DIR, "cpu_mem_usage.log")
ANALYZED_LOG_FILE = os.path.join(LOG_DIR, "analyzed_parse.log")
DAILY_LOG = os.path.join(LOG_DIR, "daily.log")
EMAIL_LOG_FILE = os.path.join(LOG_DIR, "email_notifications.log")
COMPRESSED_LOG_DIR = os.path.join(LOG_DIR, "compressed_logs")

ERROR_RATE_THRESHOLD = float(os.getenv("ERROR_RATE_THRESHOLD", 0.6))
DATE_NOW_STR = datetime.now().strftime("%Y-%m-%d")

COMPRESSED_LOG_FILE = os.path.join(COMPRESSED_LOG_DIR, f"daily-{DATE_NOW_STR}.log.gz")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(COMPRESSED_LOG_FILE, exist_ok=True)

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

logging.basicConfig(
    filename=DAILY_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def send_email_notification(subject, body):
    try:
        if not all(
            [
                SMTP_SERVER,
                SMTP_PORT,
                SMTP_USER,
                SMTP_PASSWORD,
                SENDER_EMAIL,
                RECEIVER_EMAIL,
            ]
        ):
            logging.error("SMTP configuration is incomplete !")
            return

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg.set_content(body)

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()

        logging.info(f"Email sent: {subject}")
        print("Email sent successfully.")

    except Exception as e:
        logging.error(f"Unable to send email: {e}")
        print(f"Unable to send email: {e}")
        raise


def monitor_cpu_memory():
    try:
        with open(CPU_MEM_LOG_FILE, "a") as f:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            log_entry = f"CPU: {cpu_usage}% | Memory: {memory_usage}%\n"
            logging.info(f"Logged CPU and RAM usage: {log_entry.strip()}")
            f.write(log_entry)
    except Exception as e:
        logging.error(f"Error monitoring CPU and RAM: {e}")


def compress_logs():
    try:
        with open(CPU_MEM_LOG_FILE, "rb") as f_in:
            with gzip.open(COMPRESSED_LOG_FILE, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        open(CPU_MEM_LOG_FILE, "w").close()  # Clear the original log file content
        logging.info(f"Log for {DATE_NOW_STR} compressed successfully.")

    except Exception as e:
        logging.error(f"Error compressing daily log: {e}")


def monitor_worker():
    print("Script is running ...")
    while True:
        monitor_cpu_memory()
        time.sleep(60)


if __name__ == "__main__":
    try:
        from multiprocessing import Process

        monitor_process = Process(target=monitor_worker)
        monitor_process.start()

        # Perform log compression and analysis every 24 hours
        while True:
            time.sleep(86400)  # Wait 24 hours
            compress_logs()

    except KeyboardInterrupt:
        if monitor_process:
            monitor_process.terminate()
        logging.info("Script stopped by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
