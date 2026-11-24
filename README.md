# SDA-AIE-113 group projects

The final project of **SDA-AIE-113 · Software Engineering Practices for AI Systems**
(SDAIA Academy). Your group takes a real data-science notebook and, with an AI coding agent,
turns it into a production-style AI service. You do not write code by hand. **You decide, you
check, and you understand.** Understanding the process is full marks.

Workshop site: https://aie113.ibrahimalshehri.sa · [بالعربية](#بالعربية)

## The three tracks

Every track uses real data, and every model explains its answers.

| Track | The model | Open the notebook |
|---|---|---|
| [**Stocks**](tracks/stocks/) | Forecasts tomorrow's closing price of a Saudi stock from real market data, and shows which recent signals drove the forecast. A teaching example, not investment advice. | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/snow10100/aie113-projects/blob/main/tracks/stocks/notebook.ipynb) |
| [**Fraud**](tracks/fraud/) | Flags card transactions that look like fraud, trained on real anonymised bank transactions, and gives the top reasons behind each alert. | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/snow10100/aie113-projects/blob/main/tracks/fraud/notebook.ipynb) |
| [**Vision**](tracks/vision/) | Spots disease on bean leaves in real field photos with a published model, and shows which part of the leaf it looked at. | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/snow10100/aie113-projects/blob/main/tracks/vision/notebook.ipynb) |

Each track's README explains its model in plain words, for people who have never seen machine
learning.

## The journey

**0** Meet your model → **1** Reorganise it (clean architecture) → **2** Put an API in front of it
(FastAPI) → **3** Put it in a container (Docker) → **4** Test it → **5** Automate it (GitHub
Actions) → **6** Handle secrets the modern way → *optional:* a front end with Vite and React.

[**GUIDE.md**](GUIDE.md) explains each stage: the idea, what to ask your agent, how to see for
yourself what it built, and when the stage is done. No code to copy: your agent writes the code,
the guide makes sure you understand it.

## How to start

1. **Form a group** of any size. At least one member needs an AI coding agent backed by a
   frontier model (for example Claude Code, GitHub Copilot in agent mode, Cursor, Codex or
   Gemini CLI).
2. **Pick a track** and run its notebook in Colab, top to bottom.
3. **Make your group's repository**: fork this one (or download it), then ask your agent to keep
   only your track. `AGENTS.md` tells every common coding agent to explain each step to you as
   it works.
4. **Follow [GUIDE.md](GUIDE.md)** stage by stage, and keep [JOURNAL.md](JOURNAL.md): one entry
   per stage.

A first sentence for your agent:

    Read AGENTS.md, GUIDE.md and tracks/<track>/README.md. Explain our model to us in plain words,
    then guide us through Stage 1 one step at a time.

## What you hand in

Your repository, your journal, and a short walkthrough where any member can explain any stage.
Code quality, speed and the front end are not graded.

---

<div dir="rtl" lang="ar">

## بالعربية

المشروع الختامي لورشة **ممارسات هندسة البرمجيات لأنظمة الذكاء الاصطناعي (SDA-AIE-113)** في
أكاديمية سدايا. تبدأ مجموعتك من دفتر (notebook) حقيقي لعالِم بيانات، وتحوّله بمساعدة وكيل
برمجة ذكي إلى خدمة ذكاء اصطناعي بمعايير الإنتاج. لن تكتبوا الكود بأيديكم: **أنتم تقررون،
وتتحققون، وتفهمون.** فهم العملية يعني الدرجة الكاملة.

### المسارات الثلاثة

كل مسار يستخدم بيانات حقيقية، وكل نموذج يشرح إجاباته:

- **الأسهم:** يتوقع سعر إغلاق سهم سعودي في يوم التداول التالي من بيانات سوق حقيقية، ويوضح
  الإشارات التي أثّرت في التوقع. مثال تعليمي وليس نصيحة استثمارية.
- **الاحتيال:** يرصد عمليات البطاقات المشبوهة، مدرَّب على عمليات بنكية حقيقية مجهولة الهوية،
  ويذكر أهم أسباب كل تنبيه.
- **الرؤية الحاسوبية:** يكتشف أمراض أوراق الفاصوليا في صور حقيقية من الحقول بنموذج منشور،
  ويُظهر الجزء الذي نظر إليه النموذج في الورقة.

يشرح ملف README.ar.md في مجلد كل مسار النموذج بكلمات بسيطة لمن لم يتعامل مع تعلم الآلة من قبل.

### الرحلة

**0** تعرّف على نموذجك ← **1** أعد تنظيمه (المعمارية النظيفة) ← **2** ضع أمامه واجهة برمجية
(FastAPI) ← **3** ضعه في حاوية (Docker) ← **4** اختبره ← **5** أتمته (GitHub Actions) ← **6**
تعامل مع الأسرار بالطرق الحديثة ← *اختياري:* واجهة أمامية بـ Vite وReact.

يشرح الدليل [GUIDE.ar.md](GUIDE.ar.md) كل مرحلة: الفكرة، وما تطلبه من وكيلك، وكيف ترى بنفسك
ما بناه، ومتى تنتهي المرحلة. لا يوجد كود للنسخ: الوكيل يكتب الكود، والدليل يضمن أنك تفهمه.

### كيف تبدأ

1. **كوّنوا مجموعة** بأي عدد. يحتاج عضو واحد على الأقل إلى وكيل برمجة ذكي يعمل بنموذج متقدم
   (مثل Claude Code أو GitHub Copilot في وضع الوكيل أو Cursor أو Codex أو Gemini CLI).
2. **اختاروا مسارًا** وشغّلوا دفتره في Colab من أوله إلى آخره (روابط Colab في الجدول أعلاه).
3. **أنشئوا مستودع المجموعة**: انسخوا هذا المستودع (Fork) أو نزّلوه، ثم اطلبوا من الوكيل
   الإبقاء على مساركم فقط. الملف AGENTS.md يطلب من وكلاء البرمجة الشائعين شرح كل خطوة لكم.
4. **اتبعوا الدليل** مرحلة بمرحلة، واكتبوا سجل المشروع JOURNAL.md: مدخل واحد لكل مرحلة.

جملة أولى لوكيلكم:

</div>

    Read AGENTS.md, GUIDE.ar.md and tracks/<track>/README.ar.md. Explain our model to us in plain
    words, then guide us through Stage 1 one step at a time. Reply in Arabic.

<div dir="rtl" lang="ar">

### ما تسلّمونه

مستودعكم، وسجل المشروع، وعرض قصير يستطيع فيه أي عضو شرح أي مرحلة. جودة الكود والسرعة
والواجهة الأمامية لا تدخل في التقييم.

</div>

---

## Raqib · تطبيق المجموعة لمسار الاحتيال

[شرح المشروع وطريقة عرضه](PROJECT.ar.md) · [سجل المراحل والتحقق](JOURNAL.md)

[منصة أكاديمية سدايا «أذكى X»](https://athkax.sdaia.gov.sa/) · [صفحة الدورة](https://aie113.ibrahimalshehri.sa/ar/)
