# 🧠 AgentCore — Intelligent Agent Orchestration Engine

> Built as a portfolio project inspired by enterprise AI agent platforms. AgentCore demonstrates how natural language input can be intelligently parsed, classified, routed to specialized agents, and summarized using a local LLM — all without a single paid API.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![spaCy](https://img.shields.io/badge/NLP-spaCy-09A3D5)
![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E)
![Ollama](https://img.shields.io/badge/LLM-Mistral%20(local)-8A2BE2)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📌 What is AgentCore?

AgentCore is a **mini intelligent agent orchestration engine** — a simplified version of the core intelligence layer behind enterprise AI platforms like those built by modern agent-marketplace companies.

You type a natural language request. AgentCore:
1. **Understands** it using NLP
2. **Classifies** it using a trained ML model
3. **Routes** it to the correct specialized agent
4. **Executes** a multi-step workflow
5. **Summarizes** the result using a local LLM

All running **100% locally**. No paid APIs. No cloud dependency.

---

## 🎯 Why I Built This

Enterprise AI platforms in 2026 are solving a hard problem:
> *"Given any business request in plain English, how do you automatically decide which agent, tool, or workflow should handle it?"*

That routing and orchestration intelligence is the core ML challenge. This project is my attempt to understand and rebuild that from scratch.

---

## 🏗️ System Architecture

```mermaid
graph TB
    User["👤 User Input (Natural Language)"]

    subgraph NLP ["🔍 NLP Layer (spaCy)"]
        E1[Entity Extraction]
        E2[Intent Detection]
        E3[Priority Classification]
    end

    subgraph ML ["🤖 ML Router (scikit-learn)"]
        M1[TF-IDF Vectorizer]
        M2[Logistic Regression Classifier]
        M3[Confidence Scoring]
    end

    subgraph Agents ["⚡ Agent Engine"]
        A1[👤 HR Agent]
        A2[💰 Finance Agent]
        A3[🖥️ IT Agent]
        A4[📈 Sales Agent]
        A5[🏭 Operations Agent]
    end

    subgraph LLM ["🧠 LLM Layer (Mistral)"]
        L1[Prompt Engineering]
        L2[Natural Language Response]
    end

    UI["🖥️ Streamlit Dashboard"]

    User --> NLP
    NLP --> ML
    ML --> Agents
    Agents --> LLM
    LLM --> UI
    UI --> User
```

---

## 🔄 Data Flow Diagram

### Level 0 — Context Diagram

```mermaid
graph LR
    User((👤 User)) -->|Natural Language Task| AgentCore[🧠 AgentCore System]
    AgentCore -->|Structured Result + AI Summary| User
```

---

### Level 1 — System DFD

```mermaid
graph TD
    U((User)) -->|Raw Text| P1[1.0 NLP Processing]
    P1 -->|Extracted Entities + Intent| DS1[(Entity Store)]
    P1 -->|Structured Task Data| P2[2.0 ML Routing]
    DS1 --> P2
    P2 -->|Agent Label + Confidence| DS2[(Routing Log)]
    P2 -->|Routing Decision| P3[3.0 Agent Dispatch]
    P3 -->|Workflow Steps + Output| DS3[(Execution Log)]
    P3 -->|Agent Result| P4[4.0 LLM Summarization]
    DS2 --> P3
    P4 -->|Natural Language Summary| P5[5.0 Dashboard Render]
    DS3 --> P4
    P5 -->|Visual Output| U
```

---

### Level 2 — ML Router Detail

```mermaid
graph TD
    Input[Raw Text Input] --> TF[TF-IDF Vectorizer ngram 1,2 max features 5000]
    TF --> LR[Logistic Regression max iter 1000]
    LR --> Prob[Probability Distribution across all 5 agents]
    Prob --> Max[Argmax Predicted Agent]
    Prob --> Conf[Confidence Score]
    Max --> Output[Routing Decision]
    Conf --> Output
```

---

## 🔁 Request Lifecycle Flowchart

```mermaid
flowchart TD
    Start([User submits task]) --> NLP[spaCy NLP Extraction]
    NLP --> Entities{Entities found?}
    Entities -->|Yes| EnrichML[Pass entities + text to ML Router]
    Entities -->|No| RawML[Pass raw text to ML Router]
    EnrichML --> ML[TF-IDF + Logistic Regression]
    RawML --> ML
    ML --> Conf{Confidence > 20%?}
    Conf -->|Yes| Dispatch[Dispatch to Predicted Agent]
    Conf -->|No| Fallback[Return unknown agent error]
    Dispatch --> HR{HR Agent?}
    Dispatch --> FIN{Finance Agent?}
    Dispatch --> IT{IT Agent?}
    Dispatch --> SALES{Sales Agent?}
    Dispatch --> OPS{Operations Agent?}
    HR -->|Execute| Steps[Run workflow steps]
    FIN -->|Execute| Steps
    IT -->|Execute| Steps
    SALES -->|Execute| Steps
    OPS -->|Execute| Steps
    Steps --> LLM[Send to Mistral LLM]
    LLM --> Summary[Generate natural language summary]
    Summary --> UI[Render on Streamlit Dashboard]
    UI --> End([User sees result])
    Fallback --> End
```

---

## 🧩 Component Breakdown

```mermaid
graph LR
    subgraph nlp [app/nlp]
        extractor.py
    end
    subgraph ml [app/ml]
        router.py
    end
    subgraph agents [app/agents]
        base_agent.py
        hr_agent.py
        finance_agent.py
        it_agent.py
        sales_agent.py
        operations_agent.py
        dispatcher.py
    end
    subgraph core [app]
        llm.py
        dashboard.py
    end
    subgraph data [data]
        training_data.py
    end

    extractor.py -->|structured task data| router.py
    router.py -->|routing decision| dispatcher.py
    dispatcher.py --> hr_agent.py
    dispatcher.py --> finance_agent.py
    dispatcher.py --> it_agent.py
    dispatcher.py --> sales_agent.py
    dispatcher.py --> operations_agent.py
    hr_agent.py -->|result| llm.py
    finance_agent.py -->|result| llm.py
    it_agent.py -->|result| llm.py
    sales_agent.py -->|result| llm.py
    operations_agent.py -->|result| llm.py
    llm.py -->|summary| dashboard.py
    training_data.py -->|fit| router.py
```

---

## 🛠️ Tech Stack & Reasoning

| Layer | Technology | Why This Specifically |
|---|---|---|
| NLP | spaCy en_core_web_sm | Industry standard for production NLP. Faster than NLTK, more lightweight than full transformers. Named entity recognition out of the box. |
| ML Classifier | scikit-learn LogisticRegression | Interpretable, fast to train, works well on small datasets. TF-IDF + LogReg is a proven baseline for text classification. |
| Vectorizer | TF-IDF ngram 1,2 | Captures both single words and two-word phrases which are critical for intent disambiguation. |
| LLM | Mistral 7B via Ollama | Runs 100% locally. No API costs, no data privacy concerns, no rate limits. Mistral 7B is excellent for instruction-following tasks. |
| Backend | FastAPI | Async, modern, production-grade Python API framework used widely in ML serving pipelines. |
| Frontend | Streamlit | Purpose-built for ML/data apps. Lets DS/ML engineers build clean UIs without frontend expertise. |
| Database | SQLite | Zero-setup embedded database. Perfect for local agent execution logs. |
| Language | Python 3.13 | Universal language for ML/AI. Entire stack speaks Python natively. |

---

## 📁 Project Structure

```
AgentCore/
├── app/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── hr_agent.py
│   │   ├── finance_agent.py
│   │   ├── it_agent.py
│   │   ├── sales_agent.py
│   │   ├── operations_agent.py
│   │   └── dispatcher.py
│   ├── ml/
│   │   └── router.py
│   ├── nlp/
│   │   └── extractor.py
│   ├── llm.py
│   └── dashboard.py
├── data/
│   └── training_data.py
├── models/
├── notebooks/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed

### Installation

```bash
git clone https://github.com/SGarryy/AgentCore.git
cd AgentCore
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
ollama pull mistral
```

### Run

```bash
streamlit run app/dashboard.py
```

Open `http://localhost:8501` in your browser.

---

## 💡 Example Tasks

| Input | Agent Triggered | What Happens |
|---|---|---|
| Onboard new employee Sarah to HR on Monday | HR Agent | Creates profile, sets start date, sends welcome email |
| Reconcile duplicate invoices from last month | Finance Agent | Scans invoices, flags duplicates, generates report |
| Triage bug on login page crashing on mobile | IT Agent | Creates ticket, assigns severity, notifies engineer |
| Generate leads from retail sector urgently | Sales Agent | Scores leads, identifies top prospect, updates CRM |
| Schedule vendor meeting for procurement | Operations Agent | Creates PO, contacts vendor, notifies ops team |

---

## 🧠 ML Model Performance

- **Algorithm:** Logistic Regression with TF-IDF features
- **Training samples:** 50 (10 per agent class)
- **Features:** Unigrams + Bigrams (max 5000)
- **Test accuracy:** ~62% on held-out set
- **Note:** Accuracy improves significantly with more training data. 50 samples is intentionally minimal to demonstrate the architecture.

---

## 🔮 Future Improvements

- [ ] Add SQLite logging for all agent executions
- [ ] Train on larger dataset for higher accuracy
- [ ] Add feedback loop — user rates responses, model retrains
- [ ] Plug in real APIs (Gmail, Jira, Slack) via tool-use
- [ ] Replace LogReg with fine-tuned BERT for better intent classification
- [ ] Add multi-agent chaining (one task triggers multiple agents)
- [ ] REST API via FastAPI for external integrations

---

## 👨‍💻 Author

Built as a targeted portfolio project demonstrating NLP pipeline design, ML text classification, agent orchestration patterns, local LLM integration, and full-stack ML application development.

---

## 📄 License

MIT License — free to use, modify, and distribute.