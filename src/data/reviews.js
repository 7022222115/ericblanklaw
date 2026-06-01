/*
 * Client reviews / testimonials data for Eric Blank Injury Attorneys.
 *
 * IMPORTANT — quotes must be VERBATIM client words.
 * Per FTC endorsement/testimonial guidelines and Nevada Bar advertising rules,
 * testimonial text must be the client's actual words, not paraphrased, edited
 * for substance, or invented. Paste the exact Google review text into each
 * `quote` field. Do NOT fabricate, embellish, or "clean up" wording.
 *
 * Display testimonials alongside `resultsDisclaimer` where appropriate.
 */

// Published client reviews. Verbatim Google review text.
export const reviews = [
  { name: "Karina M.", quote: "This firm was great, and I had a wonderful experience working with Cindy. She was professional, attentive, and made the whole process much easier. Would definitely recommend!" },
  { name: "Zyanya A.", quote: "I can't recommend Eric Blank and his personal injury law office enough! From the very first consultation, Eric and his team were professional, compassionate, and dedicated to my case. They kept me informed every step of the way and truly fought for the best outcome. If you need an attorney who will treat you like family and deliver results, Eric Blank is the one to trust!" },
  { name: "Andra S.", quote: "I had an amazing experience with Jorge when he handled my case. I felt that he had may back during a situation where I felt alone. He answered all my questions and made a stressful situation feel much more manageable. I'm happy with how everything turned out and would definitely recommend!" },
  { name: "Gayle C.", quote: "Thank you, Atty. Erik Blank for taking us through this difficult process. I would highly recommend both Erik and his staff. I was very fortunate to be referred to their office." },
  { name: "Jorge", quote: "The expertise at this firm is significant. They negotiate a fair settlement without having to go to trial. They are diligent in pursuing the compensation deserved while remaining empathetic to the situation. Speaking with them before hiring anyone else is a good idea." },
  { name: "Debra L.", quote: "Eric Blank And Associates managed my legal case and I received the package I was satisfied with. They acted in a professional manner communicated when needed. I'm satisfied with their work!" },
  // Result/settlement reviews — Eric-approved for publication 2026-05-31. Displayed with resultsDisclaimer (NV Bar / FTC).
  { name: "James F.", quote: "Got a great settlement. Thank you Cindy and Attorney Mr.Blank for all your help. Will definitely recommend to friends and family!" },
  { name: "Joel H.", quote: "Eric Blank Is the best lawyer in Vegas for a car accident ,he help me and my family to win my case I give him a 5 star and I totally recommend it If you have a car accident contact him cause he will win your case. thanks , my lawyer Eric Blank" },
  { name: "Angel F.", quote: "Everything was great Eric on point with paperwork and settlement..Quick and exceptional..Even the young ladies were very helpful when I need questions answered...i would highlyrecommend..." },
  { name: "Nathan G.", quote: "Fantastic experience. Ryan was a Rockstar. Handled everything quick and efficiently. Even the receptionist Anna is always nice and friendly. They will fight to get you what you deserve. Thanks Eric Blank." },
];

// Previously-pending reviews were approved by Eric 2026-05-31 and moved into `reviews` above.
// Kept as an empty export so any import references don't break.
export const pendingReviews = [];

// Aggregate Google rating for the firm.
export const googleAggregate = {
  rating: 4.8,
  count: 452, // verified against live Google listing 2026-05-31
  profileUrl: "https://www.google.com/maps/place/Eric+Blank+Injury+Attorneys/data=!4m2!3m1!1s0x0:0xb6fe4df0014e563d",
};

export const resultsDisclaimer =
  "Past results do not guarantee a similar outcome. Every case is different and must be evaluated on its own facts.";
