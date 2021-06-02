# -*- coding: utf-8 -*-
# Copyright (c) 2021, datafeatures@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.exceptions import DoesNotExistError
import requests
import xmltodict
import json


@frappe.whitelist(methods=["GET"], allow_guest=True)
def policy_template(template_id=None):
    if not template_id:
        doc = frappe.new_doc("Insurance Policy Template")
        doc.data = json.dumps(get_template())
        doc.save(ignore_permissions=True)
        frappe.db.commit()
    else:
        try:
            doc = frappe.get_doc("Insurance Policy Template", template_id)
        except frappe.DoesNotExistError:
            frappe.throw(
                _("Insurance Policy Template <b>{}</b> does not exist.").format(
                    template_id
                )
            )

    return json.loads(doc.data)


def get_template():
    rating_api_url = frappe.db.get_single_value("Insurance Settings", "ratings_api_url")
    api_response = requests.get(rating_api_url)
    dict_data = xmltodict.parse(api_response.content)
    pod = dict_data.get("ITCRateEngineRequest", {}).get("PolicyData", {})
    dict_data["ITCRateEngineRequest"]["PolicyData"] = xmltodict.parse(pod)
    return dict_data
