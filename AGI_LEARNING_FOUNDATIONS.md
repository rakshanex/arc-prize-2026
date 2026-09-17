# AGI Learning Foundations — "Kya-Kya Seekhna Zaroori Hai" (simple Hindi)

Ye ek COMPLETE learning reference hai — basics se AGI-frontier tak. Har topic ke saath:
kya hai, kyun zaroori, aur hamari library ka kaunsa file (01-12) usse jodta hai.

═══════════════════════════════════════════════════════════════════

## LEVEL 0 — Prerequisites (bina ye ke aage kuch nahi)
1. **Python programming** — AI ki main bhaasha. Variables, loops, functions, numpy.
   *Kyun:* har AI experiment Python mein hota hai.
2. **Math:**
   - **Linear Algebra** (vectors, matrices) — neural nets isi par bane hain
   - **Probability & Statistics** — AI "guess" karta hai, sab probability hai
   - **Calculus basics** (derivatives) — models "seekhte" kaise hain (gradient descent)
   *Kyun:* ye AI ki "physics" hai — bina samjhe sab magic lagega.

## LEVEL 1 — Machine Learning basics
3. **ML kya hai:** data se pattern seekhna (na ki rules hardcode karna).
4. **Core concepts:** training/test split, **overfitting** (ratta maarna vs samajhna),
   validation, features, loss function.
   *Kyun:* ye har AI system ka base. Overfitting = AGI ka core problem (file 11).
5. **Basic algorithms:** linear/logistic regression, decision trees, k-NN.

## LEVEL 2 — Deep Learning (aaj ke AI ka engine)
6. **Neural networks:** neurons, layers, weights, activation. Gradient descent se seekhna.
7. **Architectures:** CNN (images), RNN (sequences).
8. **⭐ TRANSFORMERS** — "Attention Is All You Need". GPT/Gemini/Claude sab isi par.
   *Library: file 01 (Foundations).* Ye SABSE zaroori modern concept hai.
9. **Scaling laws:** bada model + zyada data = zyada smart (par limit hai — file 02).

## LEVEL 2.5 — Modern LLM layer (2026 roadmaps se — ye ab zaroori hai)
9b. **LLMs kaise kaam karte hain** — tokenization, pretraining, next-token prediction.
9c. **Fine-tuning + LoRA** — model ko apne task ke liye adjust karna (sasta tarika).
9d. **RAG (Retrieval-Augmented Generation)** — model ko bahar se knowledge dena.
9e. **Agents + tool use** — LLM ko actions/tools dena (ye reasoning-era ka core, file 12).
9f. **Prompting + evaluation** — model se kaam nikalna aur uska output naapna.
    *Kyun:* aaj ke reasoning models (o1, R1 — file 06) inhi cheezon par bane hain.

## LEVEL 3 — AGI ka core: Reasoning & Generalization
10. **Generalization:** naye problems solve karna (jo train mein nahi the).
    *Library: file 03 (ARC-AGI).* Ye AGI ka SABSE bada unsolved problem hai.
11. **Reasoning models:** RL + chain-of-thought se "sochna" sikhaana (DeepSeek-R1, o1).
    *Library: file 06.*
12. **Memorization vs Generalization gap** — AI ratta maarta hai, sach mein samajhta nahi.
    *Library: file 12 (Apple debate).* Ye samajhna AGI ke liye critical.

## LEVEL 4 — AGI ke raaste (approaches)
13. **Program synthesis / DSL** — AI khud "program" likhe problem solve karne ko.
14. **Neuro-symbolic** — neural learning + logic reasoning jodna. *Library: file 08.*
15. **World models** — AI apne andar duniya ka model banaye, imagine karke plan kare. *File 08.*
16. **Agents & embodiment** — AI jo duniya mein ACT kare (tools, robots). *File 04, 09.*
17. **Self-improvement (RSI)** — AI khud ko behtar banaye. *File 07.*
18. **Continual learning** — bina bhoole naya seekhna. *File 11.*

## LEVEL 5 — AGI ko SAFE & samajhne layak banana
19. **AI Safety / Alignment** — smart AI ko human values ke saath rakhna. *File 05.*
20. **Interpretability** — AI ke andar dekhna, wo kaise decide karta hai. *File 10.*
21. **Abstention / calibration** — AI ka "mujhe nahi pata" kehna (hamara RAKSHANEX kaam!).
    *Library: file 12 + RAKSHANEX papers.*
22. **Evaluation** — AI kitna smart hai, theek se naapna. *File 11.*

═══════════════════════════════════════════════════════════════════

## SEEKHNE KA ORDER (roz 1 ghanta — 10_YEAR_AGI_PLAN.md dekho)
Level 0 → 1 → 2 (Year 1-2, Kaggle Learn + fast.ai)
Level 3 → 4 → 5 (Year 3+, papers padhna + experiments)

## HAMARE APNE KAAM SE CONNECTION (RAKSHANEX)
- Humne Level 3 (reasoning/ARC) + Level 5 (abstention/safety) par kaam kiya
- Hamara contribution: "AI jo jhooth nahi bolta" = Level 5 ka #21 (abstention)
- Ye ek chhota par real AGI-brick hai — 6 domains par verified

## SABSE ZAROORI SEEKH (ek line)
> AGI = generalization (Level 3) + safety (Level 5), aur ye dono abhi UNSOLVED hain.
> Jo inme se kisi ek par bhi thoda contribute kare, wo AGI research kar raha hai.

## HONEST NOTE
Ye poora seekhne mein saal lagenge (10_YEAR_AGI_PLAN.md realistic hai). Par har level
apne aap mein useful skill deta hai (job, projects, samajh). AGI "solve" karna guarantee
nahi — par ek genuine researcher banna achievable hai.

═══════════════════════════════════════════════════════════════════

## RESEARCHER KAISE KAAM KARTA HAI (2026 expert roadmaps se — verified)
Ek AI researcher ka time roughly aise bantta hai:
- **40% padhna + sochna** (papers, ideas)
- **30% experiment + debugging** (code, test)
- **20% likhna** (results, papers, notes)
- **10% baaki**
→ Isliye hamara "40 min padho + 20 min code" daily rhythm sahi disha mein hai.
→ Sabse zaroori mindset: "ye kaam kyun karta hai?" ye poochne wala banna.

## VALIDATION (web research, 2026)
Duniya ke expert roadmaps (Stanford/MIT/DeepLearning.AI-based, AssemblyAI, DataCamp)
sab yahi order kehte hain: **Math+Python → core ML → deep learning → Transformers →
LLMs/agents → specialize**. Hamara plan isse match karta hai. Free courses: sab
Stanford/MIT/Google ke free-to-audit hain (Coursera, MIT OCW, fast.ai, Kaggle Learn).

## KEY PRINCIPLE (sab experts agree)
> "Theory + prerequisites (math/Python) + REAL PROJECTS (portfolio) — teeno chahiye.
>  Sirf theory ya sirf no-code tools se researcher nahi bante. Karke + share karke seekho."
(Hamne yahi kiya — RAKSHANEX ek real project + public portfolio hai.)
