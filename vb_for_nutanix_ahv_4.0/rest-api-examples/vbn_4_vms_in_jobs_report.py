# Simple example on how Veeam Backup for Nutanix AHV (aka VBN aka VB) 4.0 public REST API can be used
#
# Current script reports info on VMs: to which jobs are they added. 
#
# The rest clien has been generated using Swagger editor: https://editor-next.swagger.io/

from argparse import ArgumentParser

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


def send_mail(smtp_server, sender_email, receiver_email, subject, html_body):

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email.replace(',',';') #  to support both "," and ";" as a separator
    message.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(smtp_server) as server:
        server.sendmail(
            sender_email, receiver_email.replace(',',';').split(';'), message.as_string()
        )

def is_service_vm(vm_name):
    if vm_name == "VeeamZip" or vm_name[0:8] == 'VeeamTmp-':
        return True

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
                swagger_client.Cluster.attribute_map['name'],
                swagger_client.Direction.ASCENDING,
                swagger_client.Collation.IGNORECASE,
            ),
            offset = offset,
            limit = limit
        )
        all_vms += vms_from_cluster.results
        total_count = vms_from_cluster.total_count

    return list(filter(lambda x: not is_service_vm(x.name), all_vms))

def get_all_jobs():
    jobs = []    

    offset = 0
    limit = 0
    total_count = 1 # will be updated
    while offset + limit < total_count:
        offset = offset + limit
        limit = 100
        jobs_page = vb_rest_client.JobsApi.jobs_get_page(
            sort = swagger_client.SortExpression(  # create sort query. VB has a very powerful sort & filter query functionality, here we use only primitive abilities.
                swagger_client.Job.attribute_map['name'],
                swagger_client.Direction.ASCENDING,
                swagger_client.Collation.IGNORECASE
            ),
            offset = offset,
            limit = limit
        )
        jobs += jobs_page.results
        total_count = jobs_page.total_count
    return jobs

def is_vm_in_job(vm, job):
    # we don't cover the case when VM is excluded by rule
    return vm.id in job._settings.vm_ids or vm.protection_domain in job._settings.protection_domains

def format_jobs_list(jobs, critical_if_none=False):
    if len(jobs) == 0:
        return colorize_text('NONE', '#FF0000') if critical_if_none else 'NONE'
    if len(jobs) > 1:
        return colorize_text(", ".join([html.escape(x.name) for x in jobs]), '#BF4706')
    return html.escape(jobs[0].name)

def generate_vms_in_jobs_table(vms, jobs):
    rpo_table = {
        'header': ["VM", "Snapshot job(s)", "Backup job(s)"],
        'data': []
    }
    for vm in vms:
        snapshot_jobs = list(filter(lambda x: x.mode != swagger_client.JobMode.BACKUP and is_vm_in_job(vm, x), jobs))
        backup_jobs = list(filter(lambda x: x.mode == swagger_client.JobMode.BACKUP and is_vm_in_job(vm, x), jobs))
    
        rpo_table['data'].append([
            html.escape(vm.name),
            format_jobs_list(snapshot_jobs),
            format_jobs_list(backup_jobs, True),
        ])
    return generate_html_table(
        header=rpo_table['header'],
        data=rpo_table['data']
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

if __name__ == "__main__":
    args = parse_arguments()
    
    # Create global client for simplicity since the script is working with only one VB
    global vb_rest_client
    vb_rest_client = Vbn4RestClient(f"https://{args.address}", args.username, args.password)

    # Patch module to add Direction and Operation 'enums'.
    swagger_client = Vbn4RestClient.patch_swagger_client_module(swagger_client)
    
    cluster_settings = get_vb_cluster_settings()[0] # For now only 1 cluster max can be here

    jobs = get_all_jobs()
    vms = get_vms_from_cluster()

    # hack to force PrettyTable to insert html inside cells    
    br = "<br>\n"
    section_header_tag = 'h4'
    mail_body = f"VM protection report for {html.escape(cluster_settings.name)} cluster. {br}{br}" + \
        generate_html(section_header_tag, 'VMs protection by jobs (please not that exclude rules are ignored):') + \
        generate_vms_in_jobs_table(vms, jobs) + br 

    send_mail(
        smtp_server = args.smtp_server,
        sender_email = args.sender_mail,
        receiver_email = args.receiver_email,
        subject = f"VM protection report for {cluster_settings.name} cluster",
        html_body = mail_body
    )