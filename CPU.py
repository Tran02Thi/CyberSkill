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
     format="%(asctime)s - %(levelname)s - %(message)s"
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


# Analyze access logs
# def analyze_access_logs():
#     try:
#         if not os.path.exists(ACCESS_LOG_FILE):
#             logging.warning("Access log file not found.")
#             return

#         with open(ACCESS_LOG_FILE, "r") as f:
#             logs = f.readlines()

#         ip_counter = Counter()
#         endpoint_counter = Counter()
#         total_requests = 0
#         error_count = 0

#         for log in logs:
#             total_requests += 1
#             parts = log.split()
#             if len(parts) < 9:
#                 continue

#             ip = parts[0]
#             endpoint = parts[6]
#             status_code = parts[8]

#             ip_counter[ip] += 1
#             endpoint_counter[endpoint] += 1

#             if status_code.startswith("4") or status_code.startswith("5"):
#                 error_count += 1

#         error_rate = error_count / total_requests if total_requests > 0 else 0

#         # Create analysis report
#         insights = {
#             "top_ips": ip_counter.most_common(5),
#             "top_endpoints": endpoint_counter.most_common(5),
#             "error_rate": error_rate,
#         }

#         with open(ANALYZED_LOG_FILE, "w") as f:
#             f.write(f"Top IPs: {insights['top_ips']}\n")
#             f.write(f"Top Endpoints: {insights['top_endpoints']}\n")
#             f.write(f"Error Rate: {insights['error_rate'] * 100:.2f}%\n")

#         logging.info(f"Log analysis completed. Results: {insights}")

#         # Send email if error rate exceeds threshold
#         if error_rate > ERROR_RATE_THRESHOLD:
#             subject = "Warning: High Error Rate"
#             body = (
#                 f"The error rate in access logs has exceeded the threshold of {ERROR_RATE_THRESHOLD * 100:.2f}%\n"
#                 f"Current error rate: {error_rate * 100:.2f}%\n"
#                 f"Check the analysis log for details: {ANALYZED_LOG_FILE}"
#             )
#             send_email_notification(subject, body)
#     except Exception as e:
#         logging.error(f"Error analyzing access logs: {e}")


def monitor_worker():
    print("Script is running ...")
    while True:
        monitor_cpu_memory()
        time.sleep(60)


if __name__ == "__main__":
    # try:
    #     from multiprocessing import Process

    #     monitor_process = Process(target=monitor_worker)
    #     monitor_process.start()

    #     # Perform log compression and analysis every 24 hours
    #     while True:
    #         time.sleep(86400)  # Wait 24 hours
    #         compress_logs()
    #         analyze_access_logs()

    # except KeyboardInterrupt:
    #     if monitor_process:
    #         monitor_process.terminate()
    #     logging.info("Script stopped by user.")
    # except Exception as e:
    #     logging.error(f"Unexpected error: {e}")
    send_email_notification("test", "Hello World")
    
