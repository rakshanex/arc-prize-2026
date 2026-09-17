# LEVEL 2.5 — LLMs + Agents (Modern Layer) — Deep, Simple Hindi

Transformers (Level 2) ke baad. Ye aaj ka "practical AI" hai — ChatGPT jaisa.

═══════════════════════════════════════════════════════════════════

## 1. LLM kya hai (Large Language Model)
- Ek bahut bada Transformer, jo internet ke bahut saare text par train hua.
- Kaam ek hi: **"agla shabd predict karo."** Bस itna! Par itne bade scale par ki wo
  baat-cheet, code, reasoning sab kar leta hai.
- Jaise: "India ki rajdhani hai ___" → model "Delhi" predict karta hai.

## 2. Tokenization (shabd → numbers)
- Model text ko "tokens" (chhote tukdon) mein todta hai, phir numbers banata hai
  (kyunki model sirf numbers samajhta hai — Level 0).
- "unbelievable" → ["un", "believ", "able"] jaise tukde.

## 3. Pretraining vs Fine-tuning
- **Pretraining:** internet ke saare text par "agla shabd" seekhna (mahine, crore rupaye,
  hazaaron GPU). Ye base model banta hai.
- **Fine-tuning:** us base ko apne khaas kaam ke liye thoda aur train karna (sasta).
- **LoRA:** fine-tuning ka sasta tarika — poora model nahi, sirf chhote "adapter" train
  karo. (CPU/chhote GPU par bhi possible.)

## 4. Prompting (model se kaam nikalna)
- Aap jo likhte ho (prompt) usse model ka output badalta hai.
- **Few-shot:** prompt mein 2-3 examples do → model pattern pakad leta hai.
- **Chain-of-thought (CoT):** "step by step socho" bolo → model behtar reason karta hai
  (ye Level 3 ke reasoning models ka base).

## 5. RAG (Retrieval-Augmented Generation)
- Problem: LLM ko sab yaad nahi, aur purana data hai.
- **RAG:** sawaal aane par pehle ek database se **relevant info dhoondho**, phir wo info
  model ko do, tab jawaab do. Jaise "open-book exam".
- Isse model latest/sahi facts de sakta hai (hallucination kam).

## 6. AGENTS (LLM + actions)
- Akela LLM sirf text deta hai. **Agent** = LLM + **tools** (calculator, search, code
  run, web).
- Agent decide karta hai: "is kaam ke liye kaunsa tool use karun?" → tool chalao →
  result dekho → agla kadam.
- Yaad hai hamari library file 12 (Apple debate)? Wahi nateeja: **akela LLM kamzor,
  LLM + tools strong.** Agents isi par bane hain.

## 7. Evaluation (model kitna achha, kaise naapein)
- Benchmarks (test sets) par score. Par dhyan: **contamination** (model ne test data
  pehle dekh liya = ratta) se score jhootha ho sakta hai.
- Isliye ARC (library file 03) jaise "naye" benchmarks zaroori hain — jo ratta na maar sake.

═══════════════════════════════════════════════════════════════════
## LEVEL 2.5 checklist
- [ ] LLM = bada transformer jo "agla shabd" predict karta hai
- [ ] tokenization, pretraining vs fine-tuning, LoRA
- [ ] prompting, few-shot, chain-of-thought
- [ ] RAG = "open-book" (bahar se info laao)
- [ ] agent = LLM + tools (actions le sake)
- [ ] evaluation + contamination ka khatra

## Practice (free)
- Hugging Face "LLM Course" (free, best for LLMs)
- Kaggle Learn "Intro to AI Ethics"
- Try: koi open LLM (jaise ek chhota model) Colab par chalao, prompt karo
- Padho: library file 06 (reasoning models), file 12 (AI + tools debate)

## LEVEL 2.5 done kab?
Jab aap samjha sako: "LLM kya karta hai, RAG kyun, agent kya, aur akela LLM vs LLM+tools
ka farak." Phir LEVEL 3 (AGI core reasoning) par — jahan hamara RAKSHANEX kaam hai.

## RAKSHANEX se connection
Hamara safe-reasoning layer kisi bhi LLM/agent ke UPAR lag sakta hai — jab wo sure na
ho, abstain kare (jhooth na bole). Ye "trustworthy agent" banane ka ek building block.
