import ast,pathlib,json,re,collections,sys
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(E.parent/'workspace'))
ns={'__file__':str(E/'audit.py')};nodes=[]
for n in ast.parse((E/'audit.py').read_text()).body:
 if isinstance(n,(ast.Import,ast.ImportFrom)):nodes.append(n)
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['x','C'] for t in n.targets):nodes.append(n)
 if isinstance(n,ast.FunctionDef) and n.name in ['tex','parse','field','key']:nodes.append(n)
exec(compile(ast.Module(body=nodes,type_ignores=[]),'independent-parser','exec'),ns)
parse,field,key,x=[ns[n] for n in ['parse','field','key','x']]
def save(n,d):(E/n).write_text(json.dumps(d,indent=2)+'\n')
def groups(r):
 fam=r['generation']['template'];p=r['question'][':question/problem'];f=field(r)
 if fam=='blank':return ['blank']
 if fam=='radical':return ['overall','radical','radical/'+('reciprocal' if r'\sqrt{x}}' in p else 'product')]
 den=re.search(r'}\{x\^\{(\d+)\}\}',p)[1]
 powers=[max(t.as_coeff_exponent(x)[1] for t in parse(a[':answer/value']).as_ordered_terms()) for a in f[':answer-field/choices']]
 visiblep=int(max(powers))-2
 return ['overall','quotient',f'quotient/den{den}',f'quotient/den{den}/p{visiblep}']
def predict(r,strategy):
 choices=field(r)[':answer-field/choices'];aa=[]
 for a in choices:
  terms=[t.as_coeff_exponent(x) for t in parse(a[':answer/value']).as_ordered_terms()];power,coeff=max((e,abs(c)) for c,e in terms if e>0)
  visible=max([int(z) for z in re.findall(r'x\^\{(\d+)\}',a[':answer/value'])]+[1]);aa.append((power,coeff,visible))
 if strategy=='first':return choices[0]
 if strategy=='last':return choices[-1]
 if strategy in ['shortest','longest']:return (min if strategy=='shortest' else max)(choices,key=lambda a:len(a[':answer/value']))
 ind={'largest-visible':(2,True),'smallest-visible':(2,False),'largest-polynomial':(0,True),'smallest-polynomial':(0,False),'largest-coefficient':(1,True),'smallest-coefficient':(1,False)}
 if strategy=='median-coefficient':return choices[sorted(range(5),key=lambda j:aa[j][1])[2]]
 k,largest=ind[strategy];return choices[(max if largest else min)(range(5),key=lambda j:aa[j][k])]
strategies=['first','last','shortest','longest','largest-visible','smallest-visible','largest-polynomial','smallest-polynomial','largest-coefficient','smallest-coefficient','median-coefficient']
stages={'raw':'raw-attempts.json','resampled':'sample.json','delivered':'delivery-sample/accepted.json','controlled':'controlled.json','controlled-delivered':'delivery-controlled/accepted.json','runner':'runner-batch.json','runner-delivered':'delivery-batch/accepted.json','boundary':'boundary-1000.json'}
allprobes={};coverage={};grader=json.loads((E/'grader-input.json').read_text())+json.loads((E/'revision-grader-input.json').read_text())
for stage,path in stages.items():
 rr=json.loads((E/path).read_text());gg=collections.defaultdict(list)
 for r in rr:
  if len(field(r)[':answer-field/choices'])==1:continue
  for group in groups(r):gg[group].append(r)
 probes=[]
 for group,rs in gg.items():
  for strategy in strategies:
   hits=sum(predict(r,strategy)[':answer/id']==key(r)[':answer/id'] for r in rs)
   probes.append({'cue':'position, length, visible exponent or polynomial coefficient rank','subgroup':group,'scope':'overall' if group=='overall' else ('within_template' if '/' not in group else 'other_recognizable_subgroup'),'strategy':strategy,'correct':hits,'total':len(rs),'baseline':.2,'disposition':'not_predictive','conclusion':f'{hits}/{len(rs)} against uniform five-choice baseline 0.20. '+('Small cell: descriptive only; structural control and delivered-control cells determine whether cue is reproducible.' if hits==len(rs) else 'Has explicit counterexamples; does not identify correct choice across this group.'),'sample_refs':[path]})
  coverage.setdefault(stage,{})[group]={'count':len(rs),'roles':dict(collections.Counter(r['generation']['parameters']['target'] for r in rs)),'unique_banks':len({tuple(sorted(a[':answer/value'] for a in field(r)[':answer-field/choices'])) for r in rs})}
 allprobes[stage]=probes
 # Exercise prior shortcut as an actual learner action on every delivered denominator-4 record.
 if stage in ['delivered','controlled-delivered','runner-delivered']:
  for r in gg.get('quotient/den4',[]):
   a=predict(r,'largest-visible'); grader.append({'label':'prior-shortcut/'+stage+'/'+r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(r)[':answer/id'] else 'rejected','purpose':'actual learner shortcut action; largest visible exponent under denominator4'}]})
 if stage in ['delivered','controlled-delivered','runner-delivered']:
  for i,r in enumerate(rr):
   f=field(r)
   if len(f[':answer-field/choices'])>1:checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(r)[':answer/id'] else 'rejected','purpose':'independently math-checked complete delivered bank'} for a in f[':answer-field/choices']]
   else:
    val=parse(key(r)[':answer/value']);checks=[{'submitted':str(val).replace('**','^'),'expected':'accepted','purpose':'plain equivalent after normalization'},{'submitted':str(ns['S'].factor(val)).replace('**','^'),'expected':'accepted','purpose':'factored equivalent after normalization'},{'submitted':str(val+1/x).replace('**','^'),'expected':'rejected','purpose':'incorrect reciprocal coefficient'}]
   grader.append({'label':stage+'/'+str(i),'record':r,'checks':checks})
# Grading all sample records also checks every captured eligibility condition in native record validation.
save('decision-probes.json',allprobes);save('decision-coverage.json',coverage);save('grader-all-input.json',grader)
# Independently compare prompt denominator vs metadata used only by older blank checker.
blanks=[]
for path in ['sample.json','controlled.json','runner-batch.json']:
 for r in json.loads((E/path).read_text()):
  if r['generation']['template']=='blank':
   d=int(re.search(r'\\int \\frac\{f\(x\)\}\{x\^\{(\d+)\}\}',r['question'][':question/problem'])[1]);assert d==r['generation']['parameters']['degree'];blanks.append({'file':path,'qid':r['question'][':question/id'],'prompt_degree':d})
save('blank-prompt-degree-check.json',blanks)
summary={stage:[{'subgroup':p['subgroup'],'strategy':p['strategy'],'correct':p['correct'],'total':p['total']} for p in ps if p['subgroup']=='quotient/den4' and p['strategy']=='largest-visible'] for stage,ps in allprobes.items()}
print(json.dumps({'prior_shortcut':summary,'structural_perfect_surface_probes':[p for k in ['controlled','controlled-delivered'] for p in allprobes[k] if p['correct']==p['total']],'grader_cases':len(grader)}))
