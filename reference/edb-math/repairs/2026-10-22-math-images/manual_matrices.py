"""Three damaged titles: transcribe intact rendered matrices and verify row operations."""
from fractions import Fraction as F
import hashlib,json,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];RAW=ROOT/'.local/edb/math-image-import-audit-2026-10-22'
def augmented(left,right):return [list(map(F,a+b)) for a,b in zip(left,right)]
def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def array(rows,n):
 def tex(x):return str(x.numerator) if x.denominator==1 else r'\frac{'+str(x.numerator)+'}{'+str(x.denominator)+'}'
 return r'\left[\begin{array}{'+'c'*n+'|'+'c'*n+'}'+r' \\ '.join(' & '.join(tex(x) for x in row) for row in rows)+r'\end{array}\right]'
def main():
 cases=[
  ('ec90e2bc02040dd0cc0195c5f02d4ddf9a219ac1bfe740db3f02f55b0a2fdf56','A',[[1,0,4],[0,1,0],[0,0,-1]],[(2,-1,None),(0,-4,2)],[r'R_3:=(-1)R_3',r'R_1:=R_1+(-4)R_3']),
  ('2470c145390237d588db20950bdf573f79961929bbf2051e8f4a067b977ddc68','A',[[1,1,0,0],[0,1,0,0],[0,0,3,0],[0,0,0,1]],[(2,F(1,3),None),(0,-1,1)],[r'R_3:=\frac{1}{3}R_3',r'R_1:=R_1+(-1)R_2']),
  ('6b6f467a3b456421d1cf5483dd88f410881e082f8f7490bc7a1a559f0befa8b1','B',[[1,0,0,0],[0,1,0,0],[0,-3,1,0],[0,0,-1,1]],[(2,3,1),(3,1,2)],[r'R_3:=R_3+3R_2',r'R_4:=R_4+R_3'])]
 out={};proof=[]
 for digest,symbol,left,operations,labels in cases:
  n=len(left);rows=augmented(left,ident(n));snapshots=[[list(r) for r in rows]]
  for i,m,j in operations:
   rows[i]=[m*x for x in rows[i]] if j is None else [x+m*y for x,y in zip(rows[i],rows[j])]
   snapshots.append([list(r) for r in rows])
  assert [row[:n] for row in rows]==ident(n)
  inv=[row[n:] for row in rows]
  assert [[sum(F(left[i][k])*inv[k][j] for k in range(n)) for j in range(n)] for i in range(n)]==ident(n)
  lines=[]
  for i,matrix in enumerate(snapshots):
   prefix='['+symbol+r'\,|\,I'+('_4' if symbol=='B' else '')+']' if i==0 else ''
   relation='=' if i==0 else r'\sim'
   lines.append(prefix+' & '+relation+' '+array(matrix,n)+' & '+(labels[i] if i<len(labels) else ''))
  lines.append(r'&=[I\,|\,'+symbol+r'^{-1}]'+('.' if digest.startswith(('ec','6b')) else '')+' &')
  tex=r'\begin{array}{rll}'+r' \\[5pt] '.join(lines)+r'\end{array}'
  path='images/'+digest[:2]+'/'+digest+'.svg';original=RAW/(digest+'.png');target=HERE/'review'/original.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(original,target)
  out[path]={'tex':tex,'method':'reviewed-source-display','evidence':str(target.relative_to(ROOT)),'evidence_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'row_operations_verified':True}
  proof.append({'path':path,'snapshots':[[[str(x) for x in r] for r in m] for m in snapshots],'final_left_is_identity':True,'inverse_product_is_identity':True})
 (HERE/'manual-recoveries.json').write_text(json.dumps(out,indent=2)+'\n');(HERE/'matrix-row-operation-verification.json').write_text(json.dumps(proof,indent=2)+'\n')
if __name__=='__main__':main()
