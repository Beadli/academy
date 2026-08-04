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

| Route | Card needed? | Expires? | Good for |
|---|---|---|---|
| **Microsoft 365 Business trial** | Usually | Yes, about a month | Seeing the whole thing work end to end |
| **Azure free account** | Yes, for identity | Directory does not expire | A tenant you can keep |
| **Azure for Students** | No, needs a school email | While you are a student | The best option if you qualify |
| **Microsoft 365 Developer Program** | No | Renewable | Only if you already qualify |

</div>

**Microsoft 365 Business trial.** Sign up with a personal Microsoft account,
get a tenant with licences for about a month. The most direct route to seeing
this module work, and the one most people will use. Set a calendar reminder to
cancel, because trials that lapse into paid subscriptions are a well-worn way
to lose money you did not mean to spend.

**Azure free account.** Gives you a directory that does not expire, plus
credit you will not need for this module because the directory's free tier
covers everything here. It asks for a card to verify you are a person. It
should not charge it for what this module does, but *should not* is doing real
work in that sentence, so watch it.

**Azure for Students.** If you have a school or university email address, this
is the route to take. No card, and it is designed for exactly this.

**Microsoft 365 Developer Program.** This used to be the obvious answer, and it
largely is not any more. It now requires a qualifying subscription such as
Visual Studio Enterprise or Professional, or partner programme membership. If
you already have one through work, it is excellent. If not, skip it rather
than trying to qualify.

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

## What this costs, plainly

The directory features this module uses are in the free tier. The trial
licences you may be given are not needed for any of it.

The risk is not the feature, it is the subscription. A trial that renews into
a paid plan, or an Azure subscription left running something you spun up out
of curiosity, are the two ways a lab costs money. Neither is caused by this
module, and both are worth a calendar reminder.

When you are finished with the module, lesson 9.9 covers deciding whether to
keep the tenant or tear it down.
