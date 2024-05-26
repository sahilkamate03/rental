from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user
from sqlalchemy import inspect

from core.models import Properties

profile = Blueprint("profile", __name__)


@profile.route("/account")
def account():
    user_data = current_user
    user_dict = {
        c.key: getattr(user_data, c.key) for c in inspect(user_data).mapper.column_attrs
    }
    print(user_dict)
    page = request.args.get("page", 1, type=int)
    properties_data = Properties.query.filter_by(seller_id=current_user.id).paginate(
        page=page, per_page=9
    )

    return render_template(
        "seller_list.html", user_data=user_dict, properties_data=properties_data
    )
