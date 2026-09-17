# LEVEL 0 — Python + Math (Foundation) — Deep, Simple Hindi

Ye SABSE zaroori level hai. Bina ye, aage sab magic lagega. Har cheez ke saath chhota
code hai — KHUD chala kar dekho (jaise `python3 file.py` ya online Python).

═══════════════════════════════════════════════════════════════════
# PART A — PYTHON (AI ki bhaasha)
═══════════════════════════════════════════════════════════════════

## 1. Variables (dabbe jismein value rakhte hain)
```python
naam = "Piyush"      # text (string)
umar = 25            # number (int)
pi = 3.14            # decimal (float)
hai_student = True   # haan/naa (boolean)
print(naam, umar)
```

## 2. Lists (cheezon ki line)
```python
numbers = [10, 20, 30, 40]
print(numbers[0])      # pehla = 10 (ginti 0 se shuru!)
numbers.append(50)     # aakhir mein jodo
print(len(numbers))    # kitne = 5
```

## 3. Loops (baar-baar karna)
```python
for n in [1, 2, 3]:
    print(n * n)       # 1, 4, 9 (har number ka square)
```

## 4. Conditions (agar-to)
```python
x = 7
if x > 5:
    print("bada")
else:
    print("chhota")
```

## 5. Functions (ek kaam ka naam de dena, baar-baar use karo)
```python
def square(n):        # 'square' naam ka function
    return n * n
print(square(4))      # 16
```

## 6. NumPy (AI ka sabse zaroori tool — numbers ke grid/array)
```python
import numpy as np
a = np.array([[1, 2], [3, 4]])   # 2x2 grid (matrix)
print(a.shape)                   # (2, 2)
print(a + 10)                    # har cell mein +10
print(a * 2)                     # har cell x2
print(a.T)                       # transpose (rows<->cols)
```
> AI mein saara data numbers ke grids (arrays) hota hai — image, text, sab. NumPy inhe
> handle karta hai. Hamare ARC grids bhi numpy arrays the!

## Python — kya zaroor aana chahiye (checklist)
- [ ] variables, lists, loops, if-else, functions
- [ ] numpy: array banana, shape, +/-/*, indexing, transpose
- **Practice:** Kaggle Learn "Python" + "Intro to Programming" (free, aapke account par)

═══════════════════════════════════════════════════════════════════
# PART B — MATH for AI (AI ki "physics")
═══════════════════════════════════════════════════════════════════
> Ghabrao mat — AI ke liye math ka MATLAB samajhna zaroori hai, ratta nahi.

## 1. LINEAR ALGEBRA (vectors + matrices) — neural nets isi par bane
- **Vector:** numbers ki ek line. `[3, 4]` — ek point/direction.
- **Matrix:** numbers ka grid. `[[1,2],[3,4]]`.
- **Kyun zaroori:** AI mein har cheez (image, word) ek vector banti hai. Neural network
  = matrices ka multiplication.
```python
import numpy as np
v = np.array([3, 4])
print(np.linalg.norm(v))     # length = 5 (Pythagoras!)
A = np.array([[1,2],[3,4]])
B = np.array([[5,6],[7,8]])
print(A @ B)                 # matrix multiply (@ = dot product)
```
- **Seekho:** 3Blue1Brown "Essence of Linear Algebra" (YouTube, visual, best).

## 2. PROBABILITY & STATISTICS — AI "guess" karta hai
- AI kabhi 100% sure nahi hota — wo probabilities deta hai (jaise "90% cat").
- **Zaroori concepts:** probability (0 se 1), average (mean), spread (variance),
  distribution (numbers kaise faile hain).
```python
import numpy as np
data = np.array([2, 4, 4, 4, 5, 5, 7, 9])
print(data.mean())    # average = 5.0
print(data.std())     # standard deviation (spread) = 2.0
```
- **Seekho:** Khan Academy "Statistics & Probability" (free).

## 3. CALCULUS (basics) — AI "seekhta" kaise hai
- Sirf ek idea zaroori: **derivative = slope = kis taraf badalna hai.**
- AI seekhta hai "gradient descent" se: error ki slope dekho, us ulti taraf thoda chalo,
  error kam karo. Baar-baar. Ye poore deep learning ka core hai.
```python
# derivative ka idea: f(x)=x^2 ka slope 2x hota hai
def f(x): return x**2
def slope(x, h=0.0001): return (f(x+h)-f(x))/h  # numerical derivative
print(slope(3))       # ~6 (kyunki 2*3=6)
```
- **Seekho:** 3Blue1Brown "Essence of Calculus" (bस pehle 3-4 videos kaafi hain).

## Math — kya zaroor samajhna (checklist)
- [ ] Vector kya hai, matrix multiply kya karta hai
- [ ] Mean/variance/probability ka matlab
- [ ] Derivative = slope, gradient descent ka idea ("error kam karne ki disha")

═══════════════════════════════════════════════════════════════════
## LEVEL 0 — kaise master karein (roz 1 ghanta)
- Week 1-4: Python (Kaggle Learn Python + code roz)
- Week 5-8: Linear Algebra (3Blue1Brown + numpy practice)
- Week 9-10: Probability/Stats (Khan Academy)
- Week 11-12: Calculus idea (3Blue1Brown, sirf basics)
- **Rule:** har concept ka chhota code KHUD likho. Sirf video dekhna kaafi nahi.

## LEVEL 0 done kab? Jab aap:
- numpy mein matrix bana, multiply, transpose kar sako
- "gradient descent error kam karta hai" — ye samajh sako
Phir LEVEL 1 (ML basics) par jao.
