#!/usr/bin/env python3
"""Revalidate reviewed hashes and compact retired archives and identical backups."""
import argparse
import collections
from contextlib import ExitStack
import gzip
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'capture'))
from scripts.archive_maintenance import share_archived_group, compress_identical_backup
from scripts.storage import file_lock


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--review',type=Path,required=True,help='Reviewed exact-duplicate-groups.jsonl.gz')
    parser.add_argument('--report',type=Path,required=True)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--wait-locks',action='store_true',help='Wait for current capture/database work to release its locks')
    args=parser.parse_args();repo=args.repo.resolve();counts=collections.Counter();saved=0
    args.report.parent.mkdir(parents=True,exist_ok=True)
    with ExitStack()as stack:
        if args.apply:
            stack.enter_context(file_lock(repo/'.local/capture/database.lock',blocking=args.wait_locks))
            for account in ['foundations','linear','multivariable','differential']:
                stack.enter_context(file_lock(repo/'.local/capture'/account/'capture.lock',blocking=args.wait_locks))
        output=stack.enter_context(args.report.open('a'))
        source=stack.enter_context(gzip.open(args.review,'rt'))
        for i,line in enumerate(source,1):
            group=json.loads(line)
            if group['bytes_per_copy'] < 4096:
                continue
            result=share_archived_group(group['paths'],group['sha256'],repo,apply=args.apply)
            rows=[result]if result else[]
            members=set(group['paths'])
            for path in group['paths']:
                if path.endswith('.previous') and path[:-9]in members:
                    result=compress_identical_backup(path,group['sha256'],repo,apply=args.apply)
                    if result:rows.append(result)
            for row in rows:
                counts[row['status']]+=1;saved+=row.get('allocated_bytes_saved',0)
                output.write(json.dumps(row)+'\n');output.flush()
            if i%10000==0:print(i,dict(counts),'allocated bytes saved',saved,flush=True)
        print(json.dumps({'apply':args.apply,'counts':dict(counts),'allocated_bytes_saved':saved}),flush=True)


if __name__=='__main__':main()
