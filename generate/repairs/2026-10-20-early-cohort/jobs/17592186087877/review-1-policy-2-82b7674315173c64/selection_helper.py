import hashlib
def choose(candidates,weights,seed,seen=()):
    # Faithful implementation of question_selection.rs::select: deduplicate and
    # sort numeric entity IDs, draw band then draw uniformly in band using SHA256.
    candidates=sorted({q[':db/id']:q for q in candidates if q[':db/id'] not in seen}.values(),key=lambda q:q[':db/id'])
    if weights is None:return candidates[0] if candidates else None
    bands=[[],[],[]];unrated=[]
    for q in candidates:
        d=q.get(':question/difficulty')
        if d is None:unrated.append(q);continue
        ident=d[':db/ident'] if isinstance(d,dict) else d
        bands[['easy','moderate','hard'].index(ident.split('/')[-1])].append(q)
    digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
    u=lambda offset:(int.from_bytes(digest[offset:offset+8],'big')>>11)/(1<<53)
    total=sum(w for w,band in zip(weights,bands) if band)
    if total>0:
        draw=u(0)*total;chosen=None
        for i,w in enumerate(weights):
            if not bands[i] or w==0:continue
            chosen=i
            if draw<w:break
            draw-=w
        pool=bands[chosen]
    else:pool=unrated
    return pool[int(u(8)*len(pool))] if pool else None
