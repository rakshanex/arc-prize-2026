"""
arc_prize_submission.py — RAKSHANEX @ ARC Prize 2026 (ARC-AGI-2 track)
=====================================================================
SELF-CONTAINED (no internet, no LLM/API) — Kaggle evaluation compliant.
Pure Python + numpy only.

Produces submission.json in the required format:
  { "<task_id>": [ {"attempt_1": <grid>, "attempt_2": <grid>}, ... one per test input ] }

RAKSHANEX approach (see paper):
  - Generate candidate transformation rules (geometry, object-ops, parameterized,
    learned local rules).
  - CONSISTENCY FILTER: keep only rules matching ALL train pairs.
  - SAFETY LAYER (calibration-free ambiguity meter): if consistent rules give exactly
    ONE distinct output -> confident answer.
  - Two-attempt policy for scoring:
       attempt_1 = safe/confident answer if available, else top candidate.
       attempt_2 = next distinct candidate (or fallback).
  RAKSHANEX's research contribution is SAFE ABSTENTION (0 confident-error); competition
  scoring needs a guess, so we still emit best-effort attempts (documented in paper).
"""
import json, os, glob
import numpy as np
from collections import deque

# ============================== DSL ==============================
def identity(g): return g
def flip_h(g): return g[:, ::-1]
def flip_v(g): return g[::-1, :]
def rot90(g): return np.rot90(g,1)
def rot180(g): return np.rot90(g,2)
def rot270(g): return np.rot90(g,3)
def transpose(g): return g.T
def anti_transpose(g): return np.rot90(g,2).T
def tile2x2(g): return np.tile(g,(2,2))
def tile3x3(g): return np.tile(g,(3,3))
def tile1x2(g): return np.tile(g,(1,2))
def tile2x1(g): return np.tile(g,(2,1))
def upscale2(g): return np.kron(g, np.ones((2,2),dtype=g.dtype))
def upscale3(g): return np.kron(g, np.ones((3,3),dtype=g.dtype))
def dup_rows(g): return np.repeat(g,2,axis=0)
def dup_cols(g): return np.repeat(g,2,axis=1)
def mirror_right(g): return np.concatenate([g, g[:, ::-1]], axis=1)
def mirror_down(g): return np.concatenate([g, g[::-1, :]], axis=0)
def quad_mirror(g):
    t=np.concatenate([g,g[:,::-1]],axis=1); return np.concatenate([t,t[::-1,:]],axis=0)
def _bg(g):
    v,c=np.unique(g,return_counts=True); return v[np.argmax(c)]
def crop_content(g):
    bg=_bg(g); m=(g!=bg)
    if not m.any(): return g
    r=np.where(m.any(1))[0]; c=np.where(m.any(0))[0]
    return g[r.min():r.max()+1, c.min():c.max()+1]
def remove_bg_to_zero(g):
    bg=_bg(g); o=g.copy(); o[g==bg]=0; return o
def _components(g,bg):
    H,W=g.shape; seen=np.zeros((H,W),bool); comps=[]
    for i in range(H):
        for j in range(W):
            if seen[i,j] or g[i,j]==bg: continue
            col=g[i,j]; q=deque([(i,j)]); seen[i,j]=True; mask=np.zeros((H,W),bool); mask[i,j]=True
            while q:
                y,x=q.popleft()
                for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                    ny,nx=y+dy,x+dx
                    if 0<=ny<H and 0<=nx<W and not seen[ny,nx] and g[ny,nx]==col:
                        seen[ny,nx]=True; mask[ny,nx]=True; q.append((ny,nx))
            comps.append((col,mask))
    return comps
def keep_largest_object(g):
    bg=_bg(g); comps=_components(g,bg)
    if not comps: return g
    big=max(comps,key=lambda cm:cm[1].sum()); o=np.full_like(g,bg); o[big[1]]=big[0]; res=crop_content(o)
    if res.shape==g.shape or (res.shape==(1,1) and g.size>1): raise ValueError("na")
    return res
def keep_smallest_object(g):
    bg=_bg(g); comps=_components(g,bg)
    if not comps: return g
    sm=min(comps,key=lambda cm:cm[1].sum()); o=np.full_like(g,bg); o[sm[1]]=sm[0]; res=crop_content(o)
    if res.shape==g.shape or (res.shape==(1,1) and g.size>1): raise ValueError("na")
    return res
def gravity_down(g):
    bg=_bg(g); o=np.full_like(g,bg)
    for c in range(g.shape[1]):
        col=[v for v in g[:,c] if v!=bg]
        if col: o[g.shape[0]-len(col):,c]=col
    return o
def gravity_up(g):
    bg=_bg(g); o=np.full_like(g,bg)
    for c in range(g.shape[1]):
        col=[v for v in g[:,c] if v!=bg]
        if col: o[:len(col),c]=col
    return o

FIXED={f.__name__:f for f in [identity,flip_h,flip_v,rot90,rot180,rot270,transpose,
    anti_transpose,tile2x2,tile3x3,tile1x2,tile2x1,upscale2,upscale3,dup_rows,dup_cols,
    mirror_right,mirror_down,quad_mirror,crop_content,remove_bg_to_zero,
    keep_largest_object,keep_smallest_object,gravity_down,gravity_up]}
NAMES=list(FIXED.keys())
FIXED_CANDS=[(n,) for n in NAMES]+[(a,b) for a in NAMES for b in NAMES]

def apply_chain(chain,g):
    x=np.asarray(g)
    for n in chain: x=np.asarray(FIXED[n](x))
    return x
def eq(a,b):
    a=np.asarray(a); b=np.asarray(b); return a.shape==b.shape and np.array_equal(a,b)

def learn_color_map(train):
    m={}
    for gi,go in train:
        if gi.shape!=go.shape: return None
        for a,b in zip(gi.flatten(),go.flatten()):
            if a in m and m[a]!=b: return None
            m[a]=b
    return m
def apply_color_map(g,m):
    for v in np.unique(g):
        if v not in m: raise ValueError("unseen color")
    o=g.copy()
    for a,b in m.items(): o[g==a]=b
    return o
def learn_local_rule(train,k):
    t={}
    for gi,go in train:
        gi=np.asarray(gi); go=np.asarray(go)
        if gi.shape!=go.shape: return None
        H,W=gi.shape; gp=np.pad(gi,k,constant_values=-1)
        for i in range(H):
            for j in range(W):
                p=tuple(gp[i:i+2*k+1,j:j+2*k+1].flatten())
                if p in t and t[p]!=go[i,j]: return None
                t[p]=int(go[i,j])
    return t
def apply_local_rule(g,t,k):
    g=np.asarray(g); H,W=g.shape; gp=np.pad(g,k,constant_values=-1); o=g.copy()
    for i in range(H):
        for j in range(W):
            p=tuple(gp[i:i+2*k+1,j:j+2*k+1].flatten())
            if p not in t: raise ValueError("unseen patch")
            o[i,j]=t[p]
    return o

def consistent_candidates(train):
    out=[]
    for ch in FIXED_CANDS:
        ok=True
        for gi,go in train:
            try:
                if not eq(apply_chain(ch,gi),go): ok=False;break
            except Exception: ok=False;break
        if ok: out.append(("fixed",ch))
    cm=learn_color_map(train)
    if cm is not None:
        try:
            if all(eq(apply_color_map(gi,cm),go) for gi,go in train): out.append(("cm",cm))
        except Exception: pass
    for k in (0,1,2):
        lt=learn_local_rule(train,k)
        if lt is not None:
            try:
                if all(eq(apply_local_rule(gi,lt,k),go) for gi,go in train):
                    out.append(("local",(k,lt))); break
            except Exception: pass
    return out

def predict(cand,g):
    kind,val=cand
    if kind=="fixed": return apply_chain(val,g)
    if kind=="cm": return apply_color_map(g,val)
    if kind=="local": k,t=val; return apply_local_rule(g,t,k)
    raise ValueError("unknown")

def distinct_outputs(cands,g):
    outs=[]
    for c in cands:
        try: o=np.asarray(predict(c,g))
        except Exception: continue
        if not any(eq(o,e) for e in outs): outs.append(o)
    return outs

def solve_test_input(train, test_input):
    """Return (attempt_1, attempt_2, confident_flag)."""
    C=consistent_candidates(train)
    D=distinct_outputs(C, test_input)
    ti=np.asarray(test_input)
    if len(D)==1:
        a1=D[0]
        return a1.tolist(), a1.tolist(), True         # RAKSHANEX confident
    elif len(D)>=2:
        return D[0].tolist(), D[1].tolist(), False     # ambiguous -> top-2 guesses
    else:
        a1=ti.tolist()
        try: a2=np.asarray(rot180(ti)).tolist()
        except Exception: a2=ti.tolist()
        return a1, a2, False                           # no candidate -> fallback

def main(test_path=None, out_path="submission.json"):
    if test_path is None:
        # Robust auto-detect: try known paths, then glob any *test_challenges*.json under /kaggle/input
        cands=["/kaggle/input/arc-prize-2026-arc-agi-2/arc-agi_test_challenges.json",
               "/kaggle/input/arc-prize-2026/arc-agi_test_challenges.json",
               "/kaggle/input/arc-prize-2026-arc-agi-2/test_challenges.json"]
        test_path=next((p for p in cands if os.path.exists(p)), None)
        if test_path is None:
            hits=glob.glob("/kaggle/input/**/*test_challenges*.json", recursive=True)
            test_path=hits[0] if hits else None
    if test_path is None or not os.path.exists(test_path):
        print("Test file not found (set test_path for local run)."); return
    tasks=json.load(open(test_path))
    submission={}; n_conf=0; n_total=0
    for tid,task in tasks.items():
        train=[(np.array(p["input"]),np.array(p["output"])) for p in task["train"]]
        preds=[]
        for tp in task["test"]:
            a1,a2,conf=solve_test_input(train, np.array(tp["input"]))
            preds.append({"attempt_1":a1,"attempt_2":a2}); n_total+=1; n_conf+=int(conf)
        submission[tid]=preds
    json.dump(submission, open(out_path,"w"))
    print(f"Wrote {out_path}: {len(submission)} tasks, {n_total} inputs, {n_conf} RAKSHANEX-confident.")

if __name__=="__main__":
    # KAGGLE NOTEBOOK ENTRYPOINT — paste into a Kaggle notebook cell and run.
    # Auto-detects test file under /kaggle/input, writes /kaggle/working/submission.json.
    # Self-contained: numpy+json only, no internet/LLM (rule-compliant).
    main(test_path=None, out_path="/kaggle/working/submission.json")
