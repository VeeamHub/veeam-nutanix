# Simple example on how Veeam Backup for Nutanix AHV (aka VBN aka VB) 4.0 public REST API can be used
#
# Current script starts a job. If job is already running, nothing will happen

from argparse import ArgumentParser

import swagger_client
from vbn_4_client_wrapper import Vbn4RestClient

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

def find_job(name):
    jobs_page = vb_rest_client.JobsApi.jobs_get_page(
        filter =  swagger_client.FilterExpression(
            _property = swagger_client.Job.attribute_map['name'],
            collation = swagger_client.Collation.IGNORECASE, # Case-insensitive. Replace to ORDINAL/LEXICOGRAPHIC if that is a problem for you
            operation = swagger_client.Operation.EQUALS,
            value = name
        ),
        offset = 0,
        limit = 2 #If we found 2 jobs with the same name, that is already a problem
    )
    return jobs_page.results

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-u", "--username", dest="username",
        help="username to access backup appliance")
    parser.add_argument("-p", "--password", dest="password", 
        help="password to access backup appliance")
    parser.add_argument("-a", "--address", dest="address", 
        help="address of veeam backup appliance")
    parser.add_argument("-j", "--job", dest="job", 
        help="name of a job which you want to start")     
    parser.add_argument("-af", "--active_full", dest="active_full", 
        help="specify this param if you want to start full")     
    args, unknown = parser.parse_known_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    
    # Create global client for simplicity since the script is working with only one VB
    global vb_rest_client
    vb_rest_client = Vbn4RestClient(f"https://{args.address}", args.username, args.password)

    # Patch module to add Direction and Operation 'enums'.
    swagger_client = Vbn4RestClient.patch_swagger_client_module(swagger_client)
    

    # Stupid way - get all jobs and find among them
    # job_candidates = list(filter(lambda x: x.name == args.job or x.id == args.job, get_all_jobs()))
    # We don't use it here because we have a better option to do it

    # Smart way: filter in the request itself
    job_candidates = find_job(args.job)
    
    if len(job_candidates) == 0:
        raise Exception ("Job {args.job} not found")

    if len(job_candidates) > 1:
        raise Exception ("Found more than one job {args.job}")

    job = job_candidates[0]
    
    if args.active_full:
        backup_mode = swagger_client.BackupMode.ACTIVEFULLBACKUP
    else:
        backup_mode = swagger_client.BackupMode.INCREMENTALBACKUP

    vb_rest_client.JobsApi.jobs_start(
        id = job.id,
        backup_mode = backup_mode
    )
