# Same-Site Plans, Authentication, and Checkout

## Goal

Add a polished Rudra24 AI plans and purchase experience to the existing website, with a path for customers to use the AI product from the same website later. Customers should not need to visit a separate Apper portal to browse plans, sign in, pay, or open the product.

## User-approved direction

- Keep the existing marketing pages lightweight and quick to load.
- Put plan selection, account access, checkout, and eventually the AI product behind routes on the Rudra24 website.
- Use the Apper platform for authentication and the dynamic backend.
- Design the future AI product as a same-site `/app` experience, similar to opening ChatGPT or Claude from their own website.
- Use restrained, smooth animations and the existing site's typography and visual theme.
- Plan names: Essential, Growth, Pro, Business.

## Current project constraints

- The checked-out project is `rudra24-ai-website`, a static website deployed with Netlify. Its current palette is cream and deep green/teal, and it uses Geist with EB Garamond for display headings.
- No Apper project is currently connected to the account.
- The AI product's GitHub source is not present in this workspace. A future `/app` integration therefore needs that repository or a defined product API before implementation.
- The offer letter provides one feature set across four tiers, with different monthly lead volumes and prices. It lists 600, 900, 1,200, and 1,500 leads per month; the introductory paragraph's separate 500–2,000 range is not used for plan cards.

## Plan content

All four plans include quality lead generation, voice assistance, AI calling, email automation, WhatsApp automation, SMS automation, CRM and sales pipeline, company location insights, and manpower data at no additional cost.

| Plan | Leads/month | Monthly base price | GST (12%) | Monthly total |
|---|---:|---:|---:|---:|
| Essential | 600 | ₹21,000 | ₹2,520 | ₹23,520 |
| Growth | 900 | ₹31,500 | ₹3,780 | ₹35,280 |
| Pro | 1,200 | ₹42,000 | ₹5,040 | ₹47,040 |
| Business | 1,500 | ₹52,500 | ₹6,300 | ₹58,800 |

Show the monthly base price and clearly disclose that 12% GST is added, including the payable total before checkout. Promotional and referral discounts remain a contact-led offer because the letter gives no fixed discount schedule.

## Experience and routes

- Add an Explore Plans entry point to the existing site navigation and relevant calls to action.
- Create a plans page that follows the supplied pricing reference's centered headline, dark green pricing canvas, and light cards, recolored and typeset to match Rudra24. Visually emphasize Pro without claiming it is the most popular or best value.
- Each plan card shows plan name, monthly lead allowance, monthly price, GST treatment, purchase action, and a smooth expandable feature list. Expansion must work with keyboard and touch, expose state accessibly, and respect reduced-motion preferences.
- Keep the implementation lightweight: use CSS transitions and existing fonts; do not add a motion dependency for card expansion.
- Provide same-site account and checkout views. Exact URL shapes can follow the repository's Netlify routing approach when implementation begins; the durable requirement is that the browser stays on the Rudra24 domain.
- Reserve `/app` for the AI product experience. Until the product repository/API is available, plans/auth/checkout work must not pretend the actual AI workspace is already integrated.

## Dynamic services and payment

- The public marketing and plan content can remain static. Authentication, customer account state, order creation, and payment verification require server-side services and must not rely on front-end-only state.
- Use Apper for authentication and backend functions. Since no Apper project exists, implementation must first create a dedicated project after reading Apper's current platform and design directives, then connect the website's UI to that project.
- Use Razorpay as the proposed Indian payment provider for UPI and other available methods. The merchant's live credentials are not present, so build and verify only the provider's test flow until credentials and merchant setup are supplied.
- Offer a ₹1 test transaction only in test mode. Clearly label it as a sandbox transaction and never mark an order as paid based only on a client-side success screen; server-side payment verification is required.
- Do not use bank-account details from the secure PDF for direct transfer setup. The UPI ID/QR is expected later, and a regulated checkout provider should handle payment credentials.
- Do not expose payment secrets in browser code or public environment variables.

## Failure and trust states

- Show clear loading, validation, failure, cancellation, and success states for sign-in and checkout.
- Failed or cancelled payment must leave the order unpaid and provide a retry path.
- If live payment credentials are missing, show that checkout is in test mode; do not imply that real money was collected.
- Explain the GST amount and final total before the customer begins payment.

## Delivery phases

1. Build the plans page, navigation entry point, responsive cards, expandable features, and lightweight motion within the existing website.
2. Add same-domain authentication and secure checkout using Apper plus Razorpay test mode, gated on a new Apper project and required platform setup.
3. Add the real AI product under `/app` after the product GitHub repository/API is available; keep its customer-facing entry point and account context within the same Rudra24 site.

## Acceptance criteria

- The four approved plan names and the offer-letter table's volumes/prices appear accurately, with all included features shown on every plan.
- The plan page follows the reference composition while using Rudra24's cream/deep-green palette and Geist/EB Garamond typography.
- Feature lists expand/collapse smoothly, work without a mouse, and reduce motion when the user requests it.
- The plans entry point, account, checkout, and future product route are designed to remain on the Rudra24 domain.
- Test checkout cannot be mistaken for a live payment; only verified server-side payment status can mark an order paid.
- The existing marketing pages remain lightweight and usable while dynamic flows are added only where needed.
