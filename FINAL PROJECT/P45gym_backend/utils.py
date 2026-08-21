import re
import logging

logger = logging.getLogger("p45gym")

EMAIL_REGEX = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
DATE_REGEX = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def success_response(message, data=None, status=200):
    from flask import jsonify
    payload = {"success": True, "message": message}
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status


def error_response(message, status=400):
    from flask import jsonify
    return jsonify({"success": False, "message": message}), status


def is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False
