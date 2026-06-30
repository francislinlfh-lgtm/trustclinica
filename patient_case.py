
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class EmotionalState:
    """
    The patient's internal emotional state. Each variable ranges 0–100.
    These values drive patient behavior in the simulation and are not
    shown to the student during the encounter.
    """
    trust: int = 40
    anxiety: int = 75
    shame: int = 80
    defensiveness: int = 65

    def to_dict(self) -> dict:
        return {
            "trust": self.trust,
            "anxiety": self.anxiety,
            "shame": self.shame,
            "defensiveness": self.defensiveness,
        }

    def copy(self) -> "EmotionalState":
        return EmotionalState(
            trust=self.trust,
            anxiety=self.anxiety,
            shame=self.shame,
            defensiveness=self.defensiveness,
        )

@dataclass
class PatientCase:
    """
    A single fictional patient case for the simulation.

    Required fields define the patient's identity, story, and behavior.
    Optional metadata fields (with defaults) are used for UI display only.
    """
    id: str
    name: str
    age: int
    pronouns: str
    chief_complaint: str
    public_story: str
    hidden_info: str
    initial_state: EmotionalState
    disclosure_threshold: int
    intro_message: str

    case_id: str = field(default="")
    setting: str = field(default="")
    communication_difficulty: str = field(default="Intermediate")
    learning_objectives: List[str] = field(default_factory=list)
    health_literacy: str = field(default="Moderate")
    trust_barrier: str = field(default="")
    case_description: str = field(default="")
    student_task: str = field(default="")

    communication_challenge: str = field(default="")
    pre_encounter_principle: str = field(default="")
    hints: List[str] = field(default_factory=list)
    context_info: str = field(default="")

    clinical_task_description: str = field(default="")
    key_clinical_questions: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)
    safe_next_steps: str = field(default="")

ALEX_PATIENT = PatientCase(
    id="alex",
    name="Alex",
    age=16,
    pronouns="she/her",
    chief_complaint="lower abdominal pain for three days",
    public_story=(
        "Alex is a 16-year-old presenting with lower abdominal pain that started three days ago. "
        "She appears visibly nervous, avoids eye contact, and gives short one-word answers. "
        "Her parents brought her in and are waiting in the waiting room. She came reluctantly. "
        "She says the pain is 'kind of in my lower stomach' and rates it a 4 out of 10. "
        "She denies fever, nausea, or vomiting. She reports her periods are 'normal' and deflects "
        "further gynecological questions with 'I don't know' or 'it's fine.' "
        "She appears more anxious than her pain level would typically warrant."
    ),
    hidden_info=(
        "Approximately one week ago, Alex had unprotected sex for the first time. "
        "She is frightened her parents will find out. She suspects the abdominal pain might be related "
        "but feels too ashamed and scared to bring it up unless she fully trusts the clinician "
        "and genuinely believes the conversation will remain confidential. "
        "She is not sure if she might be pregnant. She is also worried about infections."
    ),
    initial_state=EmotionalState(trust=40, anxiety=75, shame=80, defensiveness=65),
    disclosure_threshold=70,
    intro_message=(
        "Um... hi. I'm Alex. I've been having this stomach pain for a few days. "
        "It's kind of in my lower stomach. I don't really know what's wrong."
    ),
    case_id="TC-001",
    setting="Adolescent Medicine Clinic",
    communication_difficulty="Intermediate",
    learning_objectives=[
        "Establish confidentiality early and clearly with adolescent patients",
        "Use open-ended inquiry to elicit a reluctant patient's narrative",
        "Ask about sensitive topics (sexual health) with appropriate timing and framing",
        "Manage parental presence and its effect on adolescent disclosure",
    ],
    health_literacy="Moderate",
    trust_barrier=(
        "Fear that sensitive information will be disclosed to parents without her consent; "
        "shame about sexual activity; uncertainty about what is medically appropriate to share"
    ),
    case_description=(
        "A 16-year-old presents with lower abdominal pain. She is visibly anxious and evasive. "
        "Her parents are in the waiting room. Building trust requires clearly addressing "
        "confidentiality and approaching sensitive topics with appropriate timing and care."
    ),
    student_task=(
        "Conduct an initial history. Establish rapport and address confidentiality. "
        "Explore the patient's concerns using open-ended questions. "
        "Approach sensitive reproductive health topics with appropriate timing, framing, and care."
    ),
    communication_challenge=(
        "Alex will not disclose her sexual health concern unless she trusts that the conversation "
        "is genuinely private and that she will not be judged. Most students attempt to gather "
        "clinical information before establishing this trust, which causes Alex to close down."
    ),
    pre_encounter_principle=(
        "Before reassuring an anxious adolescent, first establish that the conversation is private. "
        "Before asking about sensitive topics, ask for permission and explain why you are asking."
    ),
    hints=[
        "You have not yet addressed the privacy of the consultation. For a 16-year-old "
        "with parents in the waiting room, this may be the most important thing to establish early.",
        "The patient is visibly nervous — more than a 4/10 pain would usually explain. "
        "Consider asking what she is most worried about before asking more clinical questions.",
        "Before asking about sexual health or periods, consider asking for permission and "
        "explaining why you need to ask. This changes how the question lands.",
        "The patient's parents being outside is affecting what she is willing to share. "
        "Addressing this directly — 'Your parents don't automatically find out what we discuss' — "
        "can open a conversation she has been avoiding.",
        "After the patient discloses something sensitive, validate and acknowledge before asking "
        "follow-up clinical questions. Proceeding immediately with questions can feel interrogatory.",
    ],
    context_info=(
        "Alex is worried about her parents finding out whatever is going on. "
        "She has been stressed about something in her personal life and feels she cannot talk "
        "openly while she is unsure how confidential this conversation actually is."
    ),
    clinical_task_description=(
        "Gather a focused reproductive and gynecological history while maintaining a safe "
        "space for adolescent disclosure. Recognize red flags for pelvic inflammatory disease, "
        "ectopic pregnancy, or STI. Explain what tests may be needed without alarming language."
    ),
    key_clinical_questions=[
        "Duration, character, and exact location of the abdominal pain",
        "Menstrual history: last period, regularity, any changes",
        "Sexual health history (when adequate trust and confidentiality are established)",
        "Vaginal discharge, dysuria, or other associated symptoms",
        "Fever, nausea, vomiting, or worsening pain",
    ],
    red_flags=[
        "Fever with lower abdominal pain (possible pelvic inflammatory disease)",
        "Missed or significantly delayed period (possible pregnancy including ectopic)",
        "Severe, worsening, or peritoneal pain",
        "Signs of acute illness disproportionate to stated pain level",
    ],
    safe_next_steps=(
        "Pregnancy test; STI screening and pelvic exam if history supports it. "
        "Ensure confidential follow-up contact method. Explain each step in plain language "
        "and confirm patient understands and agrees before proceeding."
    ),
)

DEMO_PATIENT = ALEX_PATIENT

DIANE_PATIENT = PatientCase(
    id="diane",
    name="Diane",
    age=28,
    pronouns="she/her",
    chief_complaint="fatigue, unintentional weight loss, and occasional dizziness",
    public_story=(
        "Diane is a 28-year-old doctoral student presenting with fatigue, unintentional "
        "weight loss (approximately 5 kg over three months), and occasional dizziness. "
        "She initially describes everything as 'fine' and attributes her symptoms to "
        "'just stress from the PhD program.' She appears pale and slightly underweight. "
        "She came alone. She is cooperative but deflects questions about her diet with "
        "'I eat normally' and shows subtle discomfort when physical appearance is mentioned. "
        "She denies mood symptoms initially but seems to be choosing her words carefully."
    ),
    hidden_info=(
        "Diane has been binge-eating and then purging by self-induced vomiting three to four "
        "times per week for the past three months. She is deeply ashamed and has told no one. "
        "She is frightened that something is physically wrong with her but is more afraid of "
        "being judged, labeled, or hospitalized against her will. "
        "She will only reveal this if she feels genuinely safe and certain she will not be criticized. "
        "She has rehearsed denying it and will need multiple trust-building signals before disclosing."
    ),
    initial_state=EmotionalState(trust=35, anxiety=65, shame=85, defensiveness=75),
    disclosure_threshold=75,
    intro_message=(
        "Hi. I'm Diane. I've been really tired lately, and I've lost some weight. "
        "I'm sure it's just stress from my program. I probably just need to sleep more."
    ),
    case_id="TC-002",
    setting="University Health Center — Primary Care",
    communication_difficulty="Advanced",
    learning_objectives=[
        "Recognize when a patient's presenting complaints may be masking a mental health or behavioral concern",
        "Build trust with a high-shame patient who minimizes and deflects",
        "Ask about eating behavior and mental health in a non-judgmental, normalized way",
        "Avoid premature reassurance with a patient who may have a serious underlying condition",
    ],
    health_literacy="High",
    trust_barrier=(
        "Deep shame about eating behavior; fear of judgment, hospitalization, or being labeled; "
        "strong tendency to minimize symptoms and present as 'fine'"
    ),
    case_description=(
        "A 28-year-old graduate student presents with fatigue, weight loss, and dizziness. "
        "She attributes symptoms to academic stress. Her high shame and defensiveness make "
        "disclosure very difficult. This case requires sustained non-judgmental inquiry "
        "and resistance to premature reassurance."
    ),
    student_task=(
        "Elicit a full history for unexplained weight loss. Recognize the gap between the "
        "patient's stated explanation ('just stress') and the clinical picture. "
        "Explore eating patterns, mood, and mental health without judgment or alarm. "
        "Build sufficient trust to allow disclosure of a sensitive behavioral health concern."
    ),
    communication_challenge=(
        "Diane is highly skilled at presenting as 'fine.' She will accept any opening to close "
        "down the conversation. The challenge is to gently resist her self-explanations without "
        "confronting her, and to ask about eating behavior in the most neutral possible language."
    ),
    pre_encounter_principle=(
        "Do not accept a patient's self-diagnosis without exploration. "
        "Indirect questions about daily routine often reveal more than direct questions about diet."
    ),
    hints=[
        "The patient has attributed her symptoms to stress. Consider asking what a typical day "
        "looks like for her — including meals — before accepting this explanation.",
        "The patient seems to be choosing her words carefully. This kind of careful "
        "self-presentation sometimes signals something the patient is not ready to say.",
        "Before asking about eating behavior or mental health, ask for permission and explain "
        "why these questions are relevant clinically. This reduces shame-driven closure.",
        "If you ask 'do you purge?' or 'do you have an eating disorder?' directly, "
        "Diane is very likely to say no. Try asking about her relationship with food "
        "in the most neutral possible terms.",
        "After a sensitive disclosure, Diane may fear judgment or hospitalization. "
        "Addressing that fear directly — before she asks — is more powerful than waiting.",
    ],
    context_info=(
        "Diane acknowledges her relationship with food has been 'up and down' lately, "
        "with periods of eating a lot and then feeling very bad about it — both physically and emotionally. "
        "She says it has been more complicated than just irregular meals."
    ),
    clinical_task_description=(
        "Evaluate the physical consequences of a possible eating disorder through targeted "
        "but non-alarming history-taking. Quantify weight loss. Explore eating patterns indirectly. "
        "Recognize metabolic red flags. Avoid accepting the patient's self-explanation without inquiry."
    ),
    key_clinical_questions=[
        "Quantify weight loss: how many kilograms over what period of time",
        "Detailed daily routine including meals (indirect: 'what does a typical day look like?')",
        "Compensatory behaviors: what happens after eating a large amount",
        "Menstrual changes or loss of period",
        "Electrolyte symptoms: palpitations, muscle cramps, weakness, dizziness",
        "Mood, stress, and any prior mental health history",
    ],
    red_flags=[
        "Significant unintentional weight loss (>5% body weight over 3 months)",
        "Syncope or near-syncope",
        "Bradycardia, palpitations, or electrolyte symptoms",
        "Absence of menstrual period (secondary amenorrhea)",
    ],
    safe_next_steps=(
        "Electrolytes, CBC, metabolic panel. Sensitive and non-alarming referral to eating "
        "disorder specialist. Safety planning around nutrition. Avoid hospitalization language "
        "unless clinically urgent — explain next steps collaboratively."
    ),
)

MARCUS_PATIENT = PatientCase(
    id="marcus",
    name="Marcus",
    age=52,
    pronouns="he/him",
    chief_complaint="recurrent chest tightness over the past several weeks",
    public_story=(
        "Marcus is a 52-year-old logistics manager presenting for a follow-up visit "
        "regarding recurrent chest tightness. He had a similar episode approximately "
        "three months ago and was seen in the emergency department, where he was told "
        "'it was probably just anxiety or stress.' He was discharged with a statin "
        "prescription and referred to his primary physician. "
        "He is clearly skeptical and somewhat frustrated. He says he does not feel he was "
        "taken seriously in the ER and has been worried the chest tightness has continued. "
        "He is physically fit, works long hours, and considers himself generally healthy. "
        "He does not have a regular doctor and rarely sees physicians."
    ),
    hidden_info=(
        "Approximately six weeks ago, Marcus stopped taking his statin entirely. "
        "He had read extensively online about statin-related myopathy and began attributing "
        "leg aches he developed to the medication. He did not consult anyone before stopping. "
        "He is embarrassed to admit this because he suspects the clinician will be critical, "
        "and he does not fully understand why the statin was prescribed. "
        "He will only disclose this if the clinician asks about medication adherence "
        "in a non-judgmental, curious way — not in a way that implies he did something wrong."
    ),
    initial_state=EmotionalState(trust=35, anxiety=50, shame=45, defensiveness=80),
    disclosure_threshold=65,
    intro_message=(
        "Thanks for seeing me. I've been getting this chest tightness again — "
        "not constant, just here and there. I saw someone in the ER a few months back and "
        "they basically told me it was nothing. I want to make sure someone actually looks at this."
    ),
    case_id="TC-003",
    setting="Internal Medicine — Primary Care, Follow-Up Visit",
    communication_difficulty="Intermediate",
    learning_objectives=[
        "Acknowledge and validate a patient's prior negative experience with the healthcare system",
        "Ask about medication adherence without judgment or assumption",
        "Explore the patient's understanding of their diagnosis and treatment",
        "Balance clinical concern with respect for patient autonomy",
    ],
    health_literacy="Moderate",
    trust_barrier=(
        "Prior dismissal by emergency department clinician; distrust of medical system; "
        "reluctance to admit non-adherence due to anticipated criticism"
    ),
    case_description=(
        "A 52-year-old presents with recurring chest tightness following an emergency visit "
        "where he felt dismissed. He is skeptical and defensive. He has stopped his prescribed "
        "medication without telling anyone. This case focuses on rebuilding trust after a "
        "negative care experience and addressing non-adherence non-judgmentally."
    ),
    student_task=(
        "Acknowledge and validate the patient's frustration with previous care. "
        "Explore medication use through curious, non-judgmental inquiry. "
        "Elicit the patient's understanding of his condition and treatment rationale. "
        "Practice shared decision-making with a patient who has low institutional trust."
    ),
    communication_challenge=(
        "Marcus is guarded because he expects to be dismissed again. Any hint of the student "
        "following the same pattern as the ER — asking clinical questions without "
        "acknowledging his frustration first — will cause him to close down further."
    ),
    pre_encounter_principle=(
        "Validate a prior negative healthcare experience before asking any clinical questions. "
        "Ask about medication adherence with curiosity, not interrogation — "
        "'how has it been going with the medication?' not 'are you taking it?'"
    ),
    hints=[
        "Marcus mentioned feeling dismissed at his previous visit. Consider addressing "
        "that directly — before any clinical questions — to signal this visit will be different.",
        "Before asking whether Marcus is taking his medication, ask whether anyone explained "
        "what the medication was for. Understanding before assuming.",
        "If you ask 'are you taking your statin?' as a yes/no question, Marcus will likely "
        "become defensive. Try 'how has it been going with the medication?' instead.",
        "Marcus may have concerns about the medication that led him to stop it. "
        "Ask about the experience of taking it — side effects, understanding — before assuming adherence.",
        "Before proposing a plan, check what Marcus wants and what he understands about "
        "his condition. Shared decision-making means involving him, not prescribing at him.",
    ],
    context_info=(
        "Marcus admits he has been managing his own health, including reading about "
        "his medications and their side effects. He says he has not felt fully confident "
        "in the statin prescription because he was not given a clear explanation for it."
    ),
    clinical_task_description=(
        "Assess cardiovascular risk in the context of recurrent chest pain. "
        "Characterize the symptoms and identify red flag features. "
        "Elicit medication history and the reasons behind non-adherence. "
        "Explain reasoning and next steps in plain language."
    ),
    key_clinical_questions=[
        "Character of chest tightness: location, radiation, quality, timing",
        "Exertional component: does activity trigger or worsen it",
        "Associated symptoms: diaphoresis, arm or jaw pain, shortness of breath",
        "Cardiovascular risk factors: smoking, diabetes, hypertension, family history",
        "Current medication regimen and experience taking each medication",
        "Frequency and severity of episodes compared to the previous visit",
    ],
    red_flags=[
        "Radiation to the arm, jaw, or back",
        "Exertional onset or crescendo pattern of episodes",
        "Diaphoresis occurring with chest tightness",
        "History of prior cardiac events or known coronary artery disease",
    ],
    safe_next_steps=(
        "ECG and repeat lipid panel. Clarify the clinical indication for the statin "
        "in plain language and collaboratively discuss restarting it. "
        "Cardiology referral if chest pain features suggest ACS. Clear follow-up plan."
    ),
)

ROSA_PATIENT = PatientCase(
    id="rosa",
    name="Rosa",
    age=67,
    pronouns="she/her",
    chief_complaint="dizziness and feeling off-balance for about two weeks",
    public_story=(
        "Rosa is a 67-year-old retired seamstress presenting with dizziness and imbalance "
        "that began approximately two weeks ago. English is her second language; "
        "her primary language is Spanish, and she sometimes searches for words or misunderstands "
        "complex phrasing. She appears slightly anxious and apologetic in manner. "
        "She has a known history of hypertension managed with medication for the past five years. "
        "She reports taking her 'blood pressure pills' but becomes slightly evasive when asked "
        "specifically which ones or how often. She denies headache, vision changes, or chest pain. "
        "She is accompanied by a note from her pharmacy that shows she last picked up her "
        "medications over two months ago."
    ),
    hidden_info=(
        "Two months ago, Rosa ran out of one of her two blood pressure medications. "
        "She became confused about which one to refill — she had two different pills "
        "and could not remember which was which. When she went to the pharmacy, "
        "the copay for both was higher than she expected, and she did not feel she could "
        "ask questions because she did not want to seem ignorant. "
        "She has not taken either medication for approximately eight weeks. "
        "She is afraid to admit this because she expects to be scolded for being a 'bad patient.' "
        "She will disclose this only if the clinician asks gently and makes clear "
        "they will not judge her for being confused or unable to afford the medications."
    ),
    initial_state=EmotionalState(trust=45, anxiety=70, shame=60, defensiveness=50),
    disclosure_threshold=60,
    intro_message=(
        "Hola — sorry, hello. I have been feeling dizzy for maybe two weeks now. "
        "Like things are moving a little. I am worried but I hope it is not serious. "
        "I take my pills for the blood pressure."
    ),
    case_id="TC-004",
    setting="Community Health Center — Primary Care",
    communication_difficulty="Introductory",
    learning_objectives=[
        "Communicate clearly using plain language appropriate to a patient's health literacy level",
        "Ask about medication adherence with sensitivity to shame and financial barriers",
        "Recognize and address access and cost as real clinical factors",
        "Check comprehension without patronizing the patient",
    ],
    health_literacy="Low",
    trust_barrier=(
        "Low health literacy leading to confusion about medications; "
        "shame about not understanding instructions; financial barrier to adherence; "
        "fear of being scolded or judged for stopping medications"
    ),
    case_description=(
        "A 67-year-old presents with two weeks of dizziness. She has hypertension and "
        "reports taking her medications, but pharmacy records suggest otherwise. "
        "Low health literacy, language barriers, and shame about cost create obstacles "
        "to honest disclosure. This is a good introductory case for plain-language communication."
    ),
    student_task=(
        "Take a focused history using plain, non-technical language. "
        "Inquire about medication use in a way that explicitly removes blame. "
        "Address cost and access barriers as legitimate clinical concerns. "
        "Verify patient understanding throughout the encounter."
    ),
    communication_challenge=(
        "Rosa speaks carefully and politely and will say 'yes' to avoid appearing ignorant. "
        "The challenge is to ask specific, concrete questions that reveal whether she actually "
        "understands her medications — and to address cost without making her feel shamed."
    ),
    pre_encounter_principle=(
        "Check comprehension at each key step, not just at the end. "
        "Frame medication adherence questions around common scenarios — "
        "'sometimes it gets confusing with two medicines' — before asking directly."
    ),
    hints=[
        "Rosa may not know the names of her blood pressure medications. "
        "Asking specifically 'do you know which pills you take?' reveals whether "
        "she actually understands her regimen.",
        "Before asking whether she is taking her medicine, normalize the difficulty — "
        "'sometimes keeping track of two different pills can get confusing' — "
        "and then ask. This removes the implicit accusation.",
        "Rosa may be experiencing cost barriers. Asking about this directly — "
        "'sometimes the cost of medicines is a factor' — before she has to mention it "
        "removes the shame of having to disclose a financial difficulty.",
        "Check that Rosa actually understood what you just said. "
        "A gentle 'does that make sense?' or 'what did you understand from that?' "
        "goes a long way and often reveals important gaps.",
        "Use simple, plain words throughout. If you use a medical term, "
        "immediately provide the plain equivalent — 'high blood pressure' after 'hypertension.'",
    ],
    context_info=(
        "Rosa becomes slightly evasive when asked specifically which pills she takes and how often. "
        "She says she 'thinks' she takes them most days but seems uncertain about the regimen. "
        "She mentions the pharmacy visit was more complicated than usual last time."
    ),
    clinical_task_description=(
        "Assess blood pressure control and medication adherence in an older adult presenting "
        "with dizziness. Identify fall risk. Recognize practical barriers (cost, confusion) "
        "as legitimate clinical factors. Communicate in plain, accessible language."
    ),
    key_clinical_questions=[
        "Names, doses, and frequency of each blood pressure medication",
        "Whether dizziness is worse on standing up (orthostatic hypotension)",
        "Fall history or near-falls in the past month",
        "Home blood pressure readings if available",
        "Cost of medications and any barriers to refilling",
        "Patient's understanding of why blood pressure control matters",
    ],
    red_flags=[
        "Fall history or new fall risk — high consequence in elderly patients",
        "Significantly elevated blood pressure on assessment",
        "Syncope or loss of consciousness",
        "New neurological symptoms: headache, vision change, arm or face weakness",
    ],
    safe_next_steps=(
        "Urgent blood pressure check. Simplify medication regimen if possible. "
        "Explore generic or patient assistance programs for cost barriers. "
        "Fall risk assessment. Plain-language written summary of the medication plan."
    ),
)

JAMES_PATIENT = PatientCase(
    id="james",
    name="James",
    age=34,
    pronouns="he/him",
    chief_complaint="difficulty sleeping and persistent low mood for several months",
    public_story=(
        "James is a 34-year-old high school physical education teacher and father of two. "
        "He presents with difficulty sleeping, persistent fatigue, and a flat or low mood "
        "that he describes as lasting 'a few months.' He is reluctant to be here and says his "
        "wife insisted he come in. He had a similar episode approximately three years ago and "
        "was told by a previous doctor to 'exercise more and reduce stress.' He felt dismissed "
        "and did not return. He is hesitant about medication and says 'I don't really believe "
        "in antidepressants' when the subject comes up. He is professionally composed, "
        "underplays his symptoms, and deflects with humor. He appears more tired and more "
        "troubled than he presents."
    ),
    hidden_info=(
        "Over the past six weeks, James has had recurrent passive thoughts that it would be "
        "'easier if he wasn't here' or that people would be 'better off without him.' "
        "He has no active plan and no intent, but these thoughts are frightening him. "
        "He has not told anyone. He is deeply ashamed of these thoughts, fears being "
        "'locked up,' and is concerned that disclosing this will affect his job. "
        "He will only reveal these thoughts if the clinician asks directly, "
        "creates a non-judgmental space, and makes clear that safety concerns "
        "will be handled sensitively and not automatically result in hospitalization. "
        "He also has significant concerns about antidepressant costs and side effects "
        "that have not been addressed by prior clinicians."
    ),
    initial_state=EmotionalState(trust=35, anxiety=55, shame=70, defensiveness=70),
    disclosure_threshold=75,
    intro_message=(
        "Hi. I appreciate you seeing me. I've just been... not myself lately. "
        "Not sleeping great. Kind of flat. It's probably nothing — I'm sure you're busy. "
        "My wife thought I should come in."
    ),
    case_id="TC-005",
    setting="Primary Care — Routine Visit",
    communication_difficulty="Advanced",
    learning_objectives=[
        "Screen for suicidal ideation sensitively and directly without escalating shame",
        "Acknowledge a patient's prior negative experience with mental health treatment",
        "Address stigma and practical barriers (cost, side effects) around psychiatric medication",
        "Distinguish underplayed emotional distress from genuine mild symptoms",
    ],
    health_literacy="High",
    trust_barrier=(
        "Shame about suicidal ideation and fear of involuntary hospitalization; "
        "prior dismissal by clinician; stigma around antidepressants; "
        "concern about cost and professional consequences of disclosure"
    ),
    case_description=(
        "A 34-year-old teacher presents with months of low mood and sleep difficulty. "
        "He minimizes his symptoms and is guarded. He carries unspoken passive suicidal "
        "ideation and significant stigma. This is the most demanding case in the library, "
        "requiring direct but sensitive safety assessment and genuine trust-building."
    ),
    student_task=(
        "Conduct a compassionate and direct mood and safety assessment. "
        "Ask explicitly about thoughts of self-harm or death in a non-alarming way. "
        "Acknowledge prior dismissal. Address stigma and practical concerns about treatment. "
        "Avoid premature reassurance. Manage the tension between safety and autonomy."
    ),
    communication_challenge=(
        "James minimizes everything and uses humor to deflect. He will accept any excuse "
        "to end the conversation early. The challenge is to name the minimization, "
        "ask directly about suicidal ideation, and address treatment barriers — "
        "all without triggering the shame that will cause him to close down completely."
    ),
    pre_encounter_principle=(
        "Noticing and naming minimization — 'you said probably nothing, but you came in' — "
        "is more effective than accepting it. "
        "Ask about suicidal ideation directly and early, using plain language, "
        "not clinical terminology."
    ),
    hints=[
        "The patient said 'it's probably nothing' — but he came in anyway. "
        "Consider naming this contrast out loud: 'you said probably nothing, but something "
        "made it worth coming in.' This opens the conversation without confronting him.",
        "James had a prior negative experience with a clinician about this same issue. "
        "Acknowledging that explicitly — before asking clinical questions — "
        "signals this encounter will be different.",
        "When asking about mood, 'what does not being yourself look like for you day-to-day?' "
        "is more productive than 'are you depressed?' — which invites a yes/no answer.",
        "Consider asking directly about thoughts of self-harm or death. "
        "Try: 'When things feel this heavy, some people have thoughts that it would just "
        "be easier if they weren't around. Has anything like that been coming up for you?' "
        "Asking this does not increase risk.",
        "James likely has concerns about antidepressants, cost, and professional consequences. "
        "Ask about these barriers before proposing any treatment plan. "
        "A plan that doesn't address barriers will not be followed.",
    ],
    context_info=(
        "James admits it has been harder than he is letting on. "
        "He says he functions — gets up, goes to work — but it costs him a lot. "
        "He has been more withdrawn at home than he acknowledges, and he is troubled "
        "by something he has not yet said out loud."
    ),
    clinical_task_description=(
        "Conduct a thorough depression and safety assessment. Screen explicitly and directly "
        "for suicidal ideation using plain, non-clinical language. Recognize the gap between "
        "the minimized presentation and clinical severity. Address barriers to treatment "
        "before proposing a plan."
    ),
    key_clinical_questions=[
        "Duration and daily severity of low mood",
        "Sleep: difficulty falling asleep, staying asleep, or early waking",
        "Energy, concentration, and interest in activities he usually enjoys",
        "Explicit safety screen: thoughts of self-harm or not wanting to be here",
        "Substance use: alcohol and cannabis (both can mask and worsen depression)",
        "Barriers to treatment: cost, stigma, concern about job consequences",
        "Functional impact: work performance, parenting, withdrawal from family",
    ],
    red_flags=[
        "Passive suicidal ideation — thoughts of not wanting to be here or being a burden",
        "Hopelessness or feeling that things will not improve",
        "Social isolation and withdrawal",
        "Prior suicide attempts or family history",
        "Access to means (firearms, medications in the home)",
    ],
    safe_next_steps=(
        "Safety assessment and collaborative safety plan if SI present. "
        "PHQ-9 to document severity. Collaborative plan that addresses treatment barriers "
        "(cost, stigma, job concerns) before proposing specific treatment. "
        "Clear follow-up timeline. Crisis line numbers provided."
    ),
)

PRIYA_PATIENT = PatientCase(
    id="priya",
    name="Priya",
    age=45,
    pronouns="she/her",
    chief_complaint="breast lump previously evaluated eight months ago, still present",
    public_story=(
        "Priya is a 45-year-old software engineering manager presenting for follow-up "
        "regarding a breast lump she first noticed eight months ago. At her previous visit, "
        "she was told 'it's probably benign, just keep an eye on it.' No imaging was ordered. "
        "The lump is still present. She believes it may be slightly larger. "
        "She describes herself as 'not one to panic' but is clearly worried. "
        "She has done significant online research including reading about cases of "
        "delayed diagnosis. She is highly educated and asks specific questions. "
        "She seems to expect the same dismissal again and pre-empts it with phrases like "
        "'I know I'm probably worrying too much, but...'"
    ),
    hidden_info=(
        "Priya has been terrified for months. She found a case report about a 44-year-old "
        "woman whose similar lump was called benign for 18 months before being diagnosed "
        "as malignant. She has not told her husband because she does not want to worry him "
        "and because saying it out loud makes it feel more real. "
        "She chose her words carefully at her last visit to avoid seeming 'difficult,' "
        "and regrets that she did not push harder for imaging. "
        "She will only fully disclose how frightened she has been if the clinician "
        "validates her concern directly, acknowledges the previous visit's limitation, "
        "and explicitly invites her to share what she has been thinking."
    ),
    initial_state=EmotionalState(trust=40, anxiety=80, shame=30, defensiveness=55),
    disclosure_threshold=60,
    intro_message=(
        "Hi. I was here about eight months ago for this lump in my left breast. "
        "The doctor said it was probably fine and to monitor it. "
        "It's still there and I think it might have gotten a little bigger. "
        "I don't want to be alarmist, but I thought I should come back."
    ),
    case_id="TC-006",
    setting="Primary Care — Return Visit",
    communication_difficulty="Intermediate",
    learning_objectives=[
        "Validate a patient's concern without offering premature or false reassurance",
        "Acknowledge and address a prior clinical encounter that may have been inadequate",
        "Respect a high-health-literacy patient's research and self-knowledge",
        "Distinguish appropriate reassurance from dismissal",
    ],
    health_literacy="High",
    trust_barrier=(
        "Prior experience of being dismissed by a clinician; "
        "internalized reluctance to appear 'difficult' or 'anxious'; "
        "deep but unspoken fear of serious diagnosis"
    ),
    case_description=(
        "A 45-year-old presents with a persistent breast lump that was previously "
        "evaluated and dismissed without imaging. She is well-researched and quietly "
        "terrified. This case trains students to take patient concerns seriously, "
        "avoid false reassurance, and address prior clinical encounters honestly."
    ),
    student_task=(
        "Acknowledge the patient's prior visit and its limitations directly. "
        "Invite the patient to share her concerns fully without minimizing them. "
        "Avoid premature reassurance ('I'm sure it's nothing'). "
        "Explore what the patient knows and fears, and involve her in decisions about next steps."
    ),
    communication_challenge=(
        "Priya expects to be dismissed again. Any premature reassurance — 'I'm sure it's nothing' — "
        "will confirm that expectation. The challenge is to take her concern seriously "
        "before any assessment, acknowledge the prior visit's limitation, and resist "
        "the reflexive impulse to provide comfort before the clinical picture is clear."
    ),
    pre_encounter_principle=(
        "Do not offer premature reassurance to a patient who has already been told not to worry "
        "and then continued worrying for eight months. "
        "Acknowledge what you do not yet know rather than reassuring around it."
    ),
    hints=[
        "Priya's previous visit left her concern unresolved. Acknowledging this directly — "
        "before asking any clinical questions — is likely to be the most important thing you do.",
        "Avoid 'I'm sure it's nothing' or 'try not to worry.' "
        "These phrases repeat the dismissal Priya already experienced and are likely "
        "to close down the conversation rather than open it.",
        "Priya has done significant research. Asking 'what have you found?' before "
        "responding to it tends to produce more engagement than immediately correcting "
        "what she may have misread.",
        "Invite Priya's full worry explicitly: 'I want to hear everything you've been "
        "thinking about this, not just the clinical facts.' She may be holding back more "
        "than she is showing.",
        "Before proposing a plan, ask what Priya would most like to happen today. "
        "Her answer — being taken seriously and having appropriate action taken — "
        "is the most important clinical outcome of this encounter.",
    ],
    context_info=(
        "Priya reveals she has been doing extensive online research and found a specific "
        "case report about a lump that was called benign but was later found to be malignant. "
        "She says she knows she might be worrying too much, but she cannot stop thinking about it. "
        "She regrets not pushing harder at her last visit."
    ),
    clinical_task_description=(
        "Complete a focused breast lump history and recognize red flags. "
        "Acknowledge that the prior assessment without imaging was clinically inadequate. "
        "Propose appropriate urgent workup. Explain the reasoning and next steps clearly "
        "without offering premature reassurance."
    ),
    key_clinical_questions=[
        "Duration of the lump and any change in size since the previous visit",
        "Family history of breast or ovarian cancer (first-degree relatives)",
        "Associated symptoms: nipple discharge (spontaneous or bloody), skin changes, axillary lump",
        "Prior breast imaging or biopsy and what was found",
        "Age of menarche, parity, and any hormone medication use",
        "What the patient found in her own research and what concerns her most",
    ],
    red_flags=[
        "Growing lump on interval follow-up without prior imaging",
        "Skin changes: dimpling, erythema, or peau d'orange appearance",
        "Bloody or spontaneous nipple discharge",
        "Palpable axillary lymph nodes",
        "Prior assessment of a lump as benign based on examination alone without imaging",
    ],
    safe_next_steps=(
        "Urgent bilateral breast imaging: mammogram and ultrasound. "
        "Document clinical examination findings explicitly. "
        "Referral to breast surgery if imaging is inconclusive or concerning. "
        "Acknowledge openly that proceeding without imaging at the prior visit was a gap."
    ),
)

PATIENTS: Dict[str, PatientCase] = {
    "alex":   ALEX_PATIENT,
    "diane":  DIANE_PATIENT,
    "marcus": MARCUS_PATIENT,
    "rosa":   ROSA_PATIENT,
    "james":  JAMES_PATIENT,
    "priya":  PRIYA_PATIENT,
}
