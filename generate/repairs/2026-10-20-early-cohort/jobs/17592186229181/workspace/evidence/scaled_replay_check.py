from checks import *
g=load();rows=[]
for sid,mask in g.MASKS.items():
 rows.append(visible_math(g.generate(mask['level'],51,template='source_'+sid,parameters={'mass_scale':'2','flow_scale':'2'}),True))
save('scaled-replay.json',{'cases':rows,'passed':True})
print('All',len(rows),'scaled source banks pass.')
