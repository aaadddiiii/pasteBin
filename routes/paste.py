# routes/paste.py
from flask import Blueprint, request, jsonify
from db.mongo import pastes
from utils.id_gen import gen_id
from datetime import datetime, timedelta
import config, uuid

paste_bp = Blueprint("paste", __name__)

@paste_bp.route("/paste", methods=["POST"])
def create():
    data = request.json["content"]
    if len(data) > config.MAX_PASTE_SIZE:
        return jsonify({"error":"too big"}), 413

    pid = gen_id()
    exp = request.json.get("expiry")  # minutes
    expires = datetime.utcnow() + timedelta(minutes=exp) if exp else None

    key = uuid.uuid4().hex[:12]
    pastes.insert_one({
        "paste_id": pid,
        "content": data,
        "created_at": datetime.utcnow(),
        "expires_at": expires,
        "delete_key": key
    })
    return jsonify({"id":pid, "delete_key":key})


@paste_bp.route("/paste/<pid>", methods=["GET"])
def get(pid):
    p = pastes.find_one({"paste_id":pid})
    if not p:
        return jsonify({"error":"not found"}),404

    if p["expires_at"] and p["expires_at"] < datetime.utcnow():
        pastes.delete_one({"paste_id":pid})
        return jsonify({"error":"expired"}),410

    return jsonify({"content":p["content"]})


@paste_bp.route("/paste/<pid>", methods=["DELETE"])
def delete(pid):
    key = request.json["delete_key"]
    p = pastes.find_one({"paste_id":pid})
    if not p or p["delete_key"] != key:
        return jsonify({"error":"denied"}),403

    pastes.delete_one({"paste_id":pid})
    return jsonify({"status":"deleted"})
