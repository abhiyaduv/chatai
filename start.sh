#!/usr/bin/env bash
gunicorn groq_chatbot.wsgi:application