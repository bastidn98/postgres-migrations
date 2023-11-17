from flask import jsonify, request, Blueprint, flash, Response
from http import HTTPStatus
from dotenv import load_dotenv
from .clients import client_code_domain_dict
from .models import ClientFamily
from .logger import logging

load_dotenv()
logger = logging.getLogger(__package__)
ajax_api = Blueprint('internal', __name__, url_prefix='/internal') 
api = Blueprint('api', __name__, url_prefix='/api')

@ajax_api.route("/validate-domains", methods=['POST'])
def validate_domains():
    domains = client_code_domain_dict()
    client = request.form.get('client').split(':')[0]
    head = request.form.get('family_head').split(':')[0]
    client_domains = domains[client]
    head_domains = domains[head]
    invalid_domains = []
    for domain in client_domains:
        if domain not in head_domains:
            invalid_domains.append(domain)
    is_valid = len(invalid_domains) == 0
    if not client_domains:
        flash(f'Domain check skipped because selected {client} has no domains.', 'error')
    return jsonify({'isValid':is_valid, 'invalidDomains':invalid_domains, 'headDomains':head_domains})

@api.route("/export", methods=['GET'])
def export_data():
    format = request.args.get("format", "json").lower()
    families = [family.toJson() for family in ClientFamily.query.all()]

    if format in ('csv', 'save'):
        output = []
        output.append(', '.join(families[0].keys()))
        for family in families:
            output.append(', '.join([val for val in family.values()]))
        headers = {"Content-Disposition": "attachment; filename=export.csv"} if format == "save" else {}
        return Response("\n".join(output), content_type="text/csv", headers=headers), HTTPStatus.OK
    else:
        return jsonify(families), HTTPStatus.OK
