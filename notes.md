\# Milestone 1 notes



Community: r/travel (public subreddit)

Collected by copy-paste from reddit.com/r/travel/new on 2026-11-15.

Tried an automated collector first; Reddit returned HTTP 403, so I switched.

Took posts in the order they appeared, plus 1-3 top comments from each.

So far: 41 items.



\## Candidate distinctions I saw in the text

1\. Some posts ask for help with a trip being planned. Most comments answer them.

2\. Some posts tell the story of a finished trip and ask nothing.

3\. Some posts are complaints about an airline, doctor, or travel situation:

&#x20;  venting rather than asking.

4\. Some posts are mod/maintenance posts. (Dropped: too rare, and not what

&#x20;  this classifier is about.)



\## Collection rules

\- Skip deleted/removed posts, mod posts, bots, and pure chit-chat that

&#x20; doesn't ask, advise, report or complain (including short replies that

&#x20; only question or poke at the poster, like "... too much what?").

\- Label every item from its own text alone. The model never sees the

&#x20; thread, so I don't either when labelling.



\## General decision rule

Label by the post's main purpose, not by surface features. A question

mark doesn't make a question, the word "rant" doesn't make a rant, and a

sad tone doesn't make a rant.



\## Decision rule: trip\_report vs advice (hardest boundary)

If the post's main purpose is to describe the writer's own trip, it is

trip\_report, even if it contains a tip or a "next time I'd...". It is

advice only if it is aimed at someone else's plans.



\## Hard cases

1\. "2 Weeks in Korea": has "If I could go back, I'd spend more days in

&#x20;  Busan", which reads like advice, but the purpose is sharing the trip.

&#x20;  Chose trip\_report.

2\. "Switzerland - 10 days in a fairy tale": full of tips ("go early",

&#x20;  "don't miss"), but the purpose is describing their trip. Chose

&#x20;  trip\_report. The rule held.

3\. "This sounds so risky. How long between the two flight?...": asks

&#x20;  many questions, but the purpose is advising. Chose advice.

4\. "Doctor ignoring me for rabies/typhoid vaccine": asks questions,

&#x20;  but it is mostly venting. Chose rant.

5\. "Kinda of ranting so sorry, but just how do people travel in their

&#x20;  20s?": uses the word rant, but the purpose is asking. Chose question.

6\. "Is Expedia giving any refunds...? It was a sad day": sad tone, but

&#x20;  the purpose is asking. Chose question.

7\. "Algerian Sahara": full of practical info a reader could act on

&#x20;  (TourHQ, 1550 USD price, visa cost, exchange rates), but the purpose

&#x20;  is describing the writer's own trip. Chose trip\_report. The rule held.



\## Label definitions (Milestone 2)

(Wording drafted with AI from my purpose rule and my own calls; edited by me.)



question: The writer's main purpose is to get information, help or opinions from others.

&#x20; e.g. "Is booking two one-way flights instead of round trip asking for trouble?..."

&#x20; e.g. "How to travel with pet - Connecting flights with different airlines..."



advice: The writer's main purpose is to help with someone else's plans, decision or

question: recommending, warning, correcting, or sharing an opinion or habit for them to weigh.

&#x20; e.g. "BGY is not on Milan, it is in Bergamo..."

&#x20; e.g. "sorry your NYC trip got wrecked... Under the US DOT refund rule..."



trip\_report: The writer's main purpose is to describe a trip or place they experienced

themselves, even if tips slip in.

&#x20; e.g. "A day in Verona. Yesterday I finally had the opportunity to visit Verona..."

&#x20; e.g. "Nice shots! I was also in South Korea for two weeks recently..."



rant: The writer's main purpose is to vent frustration about a travel experience or

situation, even if a question is included.

&#x20; e.g. "Left Marseille at 3am Friday And now stuck In Miami at 3am..."

&#x20; e.g. "Sadly, charging for tap water is becoming more and more common..."



\## Tie-breaker tests

\- rant vs question: delete the question. If what's left is mainly complaining, it's a

&#x20; rant. If the complaining is background for a specific request, it's a question.

\- rant vs trip\_report: is the frustration the point of the post, or one part of a trip story?



\## Stress test (Milestone 2)

Asked AI for 8 posts on my label boundaries and labelled them myself:

trip\_report, advice, rant, question, advice, rant, trip\_report, trip\_report.

All 8 fit one label under the definitions. Closest call: #7 (a trip

update that asks "is it normal for feet to hurt this much?"), which I

called trip\_report because the question is a side note to the trip.

Definitions kept as written.





