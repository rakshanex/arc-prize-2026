"""
RAKSHANEX — Phase 4: Object-Aware DSL + Parameterized Rules on REAL ARC-AGI
===========================================================================
Phase 3: 22 fixed ops, depth-2 -> 24/400 solved, 0 wrong, Safe Score 100%.
Ab DSL ko grow karte hain (world-class ARC solvers jaisa direction):
  1. OBJECT-level ops: connected components, gravity, keep-largest/smallest object,
     border, symmetry-repair.
  2. PARAMETERIZED rules: color-mapping (train pairs se seekha gaya color permutation).
     Ye "learned from demos" hai — bahut powerful, PAR consistency-checked rahega.

CORE INVARIANT (RAKSHANEX): jo bhi rule/param chuna jaaye, wo SAARE train pairs par
exactly match kare, warna abstain. Isliye WRONG ~ 0 rehna chahiye — yahi verify karenge.

Search: fixed ops (depth 1+2) + parameterized ops (learned per-task).
Selection: RAKSHANEX ambiguity meter — consistent candidates ke DISTINCT test outputs.
           |D|==1 -> answer, warna abstain.
"""
import json, glob, os, numpy as np
from collections import deque

# ---------------- fixed geometry / grid ops (Phase 3 set) ----------------
def identity(g): return g
def flip_h(g):   return g[:, ::-1]
def flip_v(g):   return g[::-1, :]
def rot90(g):    return np.rot90(g,1)
def rot180(g):   return np.rot90(g,2)
def rot270(g):   return np.rot90(g,3)
def transpose(g):return g.T
def anti_transpose(g): return np.rot90(g,2).T
def tile2x2(g):  return np.tile(g,(2,2))
def tile3x3(g):  return np.tile(g,(3,3))
def tile1x2(g):  return np.tile(g,(1,2))
def tile2x1(g):  return np.tile(g,(2,1))
def upscale2(g): return np.kron(g, np.ones((2,2),dtype=g.dtype))
def upscale3(g): return np.kron(g, np.ones((3,3),dtype=g.dtype))
def dup_rows(g): return np.repeat(g,2,axis=0)
def dup_cols(g): return np.repeat(g,2,axis=1)
def mirror_right(g): return np.concatenate([g, g[:, ::-1]], axis=1)
def mirror_down(g):  return np.concatenate([g, g[::-1, :]], axis=0)
def quad_mirror(g):
    t=np.concatenate([g,g[:,::-1]],axis=1); return np.concatenate([t,t[::-1,:]],axis=0)

def _bg(g):
    vals,cnts=np.unique(g,return_counts=True); return vals[np.argmax(cnts)]
def crop_content(g):
    bg=_bg(g); m=(g!=bg)
    if not m.any(): return g
    r=np.where(m.any(1))[0]; c=np.where(m.any(0))[0]
    return g[r.min():r.max()+1, c.min():c.max()+1]
def remove_bg_to_zero(g):
    bg=_bg(g); o=g.copy(); o[g==bg]=0; return o

# ---------------- OBJECT-level ops ----------------
def _components(g, bg):
    """4-connected same-color components (non-bg). Return list of (color, mask)."""
    H,W=g.shape; seen=np.zeros((H,W),bool); comps=[]
    for i in range(H):
        for j in range(W):
            if seen[i,j] or g[i,j]==bg: continue
            col=g[i,j]; q=deque([(i,j)]); seen[i,j]=True
            mask=np.zeros((H,W),bool); mask[i,j]=True
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
    big=max(comps,key=lambda cm:cm[1].sum())
    o=np.full_like(g,bg); o[big[1]]=big[0]; res=crop_content(o)
    # PRINCIPLED: agar result degenerate 1x1 ho jaaye jabki input bada tha, to ye op
    # is task ke liye applicable nahi (single-pixel "object") -> not-applicable.
    if np.asarray(res).shape==(1,1) and g.size>1: raise ValueError("degenerate object; N/A")
    return res
def keep_smallest_object(g):
    bg=_bg(g); comps=_components(g,bg)
    if not comps: return g
    sm=min(comps,key=lambda cm:cm[1].sum())
    o=np.full_like(g,bg); o[sm[1]]=sm[0]; res=crop_content(o)
    if np.asarray(res).shape==(1,1) and g.size>1: raise ValueError("degenerate object; N/A")
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
# NOTE: count_objects_as_grid hataya gaya — wo (1,1) degenerate outputs deta tha jo
# alag tasks par spuriously "consistent" ho jaate the (false positives -> wrong answers).
# RAKSHANEX principle: unreliable op rakhne se accha hai use na rakho (abstain > galat).

FIXED = {f.__name__: f for f in [
    identity, flip_h, flip_v, rot90, rot180, rot270, transpose, anti_transpose,
    tile2x2, tile3x3, tile1x2, tile2x1, upscale2, upscale3, dup_rows, dup_cols,
    mirror_right, mirror_down, quad_mirror, crop_content, remove_bg_to_zero,
    keep_largest_object, keep_smallest_object, gravity_down, gravity_up,
]}
FNAMES=list(FIXED.keys())

def apply_chain(chain,g):
    x=np.asarray(g)
    for n in chain: x=np.asarray(FIXED[n](x))
    return x
def eq(a,b):
    a=np.asarray(a); b=np.asarray(b)
    return a.shape==b.shape and np.array_equal(a,b)

FIXED_CANDS=[(n,) for n in FNAMES]+[(a,b) for a in FNAMES for b in FNAMES]

# ---------------- PARAMETERIZED rule: color mapping ----------------
def learn_color_map(train):
    """Agar har train pair mein shape same aur ek consistent color->color map ho,
       to wahi map return karo, warna None."""
    mapping={}
    for gi,go in train:
        if gi.shape!=go.shape: return None
        for a,b in zip(gi.flatten(),go.flatten()):
            if a in mapping and mapping[a]!=b: return None
            mapping[a]=b
    return mapping
def apply_color_map(g, mapping):
    # SAFETY (RAKSHANEX invariant): agar test grid mein koi color hai jo mapping mein
    # nahi dekha (train mein aaya hi nahi), to hum bharosemand nahi -> raise -> abstain.
    for v in np.unique(g):
        if v not in mapping:
            raise ValueError("unseen color; abstain")
    o=g.copy()
    for a,b in mapping.items(): o[g==a]=b
    return o

# ---------------- PARAMETERIZED rule: select-color (most-fragmented non-bg) ----------------
# d9fac9be-type tasks: bade grid se ek color pick karke 1x1 output.
# Data-derived rule: sabse zyada FRAGMENTED non-bg color = highest (ncomps / pixel_count).
def _ncomps_color(g, color):
    H,W=g.shape; seen=np.zeros((H,W),bool); n=0
    for i in range(H):
        for j in range(W):
            if not seen[i,j] and g[i,j]==color:
                n+=1; q=deque([(i,j)]); seen[i,j]=True
                while q:
                    y,x=q.popleft()
                    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                        ny,nx=y+dy,x+dx
                        if 0<=ny<H and 0<=nx<W and not seen[ny,nx] and g[ny,nx]==color:
                            seen[ny,nx]=True; q.append((ny,nx))
    return n

def select_most_fragmented_color(g):
    """Return 1x1 grid = non-bg color with highest components-per-pixel ratio.
       Ties/undefined -> raise (abstain)."""
    g=np.asarray(g); bg=_bg(g)
    v,c=np.unique(g,return_counts=True)
    cand=[(vv,cc) for vv,cc in zip(v,c) if vv!=bg]
    if not cand: raise ValueError("no non-bg color; abstain")
    scored=[]
    for col,cnt in cand:
        ratio=_ncomps_color(g,col)/cnt
        scored.append((ratio,col))
    scored.sort(reverse=True)
    if len(scored)>=2 and abs(scored[0][0]-scored[1][0])<1e-9:
        raise ValueError("fragmentation tie; abstain")   # ambiguous -> honest abstain
    return np.array([[scored[0][1]]], dtype=g.dtype)

# ---------------- PARAMETERIZED rule: symmetry-repair ----------------
# ARC-common: grid mein ek 'hole' color hai; use grid ki symmetry se bharo.
_SYMS = {
    "flip_h": lambda a: a[:, ::-1],
    "flip_v": lambda a: a[::-1, :],
    "rot180": lambda a: np.rot90(a,2),
    "transpose": lambda a: a.T,
    "anti":  lambda a: np.rot90(a,2).T,
}
def _fill_by_symmetry(g, hole, symfn):
    g=np.asarray(g)
    s=symfn(g)
    if s.shape!=g.shape: raise ValueError("sym shape mismatch")
    out=g.copy(); mask=(g==hole)
    # sirf tabhi bharo jab source cell hole na ho (warna hole rehne do)
    src_ok = mask & (s!=hole)
    out[src_ok]=s[src_ok]
    return out
def learn_symmetry_repair(train):
    """Ek hole_color + symmetries ka SET dhoondho jo SAARE train pairs ko explain kare.
       Multi-symmetry jointly apply hoti hai; fill ke baad hole bacha to invalid."""
    holes=set()
    for gi,go in train:
        if gi.shape!=go.shape: return None
        d=(gi!=go)
        if d.any(): holes|=set(np.unique(gi[d]).tolist())
    if not holes: return None
    for hole in holes:
        # sabhi symmetries jo train par SAFE hain (galat cell nahi bharti) collect karo
        ok_all=True
        for gi,go in train:
            try:
                pred=_apply_all_syms(gi,hole)
            except Exception:
                ok_all=False;break
            # invalid agar hole bacha ya go se match nahi
            if (pred==hole).any() or not eq(pred,go):
                ok_all=False;break
        if ok_all:
            return (hole,"ALL")
    return None

def _apply_all_syms(g, hole):
    """Iteratively saari symmetries se hole bharo jab tak convergence."""
    g=np.asarray(g); out=g.copy()
    for _ in range(4):  # few passes for convergence
        changed=False
        for sfn in _SYMS.values():
            s=sfn(out)
            if s.shape!=out.shape: continue
            mask=(out==hole)&(s!=hole)
            if mask.any():
                out[mask]=s[mask]; changed=True
        if not changed: break
    return out

def apply_symmetry_repair(g, param):
    hole,mode=param
    out=_apply_all_syms(g,hole)
    # RAKSHANEX safety: agar fill ke baad bhi hole bacha, reliable nahi -> abstain
    if (out==hole).any():
        raise ValueError("holes remain after symmetry-fill; abstain")
    return out

# ---------------- PARAMETERIZED rule: periodic-tiling-fill ----------------
# ARC-common: grid ek repeating pattern hai jismein 'hole' color hai.
# Smallest period (ph,pw) dhoondho jispe non-hole cells consistent hon, phir hole bharo.
def _fill_periodic(g, hole):
    g=np.asarray(g); H,W=g.shape
    best=None
    for ph in range(1,H+1):
        for pw in range(1,W+1):
            if ph==H and pw==W: continue   # trivial (no compression) skip
            # har residue class (i%ph, j%pw) mein non-hole value unique hona chahiye
            tile=np.full((ph,pw),-1)
            ok=True
            for i in range(H):
                for j in range(W):
                    v=g[i,j]
                    if v==hole: continue
                    r,c=i%ph,j%pw
                    if tile[r,c]==-1: tile[r,c]=v
                    elif tile[r,c]!=v: ok=False;break
                if not ok: break
            if not ok: continue
            # tile mein koi -1 (undetermined) na ho, warna fill incomplete
            if (tile==-1).any(): continue
            out=g.copy()
            for i in range(H):
                for j in range(W):
                    if g[i,j]==hole: out[i,j]=tile[i%ph,j%pw]
            if not (out==hole).any():
                best=out; return best   # smallest period first
    raise ValueError("no consistent period; abstain")

def learn_periodic_fill(train):
    """hole-color infer karo; check ki periodic-fill saare train pairs explain kare."""
    holes=set()
    for gi,go in train:
        if gi.shape!=go.shape: return None
        d=(gi!=go)
        if d.any(): holes|=set(np.unique(gi[d]).tolist())
    if not holes: return None
    for hole in holes:
        ok=True
        for gi,go in train:
            try:
                if not eq(_fill_periodic(gi,hole),go): ok=False;break
            except Exception: ok=False;break
        if ok: return hole
    return None
def apply_periodic_fill(g, hole):
    return _fill_periodic(g, hole)

# ---------------- EXTRACTION rules (output = a subgrid of input) ----------------
def _bbox_of_mask(mask):
    r=np.where(mask.any(1))[0]; c=np.where(mask.any(0))[0]
    return r.min(),r.max(),c.min(),c.max()

def extract_largest_object_bbox(g):
    g=np.asarray(g); bg=_bg(g); comps=_components(g,bg)
    if not comps: raise ValueError("no object")
    big=max(comps,key=lambda cm:cm[1].sum())
    r0,r1,c0,c1=_bbox_of_mask(big[1])
    res=g[r0:r1+1,c0:c1+1]
    if res.shape==g.shape: raise ValueError("no crop")
    if res.shape==(1,1) and g.size>1: raise ValueError("degenerate 1x1; N/A")
    return res

def extract_smallest_object_bbox(g):
    g=np.asarray(g); bg=_bg(g); comps=_components(g,bg)
    if not comps: raise ValueError("no object")
    sm=min(comps,key=lambda cm:cm[1].sum())
    r0,r1,c0,c1=_bbox_of_mask(sm[1])
    res=g[r0:r1+1,c0:c1+1]
    if res.shape==g.shape: raise ValueError("no crop")
    if res.shape==(1,1) and g.size>1: raise ValueError("degenerate 1x1; N/A")
    return res

def extract_most_common_color_bbox(g):
    """Non-bg color jiski frequency sabse zyada -> uske sabse bade component ka bbox."""
    g=np.asarray(g); bg=_bg(g)
    v,c=np.unique(g,return_counts=True)
    nb=[(cc,vv) for vv,cc in zip(v,c) if vv!=bg]
    if not nb: raise ValueError("no non-bg")
    nb.sort(reverse=True); col=nb[0][1]
    mask=(g==col)
    r0,r1,c0,c1=_bbox_of_mask(mask)
    res=g[r0:r1+1,c0:c1+1]
    if res.shape==g.shape: raise ValueError("no crop")
    if res.shape==(1,1) and g.size>1: raise ValueError("degenerate 1x1; N/A")
    return res

_EXTRACTORS={
    "largest_bbox": extract_largest_object_bbox,
    "smallest_bbox": extract_smallest_object_bbox,
    "mostcommon_bbox": extract_most_common_color_bbox,
}
def learn_extractor(train):
    for name,fn in _EXTRACTORS.items():
        ok=True
        for gi,go in train:
            try:
                if not eq(fn(gi),go): ok=False;break
            except Exception: ok=False;break
        if ok: return name
    return None
def apply_extractor(g,name):
    return _EXTRACTORS[name](g)

# ---------------- LEARNED rule: local 3x3 neighborhood -> output cell ----------------
# Ye system KHUD train se rule seekhta hai (hand-coded nahi). Same-shape tasks ke liye:
# har output cell = f(input ka 3x3 padoss). Lookup table train se banti hai.
# SAFETY: test mein koi patch jo train mein nahi dikha -> abstain (unseen patch).
def learn_local_rule(train, k=1):
    table={}
    for gi,go in train:
        gi=np.asarray(gi); go=np.asarray(go)
        if gi.shape!=go.shape: return None
        H,W=gi.shape; gp=np.pad(gi,k,constant_values=-1)
        for i in range(H):
            for j in range(W):
                patch=tuple(gp[i:i+2*k+1, j:j+2*k+1].flatten())
                if patch in table and table[patch]!=go[i,j]: return None
                table[patch]=int(go[i,j])
    return table
def apply_local_rule(gi, table, k=1):
    gi=np.asarray(gi); H,W=gi.shape; gp=np.pad(gi,k,constant_values=-1); out=gi.copy()
    for i in range(H):
        for j in range(W):
            patch=tuple(gp[i:i+2*k+1,j:j+2*k+1].flatten())
            if patch not in table:
                raise ValueError("unseen patch; abstain")   # honest abstain
            out[i,j]=table[patch]
    return out

def learn_local_rule_auto(train, ks=(0,1,2)):
    """GENERALIZED: sabse CHHOTA neighborhood size k dhoondho jo train par consistent ho.
       Chhota k = zyada general (kam overfit). Returns (k, table) or None."""
    for k in ks:
        t=learn_local_rule(train,k)
        if t is not None:
            return (k,t)
    return None

# ---------------- OBJECT-LEVEL learned rules ----------------
def _objects(g): return _components(np.asarray(g), _bg(np.asarray(g)))
def _shape_sig(mask):
    r=np.where(mask.any(1))[0]; c=np.where(mask.any(0))[0]
    sub=mask[r.min():r.max()+1, c.min():c.max()+1]
    return sub.tobytes()+bytes([sub.shape[0]%256, sub.shape[1]%256])

def learn_recolor_by_shape(train):
    """Per-object: object ka naya color uski SHAPE par depend karta hai (train se seekha)."""
    table={}
    for gi,go in train:
        gi=np.asarray(gi); go=np.asarray(go)
        if gi.shape!=go.shape: return None
        bg=_bg(gi)
        for col,mask in _objects(gi):
            ov=np.unique(go[mask])
            if len(ov)!=1: return None
            sig=_shape_sig(mask)
            if sig in table and table[sig]!=int(ov[0]): return None
            table[sig]=int(ov[0])
        if not np.array_equal(gi[gi==bg],go[gi==bg]): return None
    return table if table else None
def apply_recolor_by_shape(gi, table):
    gi=np.asarray(gi); out=gi.copy()
    for col,mask in _objects(gi):
        sig=_shape_sig(mask)
        if sig not in table: raise ValueError("unseen shape; abstain")
        out[mask]=table[sig]
    return out

def load_task(path):
    d=json.load(open(path))
    tr=[(np.array(p["input"]),np.array(p["output"])) for p in d["train"]]
    te=[(np.array(p["input"]),np.array(p["output"])) for p in d["test"]]
    return tr,te

def consistent_candidates(train):
    """Return list of ('fixed', chain) or ('colormap', mapping) that match ALL train."""
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
            ok=all(eq(apply_color_map(gi,cm),go) for gi,go in train)
        except Exception:
            ok=False
        if ok: out.append(("colormap",cm))
    # select-color (most-fragmented non-bg): consistency-check on all train pairs
    try:
        ok=all(eq(select_most_fragmented_color(gi),go) for gi,go in train)
        if ok: out.append(("selectcolor",None))
    except Exception:
        pass
    # symmetry-repair: infer (hole,symmetry) from train, consistency-checked inside
    sr=learn_symmetry_repair(train)
    if sr is not None:
        out.append(("symrepair",sr))
    # periodic-tiling-fill: infer hole; consistency-checked inside
    pf=learn_periodic_fill(train)
    if pf is not None:
        out.append(("periodicfill",pf))
    # extraction (output = subgrid of input): consistency-checked
    ex=learn_extractor(train)
    if ex is not None:
        out.append(("extract",ex))

    # LEARNED local rule (system khud seekhta hai): variable neighborhood, smallest consistent k
    lk=learn_local_rule_auto(train,(0,1,2))
    if lk is not None:
        k,lt=lk
        try:
            if all(eq(apply_local_rule(gi,lt,k),go) for gi,go in train):
                out.append(("locallearned",(k,lt)))
        except Exception:
            pass
    # OBJECT-LEVEL learned: recolor-by-shape (consistency-checked)
    rs=learn_recolor_by_shape(train)
    if rs is not None:
        try:
            if all(eq(apply_recolor_by_shape(gi,rs),go) for gi,go in train):
                out.append(("recolorshape",rs))
        except Exception:
            pass
    return out

def predict(cand, ti):
    kind,val=cand
    if kind=="fixed": return apply_chain(val,ti)
    if kind=="colormap": return apply_color_map(ti,val)
    if kind=="selectcolor": return select_most_fragmented_color(ti)
    if kind=="symrepair": return apply_symmetry_repair(ti,val)
    if kind=="periodicfill": return apply_periodic_fill(ti,val)
    if kind=="extract": return apply_extractor(ti,val)
    if kind=="locallearned":
        k,tbl=val; return apply_local_rule(ti,tbl,k)
    if kind=="recolorshape": return apply_recolor_by_shape(ti,val)
    if kind=="compose_cm":
        pre,cm=val; return apply_color_map(np.asarray(FIXED[pre](np.asarray(ti))),cm)
    if kind=="compose_pf":
        pre,hole=val; return apply_periodic_fill(np.asarray(FIXED[pre](np.asarray(ti))),hole)
    raise ValueError("unknown cand")
    # Kai tasks "geometry + color" hote hain (jaise pehle rotate, phir recolor).
    # Pre-ops chhota reliable set (shape-changing + identity) — explosion avoid.
    PRE_OPS = ["identity","flip_h","flip_v","rot90","rot180","rot270","transpose",
               "crop_content","upscale2","tile2x2"]
    for pre in PRE_OPS:
        try:
            pre_train=[(np.asarray(FIXED[pre](gi)), go) for gi,go in train]
        except Exception:
            continue
        # learned colormap on transformed inputs
        cm=learn_color_map(pre_train)
        if cm is not None:
            try:
                if all(eq(apply_color_map(gi2,cm),go) for gi2,go in pre_train):
                    out.append(("compose_cm",(pre,cm)))
            except Exception:
                pass
        # learned periodic-fill on transformed inputs
        try:
            pf2=learn_periodic_fill(pre_train)
            if pf2 is not None:
                out.append(("compose_pf",(pre,pf2)))
        except Exception:
            pass
    return out

def safe_predict(cand, ti):
    """Baseline ke liye: exception -> None (abstain-equivalent)."""
    try: return predict(cand,ti)
    except Exception: return None

def distinct_outputs(cands, ti):
    outs=[]
    for c in cands:
        try: o=predict(c,ti)
        except Exception: continue
        if not any(eq(o,e) for e in outs): outs.append(o)
    return outs

def evaluate(folder, limit=400):
    files=sorted(glob.glob(os.path.join(folder,"*.json")))[:limit]
    n=0; solved=wrong=abstain=0; b_correct=b_wrong=0; ids=[]
    n_test_pairs=0
    for f in files:
        try: tr,te=load_task(f)
        except Exception: continue
        n+=1
        C=consistent_candidates(tr)
        # RIGOR: har task ke SAARE test pairs par decision lo.
        # Task tabhi 'solved' jab har test-pair par ANSWER kiya AUR sahi.
        # Agar kisi bhi answered test-pair par galat -> 'wrong'. Agar kisi bhi pair par
        # abstain -> pura task 'abstain' (conservative: partial answer nahi maante).
        task_answered_all=True; task_wrong=False; task_all_correct=True
        for (ti,to) in te:
            n_test_pairs+=1
            D=distinct_outputs(C,ti)
            # baseline (per test pair)
            bpred=safe_predict(C[0],ti) if C else ti
            if bpred is not None and eq(bpred,to): b_correct+=1
            else: b_wrong+=1
            # RAKSHANEX decision (NO patch-guard now)
            if len(D)==1:
                if not eq(D[0],to): task_wrong=True; task_all_correct=False
            else:
                task_answered_all=False; task_all_correct=False
        if task_wrong:
            wrong+=1
        elif task_answered_all and task_all_correct:
            solved+=1; ids.append(os.path.basename(f))
        else:
            abstain+=1
    ans=solved+wrong
    p=lambda x:x/n*100 if n else 0
    safe=solved/ans*100 if ans else float('nan')
    print("="*74)
    print(f"RAKSHANEX Phase 11 — +var-neighborhood (all test pairs, no patch-guard), REAL ARC (n={n}, test_pairs={n_test_pairs})")
    print(f"|fixed ops|={len(FNAMES)}  |fixed cands|={len(FIXED_CANDS)}  +colormap +select-color")
    print("="*74)
    print(f"{'metric':<34}{'always-answer':>16}{'RAKSHANEX':>16}")
    print("-"*74)
    print(f"{'SOLVED tasks (of all) %':<34}{'':>16}{p(solved):>15.1f}%")
    print(f"{'WRONG tasks (of all) %':<34}{'':>16}{p(wrong):>15.1f}%")
    print(f"{'abstain tasks %':<34}{'':>16}{p(abstain):>15.1f}%")
    print(f"{'per-test-pair Safe (always-ans)':<34}{b_correct/(b_correct+b_wrong)*100 if (b_correct+b_wrong) else 0:>15.1f}%{'':>16}")
    print(f"{'Task Safe Score (solved/answered)':<34}{'':>16}{safe:>15.1f}%")
    print("-"*74)
    print(f"RAKSHANEX: {solved} SOLVED, {wrong} wrong, {abstain} abstained.")
    print("solved sample:", ids[:10])
    return solved,wrong,abstain,n



# ---------- extra principled rules (deep-research additions) ----------
from collections import deque as _deque
def _bg2(g):
    v,c=np.unique(g,return_counts=True); return v[np.argmax(c)]
def _enclosed_mask(g):
    g=np.asarray(g); b=_bg2(g); H,W=g.shape
    reach=np.zeros((H,W),bool); q=_deque()
    for i in range(H):
        for j in (0,W-1):
            if g[i,j]==b and not reach[i,j]: reach[i,j]=True;q.append((i,j))
    for j in range(W):
        for i in (0,H-1):
            if g[i,j]==b and not reach[i,j]: reach[i,j]=True;q.append((i,j))
    while q:
        y,x=q.popleft()
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and g[ny,nx]==b and not reach[ny,nx]:
                reach[ny,nx]=True;q.append((ny,nx))
    return (g==b)&(~reach)
def _symmetrize(g):
    g=np.asarray(g); b=_bg2(g); out=g.copy()
    for t in [g[:,::-1],g[::-1,:],np.rot90(g,2)]:
        if t.shape==g.shape:
            m=(out==b)&(t!=b); out[m]=t[m]
    return out
def _extra_candidates(train):
    out=[]
    cols=set()
    for gi,go in train: cols|=set(np.unique(go).tolist())
    for fc in cols:
        ok=True; used=False
        for gi,go in train:
            enc=_enclosed_mask(gi)
            if enc.sum()>0: used=True
            pred=np.asarray(gi).copy(); pred[enc]=fc
            if not np.array_equal(pred,go): ok=False;break
        if ok and used: out.append(("fill",fc)); break
    if all(np.asarray(gi).shape==np.asarray(go).shape and np.array_equal(_symmetrize(gi),go) for gi,go in train):
        out.append(("sym",None))
    # compress (remove uniform rows/cols)
    def _compress(g):
        g=np.asarray(g); ri=[i for i in range(g.shape[0]) if len(set(g[i]))==1]; ci=[j for j in range(g.shape[1]) if len(set(g[:,j]))==1]
        kr=[i for i in range(g.shape[0]) if i not in ri]; kc=[j for j in range(g.shape[1]) if j not in ci]
        if not kr or not kc: raise ValueError()
        return g[np.ix_(kr,kc)]
    try:
        if all(eq(_compress(gi),go) for gi,go in train): out.append(("compress",None))
    except Exception: pass
    # color switch a<->b
    pals=set()
    for gi,go in train: pals|=set(np.unique(gi).tolist())
    pl=sorted(pals)
    for _i in range(len(pl)):
        for _j in range(_i+1,len(pl)):
            a,b=pl[_i],pl[_j]; ok=True
            for gi,go in train:
                gi=np.asarray(gi); o=gi.copy(); o[gi==a]=b; o[gi==b]=a
                if not np.array_equal(o,go): ok=False;break
            if ok: out.append(("switch",(a,b)))
    return out
def _extra_predict(c,g):
    k,v=c
    if k=="fill":
        enc=_enclosed_mask(g); o=np.asarray(g).copy(); o[enc]=v; return o
    if k=="sym": return _symmetrize(g)
    if k=="compress":
        g=np.asarray(g); ri=[i for i in range(g.shape[0]) if len(set(g[i]))==1]; ci=[j for j in range(g.shape[1]) if len(set(g[:,j]))==1]
        kr=[i for i in range(g.shape[0]) if i not in ri]; kc=[j for j in range(g.shape[1]) if j not in ci]
        return g[np.ix_(kr,kc)]
    if k=="switch":
        a,b=v; g=np.asarray(g); o=g.copy(); o[g==a]=b; o[g==b]=a; return o
    raise ValueError("x")

# wrap the entrypoint's _solve_test_input to also consider extra candidates
# ================= KAGGLE ENTRYPOINT (RAKSHANEX, self-contained, no internet/LLM) =================
import glob as _glob
def _solve_test_input(train, ti):
    C=consistent_candidates(train)
    D=distinct_outputs(C, ti)
    ti=np.asarray(ti)
    for _c in _extra_candidates(train):
        try:
            _o=np.asarray(_extra_predict(_c, ti))
            if not any(eq(_o,_e) for _e in D): D.append(_o)
        except Exception: pass
    if len(D)==1: return D[0].tolist(), D[0].tolist()
    if len(D)>=2: return D[0].tolist(), D[1].tolist()
    a1=ti.tolist()
    try: a2=np.asarray(np.rot90(ti,2)).tolist()
    except Exception: a2=ti.tolist()
    return a1,a2

def kaggle_main(out_path="/kaggle/working/submission.json"):
    cands=["/kaggle/input/arc-prize-2026-arc-agi-2/arc-agi_test_challenges.json",
           "/kaggle/input/arc-prize-2026/arc-agi_test_challenges.json"]
    tp=next((p for p in cands if os.path.exists(p)), None)
    if tp is None:
        hits=_glob.glob("/kaggle/input/**/*test_challenges*.json", recursive=True)
        tp=hits[0] if hits else None
    if tp is None:
        print("test file not found"); return
    tasks=json.load(open(tp)); sub={}
    for tid,task in tasks.items():
        train=[(np.array(p["input"]),np.array(p["output"])) for p in task["train"]]
        preds=[]
        for tpair in task["test"]:
            a1,a2=_solve_test_input(train, np.array(tpair["input"]))
            preds.append({"attempt_1":a1,"attempt_2":a2})
        sub[tid]=preds
    json.dump(sub, open(out_path,"w"))
    print("wrote", out_path, len(sub), "tasks")

if __name__=="__main__":
    kaggle_main()
