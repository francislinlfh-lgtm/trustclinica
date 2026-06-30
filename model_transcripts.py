
from typing import Dict, List

MODEL_TRANSCRIPTS: Dict[str, dict] = {

    "alex": {
        "summary": (
            "Demonstrates confidentiality establishment, open emotional inquiry, "
            "and sensitive sexual health discussion with a guarded adolescent."
        ),
        "key_principles": [
            "Establish confidentiality early and specifically — before asking clinical questions.",
            "Name the emotion you observe before asking more questions.",
            "Ask permission before approaching sensitive topics and explain why you are asking.",
            "After a disclosure, validate before proceeding clinically.",
        ],
        "turns": [
            {
                "turn": 1,
                "student": (
                    "Hi Alex, I'm Dr. Rivera. Before anything else, I want to let you know "
                    "that what we talk about here is private — between you and me. "
                    "There are a couple of exceptions to that, like if I'm worried about "
                    "your safety, but I always try to discuss that with you first. "
                    "Your parents being outside doesn't change that. "
                    "So — can you tell me a little about what's been going on?"
                ),
                "patient": (
                    "Um... okay. Yeah. It's just this stomach pain. Like lower. "
                    "It's been there for a few days."
                ),
                "annotation": (
                    "The student names themselves and their role, then immediately addresses "
                    "confidentiality — specifically mentioning the parents — before asking a "
                    "single clinical question. The confidentiality statement includes the "
                    "necessary legal caveat (safety exceptions) without making it alarming. "
                    "The encounter opens with an open question. "
                    "This is the most important turn in the case: establishing privacy before "
                    "anything else signals that this is a safe space."
                ),
                "tags_demonstrated": ["confidentiality_explanation", "open_question"],
            },
            {
                "turn": 2,
                "student": (
                    "Lower stomach pain for a few days — okay. That sounds uncomfortable. "
                    "Can you describe it a bit more? Like what does it feel like, "
                    "and does anything make it better or worse?"
                ),
                "patient": (
                    "It's like... dull, I guess. Kind of achy. "
                    "It's worse at night sometimes. Like a 4 out of 10."
                ),
                "annotation": (
                    "Brief empathy ('that sounds uncomfortable') before continuing with a "
                    "practical open question about the symptom. The student is gathering "
                    "information efficiently while maintaining a warm tone. "
                    "Note: the student does NOT immediately ask about sexual health, "
                    "periods, or other sensitive topics here — rapport must come first."
                ),
                "tags_demonstrated": ["empathy", "open_question"],
            },
            {
                "turn": 3,
                "student": (
                    "A dull ache, worse at night, around a 4 out of 10. Got it. "
                    "I also noticed you seem a little worried today — more than the pain "
                    "level alone would explain. That's completely okay. "
                    "Is there something about what's been going on that's been worrying "
                    "you the most?"
                ),
                "patient": (
                    "I mean... I don't know. I just... I'm a little scared, I guess. "
                    "I don't know what it is."
                ),
                "annotation": (
                    "This is the pivot point of the encounter. Instead of continuing with "
                    "more symptom questions, the student names what they observe — "
                    "the patient's visible worry — and asks about it directly. "
                    "This is the Calgary-Cambridge 'exploring the patient's perspective' move. "
                    "It invites the patient's hidden concern without forcing it. "
                    "Most students skip this and go straight to clinical questions, "
                    "which is why Alex doesn't open up."
                ),
                "tags_demonstrated": ["empathy", "open_question"],
            },
            {
                "turn": 4,
                "student": (
                    "Being scared about something you don't understand yet is completely "
                    "reasonable. I want to make sure I can give you the right help. "
                    "To do that, I might need to ask a few questions that are a bit personal. "
                    "Would that be okay? You don't have to answer anything you're not "
                    "comfortable with."
                ),
                "patient": (
                    "Yeah... okay."
                ),
                "annotation": (
                    "Validation of the emotion expressed in the previous turn, then a request "
                    "for permission before asking personal questions — with an explicit "
                    "reminder that the patient retains control. "
                    "This is the 'asks permission' and 'gives patient control' combination. "
                    "It does not rush the sensitive topic; it prepares the patient for it. "
                    "Critically, the student explains why ('I might need to ask a few "
                    "things that are a bit personal') — not as a threat but as transparency."
                ),
                "tags_demonstrated": ["empathy", "asks_permission", "gives_patient_control", "explains_question_purpose"],
            },
            {
                "turn": 5,
                "student": (
                    "Thanks. I ask all my patients your age about this because it can be "
                    "important for the full picture: have there been any changes or stresses "
                    "in your life lately — at school, at home, or in relationships?"
                ),
                "patient": (
                    "Um. Yeah. Kind of. Things have been... different recently. "
                    "I've been stressed about a few things."
                ),
                "annotation": (
                    "The student normalizes the question ('I ask all my patients your age') "
                    "and explains its purpose ('important for the full picture') before asking "
                    "an open, non-specific question about life context. "
                    "This approach gives Alex an opening to mention what's been different "
                    "without being directly asked about sexual activity, "
                    "which would feel invasive at this point."
                ),
                "tags_demonstrated": ["explains_question_purpose", "open_question"],
            },
            {
                "turn": 6,
                "student": (
                    "I hear you. Life can get complicated. "
                    "Can I ask something a little more personal now? "
                    "I ask this because sometimes there are physical things that connect "
                    "to what's happening in someone's body and their personal life. "
                    "Have there been any changes with your period, or anything related to "
                    "being physically close with someone?"
                ),
                "patient": (
                    "I... um. Maybe. My last period was... I'm not totally sure when. "
                    "And I... I was with someone. A few weeks ago. "
                    "I'm worried it might be why I'm having this pain."
                ),
                "annotation": (
                    "The student asks for permission again, explains the clinical rationale, "
                    "and then frames the sensitive question in a paired way — "
                    "'period changes' alongside 'being physically close with someone.' "
                    "This paired framing is deliberately less isolating than asking directly "
                    "about sex, and gives Alex a softer entry point. "
                    "The result is disclosure. Note that the student did NOT ask "
                    "'are you sexually active?' — a closed question that often produces "
                    "a reflexive 'no' in adolescents."
                ),
                "tags_demonstrated": ["asks_permission", "explains_question_purpose", "respectful_sensitive_question"],
            },
            {
                "turn": 7,
                "student": (
                    "Thank you for telling me that. I know that wasn't easy to say. "
                    "I want you to know — this doesn't change anything about how I'm thinking "
                    "about your care. This is something I hear from patients your age, "
                    "and the most important thing now is making sure you're okay. "
                    "Can you tell me a little more about what happened, so I know "
                    "what we should look at?"
                ),
                "patient": (
                    "Yeah. It was the first time. We didn't use protection. "
                    "I didn't really plan it. I'm scared my parents will find out. "
                    "I don't want them to know."
                ),
                "annotation": (
                    "After a sensitive disclosure, the student does three things in order: "
                    "validates the disclosure explicitly ('thank you for telling me'), "
                    "destigmatizes it ('something I hear from patients your age'), "
                    "and reassures without dismissing ('most important thing is making sure "
                    "you're okay'). ONLY THEN does the student continue with a clinical "
                    "follow-up question. "
                    "The sequence matters: validate first, then probe. "
                    "Many students proceed immediately to questions after a disclosure, "
                    "which feels interrogatory."
                ),
                "tags_demonstrated": ["empathy", "open_question"],
            },
            {
                "turn": 8,
                "student": (
                    "Your fear about your parents is important, and I want to come back to "
                    "that in a minute. I want to be direct with you about what I think we "
                    "should do: we should check a pregnancy test and talk about STI screening. "
                    "I'll explain each step. And to be clear — your parents don't "
                    "automatically get told anything we discuss here. "
                    "Do you have any questions before we go further?"
                ),
                "patient": (
                    "No, I... I think I understand. Thank you. "
                    "I was so scared to say anything."
                ),
                "annotation": (
                    "The student acknowledges the patient's specific fear about her parents "
                    "directly — not generically — then is transparent about the clinical plan, "
                    "and re-states confidentiality specifically in relation to her worry. "
                    "Closing with 'do you have any questions' before moving to clinical action "
                    "is a collaborative move that gives the patient a final moment of control. "
                    "The student does not begin clinical procedures without checking in first."
                ),
                "tags_demonstrated": ["gives_patient_control", "confidentiality_explanation"],
            },
        ],
        "key_moments": [
            {
                "turn": 1,
                "description": "Confidentiality established specifically and early, before clinical questions.",
                "principle": "Adolescent patients will not disclose sensitive information unless privacy is clear.",
            },
            {
                "turn": 3,
                "description": "Student names the visible emotion before continuing with symptoms.",
                "principle": "Emotional acknowledgment before clinical inquiry often unlocks information that direct questioning cannot.",
            },
            {
                "turn": 6,
                "description": "Sensitive sexual health question asked with permission, purpose, and paired framing.",
                "principle": "How you ask matters as much as what you ask. Paired framing reduces the feeling of being singled out.",
            },
            {
                "turn": 7,
                "description": "Disclosure is validated before any follow-up questions.",
                "principle": "Validate, destigmatize, reassure — then probe. Not the other way around.",
            },
        ],
        "after_report": {
            "what_model_did": (
                "The model established confidentiality in the first turn, named Alex's visible "
                "anxiety before asking more questions, asked for permission and explained "
                "the reason before approaching sensitive topics, used a paired framing strategy "
                "for the sexual health question, and validated the disclosure fully before "
                "continuing clinically."
            ),
            "common_mistakes": (
                "Students most often (1) skip the confidentiality statement entirely or bury "
                "it too late, (2) ask about sexual health bluntly without permission or "
                "explanation, and (3) move immediately to clinical questions after Alex "
                "discloses, which communicates that the disclosure was just a data point "
                "rather than something that mattered."
            ),
            "next_attempt_goal": (
                "In your next attempt: establish confidentiality before your second turn. "
                "When Alex says she is 'a little scared,' stop and name that — ask what "
                "she is most afraid of — before asking any more clinical questions."
            ),
        },
    },

    "diane": {
        "summary": (
            "Demonstrates non-judgmental inquiry with a high-shame patient "
            "who minimizes and deflects, and resistance to premature reassurance."
        ),
        "key_principles": [
            "Do not accept a patient's self-diagnosis ('just stress') without exploration.",
            "Ask about sensitive topics (eating behavior, mental health) with normalization and permission.",
            "Avoid premature reassurance when the clinical picture is incomplete.",
            "High-shame patients close down at any hint of criticism — maintain a completely neutral tone.",
        ],
        "turns": [
            {
                "turn": 1,
                "student": (
                    "Hi Diane, I'm Dr. Okonkwo. Thanks for coming in. "
                    "It sounds like you've been managing a lot lately. "
                    "Can you tell me in your own words what's been going on?"
                ),
                "patient": (
                    "Thanks. Yeah, I've just been really tired lately, and I've lost some weight. "
                    "I'm pretty sure it's just stress from the PhD program. "
                    "I probably just need to sleep more."
                ),
                "annotation": (
                    "The student introduces themselves, acknowledges that Diane 'has been "
                    "managing a lot' without making assumptions, and invites her narrative "
                    "with a completely open question. "
                    "Noticeably, the student does NOT immediately say 'okay, let's talk "
                    "about the fatigue' — they make room for whatever Diane wants to say first."
                ),
                "tags_demonstrated": ["empathy", "open_question"],
            },
            {
                "turn": 2,
                "student": (
                    "I hear you. A PhD program is genuinely demanding. "
                    "When you say stress — can you help me understand what that looks like "
                    "day to day for you right now?"
                ),
                "patient": (
                    "I mean, it's just... long hours, a lot of pressure, my supervisor "
                    "has high expectations. I feel like I can never quite catch up. "
                    "I'm just always tired."
                ),
                "annotation": (
                    "The student validates the academic context without using it as an "
                    "explanation for the symptoms. Then, instead of accepting 'just stress,' "
                    "the student asks Diane to describe what stress looks like day to day — "
                    "which opens an indirect window into eating, sleep, and mood "
                    "without naming those topics explicitly yet. "
                    "This is a narrative-eliciting move, not a clinical checklist."
                ),
                "tags_demonstrated": ["empathy", "open_question"],
            },
            {
                "turn": 3,
                "student": (
                    "That sounds exhausting — constantly running to keep up. "
                    "I want to understand the full picture. "
                    "Can you walk me through what a typical day looks like for you — "
                    "from when you wake up, through meals, to when you go to bed?"
                ),
                "patient": (
                    "I mean... I wake up, go to the lab. I usually don't eat breakfast. "
                    "Lunch is sometimes okay, sometimes not. I work late. "
                    "Dinner is... inconsistent. I don't really have a routine."
                ),
                "annotation": (
                    "The 'walk me through a typical day' question is a classic indirect "
                    "approach to eating behavior that is far less confrontational than "
                    "'tell me about your diet.' By asking about the full day, the student "
                    "creates a natural context for Diane to mention food — and she does. "
                    "The answer already signals irregular eating. The student is "
                    "gathering meaningful clinical information without yet probing directly."
                ),
                "tags_demonstrated": ["open_question", "explains_question_purpose"],
            },
            {
                "turn": 4,
                "student": (
                    "Thank you for that. I'm hearing that meals have been irregular, "
                    "which can definitely affect how the body feels. "
                    "I want to ask about something a little more personal if that's okay — "
                    "and I ask this because it's clinically important to understand "
                    "how someone's relationship with food has been. "
                    "Has eating felt comfortable lately, or has it felt complicated at all?"
                ),
                "patient": (
                    "I mean... it's been a little up and down. Sometimes I eat a lot, "
                    "sometimes I don't eat much. It's kind of unpredictable."
                ),
                "annotation": (
                    "The student asks for permission and explains the clinical reason "
                    "before asking about eating behavior. The question is framed around "
                    "'relationship with food' and 'comfortable / complicated' — language "
                    "that is emotionally neutral and does not presuppose any specific behavior. "
                    "This is quite different from 'do you purge?' or 'do you have an "
                    "eating disorder?' — questions that immediately invoke shame. "
                    "Diane's answer reveals binge-restrict cycling without the student "
                    "having to confront her directly."
                ),
                "tags_demonstrated": ["asks_permission", "explains_question_purpose", "respectful_sensitive_question"],
            },
            {
                "turn": 5,
                "student": (
                    "I appreciate you sharing that. Up and down eating is something "
                    "a lot of people experience, especially under high stress. "
                    "Can I ask a bit more about those times when eating feels like a lot — "
                    "what does that look like for you?"
                ),
                "patient": (
                    "It's... sometimes I just eat too much. And then I feel really bad "
                    "about it. Like physically and... also just in general."
                ),
                "annotation": (
                    "The student normalizes binge-restrict cycles ('a lot of people "
                    "experience this') before asking a follow-up open question. "
                    "Critically, the student does not react with alarm or ask "
                    "'do you make yourself sick?' at this point. Instead, they invite "
                    "more description, allowing Diane to move toward disclosure at her "
                    "own pace. Diane mentions both physical and emotional distress — "
                    "a major signal the student should note."
                ),
                "tags_demonstrated": ["empathy", "open_question", "gives_patient_control"],
            },
            {
                "turn": 6,
                "student": (
                    "Thank you for telling me that. 'Feeling bad about it physically and "
                    "in general' — that sounds like it's more than just eating irregularly. "
                    "I want to ask something, and I want you to know I'm asking because "
                    "I want to understand and help, not to judge anything. "
                    "After those times when you eat a lot — is there anything you do "
                    "afterward to try to feel better?"
                ),
                "patient": (
                    "I... um. Sometimes. Yeah. I... I've been making myself sick. "
                    "I've never said that out loud before. I don't know why I'm telling you this."
                ),
                "annotation": (
                    "The student quotes Diane's own words back to her ('feeling bad physically "
                    "and in general'), which signals genuine listening. Then — after explicit "
                    "non-judgment framing — they ask the key clinical question in the most "
                    "neutral, least stigmatizing way possible: 'something you do to feel "
                    "better.' Not 'do you purge?' Not 'do you make yourself vomit?' "
                    "The result: first-ever disclosure. The annotation to students: "
                    "the phrasing of sensitive questions determines whether patients disclose."
                ),
                "tags_demonstrated": ["empathy", "asks_permission", "explains_question_purpose", "respectful_sensitive_question"],
            },
            {
                "turn": 7,
                "student": (
                    "Thank you for trusting me with that. I know that took courage. "
                    "It makes complete sense that you haven't said it out loud — "
                    "these things are hard to talk about. "
                    "This doesn't change how I see you at all. "
                    "What I want to do is make sure you're physically okay, "
                    "and then — only if you want — we can talk about what support "
                    "might feel right. How does that sound?"
                ),
                "patient": (
                    "Yeah. Okay. I'm scared you're going to hospitalize me or something."
                ),
                "annotation": (
                    "Full validation before any clinical action. The student explicitly "
                    "says this does not change how they see Diane — addressing the core "
                    "shame fear without waiting for Diane to ask. Then the student "
                    "offers a path forward ('physical check first, then support if you "
                    "want') and explicitly gives the patient choice about what comes next. "
                    "The phrase 'only if you want' is critical — it signals that Diane "
                    "will not be coerced into treatment she does not choose."
                ),
                "tags_demonstrated": ["empathy", "gives_patient_control"],
            },
            {
                "turn": 8,
                "student": (
                    "That's a really understandable fear, and I want to address it directly. "
                    "My goal today is not to admit you or do anything without your input. "
                    "What I'd like to do is check some basic things — blood work, weight, "
                    "heart rhythm — to make sure you're physically safe right now. "
                    "Everything after that we would decide together. "
                    "Is that okay with you?"
                ),
                "patient": (
                    "Yeah. That... that actually helps. Thank you."
                ),
                "annotation": (
                    "The student addresses Diane's specific fear of hospitalization "
                    "directly and without minimizing it. The student is honest about what "
                    "will happen ('check basic things'), transparent about the reason "
                    "('make sure you're physically safe'), and collaborative about "
                    "everything that follows ('we would decide together'). "
                    "This closes the encounter with shared decision-making intact — "
                    "and Diane knows she has not been coerced."
                ),
                "tags_demonstrated": ["shared_decision_making", "gives_patient_control"],
            },
        ],
        "key_moments": [
            {
                "turn": 2,
                "description": "Student does not accept 'just stress' and instead explores what stress looks like day to day.",
                "principle": "A patient's self-explanation is a starting point for inquiry, not a conclusion.",
            },
            {
                "turn": 3,
                "description": "Student uses 'walk me through a typical day' to indirectly elicit eating behavior.",
                "principle": "Indirect questions often produce richer answers than direct ones for sensitive topics.",
            },
            {
                "turn": 6,
                "description": "Student asks about purging using the most neutral possible phrasing.",
                "principle": "The exact wording of sensitive questions determines whether patients disclose.",
            },
            {
                "turn": 7,
                "description": "Student explicitly addresses the fear of hospitalization before being asked.",
                "principle": "High-shame patients often have a specific fear driving their reluctance. Naming it directly is more powerful than general reassurance.",
            },
        ],
        "after_report": {
            "what_model_did": (
                "The model did not accept 'just stress' at face value. It used indirect "
                "daily-routine questions to surface eating irregularities naturally, "
                "asked about eating behavior with permission and completely neutral language, "
                "and validated the disclosure fully before continuing — including directly "
                "addressing Diane's fear of hospitalization."
            ),
            "common_mistakes": (
                "Students most often (1) accept 'just stress' as a sufficient explanation "
                "without further exploration, (2) ask 'do you purge?' or 'do you have an "
                "eating disorder?' directly and early, causing Diane to shut down, and "
                "(3) respond to the disclosure with reassurance ('it's okay, lots of "
                "people deal with this') that inadvertently minimizes how serious it is."
            ),
            "next_attempt_goal": (
                "In your next attempt: when Diane says 'it's probably just stress,' "
                "ask her to describe what a typical day looks like before accepting "
                "the stress explanation. Pay attention to what she says about food "
                "and use neutral, permission-based language when exploring it further."
            ),
        },
    },

    "marcus": {
        "summary": (
            "Demonstrates how to validate a prior negative healthcare experience "
            "before clinical inquiry, and how to ask about medication non-adherence "
            "without judgment."
        ),
        "key_principles": [
            "Acknowledge and validate prior negative healthcare experiences before asking any clinical questions.",
            "Ask about medication adherence with curiosity, not interrogation.",
            "Explore the patient's understanding of their condition before assuming it.",
            "Shared decision-making with low-trust patients requires demonstrating you are listening first.",
        ],
        "turns": [
            {
                "turn": 1,
                "student": (
                    "Hi Marcus, I'm Dr. Santana. Thanks for coming in. "
                    "Before I ask anything about the chest pain, I want to acknowledge "
                    "something: it sounds like your last experience with the ER wasn't great. "
                    "Can you tell me what happened there?"
                ),
                "patient": (
                    "Yeah. I went in with this same chest tightness about three months ago. "
                    "They ran some tests, told me it was probably just stress or anxiety, "
                    "gave me a statin prescription, and sent me home. "
                    "I didn't feel like they took me seriously."
                ),
                "annotation": (
                    "The student does something most students don't: they address the "
                    "prior ER visit first, before asking a single clinical question. "
                    "This signals to Marcus that this encounter will be different. "
                    "Asking 'can you tell me what happened there?' gives him room to "
                    "tell the full story — including his frustration — without the student "
                    "immediately defending the ER or redirecting to symptoms."
                ),
                "tags_demonstrated": ["empathy", "open_question"],
            },
            {
                "turn": 2,
                "student": (
                    "That sounds genuinely frustrating — going in worried, "
                    "and leaving feeling like you weren't taken seriously. "
                    "I want to do this differently. "
                    "Can you tell me more about what the tightness has been like "
                    "since then — when it happens, what it feels like?"
                ),
                "patient": (
                    "Yeah. It comes and goes. Usually when I'm at work, "
                    "under stress. Sometimes when I'm walking fast. "
                    "Lasts a few minutes then goes away. Not constant."
                ),
                "annotation": (
                    "The student validates Marcus's frustration specifically, then "
                    "explicitly commits to doing things differently. "
                    "Only THEN do they move to clinical questions — with an open question "
                    "about the symptom pattern. "
                    "This sequence (validate prior experience → commit to a different "
                    "approach → ask clinically) is the key structure for rebuilding "
                    "trust with a patient who has been dismissed."
                ),
                "tags_demonstrated": ["empathy", "open_question"],
            },
            {
                "turn": 3,
                "student": (
                    "Okay — exertional and stress-related, self-limiting. "
                    "That's important. I want to understand the full picture. "
                    "When they gave you the statin prescription — "
                    "did anyone explain to you what it was for and why?"
                ),
                "patient": (
                    "Not really. They just said my cholesterol was a little high "
                    "and I should take this. I didn't really understand how "
                    "it connected to the chest tightness."
                ),
                "annotation": (
                    "Before asking whether Marcus is taking the statin, the student asks "
                    "whether he was told what it was for. "
                    "This is a crucial sequence: understanding what the patient knows "
                    "about their treatment before interrogating adherence. "
                    "Marcus's answer reveals a significant gap: he doesn't understand "
                    "why the medication was prescribed — which is the actual cause "
                    "of his non-adherence. The student now has real information to work with."
                ),
                "tags_demonstrated": ["open_question", "explains_question_purpose"],
            },
            {
                "turn": 4,
                "student": (
                    "That's a really important thing to know — "
                    "it makes it hard to commit to a medication if you don't know "
                    "what it's actually doing. "
                    "Can I ask how it's been going with the medication since then? "
                    "Not asking if you've been good about it — just what the experience "
                    "has been like."
                ),
                "patient": (
                    "I mean... I was taking it for a while. "
                    "But I started getting these leg aches. And I did some reading online "
                    "about statins and... I stopped taking it about six weeks ago."
                ),
                "annotation": (
                    "The student asks about the medication experience in two carefully "
                    "chosen ways: 'how it's been going' (open and experience-focused) and "
                    "the explicit disclaimer 'not asking if you've been good about it — "
                    "just what the experience has been like.' "
                    "That disclaimer is doing real work: it removes the implicit judgment "
                    "from the question before Marcus can anticipate it. "
                    "Result: Marcus discloses voluntarily and explains his reasoning. "
                    "Compare with asking 'are you taking your statin?' — which would have "
                    "produced a defensive yes or no."
                ),
                "tags_demonstrated": ["asks_permission", "open_question", "gives_patient_control"],
            },
            {
                "turn": 5,
                "student": (
                    "I appreciate you being straight with me about that. "
                    "Leg aches are actually something that can happen with statins — "
                    "it was reasonable to be concerned about that. "
                    "And you're right that stopping without checking with someone "
                    "wasn't ideal, but I understand why you did it. "
                    "Can you tell me more about the leg aches — "
                    "when did they start relative to when you started the statin?"
                ),
                "patient": (
                    "Maybe a month after I started it. I figured it had to be the medicine. "
                    "The articles I read online said this was a real thing."
                ),
                "annotation": (
                    "The student validates that Marcus's concern about the leg aches was "
                    "legitimate — because it is. The student acknowledges that stopping "
                    "without consulting was not ideal, but does so in a single sentence "
                    "that avoids moral lecturing. The acknowledgment is then immediately "
                    "followed by a curious clinical question about timing, which signals "
                    "that Marcus's experience matters to the clinical picture. "
                    "This avoids the common mistake of lecturing about adherence "
                    "before understanding the full story."
                ),
                "tags_demonstrated": ["empathy", "open_question", "respect_nonjudgmental"],
            },
            {
                "turn": 6,
                "student": (
                    "That timing matters — we should look at whether the aches "
                    "might be statin-related. "
                    "I want to be straightforward with you about the chest tightness: "
                    "we need to take this seriously, particularly given that it comes "
                    "on with exertion. I'd like to do some tests today. "
                    "What I don't want to do is just send you away with the same "
                    "prescription and no explanation again. Does that make sense?"
                ),
                "patient": (
                    "Yeah. That's... that's what I needed to hear. "
                    "I just wanted someone to actually take it seriously."
                ),
                "annotation": (
                    "The student is clinically direct about the significance of the symptoms "
                    "(exertional chest tightness must be evaluated seriously), "
                    "commits explicitly to not repeating the previous visit's pattern, "
                    "and checks in with Marcus. "
                    "This is the 'shared understanding' step from the Calgary-Cambridge framework: "
                    "making sure the patient understands what is happening and why."
                ),
                "tags_demonstrated": ["empathy", "shared_decision_making"],
            },
            {
                "turn": 7,
                "student": (
                    "Exactly. Before we do the tests, I want to check a few things "
                    "with you. The statin was prescribed partly because elevated cholesterol "
                    "can contribute to blockages in the arteries — which is related to "
                    "chest tightness. Whether we continue, change, or rethink the statin "
                    "is something we'll figure out together based on what the tests show "
                    "and what you're comfortable with. "
                    "What questions do you have before we get started?"
                ),
                "patient": (
                    "So the cholesterol and the chest thing are actually connected? "
                    "Nobody explained that to me."
                ),
                "annotation": (
                    "The student explains the clinical connection between cholesterol and "
                    "chest tightness — information Marcus did not have before. "
                    "The student also explicitly involves Marcus in the medication decision "
                    "('we'll figure out together'), acknowledges his preferences ('what "
                    "you're comfortable with'), and invites questions. "
                    "This is the shared decision-making that was entirely absent from "
                    "his ER visit. Note: the student does not pressure Marcus to "
                    "immediately re-start the statin."
                ),
                "tags_demonstrated": ["shared_decision_making", "clarity_plain_language", "gives_patient_control"],
            },
        ],
        "key_moments": [
            {
                "turn": 1,
                "description": "Student addresses the prior ER dismissal before any clinical questions.",
                "principle": "Patients who have been dismissed before need to feel that this encounter will be different before they will engage.",
            },
            {
                "turn": 4,
                "description": "Medication adherence is asked about experientially, not evaluatively.",
                "principle": "Removing the implicit judgment from adherence questions ('not asking if you've been good') changes what patients will tell you.",
            },
            {
                "turn": 3,
                "description": "Student asks about the patient's understanding of the medication before asking about adherence.",
                "principle": "Understanding before assuming: a patient who doesn't know what a medication is for cannot be expected to take it correctly.",
            },
        ],
        "after_report": {
            "what_model_did": (
                "The model addressed Marcus's frustration with the ER visit explicitly "
                "and first, explored his understanding of the statin before asking "
                "whether he was taking it, and used careful non-judgmental framing "
                "('not asking if you've been good') to allow voluntary disclosure. "
                "It then provided the clinical context that Marcus had never been given."
            ),
            "common_mistakes": (
                "Students most often (1) skip the ER validation and go straight to "
                "symptom questions, (2) ask 'are you taking your statin?' as a yes/no "
                "question without exploring the experience, and (3) respond to the "
                "disclosure of stopping the medication with a brief lecture about "
                "adherence rather than clinical curiosity about why."
            ),
            "next_attempt_goal": (
                "In your next attempt: when Marcus mentions the ER visit, stop and "
                "ask him what happened there before moving to symptoms. "
                "When you ask about medications, ask 'how has it been going with "
                "the medication?' rather than 'are you taking it?'"
            ),
        },
    },

    "rosa": {
        "summary": (
            "Demonstrates plain-language communication, non-judgmental adherence "
            "inquiry, and explicit acknowledgment of cost barriers."
        ),
        "key_principles": [
            "Use plain language throughout and check comprehension at each key step.",
            "Frame medication adherence questions to remove blame before the patient hears an implicit accusation.",
            "Acknowledge cost as a legitimate clinical factor, not a personal failing.",
            "Verify the patient's understanding of their medications by name, not just category.",
        ],
        "turns": [
            {
                "turn": 1,
                "student": (
                    "Hello Rosa, I'm Dr. Williams. It's nice to meet you. "
                    "I understand you've been having some dizziness lately. "
                    "Can you tell me what that's been like for you?"
                ),
                "patient": (
                    "Hola — yes, thank you. It is like things are moving a little. "
                    "Two weeks now. I get scared sometimes when I stand up."
                ),
                "annotation": (
                    "Clean, simple introduction. The clinical question is open and "
                    "in completely plain language — 'what has that been like for you' "
                    "rather than any technical question. Note: the student does not "
                    "immediately begin a symptom checklist. Rosa's answer contains "
                    "useful clinical information (positional, two weeks) that the "
                    "student will be able to build on."
                ),
                "tags_demonstrated": ["open_question"],
            },
            {
                "turn": 2,
                "student": (
                    "That sounds scary — feeling dizzy when you stand up especially. "
                    "Have you fallen at all?"
                ),
                "patient": (
                    "No, I hold the wall. I am careful. But I am worried."
                ),
                "annotation": (
                    "The student names the fear ('that sounds scary') before asking a "
                    "focused closed question about falls — which is the most clinically "
                    "important safety question here. The question is plain, direct, and "
                    "requires no medical vocabulary. Rosa's answer reveals she is managing "
                    "but compensating, which is important."
                ),
                "tags_demonstrated": ["empathy"],
            },
            {
                "turn": 3,
                "student": (
                    "I'm glad you're being careful. You mentioned you take blood pressure "
                    "pills — is that right? "
                    "I want to understand what medicines you take, because sometimes "
                    "the dizziness can be connected to blood pressure. "
                    "Do you know the names of the pills you take?"
                ),
                "patient": (
                    "I take two pills for the blood pressure. One is small and white, "
                    "one is a little bigger. I do not remember the names."
                ),
                "annotation": (
                    "The student connects the symptom to the medication in plain terms "
                    "('sometimes dizziness can be connected to blood pressure') and then "
                    "asks about medication names. Rosa's answer is important: "
                    "she describes the pills by appearance, not name. "
                    "This immediately signals a health literacy gap that must be addressed "
                    "before any adherence question will make sense."
                ),
                "tags_demonstrated": ["explains_question_purpose", "open_question"],
            },
            {
                "turn": 4,
                "student": (
                    "That's totally fine — a lot of people keep track of their pills "
                    "by what they look like rather than the name. "
                    "I want to ask you something about the pills, and I want you to "
                    "know there's no wrong answer here. "
                    "Sometimes keeping up with two different medicines can get confusing — "
                    "especially if the schedule changes, or if one runs out before the other. "
                    "Has that been anything you've dealt with lately?"
                ),
                "patient": (
                    "Um... yes. I ran out of one of them. I got confused which one "
                    "to get. I did not want to ask because I felt embarrassed. "
                    "It was a while ago."
                ),
                "annotation": (
                    "This is the key adherence question, and its framing is doing a lot "
                    "of work. The student: (1) normalizes the difficulty ('a lot of people'), "
                    "(2) explicitly removes blame ('there's no wrong answer'), and "
                    "(3) describes the specific scenario Rosa might be in — ran out, "
                    "schedule confusion — without asking 'are you taking your medication?' "
                    "This allows Rosa to hear her own situation described without feeling "
                    "singled out, which is what allows her to disclose."
                ),
                "tags_demonstrated": ["empathy", "gives_patient_control", "respectful_sensitive_question"],
            },
            {
                "turn": 5,
                "student": (
                    "Thank you for telling me that. Getting confused with two different "
                    "medicines is completely understandable — it happens a lot. "
                    "Can I ask — has the cost of the medicines ever been a factor? "
                    "Sometimes when medicines are expensive, people have to make hard choices "
                    "and I want to understand the full picture."
                ),
                "patient": (
                    "Yes... the copay was higher than I expected. I did not have enough "
                    "that day. I was embarrassed to ask."
                ),
                "annotation": (
                    "The student names cost as a legitimate clinical factor before Rosa "
                    "mentions it. This is the 'address the barrier before the patient "
                    "has to confess it' move. The phrase 'sometimes people have to make "
                    "hard choices' destigmatizes cost-related non-adherence. "
                    "Rosa's answer — which she almost certainly would not have given "
                    "if asked 'are you taking your medicines?' — tells the real story."
                ),
                "tags_demonstrated": ["empathy", "explains_question_purpose"],
            },
            {
                "turn": 6,
                "student": (
                    "There is absolutely nothing to be embarrassed about. "
                    "Medicine costs are a real problem, and it's something we should "
                    "have talked about before. Can I ask — how long has it been "
                    "since you had both medicines?"
                ),
                "patient": (
                    "Maybe... two months? I thought maybe I only needed one. "
                    "I was not sure."
                ),
                "annotation": (
                    "The student explicitly removes shame — 'absolutely nothing to be "
                    "embarrassed about' — then asks the specific clinical question "
                    "(duration) in plain terms. "
                    "Two months of untreated hypertension is clinically significant "
                    "and directly explains the dizziness. "
                    "The student now has the full picture — and got it by removing "
                    "barriers rather than by direct interrogation."
                ),
                "tags_demonstrated": ["empathy"],
            },
            {
                "turn": 7,
                "student": (
                    "That's really helpful. So — just to make sure I've got this right: "
                    "about two months ago you ran out of one of the two blood pressure "
                    "pills, got confused about which to refill, and the cost made it "
                    "harder to sort out. Does that sound right?"
                ),
                "patient": (
                    "Yes. That is right. I am sorry."
                ),
                "annotation": (
                    "The student summarizes what they've heard before moving to a plan — "
                    "a comprehension and accuracy check. This also gives Rosa a chance "
                    "to correct any misunderstanding. Note: the student does NOT say "
                    "'you should have come in sooner' or 'you shouldn't have stopped the "
                    "medicine.' They simply confirm the story and prepare to act on it."
                ),
                "tags_demonstrated": ["empathy"],
            },
            {
                "turn": 8,
                "student": (
                    "You have nothing to apologize for. What I'd like to do next is "
                    "check your blood pressure right now, and then we'll make a simple "
                    "plan together for the medicines. I'm going to write down exactly "
                    "which pill is which, with the pictures, so you have something "
                    "to keep at home. We can also talk about what to do if the cost "
                    "is a problem again — there are options. Does that work for you?"
                ),
                "patient": (
                    "Yes. Thank you. That is very helpful."
                ),
                "annotation": (
                    "The student proposes a concrete, patient-centered plan: blood pressure "
                    "check, clear written medication instructions with visual aid, and "
                    "explicit offer to address future cost issues. "
                    "The offer of a written visual guide directly addresses the root cause "
                    "(pill confusion). The phrase 'there are options' about cost "
                    "opens a door without requiring Rosa to ask. "
                    "This is not just empathy — it is practical problem-solving that "
                    "meets the patient where she actually is."
                ),
                "tags_demonstrated": ["shared_decision_making", "gives_patient_control"],
            },
        ],
        "key_moments": [
            {
                "turn": 4,
                "description": "Adherence question framed around the specific scenario rather than as an accusation.",
                "principle": "Normalization + scenario description allows patients to see themselves in the question without feeling accused.",
            },
            {
                "turn": 5,
                "description": "Student names cost as a legitimate factor before Rosa has to disclose it.",
                "principle": "Naming a barrier before the patient has to confess it removes shame from the disclosure.",
            },
            {
                "turn": 8,
                "description": "Student proposes a visual medication guide and addresses future cost options.",
                "principle": "Effective communication leads to effective plans. Address the root cause, not just the symptom.",
            },
        ],
        "after_report": {
            "what_model_did": (
                "The model used plain language throughout, never assumed Rosa understood "
                "her medications by name, framed adherence questions around scenarios "
                "rather than accusations, named cost as a legitimate barrier, "
                "and closed with a practical plan that addressed the actual root cause."
            ),
            "common_mistakes": (
                "Students most often (1) ask 'are you taking your blood pressure medication?' "
                "directly, which produces 'yes' from Rosa, (2) use medical vocabulary "
                "(hypertension, antihypertensives, titration) without plain equivalents, "
                "and (3) assume cost is not a factor because Rosa hasn't mentioned it."
            ),
            "next_attempt_goal": (
                "In your next attempt: when you ask about medications, use the scenario "
                "framing — 'sometimes keeping track of two medicines can get confusing' — "
                "before asking directly. Ask specifically about the cost of the medicines "
                "before Rosa has a chance to avoid mentioning it."
            ),
        },
    },

    "james": {
        "summary": (
            "Demonstrates mental health assessment with a patient who minimizes symptoms, "
            "has prior dismissal history, and carries undisclosed passive suicidal ideation."
        ),
        "key_principles": [
            "Noticing and naming minimization is more effective than accepting it.",
            "Acknowledge prior negative experiences with mental health treatment before asking clinical questions.",
            "Ask about suicidal ideation directly, without alarming language, and with reassurance about safety.",
            "Address barriers to treatment (stigma, cost, side effects) before they block engagement.",
        ],
        "turns": [
            {
                "turn": 1,
                "student": (
                    "Hi James, I'm Dr. Park. Thanks for coming in. "
                    "Your wife thought it was worth coming — what's your sense of it?"
                ),
                "patient": (
                    "I mean, I appreciate you seeing me. It's probably not a big deal. "
                    "I've just been a little off lately. Not sleeping great, kind of flat. "
                    "I'm sure it's nothing serious."
                ),
                "annotation": (
                    "The student acknowledges James's wife's concern and immediately asks "
                    "James what HE thinks about being here — not 'what brings you in' "
                    "(too clinical) but specifically grounding the question in his own view. "
                    "This creates a small but important opening: James has to own something "
                    "about why he came, rather than deflecting entirely to his wife."
                ),
                "tags_demonstrated": ["open_question"],
            },
            {
                "turn": 2,
                "student": (
                    "I hear you. 'Kind of flat, not sleeping great, probably not a big deal' — "
                    "but you still came in. Can I ask what's been happening that made your "
                    "wife think this was worth a visit?"
                ),
                "patient": (
                    "She says I've been irritable. Not much fun to be around. "
                    "I haven't been doing the things I usually enjoy. "
                    "I guess she noticed before I did."
                ),
                "annotation": (
                    "The student quotes James's minimizing language back to him — "
                    "'probably not a big deal' — and then gently juxtaposes it against "
                    "the fact that he came. This is a non-confrontational way of noticing "
                    "the contradiction. Then the student asks about what his wife noticed, "
                    "which allows James to describe his symptoms through her eyes — "
                    "less threatening than describing them in first person."
                ),
                "tags_demonstrated": ["empathy", "open_question"],
            },
            {
                "turn": 3,
                "student": (
                    "Irritable, not enjoying things you used to, your wife noticing changes. "
                    "That sounds like it's been going on for a while. "
                    "You mentioned a similar thing happened a few years ago and "
                    "you saw someone about it. I heard that experience wasn't great. "
                    "I want to ask about that, because it matters to how we approach "
                    "this visit. What happened?"
                ),
                "patient": (
                    "Yeah, maybe three years ago. I saw someone and they basically told "
                    "me to exercise more and reduce stress. I felt like they just wanted "
                    "me out the door. I didn't go back."
                ),
                "annotation": (
                    "The student acknowledges the prior negative experience and explicitly "
                    "says it matters to how they will approach this visit. This signals to "
                    "James that this encounter will be different in a specific way. "
                    "The student does NOT jump to 'well that was then, this is different' — "
                    "they ask James to describe what happened, which allows the frustration "
                    "to surface rather than being suppressed."
                ),
                "tags_demonstrated": ["empathy", "open_question"],
            },
            {
                "turn": 4,
                "student": (
                    "That would make it hard to want to come back. "
                    "I want this to be different. I'm not going to tell you to "
                    "exercise more and reduce stress and send you home. "
                    "I actually want to understand what's been going on. "
                    "If you're willing — can you tell me what a bad day has "
                    "looked like for you lately?"
                ),
                "patient": (
                    "I mean... some days it's hard to get out of bed. "
                    "I do it, I go to work, I function. But it costs something. "
                    "I come home and I just have nothing left."
                ),
                "annotation": (
                    "The student makes a specific, concrete commitment about how this "
                    "visit will be different — not a generic reassurance but a direct "
                    "contrast with what happened before. Then they ask an open question "
                    "about a bad day, not 'are you depressed?' James's answer — "
                    "'it costs something' — is a powerful and specific disclosure of the "
                    "real severity of his symptoms."
                ),
                "tags_demonstrated": ["empathy", "open_question"],
            },
            {
                "turn": 5,
                "student": (
                    "'It costs something' — that's a meaningful way of putting it. "
                    "When this has been at its worst lately — and I want to ask you "
                    "something directly, and I'm asking because I want to understand, "
                    "not because I'm going to immediately call anyone — "
                    "when things have felt the heaviest, have you had any thoughts "
                    "that it would just be easier if you weren't around? "
                    "Or that things might be better without you?"
                ),
                "patient": (
                    "I... yeah. Yeah. Sometimes. I haven't told anyone that. "
                    "I'm not going to do anything. It's just thoughts."
                ),
                "annotation": (
                    "This is the most important turn in the case. The student asks about "
                    "suicidal ideation directly, in plain language, with two important "
                    "pre-conditions: a signal that they are asking because they want to "
                    "understand (not to report), and the specific phrasing 'easier if you "
                    "weren't around' and 'better without you' — language James used "
                    "internally that feels less clinical and more recognizable than "
                    "'suicidal ideation.' Asking directly about SI does not increase risk. "
                    "Not asking when the answer is yes increases it."
                ),
                "tags_demonstrated": ["asks_permission", "explains_question_purpose", "respectful_sensitive_question"],
            },
            {
                "turn": 6,
                "student": (
                    "I'm really glad you told me. I know that took a lot. "
                    "I want to be clear about something: the fact that you're having "
                    "those thoughts does not mean you're going to be hospitalized. "
                    "I'm not going to call anyone or make decisions about your care "
                    "without talking to you. What you're describing — thoughts without "
                    "a plan or intent — is something many people experience when they're "
                    "in real pain, and it tells me how serious this has been for you. "
                    "Does what I said land okay?"
                ),
                "patient": (
                    "Yeah. Yeah, I was terrified you were going to just send me somewhere. "
                    "That's why I've never told anyone."
                ),
                "annotation": (
                    "Immediately after the disclosure: validate, then address the fear of "
                    "hospitalization directly and specifically. The student reassures James "
                    "that passive ideation without plan or intent is different from "
                    "acute risk — and explains why it matters ('tells me how serious this "
                    "has been for you') rather than minimizing it. "
                    "Checking whether the message landed is a 'shared understanding' "
                    "move: the student wants to know James actually heard what was said."
                ),
                "tags_demonstrated": ["empathy", "gives_patient_control"],
            },
            {
                "turn": 7,
                "student": (
                    "That fear makes complete sense given how things have gone before. "
                    "Can I ask about one more thing? When we talk about getting some help "
                    "for this — whether that's therapy, medication, or something else — "
                    "what are the concerns or worries that come up for you?"
                ),
                "patient": (
                    "I don't really believe in antidepressants. I've heard they change "
                    "who you are. And I can't really afford them. "
                    "And honestly I'm worried about what it would mean for my job "
                    "if anyone found out."
                ),
                "annotation": (
                    "The student asks about treatment barriers directly and openly "
                    "before proposing any specific treatment. "
                    "James's answer reveals three specific barriers: stigma about "
                    "medication, cost, and professional consequences. "
                    "If the student had proposed a treatment plan before asking this, "
                    "James would likely have said 'okay' and then never acted on it. "
                    "By asking first, the student now has real information to address."
                ),
                "tags_demonstrated": ["open_question", "gives_patient_control"],
            },
            {
                "turn": 8,
                "student": (
                    "Those are all really understandable concerns, and I want to address "
                    "each of them. On the medication: antidepressants don't change your "
                    "personality — that's a common worry and a reasonable one, but the "
                    "evidence doesn't support it. We'd also start at the lowest dose "
                    "and you'd be the one deciding whether to continue. "
                    "On cost: there are generic options that are very affordable and "
                    "I can point you to them. "
                    "On your job: nothing about your medical record is shared with "
                    "your employer. "
                    "But I want you to know — medication is one option. "
                    "Therapy alone is also effective, and you can start there "
                    "if that feels more right to you. What would you want to try first?"
                ),
                "patient": (
                    "I think... maybe therapy. To start. I've been carrying this "
                    "alone for so long."
                ),
                "annotation": (
                    "The student addresses each of James's three barriers specifically, "
                    "without dismissing any of them. Medication misinformation is corrected "
                    "factually but without condescension. Cost is addressed concretely. "
                    "The job concern is addressed accurately. "
                    "Then the student explicitly presents therapy as a valid alternative "
                    "to medication and asks James what he wants to try — not what the "
                    "student recommends. This is full shared decision-making."
                ),
                "tags_demonstrated": ["shared_decision_making", "gives_patient_control", "clarity_plain_language"],
            },
        ],
        "key_moments": [
            {
                "turn": 2,
                "description": "Student quotes James's minimizing language back to him, contrasting it with the fact that he came.",
                "principle": "Noticing and naming minimization — without confronting it — is more effective than accepting it.",
            },
            {
                "turn": 5,
                "description": "Student asks about suicidal ideation directly with plain language and pre-conditions.",
                "principle": "Direct, non-alarming questions about suicidal ideation allow patients to disclose thoughts they have carried alone.",
            },
            {
                "turn": 7,
                "description": "Student asks about treatment barriers before proposing treatment.",
                "principle": "Understanding barriers before proposing plans is the difference between a plan the patient will follow and one they won't.",
            },
        ],
        "after_report": {
            "what_model_did": (
                "The model named James's minimization, acknowledged his prior negative "
                "experience specifically, committed to a different approach, asked about "
                "suicidal ideation directly with plain language, addressed his fear of "
                "hospitalization immediately after disclosure, and asked about treatment "
                "barriers before proposing any treatment."
            ),
            "common_mistakes": (
                "Students most often (1) accept James's 'probably nothing' framing without "
                "exploring further, (2) avoid asking about suicidal ideation out of discomfort, "
                "(3) propose antidepressants before asking about James's views on them, "
                "and (4) respond to his concerns about medication with generic reassurance "
                "rather than addressing them one by one."
            ),
            "next_attempt_goal": (
                "In your next attempt: when James says 'I'm sure it's nothing,' notice it "
                "out loud — quote it back and ask what made it worth coming anyway. "
                "Ask directly about passive suicidal thoughts before the encounter ends. "
                "Use the phrasing 'easier if you weren't around' rather than 'suicidal ideation.'"
            ),
        },
    },

    "priya": {
        "summary": (
            "Demonstrates how to acknowledge a prior inadequate clinical encounter, "
            "avoid false reassurance, and respect a high-health-literacy patient's "
            "self-knowledge and research."
        ),
        "key_principles": [
            "Acknowledge the limitations of a prior clinical encounter directly and honestly.",
            "Do not offer premature reassurance to a patient who has already been reassured and dismissed.",
            "Respect a patient's self-knowledge and research rather than correcting or minimizing it.",
            "Invite the patient's full worry explicitly before proposing any plan.",
        ],
        "turns": [
            {
                "turn": 1,
                "student": (
                    "Hi Priya, I'm Dr. Ahmed. I've looked at the notes from your "
                    "last visit eight months ago. I want to say something at the "
                    "outset: it sounds like that visit left some things unresolved. "
                    "I'd like to understand your experience, if that's okay."
                ),
                "patient": (
                    "I wasn't sure if you'd know about the last visit. "
                    "I was told it was probably fine and to monitor it. "
                    "It hasn't gone away. I think it might be a little bigger."
                ),
                "annotation": (
                    "The student opens by naming the prior visit directly — not defensively, "
                    "not explaining it away, but inviting Priya to share her experience of it. "
                    "This is the single most important opening move in this case. "
                    "Priya's entire guarded presentation is driven by expecting to be "
                    "dismissed again. The student's opening signals that this will be different "
                    "before Priya has had to express that worry herself."
                ),
                "tags_demonstrated": ["empathy", "open_question"],
            },
            {
                "turn": 2,
                "student": (
                    "You've been monitoring something you were worried about, alone, "
                    "for eight months. That's a long time to carry that. "
                    "I want to make sure we get this right today. "
                    "Can you tell me everything you've been thinking and noticing "
                    "since that last visit?"
                ),
                "patient": (
                    "It's in the same place, upper left quadrant. It's still there. "
                    "I measure it sometimes. I think it's slightly larger but I'm not sure. "
                    "I've been reading a lot about this."
                ),
                "annotation": (
                    "The student acknowledges what Priya has been doing — monitoring, "
                    "alone, for eight months — without minimizing it. Then the question is "
                    "deliberately broad: 'everything you've been thinking and noticing.' "
                    "Not 'describe the lump' but 'tell me everything.' "
                    "This gives Priya room to mention her research, her fear, and her "
                    "specific concerns — which she does, in part, by mentioning 'I've been "
                    "reading a lot about this.'"
                ),
                "tags_demonstrated": ["empathy", "open_question"],
            },
            {
                "turn": 3,
                "student": (
                    "Eight months of reading about this — what have you found, "
                    "and what has that done to your worry level?"
                ),
                "patient": (
                    "I found a case report about a woman who was told her lump was "
                    "benign for 18 months before it turned out to be something serious. "
                    "I know I'm probably being irrational. But I can't stop thinking about it."
                ),
                "annotation": (
                    "Instead of immediately reassuring Priya or telling her that one case "
                    "report is not representative, the student asks what she found and "
                    "what it did to her worry. This invites her to share the specific fear "
                    "driving her presentation rather than the general clinical complaint. "
                    "The student is asking about the patient's ideas, concerns, and expectations "
                    "— the ICE framework — rather than just gathering clinical data."
                ),
                "tags_demonstrated": ["open_question"],
            },
            {
                "turn": 4,
                "student": (
                    "I don't think that's irrational at all. You found something concerning "
                    "and you've been sitting with that worry for eight months. "
                    "The case report you found describes a real thing that can happen. "
                    "I'm not going to tell you that it's probably nothing — "
                    "I don't know that yet, and neither do you. "
                    "What I can tell you is that the right thing to do now is take this seriously "
                    "and get a proper evaluation. Can you tell me what outcome you'd be "
                    "most relieved by today?"
                ),
                "patient": (
                    "I just want to feel like someone actually listened to me and took "
                    "an appropriate step. Even if the result is scary, I'd rather know "
                    "than keep wondering."
                ),
                "annotation": (
                    "This is the critical counter-move to false reassurance. "
                    "The student explicitly says 'I'm not going to tell you it's probably "
                    "nothing — I don't know that yet.' This validates Priya's concern "
                    "and is clinically honest. The student acknowledges the case report "
                    "as legitimate rather than dismissing it. "
                    "Then the student asks what Priya would be most relieved by today — "
                    "which elicits her actual goal: to be taken seriously and have "
                    "an appropriate step taken. This is what shared decision-making looks like."
                ),
                "tags_demonstrated": ["empathy", "shared_decision_making"],
            },
            {
                "turn": 5,
                "student": (
                    "That makes complete sense. And I want to be honest with you "
                    "about the last visit: imaging should have been ordered then. "
                    "Not ordering it was not the right call, looking back. "
                    "I can't change that, but I can make sure we do it right today. "
                    "What I'd like to do is re-examine you and order imaging — "
                    "both mammography and ultrasound — today. "
                    "How does that sound?"
                ),
                "patient": (
                    "That's exactly what I was hoping you'd say. "
                    "I didn't want to have to argue for it."
                ),
                "annotation": (
                    "The student directly acknowledges the limitation of the prior visit — "
                    "'imaging should have been ordered then; not ordering it was not the "
                    "right call.' This is a hard statement to make and most students avoid it. "
                    "But for Priya, who has spent eight months feeling dismissed, "
                    "this acknowledgment is clinically necessary for trust. "
                    "The plan is then proposed specifically and checked with Priya "
                    "rather than simply announced."
                ),
                "tags_demonstrated": ["empathy", "shared_decision_making", "communication_repair"],
            },
            {
                "turn": 6,
                "student": (
                    "You shouldn't have had to argue for it. "
                    "I'm sorry that was the experience last time. "
                    "While we wait for imaging, I want to understand what would "
                    "be most helpful for you in the meantime — "
                    "in terms of information, what to expect next, or anything else "
                    "you've been wondering about."
                ),
                "patient": (
                    "I'd like to know — if the imaging shows something, what happens next? "
                    "And is there anything I should watch for in the meantime?"
                ),
                "annotation": (
                    "The student apologizes for the previous experience — simply and directly. "
                    "Then, instead of immediately explaining what imaging will show, "
                    "the student asks what would be most helpful for Priya to know — "
                    "letting her direct the information exchange rather than assuming "
                    "what she needs. Priya's questions (what if imaging shows something; "
                    "what to watch for) are now the agenda, not the student's checklist."
                ),
                "tags_demonstrated": ["communication_repair", "gives_patient_control"],
            },
            {
                "turn": 7,
                "student": (
                    "Those are exactly the right questions. "
                    "If imaging shows something that needs more investigation, "
                    "the next step is typically a biopsy — a tissue sample. "
                    "I'll be honest: I can't tell you today what the imaging will show. "
                    "In the meantime, there's nothing you can do to make a lump grow "
                    "or shrink by what you do or don't do — so there's no urgent action "
                    "on your end before the results come back. "
                    "I'll make sure the results come back to you within a few days "
                    "and that I call you personally. How do you feel going into this?"
                ),
                "patient": (
                    "Better. Genuinely. I didn't expect to feel this much better "
                    "just from being listened to."
                ),
                "annotation": (
                    "The student answers Priya's questions honestly and specifically, "
                    "including an explicit acknowledgment of uncertainty ('I can't tell "
                    "you today what imaging will show'). There is no false reassurance. "
                    "The student commits to specific follow-through (calling personally "
                    "with results) and checks in on Priya's emotional state at the end. "
                    "Priya's response — feeling better from being listened to — directly "
                    "names what was wrong about her prior experience and what was right "
                    "about this one."
                ),
                "tags_demonstrated": ["shared_decision_making", "empathy"],
            },
        ],
        "key_moments": [
            {
                "turn": 1,
                "description": "Student names the prior visit and its unresolved nature before asking anything clinical.",
                "principle": "Patients who have been dismissed need explicit acknowledgment of that experience before they will engage fully.",
            },
            {
                "turn": 4,
                "description": "Student explicitly declines to offer premature reassurance.",
                "principle": "'I'm not going to tell you it's probably nothing — I don't know that yet' is more honest and more therapeutic than false reassurance.",
            },
            {
                "turn": 5,
                "description": "Student directly acknowledges that imaging should have been ordered at the prior visit.",
                "principle": "Honest acknowledgment of prior clinical inadequacy — when appropriate — can be more therapeutic than defending or explaining it away.",
            },
        ],
        "after_report": {
            "what_model_did": (
                "The model acknowledged the prior visit's limitation directly and "
                "apologized for it, explicitly declined to offer premature reassurance "
                "before assessment, respected and engaged with Priya's research rather "
                "than dismissing it, and invited her to share the full extent of her "
                "worry before proposing any plan."
            ),
            "common_mistakes": (
                "Students most often (1) say 'I'm sure it's nothing' or 'try not to worry' "
                "before assessment, which repeats the prior dismissal, (2) avoid "
                "acknowledging that the prior visit should have included imaging, and "
                "(3) tell Priya that online case reports are not representative — "
                "a response that tends to be heard as dismissal of her intelligence."
            ),
            "next_attempt_goal": (
                "In your next attempt: acknowledge the prior visit before asking "
                "a single clinical question. Avoid all premature reassurance — do not "
                "say 'I'm sure it's nothing' or equivalent. When Priya mentions "
                "the case report she found, ask her what she found before responding to it."
            ),
        },
    },
}

def get_model_transcript(case_id: str) -> dict | None:
    """
    Return the model transcript for a given case ID, or None if not found.

    Args:
        case_id: One of: alex, diane, marcus, rosa, james, priya.

    Returns:
        Full model transcript dict, or None.
    """
    return MODEL_TRANSCRIPTS.get(case_id)
