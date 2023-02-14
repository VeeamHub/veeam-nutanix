# Simple example on how Veeam Backup for Nutanix AHV (aka VBN aka VB) 4.0 public REST API can be used
#
# Current script generates simple daily session report 

from argparse import ArgumentParser

from datetime import datetime, timedelta
from dateutil import tz
from isodate import isoduration

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


def get_base_sessions(from_datetime, to_datetime):
    base_sessions = []    

    offset = 0
    limit = 0
    total_count = 1 # will be updated
    while offset + limit < total_count:
        offset = offset + limit
        limit = 100
        base_sessions_response = vb_rest_client.SessionsApi.sessions_get_base_info(
            sort = swagger_client.SortExpression(  # create sort query. VB has a very powerful sort & filter query functionality, here we use only primitive abilities.
                swagger_client.SessionBaseInfo.attribute_map['start_time_utc'], #we need to pass eact attribute name
                swagger_client.Direction.DESCENDING,
                swagger_client.Collation.ORDINAL
            ),
            _from = from_datetime,
            to = to_datetime,
            offset = offset,
            limit = limit
        )
        base_sessions += base_sessions_response.results
        total_count = base_sessions_response.total_count
    return base_sessions

def format_iso_duration(iso_duration):
    result_string = ""
    
    days  = iso_duration.days
    result_string += f"{days}d " if days else ""

    hours = iso_duration.seconds // (60*60) % 24
    result_string += f"{hours}h " if hours else ""
    
    minutes = (iso_duration.seconds // 60) % 60
    result_string += f"{minutes}m " if minutes else ""

    seconds = iso_duration.seconds % 60
    result_string += f"{seconds}s " if seconds and not days else "" # no need to print seconds if session duration is longer than 1 days

    return result_string


def get_human_readable_session_type(type):
    if type == swagger_client.SessionType.BACKUPVMJOB:
        return "Backup Job"
    if type == swagger_client.SessionType.VEEAMZIP:
        return "VeeamZIP"
    if type == swagger_client.SessionType.SNAPSHOTPDJOB:
        return "PD Snapshot Job"
    if type == swagger_client.SessionType.SNAPSHOTVMJOB:
        return "Snapshot Job"
    if type == swagger_client.SessionType.RESTOREVM:
        return "VM Restore"
    if type == swagger_client.SessionType.RESTOREVMDISKS:
        return "Disk Restore"
    if type == swagger_client.SessionType.APPLYNETWORKSETTINGS:
        return "Apply network settings"
    if type == swagger_client.SessionType.EXPORTLOGS:
        return "Export logs"
    if type == swagger_client.SessionType.REBOOTAPPLIANCE:
        return "Reboot backup appliance"
    if type == swagger_client.SessionType.RESTARTBACKUPSERVICE:
        return "Restart appliance service"
    if type == swagger_client.SessionType.RESCANBACKUPS:
        return "Refresh backups list from VBR"
    if type == swagger_client.SessionType.RESCANSNAPSHOTS:
        return "Rescan available snapshots"
    if type == swagger_client.SessionType.SHUTDOWNAPPLIANCE:
        return "Shut down appliance"
    if type == swagger_client.SessionType.CONFIGBACKUP:
        return "Export appliance configuration to zip file"
    return type # in case I missed some types here

def get_sessions_html_table(base_sessions):
    detailed_sessions_table = {
        'header': ["Name", "Type", "Result", "Start time", "End time", "Duration", "Details"],
        'data': []
    }
    for base_session in base_sessions:
        full_session = vb_rest_client.SessionsApi.sessions_get_by_id(id = base_session.id)
        interesting_events = list(filter(lambda x: x.severity != swagger_client.EventSeverity.INFORMATION, full_session._progress_state.events))

        
        name_field = full_session.name 
        # use original VM name for restoresessions 
        if is_restore_session(base_session):
            name_field = full_session.context.object_name 
        # use job name for jobs 
        if is_job_session(base_session):
            name_field = full_session.context.job_name 

        finish_time = "--"
        if full_session._finish_time_utc:
            finish_time = str(full_session._finish_time_utc.astimezone().strftime("%Y-%m-%d %H:%M %z"))

        detailed_sessions_table['data'].append([
            html.escape(name_field),
            html.escape(get_human_readable_session_type(full_session.session_type)),
            colorize_session_result(full_session.result),
            str(full_session.start_time_utc.astimezone().strftime("%Y-%m-%d %H:%M %z")),
            finish_time, # Will not present here if session is still running
            format_iso_duration(isoduration.parse_duration(full_session.duration)), 
            '<br>\n'.join([ html.escape(x.message) for x in interesting_events ])[1:2000] #There could be a lot of messages. Cut to the first 2000 symbols.
        ])
    return generate_html_table(
        header=detailed_sessions_table['header'],
        data=detailed_sessions_table['data']
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
    parser.add_argument("-f", "--from_datetime_utc", dest="from_datetime", 
        help="specify if you want to generate report for a custom period (be default, reoport is generate for the last 24 hours).")  
    parser.add_argument("-t", "--to_datetime_utc", dest="to_datetime", 
        help="specify if you want to generate report for a custom period (be default, reoport is generate for the last 24 hours).")  
    args, unknown = parser.parse_known_args()
    if (args.from_datetime and not args.to_datetime) or (not args.from_datetime and args.to_datetime): # de-facto xor 
        raise Exception("from and to fields should be specified together")
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

def is_job_session(session):
    return True if session.job_name else False

def is_restore_session(session):
    return session._session_type in [
        swagger_client.SessionType.RESTOREVM, 
        swagger_client.SessionType.RESTOREVMDISKS
    ]

def is_system_session(session):
    return not (is_restore_session(session) or is_job_session(session))


if __name__ == "__main__":
    args = parse_arguments()
    
    # Create global client for simplicity since the script is working with only one VB
    global vb_rest_client
    vb_rest_client = Vbn4RestClient(f"https://{args.address}", args.username, args.password)

    # Patch module to add Direction and Operation 'enums'.
    swagger_client = Vbn4RestClient.patch_swagger_client_module(swagger_client)

    # Getting report period
    report_period_prefix = 'Report'
    if not (args.from_datetime and args.to_datetime):
        today = datetime.utcnow().date()
        start_datetime = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
        end_datetime = start_datetime + timedelta(1)
    else: #just use 24 hours period
        start_datetime = args.from_datetime
        end_datetime = args.to_datetime
        report_period_prefix = 'Daily report'
    
    base_sessions = get_base_sessions(start_datetime, end_datetime) # base sessions do not include session details, so later we will need to get all sessions one-by-one anyway

    network_settings = get_vb_network_settings()    # Needed to get VB hostname
    cluster_settings = get_vb_cluster_settings()[0] # For now only 1 cluster max can be here
    
    # hack to force PrettyTable to insert html inside cells    
    br = "<br>\n"
    section_header_tag = 'h4'
    mail_body = f"{html.escape(report_period_prefix)} for VBN {generate_html('b',html.escape(network_settings.host_name))} on {generate_html('b', html.escape(cluster_settings.name))} cluster. {br}{br}" + \
        generate_html(section_header_tag, 'Job sessions:') + \
        get_sessions_html_table(list(filter(lambda x: is_job_session(x), base_sessions))) + br + \
        generate_html(section_header_tag, 'Restore sessions:') + \
        get_sessions_html_table(list(filter(lambda x: is_restore_session(x), base_sessions))) +  br + \
        generate_html(section_header_tag, 'System sessions:') + \
        get_sessions_html_table(list(filter(lambda x: is_system_session(x), base_sessions)))

    send_mail(
        smtp_server = args.smtp_server,
        sender_email = args.sender_mail,
        receiver_email = args.receiver_email,
        subject = f"{report_period_prefix} for VBN {network_settings.host_name} on {cluster_settings.name} cluster",
        html_body = mail_body
    )