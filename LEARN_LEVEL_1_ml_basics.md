# LEVEL 1 — Machine Learning Basics — Deep, Simple Hindi

Level 0 (Python+math) ke baad ye. Yahan aap samjhoge ki AI "seekhta" kaise hai.

═══════════════════════════════════════════════════════════════════

## 1. ML kya hai (dobara, gehrai se)
- **Normal programming:** insaan RULES likhta hai. ("agar temp>30 to garmi")
- **Machine Learning:** insaan EXAMPLES deta hai, computer khud RULE seekhta hai.
> Jab rules likhna mushkil ho (jaise "billi ki photo pehchano" — kaise likhoge?),
> tab ML use karte hain: 10,000 billi/kutte ki photos do, wo khud seekh leta hai.

## 2. Teen tarah ki ML
1. **Supervised** (sabse common): data + sahi jawaab (label) do. Jaise emails + "spam/not".
2. **Unsupervised:** sirf data, koi label nahi. Computer khud groups dhoondhta hai.
3. **Reinforcement (RL):** trial-and-error se seekhna (inaam/saza). Jaise game khelना.
   (Reasoning models jaise DeepSeek-R1 RL use karte hain — Level 3.)

## 3. Core concepts (ye SABSE zaroori hain)

### a) Features aur Labels
- **Features (X):** input (jaise email ke shabd).
- **Label (y):** sahi jawaab (spam=1, not=0).
- Model seekhta hai: X → y ka rishta.

### b) Training / Test split (bahut zaroori)
- Data ko do hisse karo: **train** (seekhne ke liye) + **test** (jaanchne ke liye).
- Test data model ne kabhi nahi dekha — isse pata chalta hai wo SACH mein seekha ya
  ratta maara.

### c) OVERFITTING (⭐ ML aur AGI ka SABSE important concept)
- **Overfitting = ratta maarna.** Model train data ko YAAD kar leta hai, par naye data
  par fail hota hai.
- Jaise ek student jisne answers ratta maar liye — same paper mein 100%, naye paper mein 0.
- **Ulta = generalization** (sach mein samajhna, naye par bhi kaam karna).
> Ye poore AGI ka core problem hai (hamari library file 03, 12): AI ratta maarta hai,
> generalize nahi karta. ARC benchmark isi ko test karta hai.

### d) Loss (galti ka maap) + Gradient Descent (seekhne ka tarika)
- **Loss:** model kitna galat hai (ek number). Jitna kam, utna achha.
- **Gradient descent:** loss ki slope dekho, us ulti disha mein weights thoda badlo,
  loss kam karo. Baar-baar. (Level 0 ka calculus yahan use hota hai.)

## 4. Basic algorithms (naam se daro mat)
- **Linear Regression:** ek seedhi line fit karna (jaise ghar ka size → keemat).
- **Logistic Regression:** haan/naa classify karna (spam/not).
- **Decision Tree:** haan/naa sawaalon ka ped ("umar>30? haan→..., naa→...").
- **k-NN:** "jo mere sabse paas hai, main bhi wahi hoon."

═══════════════════════════════════════════════════════════════════
## 5. CHHOTA CHALNE WALA EXAMPLE (KHUD chalao!)
Ek mini ML: data se ek line seekhna (linear regression, scratch se, numpy).
```python
import numpy as np

# DATA: ghar ka size (X) -> keemat (y). Rule (chhupa): keemat = 3*size + 2
X = np.array([1, 2, 3, 4, 5], dtype=float)
y = np.array([5, 8, 11, 14, 17], dtype=float)   # = 3*X + 2

# MODEL: keemat = w*size + b. w,b seekhne hain (random se shuru)
w, b = 0.0, 0.0
lr = 0.01                       # learning rate (kitna bada step)

for step in range(1000):        # training loop
    pred = w * X + b            # abhi ka guess
    error = pred - y            # kitna galat
    # gradient descent: loss kam karne ki disha mein w,b badlo
    w -= lr * (2 * (error * X).mean())
    b -= lr * (2 * error.mean())

print(f"Seekha: keemat = {w:.2f}*size + {b:.2f}")   # ~3.00*size + 2.00
print("Prediction for size=6:", w*6 + b)            # ~20 (sahi!)
```
> Ye ASLI ML hai — model ne bina rule bataye, data se "3*size+2" khud seekh liya
> (gradient descent se). Yahi principle bade neural nets mein bhi hai, bस bada.

═══════════════════════════════════════════════════════════════════
## 6. LEVEL 1 checklist
- [ ] supervised/unsupervised/RL ka farak
- [ ] features vs labels, train/test split
- [ ] **overfitting = ratta maarna** (aur ye AGI ka core problem hai)
- [ ] loss = galti, gradient descent = seekhne ka tarika
- [ ] upar wala code KHUD chalaya + samjha

## Practice (free)
- Kaggle Learn: "Intro to Machine Learning" + "Intermediate Machine Learning"
  (yahi overfitting/validation deeply sikhata hai, aapke account par)

## LEVEL 1 done kab?
Jab aap upar wala regression code khud likh/samajh sako, aur "overfitting kya hai +
kyun bura hai" simple mein samjha sako. Phir LEVEL 2 (Deep Learning) par jao.

## RAKSHANEX se connection
Hamara ARC solver bhi "train examples se rule seekhna" hai (rule induction) — ek
tarah ki ML. Aur hamara 0-hallucination kaam overfitting/generalization ke gap ko
address karta hai (jab model sure nahi, abstain kare).
