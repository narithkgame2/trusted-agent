#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Translate core lessons (Lessons 1-9) into Khmer and merge into index.html KM dictionary."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HTML_PATH = os.path.join(ROOT, "index.html")

TRANSLATIONS = {
    # === Lesson 1: The Phnom Penh property market ===
    "Know the current state of the Phnom Penh condo market using Realestate.com.kh (REAKH) data": "ដឹងពីស្ថានភាពបច្ចុប្បន្ននៃទីផ្សារខុនដូភ្នំពេញ ដោយប្រើទិន្នន័យពី Realestate.com.kh (REAKH)",
    "Know average prices and rents for the main districts": "ដឹងពីតម្លៃជាមធ្យម និងថ្លៃជួលសម្រាប់ខណ្ឌសំខាន់ៗ",
    "Calculate a simple Capital Gains Tax (CGT) example correctly": "គណនាឧទាហរណ៍ពន្ធលើចំណេញមូលធន (CGT) ដោយត្រឹមត្រូវ",
    "Realestate.com.kh (REAKH): where the numbers come from": "Realestate.com.kh (REAKH)៖ ប្រភពនៃតួលេខ",
    "Every number here comes from the Realestate.com.kh 2026 report. Say where a number comes from, and it becomes trustworthy.": "រាល់តួលេខនៅទីនេះបានមកពីរបាយការណ៍ឆ្នាំ ២០២៦ របស់ Realestate.com.kh។ ការប្រាប់ប្រភពតួលេខ ធ្វើឲ្យព័ត៌មានគួរឲ្យទុកចិត្ត។",
    "Learn these numbers. Clients will test you.": "រៀនតួលេខទាំងនេះ។ អតិថិជននឹងសាកសួរអ្នក។",
    "Buy prices are per square meter of gross floor area. Rents are for newer buildings with a pool and gym.": "តម្លៃទិញគិតជាម៉ែត្រការ៉េលើផ្ទៃក្រឡាសរុប។ ថ្លៃជួលគឺសម្រាប់អគារថ្មីៗដែលមានអាងហែលទឹក និងកន្លែងហាត់ប្រាណ។",
    "The tax a client pays when they sell: a worked example": "ពន្ធដែលអតិថិជនត្រូវបង់ពេលលក់៖ ឧទាហរណ៍ជាក់ស្តែង",
    "Capital Gains Tax is on the profit, not the full sale price. Show it with real numbers.": "ពន្ធលើចំណេញមូលធន (CGT) គឺគិតលើប្រាក់ចំណេញ មិនមែនលើតម្លៃលក់សរុបទេ។ បង្ហាញវាជាមួយតួលេខពិត។",
    "Always show the taxable gain, not the full sale price": "បង្ហាញប្រាក់ចំណេញជាប់ពន្ធជានិច្ច មិនមែនតម្លៃលក់សរុបទេ",
    "A client who thinks CGT applies to the full $200,000 will panic. Once they see it only applies to the $60,000 gain, the number feels manageable.": "អតិថិជនដែលគិតថា CGT គិតលើប្រាក់ ២០០,០០០ ដុល្លារទាំងអស់នឹងភ័យស្លន់ស្លោ។ ពេលពួកគេឃើញថាវាគិតតែលើប្រាក់ចំណេញ ៦០,០០០ ដុល្លារ តួលេខនោះអាចទទួលយកបាន។",
    "Walk through the calculation out loud with the client's own numbers, every time CGT comes up.": "ធ្វើការពន្យល់គណនាឲ្យឮៗជាមួយតួលេខរបស់អតិថិជន រាល់ពេលដែលលើកឡើងអំពី CGT។",
    "A BKK1 2-bedroom: a real transaction, not a projection": "បន្ទប់គេង ២ នៅបឹងកេងកង ១៖ ប្រតិបត្តិការជាក់ស្តែង មិនមែនការប៉ាន់ស្មាន",
    "A real BKK1 result from the 2026 report. Use it as evidence, never as a promise.": "លទ្ធផលជាក់ស្តែងនៅបឹងកេងកង ១ ពីរបាយការណ៍ឆ្នាំ ២០២៦។ ប្រើវាជាភស្តុតាង កុំប្រើជាការសន្យា។",

    # === Lesson 2: How real estate works in Cambodia ===
    "Know the difference between 2 kinds of property title, and why the difference matters": "ដឹងពីភាពខុសគ្នារវាងប្លង់កម្មសិទ្ធិ ២ ប្រភេទ និងមូលហេតុដែលវាសំខាន់",
    "Explain the 3 rules of foreign ownership to any client, in simple words": "ពន្យល់ពីច្បាប់ទាំង ៣ នៃកម្មសិទ្ធិជនបរទេសដល់អតិថិជន ដោយពាក្យសាមញ្ញ",
    "Know the 6 steps of buying an off-plan condo, in order, and explain a payment plan with real numbers": "ដឹងពី ៦ ជំហាននៃការទិញខុនដូប្លង់ តាមលំដាប់ និងពន្យល់ពីគម្រោងបង់ប្រាក់ជាមួយតួលេខពិត",
    "The single most important word in this lesson: title": "ពាក្យសំខាន់បំផុតតែមួយគត់ក្នុងមេរៀននេះ៖ ប្លង់កម្មសិទ្ធិ",
    "The title proves who owns a property. The wrong title can mean owning nothing.": "ប្លង់កម្មសិទ្ធិបញ្ជាក់ថាអ្នកណាជាម្ចាស់អចលនទ្រព្យ។ ប្លង់ខុសអាចមានន័យថាមិនមានអ្វីទាំងអស់។",
    "3 rules for foreign buyers. Know these by heart.": "ច្បាប់ ៣ សម្រាប់អ្នកទិញបរទេស។ ចងចាំឲ្យច្បាស់។",
    "Foreigners can own property under 3 rules. Clients ask about this in almost every meeting.": "ជនបរទេសអាចកាន់កាប់អចលនទ្រព្យក្រោមច្បាប់ ៣។ អតិថិជនតែងតែសួរអំពីរឿងនេះស្ទើរគ្រប់ការជួប។",
    "No ground floor in a foreigner's own name": "មិនអាចកាន់កាប់ជាន់ផ្ទាល់ដីជាឈ្មោះផ្ទាល់ខ្លួនរបស់ជនបរទេសឡើយ",
    "A foreigner can own a strata-title unit from the 1st floor up, in their own name. The ground floor cannot be in a foreigner's own name. Legal routes exist: since the 2019 Trust Law, a licensed trust company can hold it for them (over 1,700 trusts were registered by 2025), or a land-holding company that is at least 51% Cambodian-owned.": "ជនបរទេសអាចកាន់កាប់យូនីតប្លង់រឹងចំណែកឯកជន (Strata Title) ចាប់ពីជាន់ទី ១ ឡើងទៅជាឈ្មោះផ្ទាល់ខ្លួន។ ជាន់ផ្ទាល់ដីមិនអាចជាឈ្មោះជនបរទេសបានទេ។ ផ្លូវច្បាប់មាន៖ ចាប់តាំងពីច្បាប់ស្តីពីបរធនបាលកិច្ចឆ្នាំ ២០១៩ ក្រុមហ៊ុនបរធនបាលដែលមានអាជ្ញាប័ណ្ណអាចកាន់កាប់ជំនួសបាន (បរធនបាលកិច្ចជាង ១,៧០០ ត្រូវបានចុះបញ្ជីត្រឹមឆ្នាំ ២០២៥) ឬក្រុមហ៊ុនកាន់កាប់ដីដែលមានភាគហ៊ុនកម្ពុជាយ៉ាងតិច ៥១%។",
    "If a foreign client likes a ground-floor unit, say clearly it can't be in their own name. Then offer both paths: the same layout one floor up, or a legal route set up with an independent lawyer. Check with your manager before you promise anything.": "បើអតិថិជនបរទេសចូលចិត្តយូនីតជាន់ផ្ទាល់ដី ចូរប្រាប់ឲ្យច្បាស់ថាមិនអាចដាក់ឈ្មោះគាត់ផ្ទាល់បានទេ។ បន្ទាប់មកផ្តល់ជម្រើសទាំងពីរ៖ ប្លង់ដូចគ្នានៅជាន់ខាងលើ ឬតាមផ្លូវច្បាប់ជាមួយមេធាវីឯករាជ្យ។ ពិគ្រោះជាមួយអ្នកគ្រប់គ្រងមុនពេលសន្យាអ្វីមួយ។",
    "Up to 70% foreign ownership per building": "កម្មសិទ្ធិជនបរទេសរហូតដល់ ៧០% ក្នុងមួយអគារ",
    "No more than 70% of the units in one building can be owned by foreigners. This is called the \"foreign quota.\" Always check how much quota is left before you recommend a project.": "មិនលើសពី ៧០% នៃយូនីតក្នុងអគារមួយអាចត្រូវបានកាន់កាប់ដោយជនបរទេស។ នេះហៅថា «កូតាជនបរទេស»។ ត្រូវពិនិត្យជានិច្ចថាតើនៅសល់កូតាប៉ុន្មានមុនពេលណែនាំគម្រោង។",
    "Before recommending any project, ask: how much foreign quota is left in this building? If it's under 5%, say so clearly before showing anything.": "មុនពេលណែនាំគម្រោងណាមួយ ចូរសួរថា៖ តើនៅសល់កូតាជនបរទេសប៉ុន្មានក្នុងអគារនេះ? បើសល់ក្រោម ៥% ចូរប្រាប់ឲ្យច្បាស់មុនពេលបង្ហាញអ្វីៗទាំងអស់។",
    "Strata title is required, no exceptions": "តម្រូវឲ្យមានប្លង់រឹងចំណែកឯកជន (Strata Title) គ្មានការលើកលែង",
    "Every unit sold to a foreign client must have strata title. This was covered in the section above, and it matters enough to repeat here.": "គ្រប់យូនីតដែលលក់ឲ្យអតិថិជនបរទេសត្រូវតែមានប្លង់រឹងចំណែកឯកជន។ ចំណុចនេះត្រូវបានលើកឡើងខាងលើ ហើយវាសំខាន់ណាស់ក្នុងការបញ្ជាក់ម្តងទៀត។",
    "Check the title type for every unit, every time, before you mention it to a foreign client.": "ពិនិត្យប្រភេទប្លង់សម្រាប់គ្រប់យូនីត គ្រប់ពេល មុនពេលអ្នកលើកឡើងទៅកាន់អតិថិជនបរទេស។",
    "6 steps, from booking to the title in your name": "៦ ជំហាន ចាប់ពីការកក់ រហូតដល់ប្លង់ជាឈ្មោះរបស់អ្នក",
    "Most condos follow these same 6 steps. Only the payments and timing change.": "ខុនដូភាគច្រើនអនុវត្តតាម ៦ ជំហានដូចគ្នានេះ។ ខុសគ្នាតែការបង់ប្រាក់ និងពេលវេលាប៉ុណ្ណោះ។",
    "Booking": "ការកក់ទុក (Booking)",
    "The booking fee holds one specific unit while the contract is prepared, usually $500 to $2,000. It is normally counted toward the down payment. Refund terms differ by developer.": "ប្រាក់កក់ទុកដើម្បីរក្សាយូនីតជាក់លាក់ខណៈពេលរៀបចំកិច្ចសន្យា ជាទូទៅពី ៥០០ ទៅ ២,០០០ ដុល្លារ។ វាត្រូវបានរាប់បញ្ចូលក្នុងប្រាក់បង់ដំបូង។ លក្ខខណ្ឌបង្វិលសងខុសគ្នាតាមក្រុមហ៊ុនអភិវឌ្ឍន៍។",
    "Confirm in writing whether the booking fee is refundable, and when, before the client pays.": "បញ្ជាក់ជាលាយលក្ខណ៍អក្សរថាតើប្រាក់កក់អាចបង្វិលសងវិញបានឬទេ និងនៅពេលណា មុនពេលអតិថិជនបង់ប្រាក់។",
    "Down payment and the contract (SPA)": "ប្រាក់បង់ដំបូង និងកិច្ចសន្យាទិញលក់ (SPA)",
    "The Sale and Purchase Agreement (SPA) is the main legal contract between the buyer and the developer. Check the terms, the developer's obligations, the penalties for delay, the handover date and how the title will be delivered. The down payment, usually 20 to 30%, is due when it is signed, and the booking fee is part of it.": "កិច្ចសន្យាទិញលក់ (SPA) គឺជាកិច្ចសន្យាផ្លូវច្បាប់ចម្បងរវាងអ្នកទិញ និងក្រុមហ៊ុនអភិវឌ្ឍន៍។ ពិនិត្យលក្ខខណ្ឌ កាតព្វកិច្ចរបស់អ្នកអភិវឌ្ឍន៍ ការផាកពិន័យចំពោះការពន្យារពេល កាលបរិច្ឆេទប្រគល់ និងរបៀបប្រគល់ប្លង់។ ប្រាក់បង់ដំបូង ជាទូទៅ ២០ ទៅ ៣០% ត្រូវបង់ពេលចុះហត្ថលេខា ហើយប្រាក់កក់ត្រូវបានរាប់បញ្ចូលក្នុងនោះ។",
    "Say this to every client: \"I recommend having your own lawyer review the SPA before you sign.\"": "និយាយចំណុចនេះទៅកាន់អតិថិជនគ្រប់រូប៖ «ខ្ញុំសូមណែនាំឲ្យមេធាវីផ្ទាល់ខ្លួនរបស់អ្នកពិនិត្យមើល SPA មុនពេលអ្នកចុះហត្ថលេខា។»",
    "Monthly instalments": "ការបង់រំលស់ប្រចាំខែ",
    "While the building goes up, the client pays in instalments: monthly, quarterly, or at construction milestones. Each project has its own plan.": "ខណៈពេលអគារកំពុងសាងសង់ អតិថិជនបង់ជាដំណាក់កាល៖ ប្រចាំខែ ប្រចាំត្រីមាស ឬតាមវឌ្ឍនភាពនៃការសាងសង់។ គម្រោងនីមួយៗមានផែនការរៀងៗខ្លួន។",
    "Before you present a project, know its exact plan: how much, how often, and for how long.": "មុនពេលអ្នកបង្ហាញគម្រោង ចូរដឹងពីគម្រោងច្បាស់លាស់៖ ប៉ុន្មាន ញឹកញាប់ប៉ុណ្ណា និងរយៈពេលប៉ុន្មាន។",
    "Balance at handover": "ប្រាក់នៅសល់ពេលប្រគល់ផ្ទះ",
    "The largest single payment is usually the last one, when the building is finished. The client pays it in cash or with a bank loan, so a client who needs a loan should start early.": "ការបង់ប្រាក់ដុំធំបំផុតជាធម្មតាគឺការបង់ចុងក្រោយ នៅពេលអគារសាងសង់រួចរាល់។ អតិថិជនបង់ជាសាច់ប្រាក់ ឬកម្ចីធនាគារ ដូច្នេះអ្នកដែលត្រូវការកម្ចីគួរចាប់ផ្តើមរៀបចំពីដំបូង។",
    "Tell the client early how large the final payment is and when it falls due, so they can plan for it.": "ប្រាប់អតិថិជនឲ្យបានឆាប់អំពីទំហំនៃការបង់ប្រាក់ចុងក្រោយ និងកាលបរិច្ឆេទត្រូវបង់ ដើម្បីឲ្យពួកគេអាចរៀបចំផែនការទុក។",
    "Handover": "ការប្រគល់ផ្ទះ (Handover)",
    "Before taking the keys, the client inspects the unit and lists any defects (a snag list) for the developer to fix.": "មុនពេលទទួលសោ អតិថិជនចុះត្រួតពិនិត្យយូនីត និងកត់ត្រារាល់ចំណុចខ្វះខាត (Snag list) ដើម្បីឲ្យក្រុមហ៊ុនអភិវឌ្ឍន៍កែសម្រួល។",
    "Go to the handover with the client, or send them a defect checklist beforehand.": "ទៅចូលរួមការប្រគល់ផ្ទះជាមួយអតិថិជន ឬផ្ញើបញ្ជីត្រួតពិនិត្យចំណុចខ្វះខាតឲ្យពួកគេជាមុន។",
    "Title registration": "ការចុះបញ្ជីផ្ទេរកម្មសិទ្ធិ",
    "Once the unit is fully paid and handover is complete, the strata title is transferred to the buyer's name. A 4% transfer tax (stamp duty) is due at this point, usually calculated on the Cadastral valuation of the property.": "នៅពេលដែលយូនីតត្រូវបានទូទាត់ពេញលេញ និងការប្រគល់ផ្ទះរួចរាល់ ប្លង់រឹងចំណែកឯកជននឹងត្រូវផ្ទេរជាឈ្មោះអ្នកទិញ។ ពន្ធប្រថាប់ត្រា ៤% ត្រូវបង់នៅពេលនេះ ដោយគិតលើតម្លៃវាយតម្លៃរបស់សុរិយោដី។",
    "Always tell the client about the 4% transfer tax early, not at handover.": "ប្រាប់អតិថិជនជានិច្ចអំពីពន្ធប្រថាប់ត្រា ៤% ឲ្យបានឆាប់ មិនមែនចាំដល់ពេលប្រគល់ផ្ទះនោះទេ។",

    # === Lesson 3: Who our clients are ===
    "Know the 5 main client types in Cambodia: profile, goal and decision style": "ដឹងពីប្រភេទអតិថិជនសំខាន់ៗទាំង ៥ នៅកម្ពុជា៖ ប្រវត្តិ គោលដៅ និងរបៀបសម្រេចចិត្ត",
    "Tell which type a new client is within 5 minutes": "ដឹងថាអតិថិជនថ្មីជាប្រភេទណា ក្នុងរយៈពេល ៥ នាទី",
    "Know which projects fit each type, and why": "ដឹងថាតើគម្រោងណាដែលសមស្របនឹងប្រភេទនីមួយៗ និងមូលហេតុ",
    "One approach does not fit every client": "វិធីសាស្ត្រតែមួយ មិនសមស្របនឹងអតិថិជនគ្រប់រូបឡើយ",
    "Know the client type first, then match the project. Never the other way around.": "ស្គាល់ប្រភេទអតិថិជនជាមុនសិន រួចចាំជ្រើសរើសគម្រោងឲ្យត្រូវ។ កុំធ្វើបញ្ច្រាសទិសដៅឲ្យសោះ។",
    "Know each profile clearly": "ស្គាល់ប្រវត្តិ និងលក្ខណៈនីមួយៗឲ្យច្បាស់",
    "Five types of condo client, each with a different goal and best-fit property.": "អតិថិជនខុនដូ ៥ ប្រភេទ ដែលម្នាក់ៗមានគោលដៅ និងអចលនទ្រព្យសមស្របខុសៗគ្នា។",
    "Three questions, in order, tell you the type": "សំណួរ ៣ តាមលំដាប់ ប្រាប់អ្នកពីប្រភេទអតិថិជន",
    "Three questions in the first 5 minutes tell you who you're talking to.": "សំណួរ ៣ ក្នុងរយៈពេល ៥ នាទីដំបូង ប្រាប់អ្នកថាអ្នកកំពុងនិយាយជាមួយនរណា។",
    "Question 1: background": "សំណួរទី ១៖ បទពិសោធន៍",
    "\"Have you invested in property before, here or anywhere else?\" This tells you the client type fast.": "«តើលោកអ្នកធ្លាប់វិនិយោគលើអចលនទ្រព្យពីមុនមកទេ នៅទីនេះ ឬនៅកន្លែងផ្សេងទៀត?» សំណួរនេះប្រាប់អ្នកពីប្រភេទអតិថិជនយ៉ាងរហ័ស។",
    "Ask this within the first minute of any new conversation.": "សួរសំណួរនេះក្នុងនាទីដំបូងនៃការសន្ទនាថ្មីណាមួយ។",
    "Question 2: their goal": "សំណួរទី ២៖ គោលដៅរបស់ពួកគេ",
    "\"What do you hope this investment gives you?\" Rental income points to an investor. Living there points to a home buyer.": "«តើលោកអ្នកសង្ឃឹមថានឹងទទួលបានអ្វីពីការវិនិយោគនេះ?» ចំណូលពីការជួលបង្ហាញពីអ្នកវិនិយោគ។ ការរស់នៅបង្ហាញពីអ្នកទិញសម្រាប់ស្នាក់នៅ។",
    "Listen for the word \"income\" or the word \"live\". That one word tells you a lot.": "ស្តាប់ពាក្យ «ចំណូល» ឬពាក្យ «រស់នៅ»។ ពាក្យតែមួយម៉ាត់នោះប្រាប់អ្នកយ៉ាងច្រើន។",
    "Question 3: the power question": "សំណួរទី ៣៖ សំណួរគន្លឹះសំខាន់",
    "\"What would make this the wrong decision for you?\" It shows risk tolerance, decision criteria and hidden worries all at once.": "«តើអ្វីដែលធ្វើឲ្យការសម្រេចចិត្តនេះក្លាយជាការសម្រេចចិត្តខុសសម្រាប់លោកអ្នក?» វាបង្ហាញពីការទទួលយកហានិភ័យ លក្ខខណ្ឌសម្រេចចិត្ត និងការព្រួយបារម្ភលាក់កំបាំងទាំងអស់ក្នុងពេលតែមួយ។",
    "Ask it word for word. It is the most useful sentence in this lesson.": "សួរវាពាក្យមួយៗឲ្យចំ។ វាជាប្រយោគដែលមានប្រយោជន៍បំផុតក្នុងមេរៀននេះ។",
    "Background": "បទពិសោធន៍",
    "Nationality and past investing": "សញ្ជាតិ និងការវិនិយោគកន្លងមក",
    "Their goal": "គោលដៅរបស់ពួកគេ",
    "Income, lifestyle, or both": "ចំណូល របៀបរស់នៅ ឬទាំងពីរ",
    "The power question": "សំណួរគន្លឹះសំខាន់",
    "What would make this the wrong decision?": "តើអ្វីដែលធ្វើឲ្យការសម្រេចចិត្តនេះខុស?",

    # === Lesson 4: Calm your nerves ===
    "Keep your voice steady before and during a client meeting": "រក្សាសំឡេងរបស់អ្នកឲ្យនឹងនរ មុន និងអំឡុងពេលជួបអតិថិជន",
    "Use one breathing routine before every meeting": "អនុវត្តទម្លាប់ដកដង្ហើមមួយ មុនការជួបពិភាក្សាគ្រប់លើក",
    "Never announce your nerves": "កុំប្រាប់ពីភាពភ័យព្រួយរបស់អ្នកឲ្យសោះ",
    "Breathe out longer than you breathe in": "ដកដង្ហើមចេញឲ្យវែងជាងដកដង្ហើមចូល",
    "In for 4, out for 6. Three times before you walk in, once before a hard question.": "ចូល ៤ វិនាទី ចេញ ៦ វិនាទី។ បីដងមុនពេលដើរចូល និងម្តងមុនសំណួរពិបាក។",
    "Saying you're nervous makes the client notice it. Say nothing, breathe, pause, then begin.": "ការនិយាយថាអ្នកភ័យ ធ្វើឲ្យអតិថិជនចាប់អារម្មណ៍។ កុំនិយាយអ្វីទាំងអស់ ដកដង្ហើម ផ្អាកបន្តិច រួចចាប់ផ្តើម។",
    "Before every meeting: three slow breaths, in for 4, out for 6.": "មុនការប្រជុំគ្រប់លើក៖ ដកដង្ហើមយឺតៗបីដង ចូល ៤ ចេញ ៦។",
    "Take three seconds to settle": "ចំណាយពេល ៣ វិនាទីដើម្បីតាំងចិត្ត",
    "Settle, breathe out, look up, then speak. Three calm seconds look like control.": "តាំងចិត្ត ដកដង្ហើមចេញ ងើបមើល រួចនិយាយ។ បីវិនាទីដ៏ស្ងប់ស្ងាត់បង្ហាញពីការគ្រប់គ្រងស្ថានការណ៍។",
    "Settle before you speak": "តាំងចិត្តឲ្យនឹងនរមុនពេលនិយាយ",
    "Folder and phone first. Then look at the client and begin.": "រៀបចំឯកសារ និងទូរសព្ទជាមុន។ បន្ទាប់មកសម្លឹងមើលអតិថិជន រួចចាប់ផ្តើម។",
    "At your next meeting: sit, arrange, breathe out, look up, then say good morning.": "ក្នុងការជួបបន្ទាប់របស់អ្នក៖ អង្គុយ រៀបចំ ដកដង្ហើមចេញ ងើបមើល រួចនិយាយជម្រាបសួរ។",

    # === Lesson 5: Introduce yourself ===
    "Introduce yourself in one clear line": "ណែនាំខ្លួនឯងដោយមួយប្រយោគយ៉ាងច្បាស់",
    "Say your title: Investment Advisor": "ប្រាប់តួនាទីរបស់អ្នក៖ ទីប្រឹក្សាវិនិយោគ",
    "Give the client a line they can repeat": "ផ្តល់ឲ្យអតិថិជននូវប្រយោគមួយដែលពួកគេអាចនិយាយបន្តបាន",
    "Your name, your title, one clear line": "ឈ្មោះរបស់អ្នក តួនាទីរបស់អ្នក មួយប្រយោគយ៉ាងច្បាស់",
    "Your name, your title, one line about how you help. Advisor, not salesperson.": "ឈ្មោះរបស់អ្នក តួនាទីរបស់អ្នក មួយប្រយោគអំពីរបៀបដែលអ្នកជួយ។ ទីប្រឹក្សា មិនមែនអ្នកលក់។",
    "One line they can repeat": "មួយប្រយោគដែលពួកគេអាចនិយាយបន្តបាន",
    "Who you help and what they get. A client should be able to repeat it to their partner at dinner.": "តើអ្នកជួយនរណា និងអ្វីដែលពួកគេទទួលបាន។ អតិថិជនគួរតែអាចនិយាយប្រាប់ដៃគូរបស់ពួកគេនៅពេលញ៉ាំអាហារពេលល្ងាចបាន។",
    "Write your own line, and say it until it sounds natural, not like a slogan.": "សរសេរឃ្លាផ្ទាល់ខ្លួនរបស់អ្នក ហើយនិយាយវាឲ្យស្តាប់ទៅធម្មជាតិ មិនដូចពាក្យស្លោក។",
    "Match the setting": "សម្របតាមបរិបទ",
    "At a table: name, then your line. With Japanese clients: a slight bow, card with both hands.": "នៅតុ៖ ឈ្មោះ រួចឃ្លារបស់អ្នក។ ជាមួយអតិថិជនជប៉ុន៖ ឱនបន្តិច ហុចនាមប័ណ្ណដោយដៃទាំងពីរ។",
    "Business cards with both hands": "ហុចនាមប័ណ្ណដោយដៃទាំងពីរ",
    "With Japanese and many Asian clients, the card exchange is part of the respect. Offer yours facing them, with both hands.": "ជាមួយជនជាតិជប៉ុន និងអតិថិជនអាស៊ីជាច្រើន ការផ្លាស់ប្តូរនាមប័ណ្ណគឺជាផ្នែកមួយនៃការគោរព។ ហុចនាមប័ណ្ណរបស់អ្នកបែរទៅរកពួកគេ ដោយដៃទាំងពីរ។",
    "Keep cards in a case, not your pocket, and read their card before you put it away.": "ទុកនាមប័ណ្ណក្នុងប្រអប់ កុំទុកក្នុងហោប៉ៅ ហើយអាននាមប័ណ្ណរបស់ពួកគេមុនពេលទុក។",

    # === Lesson 6: Slow down ===
    "Speak slower and lower with clients": "និយាយឲ្យយឺត និងសំឡេងទាបជាងមុនជាមួយអតិថិជន",
    "Slow down before every number": "បន្ថយល្បឿនមុនរាល់តួលេខ",
    "Keep the last word strong": "រក្សាពាក្យចុងក្រោយឲ្យរឹងមាំ",
    "Slower, lower, steady to the last word": "យឺតជាងមុន ទាបជាងមុន នឹងនរដល់ពាក្យចុងក្រោយ",
    "Speak about 20% slower, and keep your volume to the last word. It is usually the important one.": "និយាយយឺតជាងមុនប្រហែល ២០% ហើយរក្សាកម្រិតសំឡេងដល់ពាក្យចុងក្រោយ។ វាជាធម្មតាជាពាក្យសំខាន់។",
    "Slow down before the number": "បន្ថយល្បឿនមុនតួលេខ",
    "Numbers are what clients remember and repeat. Pause just before the number, say it clearly, then stop.": "តួលេខគឺជាអ្វីដែលអតិថិជនចងចាំ និងនិយាយបន្ត។ ផ្អាកបន្តិចមុនតួលេខ និយាយឲ្យច្បាស់ រួចឈប់។",
    "When you give a price or a yield, pause before it. Then stop talking.": "ពេលអ្នកប្រាប់តម្លៃ ឬទិន្នផល ចូរផ្អាកមុនវានោះ។ បន្ទាប់មកឈប់និយាយ។",

    # === Lesson 7: Use silence ===
    "Stop talking after a price": "ឈប់និយាយបន្ទាប់ពីប្រាប់តម្លៃ",
    "Use a pause instead of um": "ប្រើការផ្អាកជំនួសពាក្យ អឺ",
    "Let the client think": "ទុកពេលឲ្យអតិថិជនគិត",
    "Say the price. Then stop.": "ប្រាប់តម្លៃ។ បន្ទាប់មកឈប់។",
    "State the price, then wait. Two seconds feels long to you, and normal to the client.": "ប្រាប់តម្លៃ រួចរង់ចាំ។ ពីរវិនាទីមានអារម្មណ៍ថាយូរសម្រាប់អ្នក ប៉ុន្តែធម្មតាសម្រាប់អតិថិជន។",
    "A pause instead of um": "ការផ្អាកជំនួសពាក្យ អឺ",
    "A two-second pause looks thoughtful. Fillers like um and so look lost.": "ការផ្អាកពីរវិនាទីមើលទៅហាក់ដូចជាកំពុងគិតពិចារណា។ ពាក្យបំពេញដូចជា អឺ និង អញ្ចឹង មើលទៅដូចជាបាត់បង់ទំនុកចិត្ត។",
    "Before you answer a hard question, breathe out and pause instead of saying um.": "មុនពេលអ្នកឆ្លើយសំណួរពិបាក ចូរដកដង្ហើមចេញ ហើយផ្អាកជាជាងនិយាយ អឺ។",

    # === Lesson 8: Sound certain ===
    "Remove the weak words": "ដកពាក្យដែលមិនច្បាស់លាស់ចេញ",
    "End with a falling pitch": "បញ្ចប់ដោយសំនៀងចុះក្រោម",
    "Recommend clearly": "ផ្តល់អនុសាសន៍ឲ្យបានច្បាស់លាស់",
    "Cut the words that take your authority away": "កាត់បន្ថយពាក្យដែលបន្ថយអំណាចវិជ្ជាជីវៈរបស់អ្នក",
    "Drop “I think”, “maybe” and “just”. Say your recommendation straight, and let your voice fall at the end.": "ឈប់ប្រើ «ខ្ញុំគិតថា» «ប្រហែលជា» និង «គ្រាន់តែ»។ និយាយអនុសាសន៍របស់អ្នកចំៗ ហើយទម្លាក់សំឡេងនៅចុងបញ្ចប់។",
    "Certain, not pushy": "ប្រាកដប្រជា មិនមែនបង្ខិតបង្ខំ",
    "Being certain is not the same as persuading. You can recommend clearly and still say “don't buy” when it doesn't fit.": "ភាពប្រាកដប្រជា មិនមែនជាការបញ្ចុះបញ្ចូលនោះទេ។ អ្នកអាចណែនាំឲ្យច្បាស់ ហើយនៅតែអាចនិយាយថា «កុំទិញ» នៅពេលដែលវាមិនសមស្រប។",
    "In your next meeting, count how many times you say “I think” or “just”.": "ក្នុងការជួបបន្ទាប់របស់អ្នក ចូររាប់ចំនួនដងដែលអ្នកនិយាយថា «ខ្ញុំគិតថា» ឬ «គ្រាន់តែ»។",

    # === Lesson 9: Say less ===
    "Answer first, then one reason": "ឆ្លើយជាមុនសិន រួចផ្តល់ហេតុផលមួយ",
    "Ask instead of defending": "សួរសំណួរជាជាងការការពារខ្លួន",
    "Say less than the client expects": "និយាយឲ្យតិចជាងអ្វីដែលអតិថិជនរំពឹងទុក",
    "Answer first. Then stop.": "ឆ្លើយជាមុន។ បន្ទាប់មកឈប់។",
    "Answer first. Give one reason. Then stop.": "ឆ្លើយជាមុន។ ផ្តល់ហេតុផលមួយ។ បន្ទាប់មកឈប់។",
    "When a client challenges you, a calm question sounds more secure than any defense, and it finds the real doubt.": "នៅពេលដែលអតិថិជនជំទាស់អ្នក សំណួរដ៏ស្ងប់ស្ងាត់ស្តាប់ទៅមានទំនុកចិត្តជាងការការពារខ្លួន ហើយវាជួយរកឃើញការសង្ស័យពិតប្រាកដ។",
    "When you're challenged, answer with a question: “Which part concerns you most?”": "នៅពេលមានការជំទាស់ ចូរឆ្លើយដោយសំណួរ៖ «តើផ្នែកណាដែលលោកអ្នកបារម្ភជាងគេ?»"
}

def main():
    src = open(HTML_PATH, encoding="utf-8").read()
    m = re.search(r"const KM=(\{[\s\S]*?\});\nfunction kmText", src)
    if not m:
        print("Could not find const KM in index.html")
        return
    km = json.loads(m.group(1))
    print(f"Existing KM entries: {len(km)}")
    km.update(TRANSLATIONS)
    print(f"New KM entries count: {len(km)}")
    
    new_km_str = json.dumps(km, ensure_ascii=False)
    new_src = src[:m.start(1)] + new_km_str + src[m.end(1):]
    
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(new_src)
    print("Successfully updated index.html with new translations.")

if __name__ == "__main__":
    main()
