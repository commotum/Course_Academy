"""Separated financial choices measured in the question's rounding units."""
from decimal import Decimal, ROUND_HALF_UP, localcontext
from itertools import combinations

def rounded_units(raw,places):
    return int((raw*Decimal(10)**places).to_integral_value(rounding=ROUND_HALF_UP))

def minimum_gap(key,family):
    if family=='time':return 2
    if family=='rate':return 3
    return max(5,(abs(key)+999)//1000)

def separated(values,key,family):
    return len(set(values))==5 and all(b-a>=minimum_gap(key,family)for a,b in zip(sorted(values),sorted(values)[1:]))

def away_from_halfway(raw,places):
    scaled=raw*Decimal(10)**places
    return abs((scaled%1)-Decimal('.5'))>=Decimal('.05')

def initial_bank(current,rate,time,places,rank,position,rng):
    """Use actual sign, duration, percentage, and simple-interest mistakes.

    No offset from the rounded key is a candidate recipe. If their results
    collide or are too close, reject the parameters instead of adding filler.
    """
    with localcontext()as ctx:
        ctx.prec=50;C=Decimal(str(current));r=Decimal(str(rate));t=Decimal(time);rt=r*t
        raw=C*(-rt).exp();key=rounded_units(raw,places);gap=minimum_gap(key,'gas'if places else'profit')
        errors=[(C*rt.exp(),'reverse_rate_sign'),(C,'ignore_interest'),
                (C*(-r).exp(),'ignore_elapsed_time'),
                (C*(-2*rt).exp(),'double_duration'),(C*(-rt/2).exp(),'halve_duration'),
                (C*(-r*(t-1)).exp(),'one_period_short'),(C*(-r*(t+1)).exp(),'one_period_extra'),
                (C*(-rt/100).exp(),'convert_percent_twice'),
                (C*(1-rt),'use_linear_change')]
        if 1+rt>0:errors.append((C/(1+rt),'use_simple_interest'))
        if places:
            errors.extend([(C*(-rt/12).exp(),'convert_months_to_years_unnecessarily'),
                           (C*(-12*rt).exp(),'double_convert_duration_to_months')])
        # Keep candidate amounts on a reasonable scale while preserving sign
        # and time mistakes. Outliers cannot be used merely to fill the bank.
        seen={key};candidates=[]
        for value,label in errors:
            n=rounded_units(value,places)
            if n in seen or n<=0 or not Decimal('.4')*key<=n<=Decimal('2.5')*key:continue
            seen.add(n)
            if abs(n-key)>=gap:candidates.append((n,label))
        low=[v for v in candidates if v[0]<key];high=[v for v in candidates if v[0]>key]
        # Rank is a preference, not permission to fabricate implausible
        # mistakes when four separated errors on that side do not exist.
        alternatives=[v for v in range(5)if v!=rank];rng.shuffle(alternatives)
        for chosen_rank in [rank]+alternatives:
            lows=list(combinations(low,chosen_rank));highs=list(combinations(high,4-chosen_rank));rng.shuffle(lows);rng.shuffle(highs)
            for left in lows:
                for right in highs:
                    selected=list(left+right)
                    if not separated([key]+[n for n,_ in selected],key,'gas'if places else'profit'):continue
                    rng.shuffle(selected);selected.insert(position,(key,'correct'))
                    return raw,key,[n for n,_ in selected],[label for _,label in selected]
    raise ValueError('Insufficient separated diagnostic distractors')
