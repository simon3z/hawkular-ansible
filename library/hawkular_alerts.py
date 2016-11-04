import hawkular.alerts

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec={
            'endpoint':         dict(required=True),
            'tenant':           dict(required=True),
            'token':            dict(),
            'group':            dict(type='dict'),
            'group_conditions': dict(type='dict'),
            'group_member':     dict(type='dict'),
        },
        mutually_exclusive=[
            ['group', 'group_conditions', 'group_member'],
        ],
    )

    hawkular_alerts = hawkular.alerts.HawkularAlertsClient(
        module.params['endpoint'],
        module.params['tenant'],
        token=module.params['token'],
        ssl_verify=False,  # FIXME
    )

    group = module.params['group']
    group_conditions = module.params['group_conditions']
    group_member = module.params['group_member']

    if group is not None:
        hawkular_alerts.create_group(group)

    if group_conditions is not None:
        hawkular_alerts.create_group_conditions(
            group_conditions.get('groupId'),
            group_conditions.get('triggerMode'),
            {"conditions": group_conditions['conditions']})

    if group_member is not None:
        hawkular_alerts.create_group_member(group_member)

    module.exit_json(changed=True)


if __name__ == '__main__':
    main()
