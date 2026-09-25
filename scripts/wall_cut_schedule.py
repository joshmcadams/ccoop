"""Generate a provisional, kerf-aware stock schedule from the model report.

Considers standard 90 x 45 lengths. Each candidate plan packs the longest cuts
first; each stick is then shortened to the smallest standard length that holds
its cuts. The plan with the least total lineal length wins (ties: fewer sticks).
"""
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STOCK_MM=(3000,3600,4800,6000)
TRIM_MM=5    # each end of every stick
KERF_MM=3    # reserved per piece (conservative: one more kerf than strictly needed)


def usable(stock):
    return stock-2*TRIM_MM


def pack(parts,stock):
    bins=[]
    for name,length in parts:
        for b in bins:
            if b['used']+length+KERF_MM<=usable(stock):
                break
        else:
            b={'used':0,'parts':[]};bins.append(b)
        if length+KERF_MM>usable(stock):
            return None
        b['parts'].append((name,length));b['used']+=length+KERF_MM
    for b in bins:
        b['stock']=min(s for s in STOCK_MM if b['used']<=usable(s))
        b['remaining']=usable(b['stock'])-b['used']
    return bins


def write_schedule(report):
    parts=sorted([(o['name'],math.ceil(o['cut_length_m']*1000-1e-7)) for o in report['parts'] if o['name'].startswith('Wall_')],
                 key=lambda p:(-p[1],p[0]))
    plans=[b for b in (pack(parts,s) for s in STOCK_MM) if b]
    if not plans:
        raise ValueError('Wall part exceeds the longest stock allowance')
    bins=min(plans,key=lambda b:(sum(x['stock'] for x in b),len(b)))
    total=sum(b['stock'] for b in bins)
    def describe(plan):
        counts={s:sum(1 for b in plan if b['stock']==s) for s in STOCK_MM}
        return counts,', '.join(f'{n} × {s} mm' for s,n in counts.items() if n)
    counts,summary=describe(bins)
    alternatives=sorted({(sum(x['stock'] for x in p),describe(p)[1]) for p in plans})
    lines=['# Provisional wall framing cut schedule','',
        'Generated from `model-report.json` by `scripts/wall_cut_schedule.py`. Dressed 90 × 45 timber; grade/treatment and connections pending. These are rounded-up longest-point blank lengths, including bevel geometry. Verify on the erected floor and against the installed roof bearers before cutting.','',
        f'{len(parts)} pieces; indicative allocation: **{summary}** ({total/1000:.1f} lineal metres). This is a packing heuristic, not a proven minimum or a supplier quote. Each stick reserves {TRIM_MM} mm end trimming at both ends and {KERF_MM} mm kerf per piece. Offcuts are not charged again.','',
        'Alternative allocations from the same heuristic, by total length: '+'; '.join(f'{d} = {t/1000:.1f} m' for t,d in alternatives)+'. Shorter sticks cost a little more timber but are easier to transport and handle.','',
        '| Stick | Stock length (mm) | Named cuts (mm) | Remaining after trim and kerf (mm) |','| --- | --- | --- | --- |']
    for i,b in enumerate(bins,1):
        cuts='; '.join(f'{name}: {length}' for name,length in b['parts'])
        lines.append(f'| {i} | {b["stock"]} | {cuts} | {b["remaining"]} |')
    (ROOT/'generated'/'wall-cut-list.md').write_text('\n'.join(lines)+'\n')
    return {'pieces':len(parts),'sticks':len(bins),'stock_counts_mm':{str(s):n for s,n in counts.items() if n},
            'total_stock_m':total/1000,'alternatives':[{'total_m':t/1000,'stock':d} for t,d in alternatives],
            'kerf_mm':KERF_MM,'end_trim_each_mm':TRIM_MM}


if __name__=='__main__':
    print(write_schedule(json.loads((ROOT/'generated'/'model-report.json').read_text())))
