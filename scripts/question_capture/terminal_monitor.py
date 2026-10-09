"""Compact terminal cards with comparable earned-XP activity bars."""
import math
import re
from datetime import datetime
from zoneinfo import ZoneInfo


def bars(activities, scale, length=20):
    shades='▁▂▃▄▅▆▇█'
    values=[a.get('earned',0) for a in activities[-length:]]
    rendered=''.join('↓' if value<0 else '·' if value==0 else shades[min(7,max(0,math.ceil(value/max(1,scale)*8)-1))]
                     for value in values)
    return ' '*(length-len(values))+rendered


def render(rows, width=80, *, color=False):
    width=max(40,min(width,150));inner=width-4
    stamp=datetime.now(ZoneInfo('America/Los_Angeles')).strftime('%H:%M:%S %Z')
    heading=' MATH ACADEMY  ·  '+str(sum(r['status']=='RUNNING' for r in rows))+' running '
    blocked=sum(r['status']=='BLOCKED' for r in rows)
    if blocked:heading+='· '+str(blocked)+' blocked '
    lines=['╭'+heading+'─'*max(0,width-len(heading)-len(stamp)-4)+' '+stamp+' ╮']
    def line(text):return '│ '+text[:inner].ljust(inner)+' │'
    for index,row in enumerate(rows):
        if index:lines.append('├'+'─'*(width-2)+'┤')
        percent=row.get('percent_complete')
        completion='—%' if percent is None else f'{percent:g}%'
        fill=0 if percent is None else max(0,min(8,int(percent*8/100)))
        progress='█'*fill+'░'*(8-fill)
        status=row['status'].replace('NOT CONFIGURED','UNCONFIGURED')
        name=row['window']
        symbol='●' if status=='RUNNING' else '○'
        left=f'{symbol} {name}';right=f'{status:<15} {progress} {completion}'
        lines.append(line(left+' '*max(2,inner-len(left)-len(right))+right))
        xp=row.get('daily_xp',{});points=f"{xp['earned']}/{xp['base']}" if xp else '—/—'
        counts=row.get('activity_counts',{})
        counts_text=' '.join(label+str(counts.get(kind,0)) for label,kind in
                             [('L','lesson'),('R','review'),('Q','quiz'),('M','multistep'),('D','diagnostic')])
        if width>=110:
            counts_text=' '.join(label+' '+str(counts.get(kind,0)) for label,kind in
                                 [('Lessons','lesson'),('Reviews','review'),('Quizzes','quiz'),('Multi','multistep'),('Diag','diagnostic')])
        db=row.get('database_questions',{})
        totals=f"DB +{db.get('added',0)} new / {db.get('updated',0)} existing"
        lines.append(line(f'Today {points} XP  ·  {counts_text}  ·  {totals}'))
        detail=row.get('detail','')
        if row['status']=='RUNNING' and row.get('log_age') is not None:detail+=' · '+str(row['log_age'])+'s ago'
        activities=row.get('recent_activities',[])
        scale=max([a.get('earned',0) for a in activities]+[1])
        chart=bars(activities,scale)
        if width>=110:chart=''.join(c*2 for c in chart)
        lines.append(line('Last 20 '+chart+f'  0–{scale:g} XP  ·  '+detail))
    legend=' earned XP · oldest → newest · scale shown per course '
    lines.append('╰'+legend[:width-2]+'─'*max(0,width-len(legend)-2)+'╯')
    lines.append('L lessons  R reviews  Q quizzes  M multisteps  D diagnostics · Ctrl+b d detach'[:width])
    if color:
        reset='\033[0m';muted='\033[38;5;245m';green='\033[38;5;150m';white='\033[1;38;5;255m'
        def paint(text):
            text=re.sub(r'[▁▂▃▄▅▆▇█]+',lambda m:green+m[0]+reset,text)
            text=text.replace('RUNNING',green+'RUNNING'+reset)
            text=text.replace('COMPLETE',green+'COMPLETE'+reset)
            for row in rows:
                if row['window'] in text:text=text.replace(row['window'],white+row['window']+reset)
            text=text.replace('↓','\033[38;5;221m↓'+reset)
            text=re.sub(r'BLOCKED|(?:HISTORY|IMPORT) PENDING|EXIT \d+',lambda m:'\033[38;5;221m'+m[0]+reset,text)
            if 'MATH ACADEMY' in text:text=white+text+reset
            elif text.startswith(('╰','├')) or text.startswith('L lessons'):text=muted+text+reset
            return text
        lines=[paint(text) for text in lines]
    return '\n'.join(lines)
