# LEVEL 2 — Deep Learning + Transformers — Deep, Simple Hindi

Level 1 (ML basics) ke baad. Yahan aap samjhoge aaj ke AI (ChatGPT/Gemini) ka engine.

═══════════════════════════════════════════════════════════════════
# PART A — NEURAL NETWORKS (dimaag ki nakal)
═══════════════════════════════════════════════════════════════════

## 1. Neuron (ek chhota decision-maker)
- Ek neuron: kuch numbers (inputs) leta hai, har ko ek **weight** se multiply karta hai,
  jodta hai, aur ek "activation" se guzaarta hai → ek output.
- Formula: `output = activation(w1*x1 + w2*x2 + ... + b)`
- Ye Level 1 ke linear regression jaisa hi hai, bस activation add hai.

## 2. Layers + Network
- Bahut saare neurons ki ek **layer**. Kai layers = **deep** network (isliye "deep learning").
- Input layer → hidden layers → output layer.
- Har layer pichhli se numbers leta hai, transform karta hai, aage bhejta hai.

## 3. Activation (non-linearity — ye zaroori hai)
- Bina activation, network sirf ek badi line hoti (kuch khaas nahi seekh pati).
- **ReLU** (sabse common): `max(0, x)` — negative ko 0 karo, positive rehne do.
- Isse network "tedhi-medhi" (complex) cheezein seekh sakta hai.

## 4. Backpropagation (kaise seekhta hai)
- Same idea jaise Level 1: **loss ki slope dekho, weights ko us disha mein badlo** jisse
  loss kam ho. Bस ab ye pooре network mein "peeche ki taraf" hota hai (backprop).
- Gradient descent + backprop = deep learning ka dil.

## 5. Types (kaunsa data ke liye)
- **CNN** (Convolutional) — images ke liye (ARC grids bhi!). Local patterns dekhta hai.
- **RNN** — sequences ke liye (text, time). Ek-ek karke padhta hai. (Ab purana.)
- **Transformer** — aaj ka king (neeche).

═══════════════════════════════════════════════════════════════════
# PART B — TRANSFORMERS (⭐ aaj ke AI ka base)
═══════════════════════════════════════════════════════════════════

## 6. Problem jise Transformer ne solve kiya
- RNN text ko ek-ek shabd padhta tha (slow, aur door ke shabd bhool jaata tha).
- 2017 "Attention Is All You Need" (hamari library file 01) ne Transformer diya.

## 7. ATTENTION (core idea — simple mein)
- Har shabd baaki SAARE shabdon ko "dekhta" hai aur decide karta hai kaunsa kitna
  zaroori hai (kis par "dhyan/attention" dena).
- Jaise "wo bank gaya" mein "bank" — nadi ka kinara ya paisa-wala bank? Aas-paas ke
  shabd (attention) se decide hota hai.
- Isse model poore vaakya ka context ek saath samajhta hai (RNN se behtar + tez).

## 8. Kyun itna powerful
- **Parallel** (sab shabd ek saath) → GPU par tez → bade models train ho sakte.
- **Long-range** → door ke shabd bhi jode.
- GPT, Gemini, Claude, DeepSeek — SAB transformer par bane hain. Scale badhaao
  (Level 0 ka "scaling laws") → aur smart.

## 9. Chhota code — ek mini neural network (numpy, KHUD chalao)
```python
import numpy as np
np.random.seed(0)

# TASK: XOR seekhna (0,0->0; 0,1->1; 1,0->1; 1,1->0). Ek line se solve NAHI hota,
# isliye hidden layer + activation chahiye (yahi "deep" ka point).
X = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=float)
y = np.array([[0],[1],[1],[0]], dtype=float)

def sigmoid(z): return 1/(1+np.exp(-z))
def dsig(z): return sigmoid(z)*(1-sigmoid(z))

# 2 inputs -> 4 hidden -> 1 output (random weights)
W1=np.random.randn(2,4); b1=np.zeros((1,4))
W2=np.random.randn(4,1); b2=np.zeros((1,1))
lr=0.5
for epoch in range(5000):
    # forward (guess)
    z1=X@W1+b1; a1=sigmoid(z1)
    z2=a1@W2+b2; a2=sigmoid(z2)
    # backward (seekho: error ki disha mein weights badlo)
    d2=(a2-y)*dsig(z2)
    d1=(d2@W2.T)*dsig(z1)
    W2-=lr*a1.T@d2; b2-=lr*d2.sum(0,keepdims=True)
    W1-=lr*X.T@d1; b1-=lr*d1.sum(0,keepdims=True)
preds=sigmoid(sigmoid(X@W1+b1)@W2+b2)
print("XOR predictions (goal 0,1,1,0):", preds.round(2).ravel())
```
> Ye ek asli neural network hai jo XOR seekhta hai — jo simple linear model NAHI kar
> sakta. Hidden layer + activation isi liye chahiye. Bade nets bस isi ka scaled version.

═══════════════════════════════════════════════════════════════════
## LEVEL 2 checklist
- [ ] neuron = weighted sum + activation
- [ ] layers/deep, ReLU kyun chahiye
- [ ] backprop = gradient descent poore network mein
- [ ] CNN=images, Transformer=text/sab
- [ ] **attention** = har shabd baaki shabdon par dhyan deta hai
- [ ] XOR code KHUD chalaya

## Practice (free)
- Kaggle Learn: "Intro to Deep Learning" + "Computer Vision"
- fast.ai (Practical Deep Learning — best free hands-on course)
- 3Blue1Brown "Neural Networks" playlist (visual)
- Padho: "Attention Is All You Need" (library file 01) — pehle Wikipedia summary

## LEVEL 2 done kab?
Jab aap XOR network samajh/chala sako, aur "attention" ka idea simple mein samjha sako.
Phir LEVEL 2.5 (LLMs/agents) par.
