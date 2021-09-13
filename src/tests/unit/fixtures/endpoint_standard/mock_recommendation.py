"""Mock responses for recommendations."""

SEARCH_REQ = {
    "criteria": {
        "policy_type": ['reputation_override'],
        "status": ['NEW', 'REJECTED', 'ACCEPTED'],
        "hashes": ['111', '222']
    },
    "rows": 50,
    "sort": [
        {
            "field": "impact_score",
            "order": "DESC"
        }
    ]
}

SEARCH_RESP = {
    "results": [
        {
            "recommendation_id": "91e9158f-23cc-47fd-af7f-8f56e2206523",
            "rule_type": "reputation_override",
            "policy_id": 0,
            "new_rule": {
                "override_type": "SHA256",
                "override_list": "WHITE_LIST",
                "sha256_hash": "32d2be78c00056b577295aa0943d97a5c5a0be357183fcd714c7f5036e4bdede",
                "filename": "XprotectService",
                "application": {
                    "type": "EXE",
                    "value": "FOO"
                }
            },
            "workflow": {
                "status": "NEW",
                "changed_by": "rbaratheon@example.com",
                "create_time": "2021-05-18T16:37:07.000Z",
                "update_time": "2021-08-31T20:53:39.000Z",
                "comment": "Ours is the fury"
            },
            "impact": {
                "org_adoption": "LOW",
                "impacted_devices": 45,
                "event_count": 76,
                "impact_score": 0,
                "update_time": "2021-05-18T16:37:07.000Z"
            }
        },
        {
            "recommendation_id": "bd50c2b2-5403-4e9e-8863-9991f70df026",
            "rule_type": "reputation_override",
            "policy_id": 0,
            "new_rule": {
                "override_type": "SHA256",
                "override_list": "WHITE_LIST",
                "sha256_hash": "0bbc082cd8b3ff62898ad80a57cb5e1f379e3fcfa48fa2f9858901eb0c220dc0",
                "filename": "sophos ui.msi"
            },
            "workflow": {
                "status": "NEW",
                "changed_by": "tlannister@example.com",
                "create_time": "2021-05-18T16:37:07.000Z",
                "update_time": "2021-08-31T20:53:09.000Z",
                "comment": "Always pay your debts"
            },
            "impact": {
                "org_adoption": "HIGH",
                "impacted_devices": 8,
                "event_count": 25,
                "impact_score": 0,
                "update_time": "2021-05-18T16:37:07.000Z"
            }
        },
        {
            "recommendation_id": "0d9da444-cfa7-4488-9fad-e2abab099b68",
            "rule_type": "reputation_override",
            "policy_id": 0,
            "new_rule": {
                "override_type": "SHA256",
                "override_list": "WHITE_LIST",
                "sha256_hash": "2272c5221e90f9762dfa38786da01b36a28a7da5556b07dec3523d1abc292124",
                "filename": "mimecast for outlook 7.8.0.125 (x86).msi"
            },
            "workflow": {
                "status": "NEW",
                "changed_by": "estark@example.com",
                "create_time": "2021-05-18T16:37:07.000Z",
                "update_time": "2021-08-31T15:13:40.000Z",
                "comment": "Winter is coming"
            },
            "impact": {
                "org_adoption": "MEDIUM",
                "impacted_devices": 45,
                "event_count": 79,
                "impact_score": 0,
                "update_time": "2021-05-18T16:37:07.000Z"
            }
        }
    ],
    "num_found": 3
}

ACTION_INIT = {
    "recommendation_id": "0d9da444-cfa7-4488-9fad-e2abab099b68",
    "rule_type": "reputation_override",
    "policy_id": 0,
    "new_rule": {
        "override_type": "SHA256",
        "override_list": "WHITE_LIST",
        "sha256_hash": "2272c5221e90f9762dfa38786da01b36a28a7da5556b07dec3523d1abc292124",
        "filename": "mimecast for outlook 7.8.0.125 (x86).msi"
    },
    "workflow": {
        "status": "NEW",
        "changed_by": "estark@example.com",
        "create_time": "2021-05-18T16:37:07.000Z",
        "update_time": "2021-08-31T15:13:40.000Z",
        "comment": "Winter is coming"
    },
    "impact": {
        "org_adoption": "MEDIUM",
        "impacted_devices": 45,
        "event_count": 79,
        "impact_score": 0,
        "update_time": "2021-05-18T16:37:07.000Z"
    }
}

ACTION_REQS = [
    {
        "action": "ACCEPT",
        "comment": "Alpha"
    },
    {
        "action": "RESET"
    },
    {
        "action": "REJECT",
        "comment": "Charlie"
    },
]

ACTION_REFRESH_SEARCH = {
    "criteria": {
        "policy_type": ['reputation_override'],
        "hashes": ['2272c5221e90f9762dfa38786da01b36a28a7da5556b07dec3523d1abc292124']
    },
    "rows": 50
}

ACTION_SEARCH_RESP = {
    "results": [ACTION_INIT],
    "num_found": 1
}

ACTION_REFRESH_STATUS = ['ACCEPTED', 'NEW', 'REJECTED']

ACTION_INIT_ACCEPTED = {
    "recommendation_id": "0d9da444-cfa7-4488-9fad-e2abab099b68",
    "rule_type": "reputation_override",
    "policy_id": 0,
    "new_rule": {
        "override_type": "SHA256",
        "override_list": "WHITE_LIST",
        "sha256_hash": "2272c5221e90f9762dfa38786da01b36a28a7da5556b07dec3523d1abc292124",
        "filename": "mimecast for outlook 7.8.0.125 (x86).msi"
    },
    "workflow": {
        "status": "ACCEPTED",
        "ref_id": "e9410b754ea011ebbfd0db2585a41b07",
        "changed_by": "estark@example.com",
        "create_time": "2021-05-18T16:37:07.000Z",
        "update_time": "2021-08-31T15:13:40.000Z",
        "comment": "Winter is coming"
    },
    "impact": {
        "org_adoption": "MEDIUM",
        "impacted_devices": 45,
        "event_count": 79,
        "impact_score": 0,
        "update_time": "2021-05-18T16:37:07.000Z"
    }
}
