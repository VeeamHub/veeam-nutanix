#!/usr/bin/python3

# Simple example on how Veeam Backup for Nutanix AHV (aka VBN aka VB) 4.0 public REST API can be used
#
# Current script generates simple RPO report
#
# Note that if you want you can get SMTP settings directly from VB. 
# Public REST API allows to get everything except for SMTP authentication password

from argparse import ArgumentParser

from datetime import datetime, timezone

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import html

import swagger_client
from vbn_4_client_wrapper import Vbn4RestClient

def colorize_text(text, html_rgb_color):
    return f'<font color="{html_rgb_color}">{text}</font>'

def colorize_session_result(session_result):
    if session_result == swagger_client.SessionResult.ERROR:
        return colorize_text('Error', '#FF0000')
    if session_result == swagger_client.SessionResult.WARNING:
        return colorize_text('Warning', '#CCCC00')
    if session_result == swagger_client.SessionResult.SUCCESS:
        return colorize_text('Success', '#009933')
    if session_result == swagger_client.SessionResult.NONE:
        return colorize_text('Running', '#0000FF')

    raise Exception(f"Unknown session result {session_result}")

def get_vb_network_settings():
    return vb_rest_client.ServiceSettingsApi.service_settings_get_network_settings()

def get_vb_cluster_settings():
    return vb_rest_client.ClustersApi.clusters_get()

def generate_html(tag, text, style = False, custom_attributes=False):
        style_definition = f'style="{style}"' if style else ''
        custom_attributes = custom_attributes if custom_attributes else ''
        return f'<{tag} {custom_attributes} {style_definition}>{text}</{tag}>\n'

def generate_html_table(header, data):
    def generate_table_row(row_elements, style=False):
        return generate_html(
            'tr', 
            ''.join([generate_html('td', x, border_style) for x in row_elements]),
            style
        )

    border_style = 'border-bottom: 2px solid #000000;'
    background_styles = ['background-color:#ffffff;', 'background-color:#d9e1f3;']

    header_html = generate_html(
        'tr',
        ''.join([
            generate_html(
                'th', 
                html.escape(x), 
                border_style + 'text-align: left;'
            ) for x in header
        ])        
    )
    data_html = ''.join([generate_table_row(
        x, 
        background_styles[(idx + 1) % 2]
    ) for idx, x in enumerate(data)])

    return generate_html(
        'table', 
        header_html + data_html, 
        'text-align: left;border-collapse:collapse;color:#1f2240;background-color:#ffffff;',
        'cellspacing="4" cellpadding="2" width="100%" rules="rows"'
    )

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-u", "--username", dest="username",
        help="username to access backup appliance")
    parser.add_argument("-p", "--password", dest="password", 
        help="password to access backup appliance")
    parser.add_argument("-a", "--address", dest="address", 
        help="address of veeam backup appliance")
    parser.add_argument("-m", "--smtp_mail_server", dest="smtp_server", 
        help="SMTP server for sending mail report")    
    parser.add_argument("-s", "--sender_mail", dest="sender_mail", 
        help="sender mail address for sending mail report")   
    parser.add_argument("-r", "--receiver_email", dest="receiver_email", 
        help="receiver mail addresses for sending mail report (separated by , or ;)")   
    args, unknown = parser.parse_known_args()
    return args

def send_mail(smtp_server, sender_email, receiver_email, subject, html_body):

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email.replace(',',';') #  to support both "," and ";" as a separator
    message.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(smtp_server) as server:
        server.sendmail(
            sender_email, receiver_email.replace(';',',').split(','), message.as_string()
        )

def is_service_vm(vm_name):
    if vm_name == "VeeamZip" or vm_name[0:8] == 'VeeamTmp-':
        return True # They are now skipped (in 4.0) by default, so the check can be removed

def get_vms_from_cluster():
    cluster_settings = get_vb_cluster_settings()[0] # For now only 1 cluster max can be here
    all_vms = []
    
    offset = 0
    limit = 0
    total_count = 1 # will be updated
    while offset + limit < total_count:
        offset = offset + limit
        limit = 100
        vms_from_cluster = vb_rest_client.ClustersApi.clusters_get_vms(
            id=cluster_settings.id,
            sort = swagger_client.SortExpression(  # create sort query. VB has a very powerful sort & filter query functionality, here we use only primitive abilities.
                swagger_client.VirtualMachine.attribute_map['name'], #we need to pass eact attribute name
                swagger_client.Direction.ASCENDING,
                swagger_client.Collation.IGNORECASE,
            ),
            offset = offset,
            limit = limit
        )
        all_vms += vms_from_cluster.results
        total_count = vms_from_cluster.total_count

    return list(filter(lambda x: not is_service_vm(x.name), all_vms))

def get_restore_points_for_vm(vm_id):
    ponts = []

    offset = 0
    limit = 0
    total_count = 1 # will be updated
    while offset + limit < total_count:
        offset = offset + limit
        limit = 100
        points_reponse = vb_rest_client.RestorePointsApi.restore_points_get(
            vm_id=vm_id,
            sort = swagger_client.SortExpression(  # create sort query. VB has a very powerful sort & filter query functionality, here we use only primitive abilities.
                swagger_client.RestorePointBase.attribute_map['creation_time_utc'],
                swagger_client.Direction.DESCENDING,
                swagger_client.Collation.ORDINAL,
            ),
            offset = offset,
            limit = limit
        )
        ponts += points_reponse.results
        total_count = points_reponse.total_count
    return ponts

def get_rpo(points_sorted):
    if len(points_sorted) > 0:
        last_point = points_sorted[0] 
        rpo = (datetime.now(timezone.utc) - last_point.creation_time_utc).seconds / (24 * 60 * 60)
        if rpo > 1.3: #1.3 because backup can take some time, so even with daily backup rpo is typically a bit more. 
            return colorize_text(f'{round(rpo, 2)}d', '#FF0000')
        else:
            return f'{round(rpo, 2)}d'
    else:
        return colorize_text('NONE', '#FF0000')

def get_last_point_date(points_sorted):
    if len(points_sorted) > 0:
        last_point_datetime = points_sorted[0].creation_time_utc
        return last_point_datetime.astimezone().strftime("%Y-%m-%d %H:%M %z")
    else:
        return colorize_text('NONE', '#FF0000')

def generate_rpo_table(vms):
    rpo_table = {
        'header': ["Name", "Last snapshot", "Last backup", "RPO by backup", "RPO by any point"],
        'data': []
    }
    for vm in vms:
        vm_points = get_restore_points_for_vm(vm.id)
        snapshots = list(filter(lambda x: x.type != swagger_client.RestorePointType.BACKUP, vm_points))
        backups = list(filter(lambda x: x.type == swagger_client.RestorePointType.BACKUP, vm_points))
    
        rpo_table['data'].append([
            html.escape(vm.name),
            get_last_point_date(snapshots),
            get_last_point_date(backups),
            get_rpo(backups),
            get_rpo(vm_points)
        ])
    return generate_html_table(
        header=rpo_table['header'],
        data=rpo_table['data']
    )


if __name__ == "__main__":
    args = parse_arguments()
    
    # Create global client for simplicity since the script is working with only one VB
    global vb_rest_client
    vb_rest_client = Vbn4RestClient(f"https://{args.address}", args.username, args.password)

    # Patch module to add Direction and Operation 'enums'.
    swagger_client = Vbn4RestClient.patch_swagger_client_module(swagger_client)
    
    cluster_settings = get_vb_cluster_settings()[0] # For now only 1 cluster max can be here
    
    # hack to force PrettyTable to insert html inside cells    
    br = "<br>\n"
    section_header_tag = 'h4'
    mail_body = f"RPO report for {html.escape(cluster_settings.name)} cluster. {br}{br}" + \
        generate_html(section_header_tag, 'VMs RPO information:') + \
        generate_rpo_table(get_vms_from_cluster()) + br 

    send_mail(
        smtp_server = args.smtp_server,
        sender_email = args.sender_mail,
        receiver_email = args.receiver_email,
        subject = f"RPO report for {cluster_settings.name} cluster",
        html_body = mail_body
    )