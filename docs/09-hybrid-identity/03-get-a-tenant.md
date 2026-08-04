---
title: "9.3 Getting a tenant, honestly"
sidebar_position: 3
---

# 9.3 Getting a tenant, honestly

A **tenant** is your organisation's own instance of Microsoft's cloud
directory. Everything from here needs one, and getting one free is harder than
it was two years ago.

This lesson tells you the routes as they stand, what each actually costs, and
which ones ask for a card. It is deliberately short on click-by-click steps,
because Microsoft's signup flows are redesigned often enough that any sequence
written here would be wrong before you read it.

:::warning[Everything below can change, and has]
Microsoft has narrowed free access to developer tenants more than once. If
what you find does not match what is written here, trust what is in front of
you and treat this as the shape rather than the map.

If you cannot get a tenant today, read 9.4 to 9.8 anyway. They are written so
the reasoning stands without the clicking.
:::

## The routes

<div className="labTable">

| Route | Card | Expires? | Good for |
|---|---|---|---|
| **Azure free account** | Yes, to verify you are a person | Directory does not expire | A tenant you can keep. The one I would pick. |
| **Azure for Students** | No, needs a school email | While you are a student | Best option if you qualify |
| **Microsoft 365 Business trial** | Usually | Yes, about a month | Seeing licensed features too |
| **Microsoft 365 Developer Program** | No | Renewable | Only if you already qualify |

</div>

**Azure free account.** Gives you a directory that does not expire, plus
credit you will not spend here. Asks for a card. Read the next section before
you decide how you feel about that, because the card is not what most people
assume.

**Azure for Students.** If you have a school or university email address, take
this one. No card, designed for exactly this, and you keep the directory.

**Microsoft 365 Business trial.** A month of the full licensed product. Useful
if you want to see licence assignment and cloud groups doing real work.
**This is the one route that genuinely converts to a paid subscription if you
do nothing**, so cancel it when you are finished rather than letting it lapse.

**Microsoft 365 Developer Program.** This used to be the obvious answer and
largely is not any more. It now needs a qualifying subscription such as Visual
Studio Enterprise or Professional, or partner programme membership. Excellent
if you already have one through work; not worth chasing if you do not.

## About the card, plainly

Do not let this stop you. It is worth understanding rather than avoiding,
because you will meet the same pattern with every cloud provider you ever
sign up to, and "I would not put a card in" is not a position you can hold
for a career in infrastructure.

**What the card is for.** Identity verification. Cloud providers give away
real compute, and a payment method that resolves to a real person is how they
keep automated abuse down. You may see a small temporary authorisation appear
and then disappear; that is the verification, not a charge.

**What actually stops you being billed.** Azure free accounts have a
**spending limit turned on by default**, set to the value of your credit. If
something you deployed ever consumed the whole credit, Azure **disables the
services rather than charging you**. You have to go and deliberately remove
the spending limit before any card can be charged. That is a real mechanism,
not a promise.

**What this module costs against that credit: nothing.** The directory
features you use here are in the free tier of Entra ID, which is not metered
and does not draw on Azure credit. You are not deploying a virtual machine or
a database. The sync agent runs on your DC01, on your hardware.

:::tip[Three habits that make cloud accounts safe to own]
These are worth building now, on an account where the stakes are zero, because
they are the same habits that keep a real cloud bill under control.

1. **Know where the billing page is** before you need it. Find it once, today,
   while nothing is running. Cost Management is the section you want.
2. **Leave the spending limit on.** The only reason to remove it is to run
   something that must not be interrupted, which is not this.
3. **Set a calendar reminder** for a month out to go and look. Not because
   something will go wrong, but because "I have an account somewhere I never
   check" is the actual risk, and it is a habit rather than a fear.
:::

**If you would still rather not**, use Azure for Students if you qualify, or
read 9.4 to 9.8 without a tenant. The reasoning stands without the clicking.
But signing up, understanding the spending limit, and tearing it down cleanly
at the end is itself a small piece of professional practice, and doing it once
in a lab is how it stops being intimidating.

## Do this in a browser profile you can throw away

Whichever route you take, sign up in a **separate browser profile or a private
window**, with an account you have not used for anything else.

This is not paranoia. Microsoft accounts accumulate tenant memberships, and it
is genuinely easy to end up with a lab tenant permanently attached to the
personal account you use for everything, showing up in account pickers for
years. Keeping it separate now saves an irritating afternoon later.

Note down, somewhere you will find it again:

- The **tenant name**, which looks like `yourlab.onmicrosoft.com`
- The **global administrator account** you created, and its password
- Which route you used, and **when the trial expires** if it does

Put that in your journal. Lesson 9.9 asks for it, and future-you will want to
know why there is a Microsoft tenant with your name on it.

## Verify your domain, if you have one

If you own the domain you used for UPN suffixes in 9.2, add it to the tenant
now.

In the admin portal, add a custom domain and it will hand you a TXT record to
create in that domain's public DNS. It is the same mechanism you have already
met twice: it proves you control the domain, because only its owner can add
records to it.

Once it verifies, your users can arrive with the UPNs you set in 9.2 rather
than being rewritten to `onmicrosoft.com`.

If you do not own a domain, skip this. Your users will arrive as
`sokoth@yourlab.onmicrosoft.com`, the module still works end to end, and you
will have seen exactly the outcome 9.2 was warning about.

## When you are done with it

Lesson 9.9 asks you to decide deliberately whether to keep the tenant or tear
it down, and either is a fine answer.

**Keeping it** is reasonable, and there is something to be said for having a
directory of your own to try things against. If you took the Azure route it
does not expire, the spending limit is on, and Entra ID's free tier costs
nothing.

**Tearing it down** is equally reasonable, and it is a useful exercise in its
own right. Cancelling a subscription and deleting a tenant cleanly is a thing
people are oddly bad at, and doing it once deliberately means you know how.

The only thing worth avoiding is deciding by accident, which is why it is in
the journal rather than left implied.
