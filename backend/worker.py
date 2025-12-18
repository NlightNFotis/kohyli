#!/usr/bin/env python3
"""
Worker script to run the arq background task processor.

Usage:
    python worker.py

This will start the arq worker that processes background tasks like sending
order confirmation emails.
"""

from arq import run_worker

from app.services.tasks import WorkerSettings


if __name__ == "__main__":
    run_worker(WorkerSettings)
