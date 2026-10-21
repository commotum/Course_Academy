import sys,json,copy,collections
sys.dont_write_bytecode=True
from audit import E,g,dump,shortcut
original=g.authored;valid=g.bank_valid;proposals=[];current={};seed=None

def build(level,p):
 global current
 current={'seed':seed,'difficulty':level,'parameters':copy.deepcopy(p)};proposals.append(current)
 try:
  result=original(level,p);current['construction']='passed';return result
 except ValueError as ex:current['construction']='rejected';current['reason']=str(ex);raise

def bank(M,b):
 try:
  idx=valid(M,b);current['bank']='passed';return idx
 except ValueError as ex:current['bank']='rejected';current['reason']=str(ex);raise

g.authored=build;g.bank_valid=bank;outputs=[]
for seed in range(90101,90161):outputs.append(g.generate_easy(seed=seed))
dump('resampling-stages.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python stage_audit.py','proposal_count':len(proposals),'surviving_count':len(outputs),'rejected_count':len(proposals)-len(outputs),'same_survivors_as_fresh':outputs==json.load(open(E/'fresh.json')),'proposals':proposals,'construction_rule':'All normal calls select authored_operations; rank two, pivot columns 0/1, free column 2; every free coefficient and constant sampled nonzero. Reject whole bank on duplicate affine sets, so equal-coordinate solution cases are resampled.','source_profiles':'No path in normal default sampling selects an observed source profile. Source family requests are possible only explicitly.','coverage_before_after':'Every proposal and survivor uses two equations / three variables, nonzero basic-variable slopes and constants, and a last-coordinate free variable. Rejection cannot recover omitted rank-one, zero-slope, alternate-free-role or zero-constant cases.'})
print(len(proposals),'proposals;',len(outputs),'accepted;',len(proposals)-len(outputs),'rejected')
